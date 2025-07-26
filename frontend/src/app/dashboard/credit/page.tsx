'use client';

import MainLayout from '@/components/Layout/MainLayout';
import { AlertTriangle, Calendar, CheckCircle, CreditCard, DollarSign, TrendingUp } from 'lucide-react';

// Mock Credit Data
const creditData = {
  creditScore: 750,
  scoreChange: 15,
  scoreHistory: [
    { month: 'Jan', score: 720 },
    { month: 'Feb', score: 725 },
    { month: 'Mar', score: 730 },
    { month: 'Apr', score: 735 },
    { month: 'May', score: 740 },
    { month: 'Jun', score: 750 },
  ],
  creditFactors: [
    { factor: 'Payment History', impact: 'Excellent', score: 35 },
    { factor: 'Credit Utilization', impact: 'Good', score: 30 },
    { factor: 'Credit History Length', impact: 'Good', score: 15 },
    { factor: 'Credit Mix', impact: 'Excellent', score: 10 },
    { factor: 'New Credit', impact: 'Good', score: 10 },
  ],
  loans: [
    {
      id: 1,
      name: 'Home Loan',
      amount: 2500000,
      outstanding: 2000000,
      emi: 25000,
      nextPayment: '2024-07-15',
      status: 'active',
      bank: 'HDFC Bank'
    },
    {
      id: 2,
      name: 'Car Loan',
      amount: 800000,
      outstanding: 400000,
      emi: 15000,
      nextPayment: '2024-07-20',
      status: 'active',
      bank: 'ICICI Bank'
    }
  ],
  creditCards: [
    {
      id: 1,
      name: 'HDFC Regalia',
      limit: 500000,
      used: 125000,
      dueDate: '2024-07-25',
      dueAmount: 45000,
      status: 'active'
    },
    {
      id: 2,
      name: 'ICICI Amazon Pay',
      limit: 200000,
      used: 45000,
      dueDate: '2024-07-30',
      dueAmount: 15000,
      status: 'active'
    }
  ],
  paymentHistory: [
    { month: 'Jan', onTime: true },
    { month: 'Feb', onTime: true },
    { month: 'Mar', onTime: true },
    { month: 'Apr', onTime: true },
    { month: 'May', onTime: true },
    { month: 'Jun', onTime: true },
  ]
};

export default function CreditPage() {
  const getScoreColor = (score: number) => {
    if (score >= 750) return 'text-green-600';
    if (score >= 650) return 'text-blue-600';
    if (score >= 550) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreCategory = (score: number) => {
    if (score >= 750) return 'Excellent';
    if (score >= 650) return 'Good';
    if (score >= 550) return 'Fair';
    return 'Poor';
  };

  const totalCreditLimit = creditData.creditCards.reduce((sum, card) => sum + card.limit, 0);
  const totalCreditUsed = creditData.creditCards.reduce((sum, card) => sum + card.used, 0);
  const creditUtilization = (totalCreditUsed / totalCreditLimit) * 100;

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Credit Management</h1>
          <p className="text-gray-600 mt-2">Monitor your credit score and manage loans</p>
        </div>

        {/* Credit Score Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Credit Score</h2>
            <div className="flex items-center gap-1 text-sm text-green-600">
              <TrendingUp size={16} />
              <span>+{creditData.scoreChange} pts</span>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="text-center">
              <div className={`text-4xl font-bold ${getScoreColor(creditData.creditScore)}`}>
                {creditData.creditScore}
              </div>
              <div className="text-sm text-gray-600">{getScoreCategory(creditData.creditScore)}</div>
            </div>

            <div className="flex-1">
              <div className="grid grid-cols-2 gap-4">
                {creditData.creditFactors.map((factor, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{factor.factor}</div>
                      <div className="text-xs text-gray-600">{factor.impact}</div>
                    </div>
                    <div className="text-sm font-bold text-gray-900">{factor.score}%</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Credit Utilization */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Credit Utilization</h3>
            <div className="text-3xl font-bold text-gray-900 mb-2">
              {creditUtilization.toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600 mb-4">
              ₹{totalCreditUsed.toLocaleString()} of ₹{totalCreditLimit.toLocaleString()}
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className={`h-3 rounded-full transition-all duration-300 ${
                  creditUtilization <= 30 ? 'bg-green-600' :
                  creditUtilization <= 50 ? 'bg-yellow-600' : 'bg-red-600'
                }`}
                style={{ width: `${Math.min(creditUtilization, 100)}%` }}
              ></div>
            </div>
            <div className="text-xs text-gray-500 mt-2">
              {creditUtilization <= 30 ? 'Excellent utilization' :
               creditUtilization <= 50 ? 'Good utilization' : 'High utilization - consider reducing'}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Payment History</h3>
            <div className="grid grid-cols-6 gap-2">
              {creditData.paymentHistory.map((payment, index) => (
                <div key={index} className="text-center">
                  <div className={`w-8 h-8 rounded-full mx-auto mb-1 flex items-center justify-center ${
                    payment.onTime ? 'bg-green-100' : 'bg-red-100'
                  }`}>
                    {payment.onTime ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : (
                      <AlertTriangle className="h-4 w-4 text-red-600" />
                    )}
                  </div>
                  <div className="text-xs text-gray-600">{payment.month}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Loans Overview */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Active Loans</h3>
          <div className="space-y-4">
            {creditData.loans.map((loan) => (
              <div key={loan.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <DollarSign className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">{loan.name}</div>
                    <div className="text-sm text-gray-600">{loan.bank}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-medium text-gray-900">
                    ₹{loan.outstanding.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">
                    EMI: ₹{loan.emi.toLocaleString()}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-600">Next Payment</div>
                  <div className="text-sm font-medium text-gray-900">
                    {new Date(loan.nextPayment).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Credit Cards */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Credit Cards</h3>
          <div className="space-y-4">
            {creditData.creditCards.map((card) => (
              <div key={card.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <CreditCard className="h-5 w-5 text-purple-600" />
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">{card.name}</div>
                    <div className="text-sm text-gray-600">
                      Limit: ₹{card.limit.toLocaleString()}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-medium text-gray-900">
                    ₹{card.used.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">
                    Used: {((card.used / card.limit) * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-600">Due Amount</div>
                  <div className="font-medium text-gray-900">
                    ₹{card.dueAmount.toLocaleString()}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-600">Due Date</div>
                  <div className="text-sm font-medium text-gray-900">
                    {new Date(card.dueDate).toLocaleDateString()}
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
              <CreditCard className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">Apply for Credit Card</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <Calendar className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Set Payment Reminders</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <TrendingUp className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Improve Credit Score</span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}