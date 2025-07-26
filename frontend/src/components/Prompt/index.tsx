"use client";

import { useState } from "react";
import ChatPanel from "./ChatPanel";
import PromptInput from "./PromptInput";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

const suggestedQuestions = [
  "How can I optimize my tax savings?",
  "What's the best way to invest ₹50,000?",
  "Should I refinance my home loan?",
  "How much should I save for retirement?",
  "Which mutual funds are performing well?",
  "How can I improve my credit score?",
  "What's the best debt payoff strategy?",
  "How do I create an emergency fund?",
];

export default function Prompt() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: message,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `I understand you're asking about "${message}". Let me provide you with personalized financial advice based on your portfolio and goals. This is a mock response - in the real implementation, this would connect to your AI backend for actual financial analysis and recommendations.`,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
    }, 2000);
  };

  const handleSuggestedQuestion = (question: string) => {
    handleSendMessage(question);
  };

  return (
    <div className="relative h-full flex flex-col">
      {/* Main Chat Area - Scrollable */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full px-4">
            <div className="text-center max-w-2xl">
              <div className="mb-8">
                <div className="mx-auto h-16 w-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4">
                  <svg
                    className="h-8 w-8 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                </div>
                <h1 className="text-3xl font-bold text-gray-900 mb-4">
                  Welcome to FinGenie AI
                </h1>
                <p className="text-lg text-gray-600 mb-8">
                  Your personal AI financial assistant. Ask me anything about
                  your finances, investments, or financial planning.
                </p>
              </div>

              {/* Suggested Questions */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Popular Questions
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {suggestedQuestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestedQuestion(question)}
                      className="text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 group"
                    >
                      <p className="text-sm text-gray-700 group-hover:text-gray-900">
                        {question}
                      </p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Features */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4">
                  <div className="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                    <svg
                      className="h-4 w-4 text-blue-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                      />
                    </svg>
                  </div>
                  <h4 className="font-medium text-gray-900">
                    Portfolio Analysis
                  </h4>
                  <p className="text-sm text-gray-600">
                    Get insights on your investments
                  </p>
                </div>
                <div className="text-center p-4">
                  <div className="h-8 w-8 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                    <svg
                      className="h-4 w-4 text-green-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                      />
                    </svg>
                  </div>
                  <h4 className="font-medium text-gray-900">
                    Tax Optimization
                  </h4>
                  <p className="text-sm text-gray-600">
                    Maximize your tax savings
                  </p>
                </div>
                <div className="text-center p-4">
                  <div className="h-8 w-8 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                    <svg
                      className="h-4 w-4 text-purple-600"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                      />
                    </svg>
                  </div>
                  <h4 className="font-medium text-gray-900">
                    Smart Recommendations
                  </h4>
                  <p className="text-sm text-gray-600">
                    Personalized financial advice
                  </p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <ChatPanel messages={messages} />
        )}
      </div>

      {/* Fixed Input Area at bottom */}
      <div className="sticky bottom-0 left-0 right-0 bg-white p-4 border-t border-gray-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)]">
        <PromptInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}
