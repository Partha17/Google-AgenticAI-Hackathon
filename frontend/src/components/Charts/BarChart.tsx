'use client';

import { Bar, CartesianGrid, Legend, BarChart as RechartsBarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

interface DataPoint {
  name: string;
  value: number;
  [key: string]: any;
}

interface BarChartProps {
  data: DataPoint[];
  title?: string;
  xAxisDataKey?: string;
  yAxisDataKey?: string;
  color?: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
}

export default function BarChart({
  data,
  title,
  xAxisDataKey = 'name',
  yAxisDataKey = 'value',
  color = '#3B82F6',
  height = 300,
  showGrid = true,
  showLegend = false
}: BarChartProps) {
  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />}
          <XAxis
            dataKey={xAxisDataKey}
            stroke="#6B7280"
            fontSize={12}
          />
          <YAxis
            stroke="#6B7280"
            fontSize={12}
            tickFormatter={(value) => `₹${value.toLocaleString()}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
            formatter={(value: any) => [`₹${value.toLocaleString()}`, 'Value']}
          />
          {showLegend && <Legend />}
          <Bar
            dataKey={yAxisDataKey}
            fill={color}
            radius={[4, 4, 0, 0]}
          />
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
}