"use client";

import MainLayout from "@/components/Layout/MainLayout";
import {
  BarChart3,
  Calendar,
  CheckCircle,
  DollarSign,
  TrendingUp,
  Zap,
} from "lucide-react";

// Mock SIP Data
const sipData = {
  totalInvested: 850000,
  currentValue: 920000,
  totalGain: 70000,
  totalGainPercent: 8.2,
  activeSIPs: 6,
  monthlyInvestment: 45000,
  sips: [
    {
      id: 1,
      fund: "Axis Bluechip Fund",
      category: "Large Cap",
      amount: 10000,
      frequency: "Monthly",
      startDate: "2022-01-15",
      totalInvested: 300000,
      currentValue: 325000,
      gain: 25000,
      gainPercent: 8.3,
      performance: 12.5,
      benchmark: 10.2,
      status: "active",
      nextDate: "2024-08-15",
    },
    {
      id: 2,
      fund: "HDFC Mid-Cap Fund",
      category: "Mid Cap",
      amount: 8000,
      frequency: "Monthly",
      startDate: "2022-03-20",
      totalInvested: 240000,
      currentValue: 252000,
      gain: 12000,
      gainPercent: 5.0,
      performance: 8.5,
      benchmark: 9.8,
      status: "active",
      nextDate: "2024-08-20",
    },
    {
      id: 3,
      fund: "ICICI Prudential Balanced Fund",
      category: "Balanced",
      amount: 7000,
      frequency: "Monthly",
      startDate: "2022-06-10",
      totalInvested: 180000,
      currentValue: 195000,
      gain: 15000,
      gainPercent: 8.3,
      performance: 10.2,
      benchmark: 8.5,
      status: "active",
      nextDate: "2024-08-10",
    },
    {
      id: 4,
      fund: "SBI Small Cap Fund",
      category: "Small Cap",
      amount: 6000,
      frequency: "Monthly",
      startDate: "2022-08-05",
      totalInvested: 144000,
      currentValue: 138000,
      gain: -6000,
      gainPercent: -4.2,
      performance: 6.8,
      benchmark: 7.2,
      status: "active",
      nextDate: "2024-08-05",
    },
    {
      id: 5,
      fund: "Nippon India Large Cap Fund",
      category: "Large Cap",
      amount: 5000,
      frequency: "Monthly",
      startDate: "2023-01-12",
      totalInvested: 95000,
      currentValue: 102000,
      gain: 7000,
      gainPercent: 7.4,
      performance: 11.8,
      benchmark: 10.5,
      status: "active",
      nextDate: "2024-08-12",
    },
    {
      id: 6,
      fund: "Kotak Emerging Equity Fund",
      category: "Mid Cap",
      amount: 9000,
      frequency: "Monthly",
      startDate: "2023-03-18",
      totalInvested: 162000,
      currentValue: 168000,
      gain: 6000,
      gainPercent: 3.7,
      performance: 9.2,
      benchmark: 8.9,
      status: "active",
      nextDate: "2024-08-18",
    },
  ],
  recommendations: [
    {
      type: "Switch Underperforming Fund",
      description:
        "Switch from SBI Small Cap Fund to better performing small cap fund",
      fund: "SBI Small Cap Fund",
      action: "Switch to Axis Small Cap Fund",
      potentialGain: 12000,
    },
    {
      type: "Increase Top Performer",
      description:
        "Increase SIP amount in Axis Bluechip Fund due to consistent performance",
      fund: "Axis Bluechip Fund",
      action: "Increase SIP to ₹15,000",
      potentialGain: 8000,
    },
    {
      type: "Add New Category",
      description: "Add international fund for better diversification",
      fund: "New Fund",
      action: "Start SIP in Franklin India Feeder Fund",
      potentialGain: 15000,
    },
  ],
  categoryAnalysis: [
    {
      category: "Large Cap",
      allocation: 46,
      performance: 12.1,
      benchmark: 10.3,
    },
    { category: "Mid Cap", allocation: 32, performance: 8.8, benchmark: 9.3 },
    { category: "Small Cap", allocation: 15, performance: 6.8, benchmark: 7.2 },
    { category: "Balanced", allocation: 7, performance: 10.2, benchmark: 8.5 },
  ],
};

