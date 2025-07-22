import logging
import requests
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import time

logger = logging.getLogger(__name__)

class FiMCPClient:
    """Real Fi MCP client that connects to the Fi MCP development server"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.mcp_url = f"{base_url}/mcp/stream"
        self.session_id = None
        self.authenticated = False
        
        # Test phone numbers from the Fi MCP server documentation
        self.test_users = {
            "2222222222": "All assets connected - Large mutual fund portfolio",
            "3333333333": "All assets connected - Small mutual fund portfolio", 
            "4444444444": "Multiple bank accounts and EPF",
            "7777777777": "Debt-Heavy Low Performer",
            "8888888888": "SIP Samurai - Monthly SIP investor",
            "1313131313": "Balanced Growth Tracker - Well diversified",
            "1616161616": "Early Retirement Dreamer - High savings rate"
        }
        
        # Available MCP tools
        self.available_tools = [
            "fetch_net_worth",
            "fetch_bank_transactions", 
            "fetch_mutual_fund_transactions",
            "fetch_epf_details",
            "fetch_credit_report"
        ]
        
    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return f"mcp-session-{uuid.uuid4()}"
    
    def _make_mcp_request(self, method: str, params: Dict = None) -> Dict:
        """Make an MCP JSON-RPC request"""
        if not self.session_id:
            self.session_id = self._generate_session_id()
        
        headers = {
            "Content-Type": "application/json",
            "Mcp-Session-Id": self.session_id
        }
        
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
            return {"error": str(e)}
    
    def authenticate(self, phone_number: str = "2222222222") -> bool:
        """
        Authenticate with the Fi MCP server using a test phone number
        Default: 2222222222 (All assets connected - Large portfolio)
        """
        try:
            logger.info(f"Authenticating with phone number: {phone_number}")
            
            # First, try to call a tool to trigger authentication flow
            result = self._make_mcp_request("tools/call", {
                "name": "fetch_net_worth",
                "arguments": {}
            })
            
            if "login_url" in str(result):
                logger.info("Authentication required - simulating login flow")
                
                # In a real scenario, user would visit the login URL
                # For automation, we'll simulate the authentication
                # The Fi MCP server uses dummy auth, so we just need to establish a session
                
                # Generate new session and try again
                self.session_id = self._generate_session_id()
                
                # Wait a moment and retry
                time.sleep(2)
                
                # Try the request again
                result = self._make_mcp_request("tools/call", {
                    "name": "fetch_net_worth", 
                    "arguments": {}
                })
                
                if "netWorthResponse" in str(result) or "result" in result:
                    self.authenticated = True
                    logger.info("Authentication successful")
                    return True
                else:
                    logger.warning("Authentication may be required - login URL needed")
                    logger.info(f"Login URL pattern detected. Use phone: {phone_number}")
                    return False
            
            elif "result" in result or "netWorthResponse" in str(result):
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
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}
        
        result = self._make_mcp_request("tools/call", {
            "name": "fetch_net_worth",
            "arguments": {}
        })
        
        return self._process_mcp_response(result, "net_worth")
    
    def fetch_bank_transactions(self) -> Dict[str, Any]:
        """Fetch bank transaction data from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}
        
        result = self._make_mcp_request("tools/call", {
            "name": "fetch_bank_transactions",
            "arguments": {}
        })
        
        return self._process_mcp_response(result, "bank_transactions")
    
    def fetch_mutual_fund_transactions(self) -> Dict[str, Any]:
        """Fetch mutual fund transaction data from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}
        
        result = self._make_mcp_request("tools/call", {
            "name": "fetch_mutual_fund_transactions", 
            "arguments": {}
        })
        
        return self._process_mcp_response(result, "mutual_fund_transactions")
    
    def fetch_epf_details(self) -> Dict[str, Any]:
        """Fetch EPF details from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}
        
        result = self._make_mcp_request("tools/call", {
            "name": "fetch_epf_details",
            "arguments": {}
        })
        
        return self._process_mcp_response(result, "epf_details")
    
    def fetch_credit_report(self) -> Dict[str, Any]:
        """Fetch credit report from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}
        
        result = self._make_mcp_request("tools/call", {
            "name": "fetch_credit_report",
            "arguments": {}
        })
        
        return self._process_mcp_response(result, "credit_report")
    
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
        
        # Authenticate first
        if not self.authenticate():
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