'use client';

import MainLayout from '@/components/Layout/MainLayout';
import { AlertTriangle, Calendar, CheckCircle, DollarSign, Settings, TrendingUp, Zap } from 'lucide-react';

// Mock Subscription Data
const subscriptionData = {
  totalMonthlyCost: 3500,
  totalYearlyCost: 42000,
  activeSubscriptions: 8,
  unusedSubscriptions: 2,
  subscriptions: [
    {
      id: 1,
      name: 'Netflix',
      category: 'Entertainment',
      monthlyCost: 649,
      yearlyCost: 7788,
      usage: 85,
      lastUsed: '2024-07-20',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-15',
      icon: '🎬'
    },
    {
      id: 2,
      name: 'Spotify Premium',
      category: 'Music',
      monthlyCost: 119,
      yearlyCost: 1428,
      usage: 95,
      lastUsed: '2024-07-21',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-10',
      icon: '🎵'
    },
    {
      id: 3,
      name: 'Amazon Prime',
      category: 'Shopping',
      monthlyCost: 999,
      yearlyCost: 11988,
      usage: 60,
      lastUsed: '2024-07-18',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-01',
      icon: '📦'
    },
    {
      id: 4,
      name: 'Adobe Creative Cloud',
      category: 'Productivity',
      monthlyCost: 1499,
      yearlyCost: 17988,
      usage: 30,
      lastUsed: '2024-07-10',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-05',
      icon: '🎨'
    },
    {
      id: 5,
      name: 'Microsoft 365',
      category: 'Productivity',
      monthlyCost: 199,
      yearlyCost: 2388,
      usage: 70,
      lastUsed: '2024-07-19',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-12',
      icon: '💼'
    },
    {
      id: 6,
      name: 'Gym Membership',
      category: 'Health',
      monthlyCost: 1500,
      yearlyCost: 18000,
      usage: 20,
      lastUsed: '2024-07-05',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-01',
      icon: '💪'
    },
    {
      id: 7,
      name: 'LinkedIn Premium',
      category: 'Professional',
      monthlyCost: 999,
      yearlyCost: 11988,
      usage: 10,
      lastUsed: '2024-06-25',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-20',
      icon: '💼'
    },
    {
      id: 8,
      name: 'Disney+ Hotstar',
      category: 'Entertainment',
      monthlyCost: 299,
      yearlyCost: 3588,
      usage: 40,
      lastUsed: '2024-07-15',
      status: 'active',
      autoRenew: true,
      nextBilling: '2024-08-08',
      icon: '🎭'
    }
  ],
  recommendations: [
    {
      type: 'Cancel Unused',
      description: 'Cancel LinkedIn Premium - only 10% usage in last month',
      potentialSavings: 11988,
      action: 'Cancel subscription'
    },
    {
      type: 'Switch to Annual',
      description: 'Switch Netflix to annual plan for 15% savings',
      potentialSavings: 1168,
      action: 'Upgrade to annual'
    },
    {
      type: 'Pause Subscription',
      description: 'Pause Adobe Creative Cloud - low usage period',
      potentialSavings: 1499,
      action: 'Pause for 3 months'
    }
  ],
  categories: [
    { name: 'Entertainment', total: 948, count: 2 },
    { name: 'Productivity', total: 1698, count: 2 },
    { name: 'Shopping', total: 999, count: 1 },
    { name: 'Health', total: 1500, count: 1 },
    { name: 'Professional', total: 999, count: 1 },
    { name: 'Music', total: 119, count: 1 }
  ]
};

export default function SubscriptionsPage() {
  const getUsageColor = (usage: number) => {
    if (usage >= 80) return 'text-green-600';
    if (usage >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getUsageStatus = (usage: number) => {
    if (usage >= 80) return 'High Usage';
    if (usage >= 50) return 'Moderate Usage';
    return 'Low Usage';
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Subscription Manager</h1>
          <p className="text-gray-600 mt-2">Track and optimize your subscription spending</p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <DollarSign className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Monthly Cost</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{subscriptionData.totalMonthlyCost.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Total monthly</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Calendar className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Yearly Cost</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{subscriptionData.totalYearlyCost.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Total yearly</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Settings className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Active Subscriptions</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {subscriptionData.activeSubscriptions}
            </div>
            <div className="text-sm text-gray-600">Total subscriptions</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-red-100 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-red-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Unused</h3>
            </div>
            <div className="text-2xl font-bold text-red-600">
              {subscriptionData.unusedSubscriptions}
            </div>
            <div className="text-sm text-gray-600">Low usage</div>
          </div>
        </div>

        {/* Subscriptions List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Active Subscriptions</h3>
          <div className="space-y-4">
            {subscriptionData.subscriptions.map((sub) => (
              <div key={sub.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="text-2xl">{sub.icon}</div>
                    <div>
                      <h4 className="font-medium text-gray-900">{sub.name}</h4>
                      <p className="text-sm text-gray-600">{sub.category}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium text-gray-900">₹{sub.monthlyCost}</div>
                    <div className="text-sm text-gray-600">per month</div>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <div className="text-sm text-gray-600">Usage</div>
                    <div className={`font-medium ${getUsageColor(sub.usage)}`}>
                      {sub.usage}% - {getUsageStatus(sub.usage)}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Last Used</div>
                    <div className="font-medium text-gray-900">
                      {new Date(sub.lastUsed).toLocaleDateString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Next Billing</div>
                    <div className="font-medium text-gray-900">
                      {new Date(sub.nextBilling).toLocaleDateString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Auto Renew</div>
                    <div className={`font-medium ${sub.autoRenew ? 'text-green-600' : 'text-red-600'}`}>
                      {sub.autoRenew ? 'Yes' : 'No'}
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                      Manage
                    </button>
                    <button className="text-sm text-red-600 hover:text-red-700 font-medium">
                      Cancel
                    </button>
                  </div>
                  <div className="text-sm text-gray-600">
                    Yearly: ₹{sub.yearlyCost.toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Spending by Category */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Spending by Category</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {subscriptionData.categories.map((category, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900">{category.name}</h4>
                  <span className="text-sm text-gray-600">{category.count} subs</span>
                </div>
                <div className="text-2xl font-bold text-gray-900">
                  ₹{category.total.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600">per month</div>
              </div>
            ))}
          </div>
        </div>

        {/* Optimization Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Optimization Recommendations</h3>
          <div className="space-y-4">
            {subscriptionData.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                </div>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 mb-2">{rec.type}</h4>
                  <p className="text-sm text-gray-600 mb-2">{rec.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-green-600 font-medium">
                      Potential Savings: ₹{rec.potentialSavings.toLocaleString()}/year
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
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
              <Zap className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">Add Subscription</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <TrendingUp className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Usage Analytics</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <Calendar className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Billing Calendar</span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}