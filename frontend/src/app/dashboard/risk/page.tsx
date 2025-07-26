'use client';

import MainLayout from '@/components/Layout/MainLayout';
import { AlertTriangle, BarChart3, Shield, Target, TrendingUp, Zap } from 'lucide-react';

// Mock Risk Data
const riskData = {
  overallRiskScore: 65,
  riskLevel: 'Moderate',
  riskCategory: 'Balanced',
  portfolioRisk: {
    equity: 60,
    debt: 24,
    gold: 10,
    cash: 6
  },
  riskMetrics: {
    volatility: 12.5,
    beta: 0.85,
    sharpeRatio: 1.2,
    maxDrawdown: -8.2,
    var95: -5.8,
    correlation: 0.75
  },
  assetRiskAnalysis: [
    {
      asset: 'Equity Funds',
      allocation: 60,
      risk: 'High',
      return: 12.5,
      volatility: 18.2,
      recommendation: 'Maintain allocation'
    },
    {
      asset: 'Debt Funds',
      allocation: 24,
      risk: 'Low',
      return: 7.2,
      volatility: 3.5,
      recommendation: 'Increase allocation'
    },
    {
      asset: 'Gold ETF',
      allocation: 10,
      risk: 'Medium',
      return: 8.5,
      volatility: 15.8,
      recommendation: 'Hold current position'
    },
    {
      asset: 'Cash',
      allocation: 6,
      risk: 'Very Low',
      return: 4.2,
      volatility: 0.5,
      recommendation: 'Reduce for better returns'
    }
  ],
  sipRiskAnalysis: [
    {
      fund: 'Axis Bluechip Fund',
      amount: 10000,
      risk: 'Medium',
      performance: 8.5,
      recommendation: 'Continue SIP'
    },
    {
      fund: 'HDFC Mid-Cap Fund',
      amount: 8000,
      risk: 'High',
      performance: 6.2,
      recommendation: 'Consider switching'
    },
    {
      fund: 'ICICI Prudential Balanced Fund',
      amount: 7000,
      risk: 'Low',
      performance: 9.1,
      recommendation: 'Increase allocation'
    }
  ],
  riskAlerts: [
    {
      type: 'High Concentration',
      message: '60% allocation in equity - consider rebalancing',
      severity: 'Medium',
      action: 'Rebalance portfolio'
    },
    {
      type: 'Underperforming SIP',
      message: 'HDFC Mid-Cap Fund underperforming benchmark',
      severity: 'High',
      action: 'Review and switch'
    },
    {
      type: 'Low Diversification',
      message: 'Only 4 asset classes - consider adding more',
      severity: 'Low',
      action: 'Add international funds'
    }
  ],
  stressTest: {
    scenario1: { name: 'Market Crash (-20%)', impact: -12.5 },
    scenario2: { name: 'Interest Rate Hike', impact: -3.2 },
    scenario3: { name: 'Inflation Spike', impact: -5.8 },
    scenario4: { name: 'Currency Depreciation', impact: -2.1 }
  }
};

export default function RiskPage() {
  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'very low': return 'text-green-600';
      case 'low': return 'text-blue-600';
      case 'medium': return 'text-yellow-600';
      case 'high': return 'text-orange-600';
      case 'very high': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'low': return 'bg-green-100 text-green-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'high': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Risk Manager</h1>
          <p className="text-gray-600 mt-2">Comprehensive risk analysis and management</p>
        </div>

        {/* Risk Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Shield className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Risk Score</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {riskData.overallRiskScore}/100
            </div>
            <div className="text-sm text-gray-600">{riskData.riskLevel}</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Target className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Risk Category</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {riskData.riskCategory}
            </div>
            <div className="text-sm text-gray-600">Portfolio type</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <BarChart3 className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Volatility</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {riskData.riskMetrics.volatility}%
            </div>
            <div className="text-sm text-gray-600">Annualized</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="h-5 w-5 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Sharpe Ratio</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {riskData.riskMetrics.sharpeRatio}
            </div>
            <div className="text-sm text-gray-600">Risk-adjusted return</div>
          </div>
        </div>

        {/* Risk Metrics */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Metrics</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{riskData.riskMetrics.beta}</div>
              <div className="text-sm text-gray-600">Beta</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{riskData.riskMetrics.volatility}%</div>
              <div className="text-sm text-gray-600">Volatility</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{riskData.riskMetrics.sharpeRatio}</div>
              <div className="text-sm text-gray-600">Sharpe Ratio</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">{riskData.riskMetrics.maxDrawdown}%</div>
              <div className="text-sm text-gray-600">Max Drawdown</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">{riskData.riskMetrics.var95}%</div>
              <div className="text-sm text-gray-600">VaR (95%)</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{riskData.riskMetrics.correlation}</div>
              <div className="text-sm text-gray-600">Correlation</div>
            </div>
          </div>
        </div>

        {/* Asset Risk Analysis */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Asset Risk Analysis</h3>
          <div className="space-y-4">
            {riskData.assetRiskAnalysis.map((asset, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h4 className="font-medium text-gray-900">{asset.asset}</h4>
                    <p className="text-sm text-gray-600">Allocation: {asset.allocation}%</p>
                  </div>
                  <div className={`px-2 py-1 rounded-full text-xs ${getRiskColor(asset.risk)}`}>
                    {asset.risk} Risk
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <div className="text-sm text-gray-600">Expected Return</div>
                    <div className="font-medium text-gray-900">{asset.return}%</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Volatility</div>
                    <div className="font-medium text-gray-900">{asset.volatility}%</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Risk Level</div>
                    <div className={`font-medium ${getRiskColor(asset.risk)}`}>{asset.risk}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Recommendation</div>
                    <div className="font-medium text-gray-900">{asset.recommendation}</div>
                  </div>
                </div>

                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${asset.allocation}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* SIP Risk Analysis */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">SIP Risk Analysis</h3>
          <div className="space-y-4">
            {riskData.sipRiskAnalysis.map((sip, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <BarChart3 className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{sip.fund}</h4>
                    <p className="text-sm text-gray-600">₹{sip.amount.toLocaleString()}/month</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-center">
                    <div className={`text-sm font-medium ${getRiskColor(sip.risk)}`}>{sip.risk}</div>
                    <div className="text-xs text-gray-600">Risk</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-medium text-gray-900">{sip.performance}%</div>
                    <div className="text-xs text-gray-600">Performance</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-medium text-blue-600">{sip.recommendation}</div>
                    <div className="text-xs text-gray-600">Action</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Alerts */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Alerts</h3>
          <div className="space-y-4">
            {riskData.riskAlerts.map((alert, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="p-2 bg-red-100 rounded-lg">
                  <AlertTriangle className="h-5 w-5 text-red-600" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-medium text-gray-900">{alert.type}</h4>
                    <span className={`text-xs px-2 py-1 rounded-full ${getSeverityColor(alert.severity)}`}>
                      {alert.severity}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{alert.message}</p>
                  <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                    {alert.action}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Stress Testing */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Stress Testing</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(riskData.stressTest).map(([key, scenario]) => (
              <div key={key} className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">{scenario.name}</h4>
                <div className={`text-2xl font-bold ${scenario.impact >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {scenario.impact >= 0 ? '+' : ''}{scenario.impact}%
                </div>
                <div className="text-sm text-gray-600">Portfolio impact</div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
              <Shield className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">Risk Assessment</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <Target className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Rebalance Portfolio</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <Zap className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Stress Test</span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}