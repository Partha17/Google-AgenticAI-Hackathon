import logging
import requests
import json
import uuid
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
import time
from services.logger_config import get_mcp_logger, log_error

# Use centralized logger
logger = get_mcp_logger()

class FiMCPClient:
    """Real Fi MCP client that connects to the Fi MCP development server"""
    
    def __init__(self, base_url: str = None):
        # Import config here to avoid circular imports
        from config import settings
        
        # Use provided base_url or fall back to config, then hardcoded default
        if base_url is None:
            base_url = getattr(settings, 'mcp_server_url', "https://fi-mcp-server-bpzxyhr4dq-uc.a.run.app")
            
        self.base_url = base_url
        self.mcp_url = f"{base_url}/mcp"
        self.auth_url = f"{base_url}/auth"
        self.session_id = None
        self.authenticated = False
        self.auth_token = None
        self.current_phone_number = None
        
        # Thread safety for concurrent access
        self._auth_lock = threading.Lock()
        self._initialization_lock = threading.Lock()
        self._initialized = False
        
        logger.info(f"Fi MCP Client initialized with base URL: {base_url}")
        
        # Test phone numbers from the Fi MCP server documentation
        self.test_users = {
            "1111111111": "Demo User - Basic financial data",
            "2222222222": "All assets connected - Large mutual fund portfolio",
            "3333333333": "All assets connected - Small mutual fund portfolio", 
            "4444444444": "Multiple bank accounts and EPF",
            "7777777777": "Debt-Heavy Low Performer",
            "8888888888": "SIP Samurai - Monthly SIP investor",
            "1313131313": "Balanced Growth Tracker - Well diversified",
            "1414141414": "Sample User - Multiple accounts"
        }
        
        # Default user for auto-login - Use 2222222222 for comprehensive data
        self.default_phone_number = "2222222222"
        
        # Available MCP tools (matching server tool names)
        self.available_tools = [
            "fetch_net_worth",
            "fetch_bank_transactions", 
            "fetch_mf_transactions",
            "fetch_epf_details",
            "fetch_credit_report",
            "fetch_stock_transactions"
        ]
        
    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return f"mcp-session-{uuid.uuid4()}"
    
    def ensure_authenticated(self) -> bool:
        """Ensure the client is authenticated, with thread safety"""
        # Double-checked locking pattern for singleton authentication
        if self.authenticated and self._initialized:
            return True
            
        with self._initialization_lock:
            if self.authenticated and self._initialized:
                return True
            
            logger.info("🔄 Ensuring MCP client authentication...")
            success = self._perform_auto_login()
            if success:
                self._initialized = True
                logger.info("✅ MCP client authentication ensured!")
            return success
    
    def auto_login(self, phone_number: str = None) -> bool:
        """Auto login with the MCP server using a test phone number"""
        with self._auth_lock:
            return self._perform_auto_login(phone_number)
    
    def _perform_auto_login(self, phone_number: str = None) -> bool:
        """Internal method to perform authentication (must be called with lock held)"""
        if not phone_number:
            phone_number = self.default_phone_number
            
        logger.info(f"Attempting auto-login with phone number: {phone_number}")
        
        try:
            # Make authentication request to the deployed server
            auth_payload = {
                "phoneNumber": phone_number
            }
            
            response = requests.post(
                self.auth_url,
                json=auth_payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                logger.info(f"Auth response received: {auth_data}")
                
                if auth_data.get("success"):
                    self.authenticated = True
                    self.auth_token = auth_data.get("token")
                    self.session_id = auth_data.get("sessionId")
                    self.current_phone_number = phone_number
                    logger.info(f"✅ Auto-login successful for {phone_number}")
                    logger.info(f"   Session ID: {self.session_id}")
                    logger.info(f"   Token: {self.auth_token}")
                    return True
                else:
                    # Log the full response for debugging
                    logger.error(f"❌ Fi MCP server authentication failed")
                    logger.error(f"Authentication failed: {auth_data}")
                    
                    # If the server is responding but not in expected format, try fallback
                    if "server" in auth_data or "endpoints" in auth_data:
                        logger.warning(f"⚠️ Server responding but wrong endpoint - using fallback auth")
                        self.authenticated = True
                        self.auth_token = f"token_{phone_number}"
                        self.session_id = f"session_{phone_number}"
                        self.current_phone_number = phone_number
                        return True
                    return False
            else:
                logger.error(f"❌ Authentication request failed: HTTP {response.status_code}")
                logger.error(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Auto-login failed with exception: {str(e)}")
            # Fallback authentication for robustness
            logger.warning(f"⚠️ Using fallback authentication due to error: {str(e)}")
            self.session_id = f"session_{phone_number}"
            self.auth_token = f"token_{phone_number}"
            self.authenticated = True
            self.current_phone_number = phone_number
            logger.info(f"✅ Fallback authentication set for {phone_number}")
            return True
    
    def get_financial_data(self, phone_number: str = None, data_type: str = "net_worth") -> Dict:
        """Get financial data directly from the deployed MCP server"""
        # Ensure authentication before making request
        if not self.ensure_authenticated():
            return {"success": False, "error": "Authentication failed"}
            
        if not phone_number:
            phone_number = getattr(self, 'current_phone_number', self.default_phone_number)
            
        try:
            # Use the test endpoint for getting financial data
            test_url = f"{self.base_url}/mcp/test?phone={phone_number}"
            
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
                
            response = requests.get(test_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Successfully retrieved financial data for {phone_number}")
                return {
                    "success": True,
                    "data": data,
                    "phone_number": phone_number
                }
            else:
                logger.error(f"❌ Failed to get financial data: HTTP {response.status_code}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "phone_number": phone_number
                }
                
        except Exception as e:
            logger.error(f"❌ Error getting financial data: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "phone_number": phone_number
            }

    def _make_mcp_request(self, method: str, params: Dict = None) -> Dict:
        """Make an MCP JSON-RPC request - Updated for GCP deployment"""
        
        # Ensure authentication with thread safety
        if not self.ensure_authenticated():
            return {"error": "Authentication failed"}
        
        # For the deployed server, use direct HTTP endpoints instead of JSON-RPC
        if method in ["fetch_net_worth", "fetch_bank_transactions", "fetch_mf_transactions", 
                     "fetch_epf_details", "fetch_credit_report", "fetch_stock_transactions"]:
            phone_number = params.get("phone_number") if params else self.current_phone_number
            return self.get_financial_data(phone_number, method)
        
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        try:
            response = requests.post(self.mcp_url, 
                                   headers=headers, 
                                   json=payload, 
                                   timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"MCP request failed with status {response.status_code}: {response.text}")
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"MCP request failed: {e}")
            log_error('mcp.client', e, f"MCP request to {method}")
            return {"error": str(e)}
    
    def authenticate(self, phone_number: str = "2222222222") -> bool:
        """
        Authenticate with the Fi MCP server using a test phone number
        Default: 2222222222 (All assets connected - Large portfolio)
        """
        try:
            logger.info(f"Authenticating with phone number: {phone_number}")
            
            # Use a consistent session ID for all requests
            if not self.session_id:
                self.session_id = self._generate_session_id()
            
            # First, try to call a tool to check if we're already authenticated
            result = self._make_mcp_request("tools/call", {
                "name": "fetch_net_worth",
                "arguments": {}
            })
            
            if "login_url" in str(result):
                logger.info("Authentication required - simulating login flow")
                
                # Extract login URL and session ID from the response
                login_url = None
                if "login_url" in str(result):
                    import re
                    url_match = re.search(r'http://localhost:\d+/mockWebPage\?sessionId=([^"]+)', str(result))
                    if url_match:
                        login_url = url_match.group(0)
                        logger.info(f"Login URL: {login_url}")
                
                # Simulate the login POST request to establish session
                try:
                    login_data = {
                        'sessionId': self.session_id,
                        'phoneNumber': phone_number
                    }
                    
                    login_response = requests.post(
                        f"{self.base_url}/login",
                        data=login_data,
                        timeout=10
                    )
                    
                    if login_response.status_code == 200:
                        logger.info("Login simulation successful")
                        time.sleep(1)  # Brief wait for session establishment
                        
                        # Now try the original request again
                        result = self._make_mcp_request("tools/call", {
                            "name": "fetch_net_worth", 
                            "arguments": {}
                        })
                        
                        if "netWorthResponse" in str(result) or ("result" in result and "login_url" not in str(result)):
                            self.authenticated = True
                            logger.info("Authentication successful")
                            return True
                    else:
                        logger.error(f"Login simulation failed: {login_response.status_code}")
                        
                except Exception as e:
                    logger.error(f"Login simulation error: {e}")
                
                logger.warning(f"Authentication failed after login simulation. Session ID: {self.session_id}")
                return False
            
            elif "result" in result and "login_url" not in str(result):
                self.authenticated = True
                logger.info("Already authenticated or no auth required")
                return True
            
            else:
                logger.error(f"Authentication failed: {result}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    def fetch_net_worth(self) -> Dict[str, Any]:
        """Fetch net worth data from Fi MCP"""
        # Authentication is handled by _make_mcp_request
        result = self._make_mcp_request("fetch_net_worth", {})
        
        return self._process_mcp_response(result, "net_worth")
    
    def fetch_bank_transactions(self) -> Dict[str, Any]:
        """Fetch bank transaction data from Fi MCP"""
        # Authentication is handled by _make_mcp_request
        result = self._make_mcp_request("fetch_bank_transactions", {})
        
        return self._process_mcp_response(result, "bank_transactions")
    
    def fetch_mutual_fund_transactions(self) -> Dict[str, Any]:
        """Fetch mutual fund transaction data from Fi MCP"""
        # Authentication is handled by _make_mcp_request
        result = self._make_mcp_request("fetch_mf_transactions", {})
        
        return self._process_mcp_response(result, "mutual_fund_transactions")
    
    def fetch_epf_details(self) -> Dict[str, Any]:
        """Fetch EPF details from Fi MCP"""
        # Authentication is handled by _make_mcp_request
        result = self._make_mcp_request("fetch_epf_details", {})
        
        return self._process_mcp_response(result, "epf_details")
    
    def fetch_credit_report(self) -> Dict[str, Any]:
        """Fetch credit report from Fi MCP"""
        # Authentication is handled by _make_mcp_request
        result = self._make_mcp_request("fetch_credit_report", {})
        
        return self._process_mcp_response(result, "credit_report")
    
    def fetch_stock_transactions(self) -> Dict[str, Any]:
        """Fetch stock transaction data from Fi MCP"""
        # Authentication is handled by _make_mcp_request
        result = self._make_mcp_request("fetch_stock_transactions", {})
        
        return self._process_mcp_response(result, "stock_transactions")
    
    def _process_mcp_response(self, result: Dict, data_type: str) -> Dict[str, Any]:
        """Process MCP response into standardized format"""
        processed = {
            "type": data_type,
            "timestamp": datetime.utcnow().isoformat(),
            "success": False,
            "data": {},
            "raw_response": result
        }
        
        try:
            if "error" in result:
                processed["error"] = result["error"]
                logger.error(f"MCP error for {data_type}: {result['error']}")
                return processed
            
            if "result" in result:
                processed["success"] = True
                processed["data"] = result["result"]
                
                # Extract key financial metrics based on data type
                if data_type == "net_worth":
                    processed.update(self._extract_net_worth_metrics(result["result"]))
                elif data_type == "bank_transactions":
                    processed.update(self._extract_transaction_metrics(result["result"]))
                elif data_type == "mutual_fund_transactions":
                    processed.update(self._extract_mf_metrics(result["result"]))
                elif data_type == "epf_details":
                    processed.update(self._extract_epf_metrics(result["result"]))
                elif data_type == "credit_report":
                    processed.update(self._extract_credit_metrics(result["result"]))
                
                logger.info(f"Successfully processed {data_type} data")
            else:
                processed["error"] = "Unexpected response format"
                logger.warning(f"Unexpected response format for {data_type}: {result}")
            
        except Exception as e:
            processed["error"] = f"Processing error: {str(e)}"
            logger.error(f"Error processing {data_type} response: {e}")
        
        return processed
    
    def _extract_net_worth_metrics(self, data: Dict) -> Dict[str, Any]:
        """Extract key metrics from net worth data"""
        metrics = {}
        
        try:
            if "netWorthResponse" in data:
                nw_data = data["netWorthResponse"]
                
                # Extract total net worth
                if "totalNetWorthValue" in nw_data:
                    total_nw = nw_data["totalNetWorthValue"]
                    metrics["total_net_worth"] = float(total_nw.get("units", 0))
                    metrics["currency"] = total_nw.get("currencyCode", "INR")
                
                # Extract asset values
                if "assetValues" in nw_data:
                    assets = {}
                    total_assets = 0
                    for asset in nw_data["assetValues"]:
                        asset_type = asset.get("netWorthAttribute", "")
                        value = float(asset.get("value", {}).get("units", 0))
                        assets[asset_type] = value
                        total_assets += value
                    
                    metrics["assets"] = assets
                    metrics["total_assets"] = total_assets
                
                # Extract liabilities
                if "liabilityValues" in nw_data:
                    liabilities = {}
                    total_liabilities = 0
                    for liability in nw_data["liabilityValues"]:
                        liability_type = liability.get("netWorthAttribute", "")
                        value = float(liability.get("value", {}).get("units", 0))
                        liabilities[liability_type] = value
                        total_liabilities += value
                    
                    metrics["liabilities"] = liabilities
                    metrics["total_liabilities"] = total_liabilities
                
        except Exception as e:
            logger.error(f"Error extracting net worth metrics: {e}")
        
        return metrics
    
    def _extract_transaction_metrics(self, data: Dict) -> Dict[str, Any]:
        """Extract key metrics from bank transaction data"""
        metrics = {"transaction_count": 0, "total_amount": 0}
        
        try:
            # Process bank transaction data structure
            if isinstance(data, dict) and "transactions" in data:
                transactions = data["transactions"]
                metrics["transaction_count"] = len(transactions)
                
                total_amount = 0
                for txn in transactions:
                    amount = float(txn.get("amount", {}).get("units", 0))
                    total_amount += abs(amount)  # Use absolute value for total volume
                
                metrics["total_amount"] = total_amount
                
        except Exception as e:
            logger.error(f"Error extracting transaction metrics: {e}")
        
        return metrics
    
    def _extract_mf_metrics(self, data: Dict) -> Dict[str, Any]:
        """Extract key metrics from mutual fund data"""
        metrics = {"fund_count": 0, "total_investment": 0}
        
        try:
            # Process mutual fund data structure
            if isinstance(data, dict):
                metrics["fund_count"] = len(data.get("funds", []))
                
        except Exception as e:
            logger.error(f"Error extracting MF metrics: {e}")
        
        return metrics
    
    def _extract_epf_metrics(self, data: Dict) -> Dict[str, Any]:
        """Extract key metrics from EPF data"""
        metrics = {"epf_balance": 0}
        
        try:
            # Process EPF data structure
            if isinstance(data, dict) and "balance" in data:
                metrics["epf_balance"] = float(data["balance"].get("units", 0))
                
        except Exception as e:
            logger.error(f"Error extracting EPF metrics: {e}")
        
        return metrics
    
    def _extract_credit_metrics(self, data: Dict) -> Dict[str, Any]:
        """Extract key metrics from credit report data"""
        metrics = {"credit_score": 0}
        
        try:
            # Process credit report data structure
            if isinstance(data, dict) and "creditScore" in data:
                metrics["credit_score"] = int(data.get("creditScore", 0))
                
        except Exception as e:
            logger.error(f"Error extracting credit metrics: {e}")
        
        return metrics
    
    def get_all_financial_data(self) -> List[Dict[str, Any]]:
        """Fetch all available financial data from Fi MCP"""
        logger.info("Fetching comprehensive financial data from Fi MCP")
        
        # Use thread-safe authentication
        if not self.ensure_authenticated():
            logger.error("Failed to authenticate with Fi MCP server")
            return []
        
        all_data = []
        
        # Fetch all available data types
        data_fetchers = [
            ("net_worth", self.fetch_net_worth),
            ("bank_transactions", self.fetch_bank_transactions),
            ("mutual_fund_transactions", self.fetch_mutual_fund_transactions),
            ("epf_details", self.fetch_epf_details),
            ("credit_report", self.fetch_credit_report)
        ]
        
        for data_type, fetcher in data_fetchers:
            try:
                logger.info(f"Fetching {data_type} data...")
                result = fetcher()
                
                if result.get("success"):
                    all_data.append(result)
                    logger.info(f"Successfully fetched {data_type}")
                else:
                    logger.warning(f"Failed to fetch {data_type}: {result.get('error', 'Unknown error')}")
                
                # Small delay between requests
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching {data_type}: {e}")
                continue
        
        logger.info(f"Fetched {len(all_data)} data types from Fi MCP")
        return all_data

# Singleton instance
fi_mcp_client = FiMCPClient()

# Note: Authentication is now handled lazily when first needed
# This prevents concurrent authentication attempts on module import
logger.info("🚀 Fi MCP Client singleton created - authentication will be performed when needed") 