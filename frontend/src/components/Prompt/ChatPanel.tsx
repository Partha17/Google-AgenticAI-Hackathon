'use client';

import { ArrowLeft, Menu, Plus, X } from 'lucide-react';
import { useState } from 'react';
import Prompt from './index';

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ChatPanel({ isOpen, onClose }: ChatPanelProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const handleBackToDashboard = () => {
    onClose();
  };

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
          onClick={onClose}
        />
      )}

      {/* Chat Panel */}
      <div
        className={`
          fixed inset-0 z-50
          bg-white
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : 'translate-x-full'}
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-white h-16">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Menu className="w-5 h-5 text-gray-600" />
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold text-sm">AI</span>
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-900">FinGenie AI</h2>
                <p className="text-sm text-gray-500">Your financial assistant</p>
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            aria-label="Close chat"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Main Content */}
        <div className="flex h-full" style={{ height: 'calc(100vh - 64px)' }}>
          {/* Sidebar */}
          <div
            className={`
              bg-gray-50 border-r border-gray-200 transition-all duration-300
              ${isSidebarOpen ? 'w-64' : 'w-0 overflow-hidden'}
            `}
          >
            <div className="p-4">
              {/* New Chat Button */}
              <button className="w-full flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors mb-4">
                <Plus className="w-5 h-5 text-gray-600" />
                <span className="text-gray-700 font-medium">New Chat</span>
              </button>

              {/* Back to Dashboard */}
              <button
                onClick={handleBackToDashboard}
                className="w-full flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200 hover:bg-blue-100 transition-colors mb-4"
              >
                <ArrowLeft className="w-5 h-5 text-blue-600" />
                <span className="text-blue-700 font-medium">Back to Dashboard</span>
              </button>

              {/* Chat History */}
              <div className="space-y-2">
                <h3 className="text-sm font-medium text-gray-700 mb-3">Recent Chats</h3>
                <div className="space-y-1">
                  <button className="w-full text-left p-2 text-sm text-gray-600 hover:bg-white rounded-lg transition-colors">
                    Portfolio Analysis
                  </button>
                  <button className="w-full text-left p-2 text-sm text-gray-600 hover:bg-white rounded-lg transition-colors">
                    Investment Recommendations
                  </button>
                  <button className="w-full text-left p-2 text-sm text-gray-600 hover:bg-white rounded-lg transition-colors">
                    Tax Optimization
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Chat Area */}
          <div className="flex-1 h-full">
            <Prompt />
          </div>
        </div>
      </div>
    </>
  );
}