#!/bin/bash

FUNCTION_URL=$1

if [ -z "$FUNCTION_URL" ]; then
    echo "Usage: $0 <function-url>"
    echo "Example: $0 https://your-region-your-project.cloudfunctions.net/fi-mcp-function"
    exit 1
fi

echo "🧪 Testing Fi MCP Function deployment..."

# Test health endpoint
echo "1. Testing health endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "404" ]; then
    echo "   ✅ Function is responding (HTTP $HTTP_CODE)"
else
    echo "   ❌ Function not responding (HTTP $HTTP_CODE)"
    exit 1
fi

# Test MCP endpoint
echo "2. Testing MCP endpoint..."
MCP_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Mcp-Session-Id: test-session-123" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
    "$FUNCTION_URL/mcp/stream")

if echo "$MCP_RESPONSE" | grep -q "tools"; then
    echo "   ✅ MCP endpoint is working"
else
    echo "   ❌ MCP endpoint not working"
    echo "   Response: $MCP_RESPONSE"
fi

# Test static files
echo "3. Testing static files..."
STATIC_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL/static/fi_qr.png")
if [ "$STATIC_CODE" = "200" ]; then
    echo "   ✅ Static files are served correctly"
else
    echo "   ❌ Static files not accessible (HTTP $STATIC_CODE)"
fi

# Test login page
echo "4. Testing login page..."
LOGIN_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FUNCTION_URL/mockWebPage?sessionId=test-123")
if [ "$LOGIN_CODE" = "200" ]; then
    echo "   ✅ Login page is accessible"
else
    echo "   ❌ Login page not accessible (HTTP $LOGIN_CODE)"
fi

echo "🎉 Deployment test completed!"
echo ""
echo "📝 Manual tests to perform:"
echo "   1. Open $FUNCTION_URL/mockWebPage?sessionId=test-session in browser"
echo "   2. Login with phone number: 1111111111"
echo "   3. Test MCP tools after authentication" 