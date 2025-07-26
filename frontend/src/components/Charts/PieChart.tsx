'use client';

import { Cell, Legend, Pie, PieChart as RechartsPieChart, ResponsiveContainer, Tooltip } from 'recharts';

interface DataPoint {
  name: string;
  value: number;
  color?: string;
}

interface PieChartProps {
  data: DataPoint[];
  title?: string;
  height?: number;
  showLegend?: boolean;
  colors?: string[];
}

const defaultColors = [
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
  '#8B5CF6', '#06B6D4', '#84CC16', '#F97316'
];

export default function PieChart({
  data,
  title,
  height = 300,
  showLegend = true,
  colors = defaultColors
}: PieChartProps) {
  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsPieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.color || colors[index % colors.length]}
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
            formatter={(value: any) => [`₹${value.toLocaleString()}`, 'Value']}
          />
          {showLegend && (
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value, entry, index) => (
                <span style={{ color: colors[index % colors.length] }}>
                  {value}
                </span>
              )}
            />
          )}
        </RechartsPieChart>
      </ResponsiveContainer>
    </div>
  );
}