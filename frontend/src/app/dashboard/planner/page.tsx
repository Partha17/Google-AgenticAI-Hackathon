"use client";

import MainLayout from "@/components/Layout/MainLayout";
import {
  BarChart3,
  Calculator,
  Calendar,
  DollarSign,
  Target,
  TrendingUp,
} from "lucide-react";

// Mock Planner Data
const plannerData = {
  currentAge: 32,
  retirementAge: 60,
  lifeExpectancy: 85,
  currentSavings: 2500000,
  monthlyIncome: 120000,
  monthlyExpenses: 75000,
  monthlySavings: 45000,
  retirementGoal: 50000000,
  budget: {
    housing: 25000,
    food: 15000,
    transportation: 8000,
    utilities: 5000,
    entertainment: 5000,
    healthcare: 3000,
    insurance: 4000,
    savings: 45000,
    other: 5000,
  },
  financialGoals: [
    {
      name: "Emergency Fund",
      target: 450000,
      current: 300000,
      deadline: "2024-12-31",
      priority: "High",
      monthlyContribution: 15000,
    },
    {
      name: "Down Payment",
      target: 2000000,
      current: 800000,
      deadline: "2026-06-30",
      priority: "High",
      monthlyContribution: 25000,
    },
    {
      name: "Child Education",
      target: 5000000,
      current: 500000,
      deadline: "2035-06-30",
      priority: "Medium",
      monthlyContribution: 15000,
    },
    {
      name: "Retirement",
      target: 50000000,
      current: 2500000,
      deadline: "2052-06-30",
      priority: "Medium",
      monthlyContribution: 20000,
    },
  ],
  retirementProjection: {
    currentSavings: 2500000,
    monthlyContribution: 20000,
    expectedReturn: 8.5,
    inflationRate: 6,
    projectedAmount: 45000000,
    shortfall: 5000000,
    yearsToRetirement: 28,
  },
  recommendations: [
    {
      type: "Increase Savings",
      description:
        "Increase monthly savings by ₹10,000 to meet retirement goal",
      impact: "High",
      action: "Reduce entertainment budget by ₹5,000 and dining out by ₹5,000",
    },
    {
      type: "Investment Strategy",
      description: "Allocate 70% to equity for better long-term returns",
      impact: "Medium",
      action: "Rebalance portfolio to increase equity allocation",
    },
    {
      type: "Emergency Fund",
      description: "Complete emergency fund target in next 10 months",
      impact: "High",
      action: "Continue monthly contribution of ₹15,000",
    },
  ],
};