export default function SIPsPage() {
  const getPerformanceColor = (performance: number, benchmark: number) => {
    return performance >= benchmark ? "text-green-600" : "text-red-600";
  };

  const getGainColor = (gain: number) => {
    return gain >= 0 ? "text-green-600" : "text-red-600";
  };

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">SIP Manager</h1>
          <p className="text-gray-600 mt-2">
            Track and optimize your Systematic Investment Plans
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <DollarSign className="h-5 w-5 text-blue-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Total Invested</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{sipData.totalInvested.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Across all SIPs</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="h-5 w-5 text-green-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Current Value</h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{sipData.currentValue.toLocaleString()}
            </div>
            <div className="text-sm text-green-600">
              +{sipData.totalGainPercent.toFixed(1)}% gain
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Calendar className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="font-semibold text-gray-900">
                Monthly Investment
              </h3>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              ₹{sipData.monthlyInvestment.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">
              {sipData.activeSIPs} active SIPs
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <BarChart3 className="h-5 w-5 text-orange-600" />
              </div>
              <h3 className="font-semibold text-gray-900">Total Gain</h3>
            </div>
            <div className="text-2xl font-bold text-green-600">
              ₹{sipData.totalGain.toLocaleString()}
            </div>
            <div className="text-sm text-gray-600">Absolute returns</div>
          </div>
        </div>

        {/* SIP List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Active SIPs
          </h3>
          <div className="space-y-4">
            {sipData.sips.map((sip) => (
              <div
                key={sip.id}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h4 className="font-medium text-gray-900">{sip.fund}</h4>
                    <p className="text-sm text-gray-600">{sip.category}</p>
                  </div>
                  <div className="text-right">
                    <div className="font-medium text-gray-900">
                      ₹{sip.amount.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">per month</div>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <div className="text-sm text-gray-600">Total Invested</div>
                    <div className="font-medium text-gray-900">
                      ₹{sip.totalInvested.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Current Value</div>
                    <div className="font-medium text-gray-900">
                      ₹{sip.currentValue.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Gain/Loss</div>
                    <div className={`font-medium ${getGainColor(sip.gain)}`}>
                      {sip.gain >= 0 ? "+" : ""}₹{sip.gain.toLocaleString()} (
                      {sip.gainPercent >= 0 ? "+" : ""}
                      {sip.gainPercent.toFixed(1)}%)
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Performance</div>
                    <div
                      className={`font-medium ${getPerformanceColor(
                        sip.performance,
                        sip.benchmark
                      )}`}
                    >
                      {sip.performance}% vs {sip.benchmark}%
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-600">
                    Next SIP: {new Date(sip.nextDate).toLocaleDateString()}
                  </div>
                  <div className="flex items-center gap-2">
                    <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                      Modify
                    </button>
                    <button className="text-sm text-red-600 hover:text-red-700 font-medium">
                      Stop
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Category Analysis */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Category Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {sipData.categoryAnalysis.map((category, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">
                  {category.category}
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Allocation:</span>
                    <span className="font-medium">{category.allocation}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Performance:</span>
                    <span
                      className={`font-medium ${getPerformanceColor(
                        category.performance,
                        category.benchmark
                      )}`}
                    >
                      {category.performance}%
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Benchmark:</span>
                    <span className="font-medium">{category.benchmark}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            SIP Recommendations
          </h3>
          <div className="space-y-4">
            {sipData.recommendations.map((rec, index) => (
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
                      Fund: {rec.fund}
                    </span>
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-green-600 font-medium">
                        Potential Gain: ₹{rec.potentialGain.toLocaleString()}
                      </span>
                      <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                        {rec.action}
                      </button>
                    </div>
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
              <span className="font-medium text-blue-900">Start New SIP</span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <BarChart3 className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">
                Performance Analysis
              </span>
            </button>

            <button className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <Zap className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">
                Auto Rebalance
              </span>
            </button>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
