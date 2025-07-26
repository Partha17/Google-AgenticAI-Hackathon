'use client';

import { CartesianGrid, Legend, Line, LineChart as RechartsLineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

interface DataPoint {
  name: string;
  value: number;
  [key: string]: any;
}

interface LineChartProps {
  data: DataPoint[];
  title?: string;
  xAxisDataKey?: string;
  yAxisDataKey?: string;
  color?: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
}

export default function LineChart({
  data,
  title,
  xAxisDataKey = 'name',
  yAxisDataKey = 'value',
  color = '#3B82F6',
  height = 300,
  showGrid = true,
  showLegend = false
}: LineChartProps) {
  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsLineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
          <Line
            type="monotone"
            dataKey={yAxisDataKey}
            stroke={color}
            strokeWidth={2}
            dot={{ fill: color, strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: color, strokeWidth: 2 }}
          />
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  );
}