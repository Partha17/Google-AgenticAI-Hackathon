"use client";

import MainLayout from "@/components/Layout/MainLayout";
import {
  AlertTriangle,
  BarChart3,
  Calendar,
  CheckCircle,
  DollarSign,
  TrendingUp,
  Zap,
} from "lucide-react";

// Mock Liquidity Data
const liquidityData = {
  totalLiquidAssets: 450000,
  emergencyFund: 300000,
  monthlyExpenses: 75000,
  emergencyFundMonths: 4,
  liquidAssets: [
    {
      name: "Savings Account",
      amount: 150000,
      liquidity: "Instant",
      return: 3.5,
      risk: "Very Low",
      category: "Cash",
    },
    {
      name: "Fixed Deposits",
      amount: 200000,
      liquidity: "7-30 days",
      return: 7.2,
      risk: "Low",
      category: "Fixed Income",
    },
    {
      name: "Liquid Funds",
      amount: 100000,
      liquidity: "1-2 days",
      return: 6.8,
      risk: "Low",
      category: "Mutual Funds",
    },
  ],
  illiquidAssets: [
    {
      name: "Real Estate",
      amount: 5000000,
      liquidity: "3-6 months",
      return: 8.5,
      risk: "Medium",
      category: "Property",
    },
    {
      name: "Equity Funds",
      amount: 800000,
      liquidity: "3-5 days",
      return: 12.5,
      risk: "High",
      category: "Equity",
    },
    {
      name: "Gold ETF",
      amount: 200000,
      liquidity: "1-2 days",
      return: 8.2,
      risk: "Medium",
      category: "Commodity",
    },
  ],
  cashFlow: {
    monthlyIncome: 120000,
    monthlyExpenses: 75000,
    monthlySavings: 45000,
    upcomingExpenses: [
      { name: "Car Insurance", amount: 25000, due: "2024-08-15" },
      { name: "Property Tax", amount: 15000, due: "2024-09-01" },
      { name: "School Fees", amount: 50000, due: "2024-08-20" },
    ],
  },
  recommendations: [
    {
      type: "Emergency Fund",
      description: "Increase emergency fund to 6 months of expenses",
      current: 300000,
      target: 450000,
      action: "Save ₹15,000/month for 10 months",
    },
    {
      type: "Liquid Fund Allocation",
      description:
        "Move ₹50,000 from savings to liquid funds for better returns",
      potentialGain: 1650,
      action: "Transfer to liquid funds",
    },
    {
      type: "Fixed Deposit Ladder",
      description: "Create FD ladder for better liquidity management",
      potentialGain: 2000,
      action: "Split FDs into 3-month intervals",
    },
  ],
  liquidityRatios: {
    currentRatio: 2.1,
    quickRatio: 1.8,
    cashRatio: 0.9,
    workingCapital: 375000,
  },
};

