'use client';

import { AlertTriangle, DollarSign, Target, TrendingDown, TrendingUp } from 'lucide-react';
import LineChart from '../Charts/LineChart';

interface FinancialOverviewProps {
  netWorth: number;
  netWorthChange: number;
  netWorthChangePercent: number;
  monthlyIncome: number;
  monthlyExpenses: number;
  savingsRate: number;
  netWorthHistory: Array<{ name: string; value: number }>;
}

export default function FinancialOverview({
  netWorth,
  netWorthChange,
  netWorthChangePercent,
  monthlyIncome,
  monthlyExpenses,
  savingsRate,
  netWorthHistory
}: FinancialOverviewProps) {
  const isPositive = netWorthChange >= 0;

  return (
    <div className="space-y-6">
      {/* Net Worth Card */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Net Worth</h2>
          <div className={`flex items-center gap-1 text-sm ${
            isPositive ? 'text-green-600' : 'text-red-600'
          }`}>
            {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
            <span>{isPositive ? '+' : ''}{netWorthChangePercent.toFixed(2)}%</span>
          </div>
        </div>

        <div className="text-3xl font-bold text-gray-900 mb-2">
          ₹{netWorth.toLocaleString()}
        </div>

        <div className="text-sm text-gray-500">
          {isPositive ? '+' : ''}₹{netWorthChange.toLocaleString()} this month
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Monthly Income */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <DollarSign className="h-5 w-5 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Monthly Income</h3>
          </div>
          <div className="text-2xl font-bold text-gray-900">
            ₹{monthlyIncome.toLocaleString()}
          </div>
        </div>

        {/* Monthly Expenses */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-red-100 rounded-lg">
              <AlertTriangle className="h-5 w-5 text-red-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Monthly Expenses</h3>
          </div>
          <div className="text-2xl font-bold text-gray-900">
            ₹{monthlyExpenses.toLocaleString()}
          </div>
        </div>

        {/* Savings Rate */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Target className="h-5 w-5 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Savings Rate</h3>
          </div>
          <div className="text-2xl font-bold text-gray-900">
            {savingsRate.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Net Worth Chart */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <LineChart
          data={netWorthHistory}
          title="Net Worth Trend"
          xAxisDataKey="name"
          yAxisDataKey="value"
          color="#3B82F6"
          height={300}
        />
      </div>
    </div>
  );
}