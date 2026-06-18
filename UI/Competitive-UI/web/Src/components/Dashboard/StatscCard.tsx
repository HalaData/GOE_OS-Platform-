import React from 'react';
import { Activity, FileText, AlertTriangle, TrendingUp } from 'lucide-react';

interface StatsCardsProps {
  analysisResult: any;
  indicatorsCount: number;
}

const StatsCards: React.FC<StatsCardsProps> = ({ analysisResult, indicatorsCount }) => {
  const stats = [
    {
      title: 'درجة اليقظة',
      value: analysisResult?.vigilance_score || '--',
      icon: Activity,
      color: 'text-blue-600 dark:text-blue-400',
      bg: 'bg-blue-50 dark:bg-blue-900/20',
    },
    {
      title: 'المؤشرات',
      value: indicatorsCount || '--',
      icon: FileText,
      color: 'text-green-600 dark:text-green-400',
      bg: 'bg-green-50 dark:bg-green-900/20',
    },
    {
      title: 'الأسئلة المحرمة',
      value: analysisResult?.forbidden_questions?.length || 0,
      icon: AlertTriangle,
      color: 'text-yellow-600 dark:text-yellow-400',
      bg: 'bg-yellow-50 dark:bg-yellow-900/20',
    },
    {
      title: 'المسلمات',
      value: analysisResult?.dogmas?.length || 0,
      icon: TrendingUp,
      color: 'text-red-600 dark:text-red-400',
      bg: 'bg-red-50 dark:bg-red-900/20',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <div key={stat.title} className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${stat.bg}`}>
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">{stat.title}</p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">{stat.value}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatsCards;
