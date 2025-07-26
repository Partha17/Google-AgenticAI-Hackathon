'use client';

import { AlertCircle, Bot, CheckCircle, Loader2 } from 'lucide-react';
import { useEffect, useState } from 'react';

interface PromptResponseProps {
  response: string;
  isLoading: boolean;
  error?: string;
  isStreaming?: boolean;
}

export default function PromptResponse({
  response,
  isLoading,
  error,
  isStreaming = false
}: PromptResponseProps) {
  const [displayedResponse, setDisplayedResponse] = useState('');

  useEffect(() => {
    if (isStreaming && response) {
      let index = 0;
      const interval = setInterval(() => {
        if (index < response.length) {
          setDisplayedResponse(response.slice(0, index + 1));
          index++;
        } else {
          clearInterval(interval);
        }
      }, 20);
      return () => clearInterval(interval);
    } else {
      setDisplayedResponse(response);
    }
  }, [response, isStreaming]);

  if (isLoading) {
    return (
      <div className="flex gap-4">
        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
          <Bot className="w-4 h-4 text-white" />
        </div>
        <div className="flex items-center gap-3 p-4 bg-gray-100 rounded-2xl">
          <Loader2 size={20} className="animate-spin text-blue-600" />
          <div>
            <p className="text-blue-900 font-medium">FinGenie is thinking...</p>
            <p className="text-blue-700 text-sm">Analyzing your financial data</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex gap-4">
        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
          <Bot className="w-4 h-4 text-white" />
        </div>
        <div className="flex items-center gap-3 p-4 bg-red-50 rounded-2xl border border-red-200">
          <AlertCircle size={20} className="text-red-600" />
          <div>
            <p className="text-red-900 font-medium">Error</p>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!response) {
    return null;
  }

  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
        <Bot className="w-4 h-4 text-white" />
      </div>
      <div className="flex-1">
        <div className="bg-gray-100 rounded-2xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <h4 className="font-semibold text-gray-900">FinGenie AI</h4>
            {isStreaming && (
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse" />
                <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse delay-100" />
                <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse delay-200" />
              </div>
            )}
            {!isStreaming && displayedResponse === response && (
              <CheckCircle size={16} className="text-green-600" />
            )}
          </div>
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
              {displayedResponse}
              {isStreaming && displayedResponse !== response && (
                <span className="inline-block w-2 h-4 bg-blue-600 animate-pulse" />
              )}
            </div>
          </div>
        </div>
        {!isStreaming && displayedResponse === response && (
          <div className="flex items-center gap-4 mt-3">
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
              Save to Portfolio
            </button>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
              Generate Report
            </button>
            <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
              Share Insights
            </button>
          </div>
        )}
      </div>
    </div>
  );
}