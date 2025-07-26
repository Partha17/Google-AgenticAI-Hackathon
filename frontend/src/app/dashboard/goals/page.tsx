'use client';

import MainLayout from '@/components/Layout/MainLayout';
import { Calendar, CheckCircle, Clock, DollarSign, Target, TrendingUp } from 'lucide-react';

// Mock Goals Data
const goalsData = {
  totalGoals: 5,
  completedGoals: 2,
  activeGoals: 3,
  totalSaved: 850000,
  totalTarget: 2000000,
  goals: [
    {
      id: 1,
      name: 'Emergency Fund',
      target: 300000,
      saved: 225000,
      deadline: '2024-12-31',
      category: 'Short-term',
      priority: 'High',
      status: 'active',
      monthlyContribution: 15000,
      icon: '🛡️'
    },
    {
      id: 2,
      name: 'Home Down Payment',
      target: 1000000,
      saved: 400000,
      deadline: '2026-06-30',
      category: 'Medium-term',
      priority: 'High',
      status: 'active',
      monthlyContribution: 25000,
      icon: '🏠'
    },
    {
      id: 3,
      name: 'Europe Vacation',
      target: 200000,
      saved: 150000,
      deadline: '2024-08-15',
      category: 'Short-term',
      priority: 'Medium',
      status: 'active',
      monthlyContribution: 10000,
      icon: '✈️'
    },
    {
      id: 4,
      name: 'Retirement Fund',
      target: 5000000,
      saved: 75000,
      deadline: '2040-01-01',
      category: 'Long-term',
      priority: 'High',
      status: 'active',
      monthlyContribution: 20000,
      icon: '🌅'
    },
    {
      id: 5,
      name: 'Car Purchase',
      target: 800000,
      saved: 800000,
      deadline: '2023-12-31',
      category: 'Medium-term',
      priority: 'Medium',
      status: 'completed',
      monthlyContribution: 0,
      icon: '🚗'
    }
  ]
};

export default function GoalsPage() {
  const overallProgress = (goalsData.totalSaved / goalsData.totalTarget) * 100;

  const getDaysRemaining = (deadline: string) => {
    const today = new Date();
    const deadlineDate = new Date(deadline);
    const diffTime = deadlineDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'text-green-600';
    if (progress >= 60) return 'text-blue-600';
    if (progress >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Financial Goals</h1>
          <p className="text-gray-600 mt-2">Track your progress towards financial milestones</p>
        </div>

        {/* Overall Progress */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Overall Progress</h2>
            <div className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span className="text-sm text-gray-600">{goalsData.completedGoals} completed</span>
            </div>
          </div>

          <div className="text-3xl font-bold text-gray-900 mb-2">
            ₹{goalsData.totalSaved.toLocaleString()}
          </div>

          <div className="text-sm text-gray-500 mb-4">
            of ₹{goalsData.totalTarget.toLocaleString()} target
          </div>

          <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
            <div
              className="bg-blue-600 h-3 rounded-full transition-all duration-300"
              style={{ width: `${overallProgress}%` }}
            ></div>
          </div>

          <div className="text-sm text-gray-600">
            {overallProgress.toFixed(1)}% complete
          </div>
        </div>

        {/* Goals Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {goalsData.goals.map((goal) => {
            const progress = (goal.saved / goal.target) * 100;
            const daysRemaining = getDaysRemaining(goal.deadline);
            const isCompleted = goal.status === 'completed';

            return (
              <div key={goal.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="text-3xl">{goal.icon}</div>
                  <div className="flex items-center gap-2">
                    {isCompleted ? (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    ) : (
                      <Clock className="h-5 w-5 text-blue-600" />
                    )}
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      goal.priority === 'High' ? 'bg-red-100 text-red-700' :
                      goal.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'
                    }`}>
                      {goal.priority}
                    </span>
                  </div>
                </div>

                <h3 className="text-lg font-semibold text-gray-900 mb-2">{goal.name}</h3>

                <div className="space-y-3 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Target:</span>
                    <span className="font-medium">₹{goal.target.toLocaleString()}</span>
                  </div>

                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Saved:</span>
                    <span className="font-medium">₹{goal.saved.toLocaleString()}</span>
                  </div>

                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Progress:</span>
                    <span className={`font-medium ${getProgressColor(progress)}`}>
                      {progress.toFixed(1)}%
                    </span>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${
                      progress >= 80 ? 'bg-green-600' :
                      progress >= 60 ? 'bg-blue-600' :
                      progress >= 40 ? 'bg-yellow-600' : 'bg-red-600'
                    }`}
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>

                {/* Additional Info */}
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    <span>{daysRemaining > 0 ? `${daysRemaining} days left` : 'Completed'}</span>
                  </div>

                  {!isCompleted && (
                    <div className="flex items-center gap-2">
                      <DollarSign className="h-4 w-4" />
                      <span>₹{goal.monthlyContribution.toLocaleString()}/month</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="flex items-center gap-3 p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
              <Target className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">Add New Goal</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <TrendingUp className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Update Progress</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <Calendar className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Set Reminders</span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}