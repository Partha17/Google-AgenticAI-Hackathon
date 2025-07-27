import logging
import requests
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import time
from services.logger_config import get_mcp_logger, log_error

# Use centralized logger
logger = get_mcp_logger()

class FiMCPClient:
    """Real Fi MCP client that connects to the Fi MCP development server"""

    def __init__(self, base_url: str = "https://fi-mcp-server-bpzxyhr4dq-uc.a.run.app"):
        self.base_url = base_url
        self.mcp_url = f"{base_url}/mcp/stream"
        self.test_url = f"{base_url}/mcp/test"
        self.session_id = None
        self.authenticated = False
        self.phone_number = None
        logger.info(f"Fi MCP Client initialized with base URL: {base_url}")

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

    def _make_mcp_request(self, method: str, params: Dict = None) -> Dict:
        """Make an MCP JSON-RPC request"""
        # Only generate session ID if we don't have one
        if not self.session_id:
            self.session_id = self._generate_session_id()
            logger.info(f"Generated new session ID: {self.session_id}")

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
            log_error('mcp.client', e, f"MCP request to {method}")
            return {"error": str(e)}

    def authenticate(self, phone_number: str = "2222222222") -> bool:
        """
        Authenticate with the Fi MCP server using a test phone number
        Default: 2222222222 (All assets connected - Large portfolio)
        """
        try:
            logger.info(f"Authenticating with phone number: {phone_number}")
            self.phone_number = phone_number

            # For deployed server, we use the test endpoint directly
            if "a.run.app" in self.base_url:
                # Test the connection by fetching net worth data
                test_response = requests.get(f"{self.test_url}?phone={phone_number}", timeout=10)

                if test_response.status_code == 200:
                    try:
                        data = test_response.json()
                        if "netWorthResponse" in data:
                            self.authenticated = True
                            logger.info(f"Successfully authenticated with deployed server using phone: {phone_number}")
                            return True
                        else:
                            logger.error(f"Unexpected response format from deployed server: {data}")
                            return False
                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON response from deployed server: {test_response.text}")
                        return False
                else:
                    logger.error(f"Failed to connect to deployed server: {test_response.status_code}")
                    return False
            else:
                # Original local server logic
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
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}

        try:
            if "a.run.app" in self.base_url and self.phone_number:
                # Use deployed server's test endpoint
                response = requests.get(f"{self.test_url}?phone={self.phone_number}", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    return self._process_mcp_response(data, "net_worth")
                else:
                    logger.error(f"Failed to fetch net worth from deployed server: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}"}
            else:
                # Original local server logic
                result = self._make_mcp_request("tools/call", {
                    "name": "fetch_net_worth",
                    "arguments": {}
                })
                return self._process_mcp_response(result, "net_worth")

        except Exception as e:
            logger.error(f"Error fetching net worth: {e}")
            return {"error": str(e)}

    def fetch_bank_transactions(self) -> Dict[str, Any]:
        """Fetch bank transaction data from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}

        try:
            if "a.run.app" in self.base_url and self.phone_number:
                # Use deployed server's test endpoint (returns all data)
                response = requests.get(f"{self.test_url}?phone={self.phone_number}", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    return self._process_mcp_response(data, "bank_transactions")
                else:
                    logger.error(f"Failed to fetch bank transactions from deployed server: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}"}
            else:
                # Original local server logic
                result = self._make_mcp_request("tools/call", {
                    "name": "fetch_bank_transactions",
                    "arguments": {}
                })
                return self._process_mcp_response(result, "bank_transactions")

        except Exception as e:
            logger.error(f"Error fetching bank transactions: {e}")
            return {"error": str(e)}

    def fetch_mutual_fund_transactions(self) -> Dict[str, Any]:
        """Fetch mutual fund transaction data from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}

        try:
            if "a.run.app" in self.base_url and self.phone_number:
                # Use deployed server's test endpoint (returns all data)
                response = requests.get(f"{self.test_url}?phone={self.phone_number}", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    return self._process_mcp_response(data, "mf_transactions")
                else:
                    logger.error(f"Failed to fetch MF transactions from deployed server: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}"}
            else:
                # Original local server logic
                result = self._make_mcp_request("tools/call", {
                    "name": "fetch_mf_transactions",
                    "arguments": {}
                })
                return self._process_mcp_response(result, "mf_transactions")

        except Exception as e:
            logger.error(f"Error fetching MF transactions: {e}")
            return {"error": str(e)}

    def fetch_epf_details(self) -> Dict[str, Any]:
        """Fetch EPF details from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}

        try:
            if "a.run.app" in self.base_url and self.phone_number:
                # Use deployed server's test endpoint (returns all data)
                response = requests.get(f"{self.test_url}?phone={self.phone_number}", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    return self._process_mcp_response(data, "epf_details")
                else:
                    logger.error(f"Failed to fetch EPF details from deployed server: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}"}
            else:
                # Original local server logic
                result = self._make_mcp_request("tools/call", {
                    "name": "fetch_epf_details",
                    "arguments": {}
                })
                return self._process_mcp_response(result, "epf_details")

        except Exception as e:
            logger.error(f"Error fetching EPF details: {e}")
            return {"error": str(e)}

    def fetch_credit_report(self) -> Dict[str, Any]:
        """Fetch credit report from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}

        try:
            if "a.run.app" in self.base_url and self.phone_number:
                # Use deployed server's test endpoint (returns all data)
                response = requests.get(f"{self.test_url}?phone={self.phone_number}", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    return self._process_mcp_response(data, "credit_report")
                else:
                    logger.error(f"Failed to fetch credit report from deployed server: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}"}
            else:
                # Original local server logic
                result = self._make_mcp_request("tools/call", {
                    "name": "fetch_credit_report",
                    "arguments": {}
                })
                return self._process_mcp_response(result, "credit_report")

        except Exception as e:
            logger.error(f"Error fetching credit report: {e}")
            return {"error": str(e)}

    def fetch_stock_transactions(self) -> Dict[str, Any]:
        """Fetch stock transaction data from Fi MCP"""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication required"}

        try:
            if "a.run.app" in self.base_url and self.phone_number:
                # Use deployed server's test endpoint (returns all data)
                response = requests.get(f"{self.test_url}?phone={self.phone_number}", timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    return self._process_mcp_response(data, "stock_transactions")
                else:
                    logger.error(f"Failed to fetch stock transactions from deployed server: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}"}
            else:
                # Original local server logic
                result = self._make_mcp_request("tools/call", {
                    "name": "fetch_stock_transactions",
                    "arguments": {}
                })
                return self._process_mcp_response(result, "stock_transactions")

        except Exception as e:
            logger.error(f"Error fetching stock transactions: {e}")
            return {"error": str(e)}

    def _process_mcp_response(self, result: Dict, data_type: str) -> Dict[str, Any]:
        """Process MCP response into standardized format"""
        processed = {
            "success": False,
            "data_type": data_type,
            "timestamp": datetime.now().isoformat(),
            "raw_data": result
        }

        try:
            # For deployed server, the response contains all data types in one response
            if "a.run.app" in self.base_url:
                # The deployed server returns all data in one response
                # We need to extract the specific data type from the unified response
                if "netWorthResponse" in result:
                    # This is the main response containing all data
                    processed["success"] = True
                    processed["data"] = result

                    # Extract specific metrics based on data_type
                    if data_type == "net_worth":
                        processed.update(self._extract_net_worth_metrics(result))
                    elif data_type == "bank_transactions":
                        # For deployed server, bank transactions are in accountDetailsBulkResponse
                        if "accountDetailsBulkResponse" in result:
                            processed.update(self._extract_transaction_metrics(result))
                    elif data_type == "mf_transactions":
                        # For deployed server, MF data is in mfSchemeAnalytics
                        if "mfSchemeAnalytics" in result:
                            processed.update(self._extract_mf_metrics(result))
                    elif data_type == "epf_details":
                        # EPF data is in netWorthResponse.assetValues
                        if "netWorthResponse" in result and "assetValues" in result["netWorthResponse"]:
                            processed.update(self._extract_epf_metrics(result))
                    elif data_type == "credit_report":
                        # Credit report data might be in a different section
                        # For now, we'll use the net worth data as a proxy
                        processed.update(self._extract_credit_metrics(result))
                    elif data_type == "stock_transactions":
                        # Stock data is in accountDetailsBulkResponse
                        if "accountDetailsBulkResponse" in result:
                            processed.update(self._extract_stock_metrics(result))

                    logger.info(f"Successfully processed {data_type} data from deployed server")
                    return processed
                else:
                    logger.warning(f"Unexpected response format for {data_type}: {result}")
                    return processed
            else:
                # Original local server logic
                if "result" in result and result["result"]:
                    processed["success"] = True
                    processed["data"] = result["result"]

                    # Extract specific metrics based on data type
                    if data_type == "net_worth":
                        processed.update(self._extract_net_worth_metrics(result["result"]))
                    elif data_type == "bank_transactions":
                        processed.update(self._extract_transaction_metrics(result["result"]))
                    elif data_type == "mf_transactions":
                        processed.update(self._extract_mf_metrics(result["result"]))
                    elif data_type == "epf_details":
                        processed.update(self._extract_epf_metrics(result["result"]))
                    elif data_type == "credit_report":
                        processed.update(self._extract_credit_metrics(result["result"]))
                    elif data_type == "stock_transactions":
                        processed.update(self._extract_stock_metrics(result["result"]))

                    logger.info(f"Successfully processed {data_type} data")
                    return processed
                else:
                    logger.warning(f"Unexpected response format for {data_type}: {result}")
                    return processed

        except Exception as e:
            logger.error(f"Error processing {data_type} response: {e}")
            processed["error"] = str(e)

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

    def _extract_stock_metrics(self, data: Dict) -> Dict[str, Any]:
        """Extract key metrics from stock transaction data"""
        metrics = {"stock_transaction_count": 0, "total_stock_value": 0}

        try:
            # Process stock transaction data structure
            if isinstance(data, dict) and "transactions" in data:
                transactions = data["transactions"]
                metrics["stock_transaction_count"] = len(transactions)

                total_stock_value = 0
                for txn in transactions:
                    amount = float(txn.get("amount", {}).get("units", 0))
                    total_stock_value += abs(amount)

                metrics["total_stock_value"] = total_stock_value

        except Exception as e:
            logger.error(f"Error extracting stock metrics: {e}")

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
            ("credit_report", self.fetch_credit_report),
            ("stock_transactions", self.fetch_stock_transactions)
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