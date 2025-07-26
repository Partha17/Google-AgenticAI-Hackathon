import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json();
    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    // TODO: Replace with actual connection to your Python backend
    // For now, return a mock response
    const mockResponse = `Thank you for your question: "${message}".
I'm FinGenie, your AI financial assistant. I can help you with:
📊 **Portfolio Analysis** - Risk assessment, diversification analysis
💰 **Investment Recommendations** - Based on your goals and risk tolerance
📈 **Market Insights** - Current trends and opportunities
🎯 **Financial Planning** - Goal setting and strategy development
To get started, I'll need to connect to your financial data through our secure MCP server. Would you like me to analyze your current portfolio or help you with a specific financial goal?`;

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 1000));

    return NextResponse.json({
      response: mockResponse,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}