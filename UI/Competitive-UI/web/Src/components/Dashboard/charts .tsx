import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface ChartsProps {
  analysisResult: any;
}

const Charts: React.FC<ChartsProps> = ({ analysisResult }) => {
  const indicators = analysisResult?.indicators || {};
  const chartData = Object.entries(indicators).map(([key, value]: [string, any]) => ({
    name: key,
    score: value.score || 0,
    threshold: value.threshold || 0.7,
  }));

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-700">
      <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">توزيع المؤشرات</h3>
      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" tick={{ fill: '#9ca3af' }} />
            <YAxis domain={[0, 1]} tick={{ fill: '#9ca3af' }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
              labelStyle={{ color: '#f3f4f6' }}
            />
            <Bar dataKey="score" fill="#3b82f6" radius={[4, 4, 0, 0]}>
              {chartData.map((entry) => (
                <Cell key={entry.name} fill={entry.score > entry.threshold ? '#ef4444' : '#3b82f6'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <div className="text-center text-gray-400 py-8">لا توجد بيانات لعرضها</div>
      )}
    </div>
  );
};

export default Charts;
