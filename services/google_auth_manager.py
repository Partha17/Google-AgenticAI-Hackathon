"""
Google Authentication Manager
Secure user authentication and authorization using Google OAuth and Firebase Auth
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import base64
import secrets

# Google Auth imports
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import google.oauth2.id_token

# Firebase Auth imports (optional, if using Firebase)
try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth
    from firebase_admin import credentials as firebase_credentials
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

import streamlit as st
from config import settings

logger = logging.getLogger(__name__)

class GoogleAuthManager:
    """Comprehensive Google Authentication and Authorization Manager"""
    
    def __init__(self):
        self.client_id = settings.google_oauth_client_id
        self.client_secret = settings.google_oauth_client_secret
        self.redirect_uri = settings.google_oauth_redirect_uri
        self.project_id = settings.google_cloud_project
        
        self.scopes = [
            'openid',
            'email',
            'profile',
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
        
        self.firebase_app = None
        self.authenticated_users = {}
        self.user_sessions = {}
        
        # Initialize services
        self._initialize_auth_services()
    
    def _initialize_auth_services(self):
        """Initialize authentication services"""
        try:
            # Initialize Firebase if available and configured
            if FIREBASE_AVAILABLE and self.project_id:
                try:
                    # Check if app already exists
                    self.firebase_app = firebase_admin.get_app()
                except ValueError:
                    # Initialize new app
                    cred = firebase_credentials.ApplicationDefault()
                    self.firebase_app = firebase_admin.initialize_app(cred, {
                        'projectId': self.project_id
                    })
                logger.info("✅ Firebase Auth initialized")
            
        except Exception as e:
            logger.error(f"Error initializing auth services: {e}")
    
    # === OAuth Flow Management ===
    
    def create_oauth_flow(self) -> Flow:
        """Create OAuth 2.0 flow for user authentication"""
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            return flow
            
        except Exception as e:
            logger.error(f"Error creating OAuth flow: {e}")
            return None
    
    def get_authorization_url(self) -> Optional[str]:
        """Get authorization URL for OAuth flow"""
        try:
            flow = self.create_oauth_flow()
            if not flow:
                return None
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            # Store state for validation
            if 'oauth_state' not in st.session_state:
                st.session_state.oauth_state = state
            
            return authorization_url
            
        except Exception as e:
            logger.error(f"Error getting authorization URL: {e}")
            return None
    
    async def handle_oauth_callback(self, authorization_code: str, state: str) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for tokens"""
        try:
            # Validate state
            if 'oauth_state' in st.session_state and st.session_state.oauth_state != state:
                return {"success": False, "error": "Invalid state parameter"}
            
            flow = self.create_oauth_flow()
            if not flow:
                return {"success": False, "error": "Failed to create OAuth flow"}
            
            # Exchange authorization code for tokens
            flow.fetch_token(code=authorization_code)
            
            # Get user info
            credentials = flow.credentials
            user_info = await self._get_user_info(credentials.token)
            
            if user_info.get("success"):
                # Create user session
                session_token = self._create_user_session(user_info["user_data"])
                
                return {
                    "success": True,
                    "user": user_info["user_data"],
                    "session_token": session_token,
                    "access_token": credentials.token,
                    "refresh_token": credentials.refresh_token
                }
            else:
                return {"success": False, "error": "Failed to get user information"}
                
        except Exception as e:
            logger.error(f"Error handling OAuth callback: {e}")
            return {"success": False, "error": str(e)}
    
    async def _get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google API"""
        try:
            import httpx
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers=headers
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    return {
                        "success": True,
                        "user_data": {
                            "id": user_data.get("id"),
                            "email": user_data.get("email"),
                            "name": user_data.get("name"),
                            "picture": user_data.get("picture"),
                            "verified_email": user_data.get("verified_email", False)
                        }
                    }
                else:
                    return {"success": False, "error": f"API error: {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {"success": False, "error": str(e)}
    
    # === Session Management ===
    
    def _create_user_session(self, user_data: Dict[str, Any]) -> str:
        """Create secure user session"""
        try:
            session_token = secrets.token_urlsafe(32)
            
            session_data = {
                "user_id": user_data.get("id"),
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
                "permissions": self._get_user_permissions(user_data)
            }
            
            self.user_sessions[session_token] = session_data
            self.authenticated_users[user_data.get("id")] = session_data
            
            logger.info(f"Created session for user: {user_data.get('email')}")
            return session_token
            
        except Exception as e:
            logger.error(f"Error creating user session: {e}")
            return None
    
    def validate_session(self, session_token: str) -> Dict[str, Any]:
        """Validate user session token"""
        try:
            if session_token not in self.user_sessions:
                return {"valid": False, "error": "Invalid session token"}
            
            session_data = self.user_sessions[session_token]
            expires_at = datetime.fromisoformat(session_data["expires_at"])
            
            if datetime.utcnow() > expires_at:
                # Remove expired session
                del self.user_sessions[session_token]
                return {"valid": False, "error": "Session expired"}
            
            return {
                "valid": True,
                "user": session_data
            }
            
        except Exception as e:
            logger.error(f"Error validating session: {e}")
            return {"valid": False, "error": str(e)}
    
    def logout_user(self, session_token: str) -> bool:
        """Logout user and invalidate session"""
        try:
            if session_token in self.user_sessions:
                user_id = self.user_sessions[session_token].get("user_id")
                
                # Remove session
                del self.user_sessions[session_token]
                
                # Remove from authenticated users
                if user_id in self.authenticated_users:
                    del self.authenticated_users[user_id]
                
                logger.info(f"User logged out: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error logging out user: {e}")
            return False
    
    # === Permission Management ===
    
    def _get_user_permissions(self, user_data: Dict[str, Any]) -> List[str]:
        """Get user permissions based on email domain and user data"""
        permissions = ["read_portfolio", "view_analytics"]
        
        email = user_data.get("email", "")
        
        # Add permissions based on email domain or specific users
        if email.endswith("@yourcompany.com"):  # Replace with your domain
            permissions.extend(["admin", "write_portfolio", "manage_users"])
        elif email in ["admin@example.com"]:  # Specific admin users
            permissions.extend(["admin", "write_portfolio", "manage_users"])
        elif user_data.get("verified_email"):
            permissions.extend(["write_portfolio"])
        
        return permissions
    
    def check_permission(self, session_token: str, required_permission: str) -> bool:
        """Check if user has required permission"""
        try:
            session_validation = self.validate_session(session_token)
            if not session_validation.get("valid"):
                return False
            
            user_permissions = session_validation["user"].get("permissions", [])
            return required_permission in user_permissions or "admin" in user_permissions
            
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
    
    # === Firebase Integration (Optional) ===
    
    async def create_firebase_custom_token(self, user_id: str) -> Optional[str]:
        """Create custom Firebase token for authenticated user"""
        try:
            if not FIREBASE_AVAILABLE or not self.firebase_app:
                return None
            
            custom_token = firebase_auth.create_custom_token(user_id)
            return custom_token.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error creating Firebase custom token: {e}")
            return None
    
    async def verify_firebase_token(self, id_token: str) -> Dict[str, Any]:
        """Verify Firebase ID token"""
        try:
            if not FIREBASE_AVAILABLE or not self.firebase_app:
                return {"success": False, "error": "Firebase not available"}
            
            decoded_token = firebase_auth.verify_id_token(id_token)
            return {
                "success": True,
                "user_id": decoded_token["uid"],
                "email": decoded_token.get("email"),
                "email_verified": decoded_token.get("email_verified", False)
            }
            
        except Exception as e:
            logger.error(f"Error verifying Firebase token: {e}")
            return {"success": False, "error": str(e)}
    
    # === Streamlit Integration ===
    
    def create_login_widget(self) -> Dict[str, Any]:
        """Create Streamlit login widget"""
        try:
            st.markdown("### 🔐 Google Authentication")
            
            # Check if user is already authenticated
            if "auth_token" in st.session_state:
                session_validation = self.validate_session(st.session_state.auth_token)
                if session_validation.get("valid"):
                    user_data = session_validation["user"]
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.success(f"✅ Logged in as: {user_data.get('name')} ({user_data.get('email')})")
                    with col2:
                        if st.button("Logout"):
                            self.logout_user(st.session_state.auth_token)
                            del st.session_state.auth_token
                            st.rerun()
                    
                    return {
                        "authenticated": True,
                        "user": user_data
                    }
            
            # Show login button
            auth_url = self.get_authorization_url()
            if auth_url:
                st.markdown(f"""
                <a href="{auth_url}" target="_blank">
                    <button style="
                        background-color: #4285f4;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                    ">
                        🔗 Sign in with Google
                    </button>
                </a>
                """, unsafe_allow_html=True)
                
                # Handle callback (you would need to implement this based on your deployment)
                st.info("After signing in, you'll be redirected back to continue using the application.")
            else:
                st.error("❌ Authentication not properly configured")
            
            return {"authenticated": False}
            
        except Exception as e:
            logger.error(f"Error creating login widget: {e}")
            st.error(f"Authentication error: {str(e)}")
            return {"authenticated": False}
    
    def require_authentication(self, required_permission: str = None):
        """Decorator to require authentication for Streamlit functions"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if "auth_token" not in st.session_state:
                    st.warning("🔒 Please authenticate to access this feature")
                    self.create_login_widget()
                    return None
                
                session_validation = self.validate_session(st.session_state.auth_token)
                if not session_validation.get("valid"):
                    st.error("❌ Session expired. Please log in again.")
                    del st.session_state.auth_token
                    st.rerun()
                    return None
                
                if required_permission and not self.check_permission(st.session_state.auth_token, required_permission):
                    st.error(f"❌ Insufficient permissions. Required: {required_permission}")
                    return None
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    # === User Management ===
    
    def get_authenticated_users(self) -> List[Dict[str, Any]]:
        """Get list of currently authenticated users"""
        users = []
        for user_id, session_data in self.authenticated_users.items():
            users.append({
                "user_id": user_id,
                "email": session_data.get("email"),
                "name": session_data.get("name"),
                "created_at": session_data.get("created_at"),
                "permissions": session_data.get("permissions", [])
            })
        return users
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        try:
            current_time = datetime.utcnow()
            expired_tokens = []
            
            for token, session_data in self.user_sessions.items():
                expires_at = datetime.fromisoformat(session_data["expires_at"])
                if current_time > expires_at:
                    expired_tokens.append(token)
            
            for token in expired_tokens:
                user_id = self.user_sessions[token].get("user_id")
                del self.user_sessions[token]
                if user_id in self.authenticated_users:
                    del self.authenticated_users[user_id]
            
            if expired_tokens:
                logger.info(f"Cleaned up {len(expired_tokens)} expired sessions")
                
        except Exception as e:
            logger.error(f"Error cleaning up expired sessions: {e}")
    
    # === Security Features ===
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token for form protection"""
        return secrets.token_urlsafe(32)
    
    def validate_csrf_token(self, token: str, expected_token: str) -> bool:
        """Validate CSRF token"""
        return secrets.compare_digest(token, expected_token)
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for web responses"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.gstatic.com"
        }
    
    # === Status and Monitoring ===
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Get authentication system status"""
        return {
            "oauth_configured": bool(self.client_id and self.client_secret),
            "firebase_available": FIREBASE_AVAILABLE and self.firebase_app is not None,
            "active_sessions": len(self.user_sessions),
            "authenticated_users": len(self.authenticated_users),
            "timestamp": datetime.utcnow().isoformat()
        }

# Global instance
google_auth_manager = GoogleAuthManager() 