export default function LiquidityPage() {
  const getLiquidityColor = (liquidity: string) => {
    if (liquidity.includes("Instant") || liquidity.includes("1-2"))
      return "text-green-600";
    if (liquidity.includes("7-30") || liquidity.includes("3-5"))
      return "text-yellow-600";
    return "text-red-600";
  };

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case "very low":
        return "text-green-600";
      case "low":
        return "text-blue-600";
      case "medium":
        return "text-yellow-600";
      case "high":
        return "text-red-600";
      default:
        return "text-gray-600";
    }
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Liquidity Manager
          </h1>
          <p className="text-gray-600 mt-2">
            Manage your liquid assets and cash flow
          </p>
        </div>

        {/* Liquidity Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <DollarSign className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Liquid Assets</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{liquidityData.totalLiquidAssets.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Readily available</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Emergency Fund</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{liquidityData.emergencyFund.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">
              {liquidityData.emergencyFundMonths} months coverage
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Calendar className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Monthly Expenses</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{liquidityData.monthlyExpenses.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Average monthly</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="h-5 w-5 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Working Capital</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{liquidityData.liquidityRatios.workingCapital.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Available for use</div>
          </div>
        </div>

        {/* Liquidity Ratios */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Liquidity Ratios
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {liquidityData.liquidityRatios.currentRatio}
              </div>
              <div className="text-sm text-gray-600">Current Ratio</div>
              <div className="text-xs text-green-600">Good</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {liquidityData.liquidityRatios.quickRatio}
              </div>
              <div className="text-sm text-gray-600">Quick Ratio</div>
              <div className="text-xs text-green-600">Good</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {liquidityData.liquidityRatios.cashRatio}
              </div>
              <div className="text-sm text-gray-600">Cash Ratio</div>
              <div className="text-xs text-yellow-600">Fair</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                ₹
                {(
                  liquidityData.liquidityRatios.workingCapital / 100000
                ).toFixed(1)}
                L
              </div>
              <div className="text-sm text-gray-600">Working Capital</div>
              <div className="text-xs text-green-600">Strong</div>
            </div>
          </div>
        </div>

        {/* Liquid Assets */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Liquid Assets
          </h3>
          <div className="space-y-4">
            {liquidityData.liquidAssets.map((asset, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h4 className="font-medium text-gray-900">{asset.name}</h4>
                    <p className="text-sm text-gray-600">{asset.category}</p>
                  </div>
                  <div className="text-right">
                    <div className="font-medium text-gray-900">
                      ₹{asset.amount.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">
                      {asset.return}% return
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <div className="text-sm text-gray-600">Liquidity</div>
                    <div
                      className={`font-medium ${getLiquidityColor(
                        asset.liquidity
                      )}`}
                    >
                      {asset.liquidity}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Risk</div>
                    <div className={`font-medium ${getRiskColor(asset.risk)}`}>
                      {asset.risk}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Return</div>
                    <div className="font-medium text-gray-900">
                      {asset.return}%
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Cash Flow */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Cash Flow Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-4">
                Monthly Cash Flow
              </h4>
              <div className="space-y-3">
                <div className="flex justify-between p-3 bg-green-50 rounded-lg">
                  <span className="text-gray-700">Income</span>
                  <span className="font-medium text-green-600">
                    ₹{liquidityData.cashFlow.monthlyIncome.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-red-50 rounded-lg">
                  <span className="text-gray-700">Expenses</span>
                  <span className="font-medium text-red-600">
                    ₹{liquidityData.cashFlow.monthlyExpenses.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-blue-50 rounded-lg">
                  <span className="text-gray-700">Savings</span>
                  <span className="font-medium text-blue-600">
                    ₹{liquidityData.cashFlow.monthlySavings.toLocaleString()}
                  </span>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-gray-900 mb-4">
                Upcoming Expenses
              </h4>
              <div className="space-y-3">
                {liquidityData.cashFlow.upcomingExpenses.map(
                  (expense, index) => (
                    <div
                      key={index}
                      className="flex justify-between p-3 bg-yellow-50 rounded-lg"
                    >
                      <div>
                        <div className="font-medium text-gray-900">
                          {expense.name}
                        </div>
                        <div className="text-sm text-gray-600">
                          Due: {new Date(expense.due).toLocaleDateString()}
                        </div>
                      </div>
                      <span className="font-medium text-yellow-600">
                        ₹{expense.amount.toLocaleString()}
                      </span>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Liquidity Recommendations
          </h3>
          <div className="space-y-4">
            {liquidityData.recommendations.map((rec, index) => (
              <div
                key={index}
                className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg"
              >
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                </div>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 mb-2">{rec.type}</h4>
                  <p className="text-sm text-gray-600 mb-2">
                    {rec.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">
                      {rec.current && rec.target ? (
                        <>
                          Current: ₹{rec.current.toLocaleString()} → Target: ₹
                          {rec.target.toLocaleString()}
                        </>
                      ) : rec.potentialGain ? (
                        <>
                          Potential Gain: ₹{rec.potentialGain.toLocaleString()}
                        </>
                      ) : (
                        rec.description
                      )}
                    </span>
                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                      {rec.action}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
              <DollarSign className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">
                Add Liquid Asset
              </span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <BarChart3 className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">
                Cash Flow Analysis
              </span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <Zap className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">
                Emergency Fund
              </span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
