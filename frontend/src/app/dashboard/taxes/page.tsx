'use client';

import MainLayout from '@/components/Layout/MainLayout';
import { AlertTriangle, Calculator, Calendar, CheckCircle, DollarSign, FileText, TrendingUp } from 'lucide-react';

// Mock Tax Data
const taxData = {
  currentYear: '2024-25',
  totalIncome: 1200000,
  taxableIncome: 900000,
  totalTax: 125000,
  taxSaved: 45000,
  deductions: [
    {
      category: 'Section 80C',
      limit: 150000,
      used: 120000,
      remaining: 30000,
      items: [
        { name: 'ELSS Investment', amount: 50000, status: 'active' },
        { name: 'EPF Contribution', amount: 40000, status: 'active' },
        { name: 'Life Insurance Premium', amount: 15000, status: 'active' },
        { name: 'NPS Contribution', amount: 15000, status: 'active' }
      ]
    },
    {
      category: 'Section 80D',
      limit: 25000,
      used: 20000,
      remaining: 5000,
      items: [
        { name: 'Health Insurance Premium', amount: 15000, status: 'active' },
        { name: 'Preventive Health Checkup', amount: 5000, status: 'active' }
      ]
    },
    {
      category: 'Section 80TTA',
      limit: 10000,
      used: 8000,
      remaining: 2000,
      items: [
        { name: 'Savings Account Interest', amount: 8000, status: 'active' }
      ]
    },
    {
      category: 'HRA',
      limit: 120000,
      used: 96000,
      remaining: 24000,
      items: [
        { name: 'House Rent Allowance', amount: 96000, status: 'active' }
      ]
    }
  ],
  recommendations: [
    {
      type: 'ELSS Investment',
      description: 'Invest ₹30,000 more in ELSS to fully utilize Section 80C',
      potentialSavings: 9000,
      priority: 'High',
      action: 'Invest in Axis Long Term Equity Fund'
    },
    {
      type: 'NPS Contribution',
      description: 'Increase NPS contribution by ₹10,000 for additional tax benefit',
      potentialSavings: 3000,
      priority: 'Medium',
      action: 'Increase monthly NPS contribution'
    },
    {
      type: 'Health Insurance',
      description: 'Add parents to health insurance for additional ₹25,000 deduction',
      potentialSavings: 7500,
      priority: 'Medium',
      action: 'Purchase family floater plan'
    }
  ],
  taxCalendar: [
    { date: '2024-07-31', event: 'Advance Tax Payment (Q1)', status: 'completed' },
    { date: '2024-09-15', event: 'Advance Tax Payment (Q2)', status: 'upcoming' },
    { date: '2024-12-15', event: 'Advance Tax Payment (Q3)', status: 'upcoming' },
    { date: '2025-03-15', event: 'Advance Tax Payment (Q4)', status: 'upcoming' },
    { date: '2025-07-31', event: 'Income Tax Return Filing', status: 'upcoming' }
  ]
};

export default function TaxesPage() {
  const totalDeductions = taxData.deductions.reduce((sum, ded) => sum + ded.used, 0);
  const totalLimit = taxData.deductions.reduce((sum, ded) => sum + ded.limit, 0);
  const utilizationPercentage = (totalDeductions / totalLimit) * 100;

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tax Optimization</h1>
          <p className="text-gray-600 mt-2">Maximize your tax savings with smart deductions</p>
        </div>

        {/* Tax Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-red-100 rounded-lg">
                <DollarSign className="h-5 w-5 text-red-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Total Tax</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{taxData.totalTax.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">FY {taxData.currentYear}</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Tax Saved</h3>
            </div>
            <div className="text-2xl font-bold text-green-600">
              ₹{taxData.taxSaved.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Through deductions</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Calculator className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Deduction Utilization</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {utilizationPercentage.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">
              ₹{totalDeductions.toLocaleString()}/₹{totalLimit.toLocaleString()}
            </div>
          </div>
        </div>

        {/* Deductions Breakdown */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Deductions Breakdown</h3>
          <div className="space-y-4">
            {taxData.deductions.map((deduction, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-medium text-gray-900">{deduction.category}</h4>
                  <div className="text-sm text-gray-600">
                    ₹{deduction.used.toLocaleString()}/₹{deduction.limit.toLocaleString()}
                  </div>
                </div>

                <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(deduction.used / deduction.limit) * 100}%` }}
                  ></div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {deduction.items.map((item, itemIndex) => (
                    <div key={itemIndex} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <span className="text-sm text-gray-700">{item.name}</span>
                      <span className="text-sm font-medium text-gray-900">
                        ₹{item.amount.toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>

                {deduction.remaining > 0 && (
                  <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4 text-yellow-600" />
                      <span className="text-sm text-yellow-800">
                        ₹{deduction.remaining.toLocaleString()} remaining to claim
                      </span>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Tax Saving Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tax Saving Recommendations</h3>
          <div className="space-y-4">
            {taxData.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className={`p-2 rounded-lg ${
                  rec.priority === 'High' ? 'bg-red-100' : 'bg-blue-100'
                }`}>
                  <CheckCircle className={`h-5 w-5 ${
                    rec.priority === 'High' ? 'text-red-600' : 'text-blue-600'
                  }`} />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-medium text-gray-900">{rec.type}</h4>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      rec.priority === 'High' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                    }`}>
                      {rec.priority} Priority
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{rec.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Potential Savings: ₹{rec.potentialSavings.toLocaleString()}</span>
                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                      {rec.action}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Tax Calendar */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tax Calendar</h3>
          <div className="space-y-3">
            {taxData.taxCalendar.map((event, index) => (
              <div key={index} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                <div className={`p-2 rounded-lg ${
                  event.status === 'completed' ? 'bg-green-100' : 'bg-blue-100'
                }`}>
                  <Calendar className={`h-4 w-4 ${
                    event.status === 'completed' ? 'text-green-600' : 'text-blue-600'
                  }`} />
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{event.event}</div>
                  <div className="text-sm text-gray-600">
                    {new Date(event.date).toLocaleDateString('en-IN', {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric'
                    })}
                  </div>
                </div>
                <div className={`text-xs px-2 py-1 rounded-full ${
                  event.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'
                }`}>
                  {event.status}
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
              <Calculator className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">Tax Calculator</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <FileText className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Download Form 16</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <TrendingUp className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Tax Planning</span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}