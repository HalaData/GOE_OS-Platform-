import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { governanceAPI, statusAPI } from '../api/client';
import StatsCards from '../components/Dashboard/StatsCards';
import Charts from '../components/Dashboard/Charts';

const Dashboard: React.FC = () => {
  const [sampleText, setSampleText] = useState('هذا نص تجريبي للتحليل');
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  // جلب حالة النظام
  const { data: statusData } = useQuery({
    queryKey: ['status'],
    queryFn: () => statusAPI.getStatus().then(res => res.data),
    refetchInterval: 30000,
  });

  // جلب المؤشرات
  const { data: indicatorsData } = useQuery({
    queryKey: ['indicators'],
    queryFn: () => governanceAPI.getIndicators().then(res => res.data),
  });

  // تحليل تجريبي
  const handleAnalyze = async () => {
    try {
      const res = await governanceAPI.analyze({
        text: sampleText,
        domain: 'general',
        consent_given: true,
      });
      setAnalysisResult(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    handleAnalyze();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">لوحة التحكم</h1>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {statusData?.status === 'running' ? '🟢 النظام يعمل' : '🔴 النظام متوقف'}
        </span>
      </div>

      <StatsCards analysisResult={analysisResult} indicatorsCount={Object.keys(indicatorsData || {}).length} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Charts analysisResult={analysisResult} />
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">تحليل سريع</h3>
          <textarea
            className="w-full h-24 p-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 text-sm"
            value={sampleText}
            onChange={(e) => setSampleText(e.target.value)}
          />
          <button
            onClick={handleAnalyze}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm"
          >
            تحليل
          </button>
          {analysisResult && (
            <div className="mt-3 text-sm text-gray-600 dark:text-gray-400">
              درجة اليقظة: <strong>{analysisResult.vigilance_score}%</strong>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