export default function PlannerPage() {
  const totalBudget = Object.values(plannerData.budget).reduce(
    (sum, amount) => sum + amount,
    0
  );
  const totalGoals = plannerData.financialGoals.reduce(
    (sum, goal) => sum + goal.target,
    0
  );
  const totalCurrent = plannerData.financialGoals.reduce(
    (sum, goal) => sum + goal.current,
    0
  );
  const progressPercentage = (totalCurrent / totalGoals) * 100;

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "high":
        return "text-red-600";
      case "medium":
        return "text-yellow-600";
      case "low":
        return "text-green-600";
      default:
        return "text-gray-600";
    }
  };

  const getPriorityBg = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "high":
        return "bg-red-100 text-red-700";
      case "medium":
        return "bg-yellow-100 text-yellow-700";
      case "low":
        return "bg-green-100 text-green-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Financial Planner
          </h1>
          <p className="text-gray-600 mt-2">
            Plan your financial future with smart budgeting and goal tracking
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Target className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Goals Progress</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {progressPercentage.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">
              ₹{totalCurrent.toLocaleString()}/₹{totalGoals.toLocaleString()}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <DollarSign className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Monthly Savings</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{plannerData.monthlySavings.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">
              {(
                (plannerData.monthlySavings / plannerData.monthlyIncome) *
                100
              ).toFixed(1)}
              % of income
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Calendar className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900">
                Years to Retirement
              </h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {plannerData.retirementProjection.yearsToRetirement}
            </div>
            <div className="text-sm text-gray-600">
              Age {plannerData.currentAge} → {plannerData.retirementAge}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="h-5 w-5 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Retirement Goal</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{(plannerData.retirementGoal / 10000000).toFixed(1)}Cr
            </div>
            <div className="text-sm text-gray-600">Target amount</div>
          </div>
        </div>

        {/* Budget Breakdown */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Monthly Budget Breakdown
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(plannerData.budget).map(([category, amount]) => (
              <div key={category} className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 capitalize">
                    {category}
                  </h4>
                  <span className="text-sm text-gray-600">
                    {((amount / totalBudget) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="text-2xl font-bold text-gray-900">
                  ₹{amount.toLocaleString()}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(amount / totalBudget) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Financial Goals */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Financial Goals
          </h3>
          <div className="space-y-4">
            {plannerData.financialGoals.map((goal, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h4 className="font-medium text-gray-900">{goal.name}</h4>
                    <p className="text-sm text-gray-600">
                      Due: {new Date(goal.deadline).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${getPriorityBg(
                        goal.priority
                      )}`}
                    >
                      {goal.priority} Priority
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <div className="text-sm text-gray-600">Target</div>
                    <div className="font-medium text-gray-900">
                      ₹{goal.target.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Current</div>
                    <div className="font-medium text-gray-900">
                      ₹{goal.current.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">
                      Monthly Contribution
                    </div>
                    <div className="font-medium text-gray-900">
                      ₹{goal.monthlyContribution.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Progress</div>
                    <div className="font-medium text-gray-900">
                      {((goal.current / goal.target) * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>

                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(goal.current / goal.target) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Retirement Projection */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Retirement Projection
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-4">Current Status</h4>
              <div className="space-y-3">
                <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700">Current Savings</span>
                  <span className="font-medium">
                    ₹
                    {plannerData.retirementProjection.currentSavings.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700">Monthly Contribution</span>
                  <span className="font-medium">
                    ₹
                    {plannerData.retirementProjection.monthlyContribution.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700">Expected Return</span>
                  <span className="font-medium">
                    {plannerData.retirementProjection.expectedReturn}%
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700">Inflation Rate</span>
                  <span className="font-medium">
                    {plannerData.retirementProjection.inflationRate}%
                  </span>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-gray-900 mb-4">
                Projection Results
              </h4>
              <div className="space-y-3">
                <div className="flex justify-between p-3 bg-blue-50 rounded-lg">
                  <span className="text-gray-700">Projected Amount</span>
                  <span className="font-medium text-blue-600">
                    ₹
                    {(
                      plannerData.retirementProjection.projectedAmount /
                      10000000
                    ).toFixed(1)}
                    Cr
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-green-50 rounded-lg">
                  <span className="text-gray-700">Retirement Goal</span>
                  <span className="font-medium text-green-600">
                    ₹{(plannerData.retirementGoal / 10000000).toFixed(1)}Cr
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-red-50 rounded-lg">
                  <span className="text-gray-700">Shortfall</span>
                  <span className="font-medium text-red-600">
                    ₹
                    {(
                      plannerData.retirementProjection.shortfall / 1000000
                    ).toFixed(1)}
                    M
                  </span>
                </div>
                <div className="flex justify-between p-3 bg-yellow-50 rounded-lg">
                  <span className="text-gray-700">Years to Retirement</span>
                  <span className="font-medium text-yellow-600">
                    {plannerData.retirementProjection.yearsToRetirement} years
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Planning Recommendations
          </h3>
          <div className="space-y-4">
            {plannerData.recommendations.map((rec, index) => (
              <div
                key={index}
                className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg"
              >
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Calculator className="h-5 w-5 text-blue-600" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-medium text-gray-900">{rec.type}</h4>
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        rec.impact === "High"
                          ? "bg-red-100 text-red-700"
                          : "bg-yellow-100 text-yellow-700"
                      }`}
                    >
                      {rec.impact} Impact
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    {rec.description}
                  </p>
                  <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                    {rec.action}
                  </button>
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
              <Target className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">Set New Goal</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <Calculator className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">
                Retirement Calculator
              </span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <BarChart3 className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">
                Budget Analysis
              </span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
