"use client";

import LineChart from "@/components/Charts/LineChart";
import PieChart from "@/components/Charts/PieChart";
import MainLayout from "@/components/Layout/MainLayout";
import { TrendingDown, TrendingUp } from "lucide-react";

// Mock Portfolio Data
const portfolioData = {
  totalValue: 1250000,
  totalChange: 85000,
  totalChangePercent: 7.3,
  assetAllocation: [
    { name: "Equity", value: 750000, color: "#3B82F6" },
    { name: "Debt", value: 300000, color: "#10B981" },
    { name: "Gold", value: 125000, color: "#F59E0B" },
    { name: "Cash", value: 75000, color: "#6B7280" },
  ],
  performance: [
    { name: "Jan", value: 1100000 },
    { name: "Feb", value: 1120000 },
    { name: "Mar", value: 1150000 },
    { name: "Apr", value: 1180000 },
    { name: "May", value: 1200000 },
    { name: "Jun", value: 1250000 },
  ],
  holdings: [
    {
      name: "HDFC Bank",
      type: "Equity",
      value: 150000,
      change: 8.5,
      quantity: 1000,
    },
    {
      name: "Reliance Industries",
      type: "Equity",
      value: 120000,
      change: 12.3,
      quantity: 500,
    },
    {
      name: "ICICI Prudential Bluechip",
      type: "Mutual Fund",
      value: 200000,
      change: 6.8,
      quantity: 10000,
    },
    {
      name: "SBI Gold ETF",
      type: "ETF",
      value: 125000,
      change: 4.2,
      quantity: 5000,
    },
    {
      name: "Axis Bluechip Fund",
      type: "Mutual Fund",
      value: 180000,
      change: 9.1,
      quantity: 8000,
    },
    {
      name: "Tata Consultancy",
      type: "Equity",
      value: 100000,
      change: 5.7,
      quantity: 400,
    },
  ],
  riskMetrics: {
    beta: 0.85,
    sharpeRatio: 1.2,
    volatility: 12.5,
    maxDrawdown: -8.2,
  },
};

export default function PortfolioPage() {
  const isPositive = portfolioData.totalChange >= 0;

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Portfolio Analysis
          </h1>
          <p className="text-gray-600 mt-2">
            Comprehensive view of your investment portfolio
          </p>
        </div>

        {/* Portfolio Summary */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">
              Portfolio Value
            </h2>
            <div
              className={`flex items-center gap-1 text-sm ${
                isPositive ? "text-green-600" : "text-red-600"
              }`}
            >
              {isPositive ? (
                <TrendingUp size={16} />
              ) : (
                <TrendingDown size={16} />
              )}
              <span>
                {isPositive ? "+" : ""}
                {portfolioData.totalChangePercent.toFixed(1)}%
              </span>
            </div>
          </div>

          <div className="text-3xl font-bold text-gray-900 mb-2">
            ₹{portfolioData.totalValue.toLocaleString()}
          </div>

          <div className="text-sm text-gray-500">
            {isPositive ? "+" : ""}₹{portfolioData.totalChange.toLocaleString()}{" "}
            this month
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Asset Allocation */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Asset Allocation
            </h3>
            <div className="h-64">
              <PieChart data={portfolioData.assetAllocation} height={256} />
            </div>
          </div>

          {/* Performance Chart */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Portfolio Performance
            </h3>
            <div className="h-64">
              <LineChart data={portfolioData.performance} height={256} />
            </div>
          </div>
        </div>

        {/* Risk Metrics */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Risk Metrics
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {portfolioData.riskMetrics.beta}
              </div>
              <div className="text-sm text-gray-600">Beta</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {portfolioData.riskMetrics.sharpeRatio}
              </div>
              <div className="text-sm text-gray-600">Sharpe Ratio</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {portfolioData.riskMetrics.volatility}%
              </div>
              <div className="text-sm text-gray-600">Volatility</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-red-600">
                {portfolioData.riskMetrics.maxDrawdown}%
              </div>
              <div className="text-sm text-gray-600">Max Drawdown</div>
            </div>
          </div>
        </div>

        {/* Holdings Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Holdings</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-900">
                    Name
                  </th>
                  <th className="text-left py-3 px-4 font-medium text-gray-900">
                    Type
                  </th>
                  <th className="text-right py-3 px-4 font-medium text-gray-900">
                    Value
                  </th>
                  <th className="text-right py-3 px-4 font-medium text-gray-900">
                    Change
                  </th>
                  <th className="text-right py-3 px-4 font-medium text-gray-900">
                    Quantity
                  </th>
                </tr>
              </thead>
              <tbody>
                {portfolioData.holdings.map((holding, index) => (
                  <tr
                    key={index}
                    className="border-b border-gray-100 hover:bg-gray-50"
                  >
                    <td className="py-3 px-4 font-medium text-gray-900">
                      {holding.name}
                    </td>
                    <td className="py-3 px-4 text-gray-600">{holding.type}</td>
                    <td className="py-3 px-4 text-right font-medium text-gray-900">
                      ₹{holding.value.toLocaleString()}
                    </td>
                    <td
                      className={`py-3 px-4 text-right font-medium ${
                        holding.change >= 0 ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {holding.change >= 0 ? "+" : ""}
                      {holding.change}%
                    </td>
                    <td className="py-3 px-4 text-right text-gray-600">
                      {holding.quantity.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
