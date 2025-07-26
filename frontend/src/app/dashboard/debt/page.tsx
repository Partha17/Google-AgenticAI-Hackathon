'use client';

import MainLayout from '@/components/Layout/MainLayout';
import { AlertTriangle, Calculator, Calendar, CheckCircle, DollarSign, Target, TrendingDown } from 'lucide-react';

// Mock Debt Data
const debtData = {
  totalDebt: 2400000,
  totalEMI: 55000,
  totalInterest: 180000,
  debtToIncomeRatio: 35,
  loans: [
    {
      id: 1,
      name: 'Home Loan',
      principal: 2000000,
      outstanding: 1800000,
      emi: 25000,
      interestRate: 8.5,
      tenure: 20,
      bank: 'HDFC Bank',
      nextPayment: '2024-07-15',
      status: 'active',
      type: 'secured'
    },
    {
      id: 2,
      name: 'Car Loan',
      principal: 800000,
      outstanding: 400000,
      emi: 15000,
      interestRate: 12.5,
      tenure: 5,
      bank: 'ICICI Bank',
      nextPayment: '2024-07-20',
      status: 'active',
      type: 'secured'
    },
    {
      id: 3,
      name: 'Personal Loan',
      principal: 300000,
      outstanding: 200000,
      emi: 15000,
      interestRate: 15.5,
      tenure: 3,
      bank: 'Axis Bank',
      nextPayment: '2024-07-25',
      status: 'active',
      type: 'unsecured'
    }
  ],
  payoffStrategies: [
    {
      name: 'Debt Snowball',
      description: 'Pay off smallest debts first',
      totalInterest: 150000,
      timeToPayoff: 8,
      monthlyPayment: 65000,
      savings: 30000
    },
    {
      name: 'Debt Avalanche',
      description: 'Pay off highest interest debts first',
      totalInterest: 140000,
      timeToPayoff: 7,
      monthlyPayment: 70000,
      savings: 40000
    },
    {
      name: 'Current Plan',
      description: 'Continue with current payments',
      totalInterest: 180000,
      timeToPayoff: 12,
      monthlyPayment: 55000,
      savings: 0
    }
  ],
  recommendations: [
    {
      type: 'Refinance Personal Loan',
      description: 'Refinance personal loan at lower rate (12% vs 15.5%)',
      potentialSavings: 25000,
      action: 'Apply for balance transfer'
    },
    {
      type: 'Increase EMI',
      description: 'Increase car loan EMI by ₹5,000 to pay off faster',
      potentialSavings: 15000,
      action: 'Update EMI amount'
    },
    {
      type: 'Lump Sum Payment',
      description: 'Use bonus to make lump sum payment on personal loan',
      potentialSavings: 20000,
      action: 'Make ₹50,000 payment'
    }
  ]
};

export default function DebtPage() {
  const totalOutstanding = debtData.loans.reduce((sum, loan) => sum + loan.outstanding, 0);
  const totalEMI = debtData.loans.reduce((sum, loan) => sum + loan.emi, 0);

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Debt Management</h1>
          <p className="text-gray-600 mt-2">Track and optimize your debt payoff strategy</p>
        </div>

        {/* Debt Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-red-100 rounded-lg">
                <DollarSign className="h-5 w-5 text-red-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Total Debt</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{debtData.totalDebt.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Outstanding</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <Calendar className="h-5 w-5 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Monthly EMI</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{totalEMI.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Total payments</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-yellow-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Interest Cost</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{debtData.totalInterest.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">This year</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Target className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Debt-to-Income</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {debtData.debtToIncomeRatio}%
            </div>
            <div className="text-sm text-gray-600">Ratio</div>
          </div>
        </div>

        {/* Active Loans */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Active Loans</h3>
          <div className="space-y-4">
            {debtData.loans.map((loan) => (
              <div key={loan.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h4 className="font-medium text-gray-900">{loan.name}</h4>
                    <p className="text-sm text-gray-600">{loan.bank}</p>
                  </div>
                  <div className={`px-2 py-1 rounded-full text-xs ${
                    loan.type === 'secured' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                  }`}>
                    {loan.type}
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <div className="text-sm text-gray-600">Outstanding</div>
                    <div className="font-medium text-gray-900">₹{loan.outstanding.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">EMI</div>
                    <div className="font-medium text-gray-900">₹{loan.emi.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Interest Rate</div>
                    <div className="font-medium text-gray-900">{loan.interestRate}%</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Next Payment</div>
                    <div className="font-medium text-gray-900">
                      {new Date(loan.nextPayment).toLocaleDateString()}
                    </div>
                  </div>
                </div>

                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${((loan.principal - loan.outstanding) / loan.principal) * 100}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {((loan.principal - loan.outstanding) / loan.principal * 100).toFixed(1)}% paid
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Payoff Strategies */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Payoff Strategies</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {debtData.payoffStrategies.map((strategy, index) => (
              <div key={index} className={`border rounded-lg p-4 ${
                strategy.name === 'Current Plan' ? 'border-blue-200 bg-blue-50' : 'border-gray-200'
              }`}>
                <div className="flex items-center gap-2 mb-3">
                  <h4 className="font-medium text-gray-900">{strategy.name}</h4>
                  {strategy.name === 'Current Plan' && (
                    <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">Current</span>
                  )}
                </div>

                <p className="text-sm text-gray-600 mb-4">{strategy.description}</p>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Total Interest:</span>
                    <span className="font-medium">₹{strategy.totalInterest.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Time to Payoff:</span>
                    <span className="font-medium">{strategy.timeToPayoff} years</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Monthly Payment:</span>
                    <span className="font-medium">₹{strategy.monthlyPayment.toLocaleString()}</span>
                  </div>
                  {strategy.savings > 0 && (
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Interest Savings:</span>
                      <span className="font-medium text-green-600">₹{strategy.savings.toLocaleString()}</span>
                    </div>
                  )}
                </div>

                {strategy.name !== 'Current Plan' && (
                  <button className="w-full mt-4 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
                    Switch to {strategy.name}
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Smart Recommendations</h3>
          <div className="space-y-4">
            {debtData.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                </div>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 mb-2">{rec.type}</h4>
                  <p className="text-sm text-gray-600 mb-2">{rec.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-green-600 font-medium">
                      Potential Savings: ₹{rec.potentialSavings.toLocaleString()}
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
              <Calculator className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">EMI Calculator</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <TrendingDown className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Refinance Loan</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <Target className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Set Payoff Goal</span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}