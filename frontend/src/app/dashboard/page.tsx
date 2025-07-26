"use client";

import FinancialOverview from "@/components/Dashboard/FinancialOverview";
import MainLayout from "@/components/Layout/MainLayout";
import { DASHBOARD_ROUTES } from "@/constants";
import {
  ArrowRight,
  BarChart3,
  Bot,
  Calculator,
  CreditCard,
  DollarSign,
  Settings,
  Shield,
  Target,
  TrendingUp,
} from "lucide-react";
import Link from "next/link";

// Mock data - replace with real data from your backend
const mockData = {
  netWorth: 2500000,
  netWorthChange: 125000,
  netWorthChangePercent: 5.26,
  monthlyIncome: 85000,
  monthlyExpenses: 45000,
  savingsRate: 47.1,
  netWorthHistory: [
    { name: "Jan", value: 2200000 },
    { name: "Feb", value: 2250000 },
    { name: "Mar", value: 2300000 },
    { name: "Apr", value: 2350000 },
    { name: "May", value: 2400000 },
    { name: "Jun", value: 2500000 },
  ],
};

const dashboardCards = [
  {
    title: "AI Assistant",
    description: "Get personalized financial advice",
    icon: Bot,
    href: "/chat",
    color: "bg-gradient-to-r from-blue-500 to-purple-600",
    value: "Ask FinGenie",
    change: "24/7 Help",
    featured: true,
  },
  {
    title: "Portfolio",
    description: "Asset allocation & performance",
    icon: TrendingUp,
    href: DASHBOARD_ROUTES.PORTFOLIO,
    color: "bg-blue-500",
    value: "₹1,250,000",
    change: "+8.5%",
  },
  {
    title: "Goals",
    description: "Track your financial goals",
    icon: Target,
    href: DASHBOARD_ROUTES.GOALS,
    color: "bg-green-500",
    value: "3 Active",
    change: "2 Complete",
  },
  {
    title: "Credit",
    description: "Credit score & loans",
    icon: CreditCard,
    href: DASHBOARD_ROUTES.CREDIT,
    color: "bg-purple-500",
    value: "750",
    change: "+15 pts",
  },
  {
    title: "Taxes",
    description: "Tax optimization tools",
    icon: Calculator,
    href: DASHBOARD_ROUTES.TAXES,
    color: "bg-orange-500",
    value: "₹45,000",
    change: "Saved",
  },
  {
    title: "Debt",
    description: "Debt payoff strategies",
    icon: DollarSign,
    href: DASHBOARD_ROUTES.DEBT,
    color: "bg-red-500",
    value: "₹200,000",
    change: "-12%",
  },
  {
    title: "SIPs",
    description: "SIP analysis & optimization",
    icon: BarChart3,
    href: DASHBOARD_ROUTES.SIPS,
    color: "bg-indigo-500",
    value: "₹25,000",
    change: "+15%",
  },
  {
    title: "Subscriptions",
    description: "Manage subscriptions",
    icon: Settings,
    href: DASHBOARD_ROUTES.SUBSCRIPTIONS,
    color: "bg-pink-500",
    value: "₹3,500",
    change: "-₹500",
  },
  {
    title: "Risk Manager",
    description: "Risk assessment & management",
    icon: Shield,
    href: DASHBOARD_ROUTES.RISK,
    color: "bg-yellow-500",
    value: "Medium",
    change: "Stable",
  },
];

export default function Dashboard() {
  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Your financial overview and insights
          </p>
        </div>

        {/* Financial Overview */}
        <FinancialOverview {...mockData} />

        {/* AI Assistant Prominent Card */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                <Bot className="h-8 w-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">
                  AI Financial Assistant
                </h2>
                <p className="text-gray-600">
                  Get personalized financial advice, analyze your portfolio, and
                  plan your investments
                </p>
              </div>
            </div>
            <Link
              href="/chat"
              className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 font-medium"
            >
              Start Chat
            </Link>
          </div>
        </div>

        {/* Dashboard Cards Grid */}
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Quick Access
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {dashboardCards.map((card) => (
              <Link
                key={card.title}
                href={card.href}
                className={`group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-200 hover:border-gray-300 ${
                  card.featured ? "ring-2 ring-blue-200 shadow-lg" : ""
                }`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className={`p-3 rounded-lg ${card.color}`}>
                    <card.icon className="h-6 w-6 text-white" />
                  </div>
                  <ArrowRight className="h-5 w-5 text-gray-400 group-hover:text-gray-600 transition-colors" />
                </div>

                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {card.title}
                </h3>

                <p className="text-sm text-gray-600 mb-4">{card.description}</p>

                <div className="flex items-center justify-between">
                  <div className="text-2xl font-bold text-gray-900">
                    {card.value}
                  </div>
                  <div className="text-sm text-green-600 font-medium">
                    {card.change}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Recent Activity
          </h2>
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="h-4 w-4 text-green-600" />
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">SIP Investment</p>
                <p className="text-sm text-gray-600">
                  ₹25,000 invested in HDFC Mid-Cap Fund
                </p>
              </div>
              <span className="text-sm text-gray-500">2 hours ago</span>
            </div>

            <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Target className="h-4 w-4 text-blue-600" />
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">Goal Milestone</p>
                <p className="text-sm text-gray-600">
                  Emergency fund goal 75% complete
                </p>
              </div>
              <span className="text-sm text-gray-500">1 day ago</span>
            </div>

            <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
              <div className="p-2 bg-orange-100 rounded-lg">
                <Calculator className="h-4 w-4 text-orange-600" />
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">Tax Optimization</p>
                <p className="text-sm text-gray-600">
                  ELSS investment recommended
                </p>
              </div>
              <span className="text-sm text-gray-500">3 days ago</span>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
