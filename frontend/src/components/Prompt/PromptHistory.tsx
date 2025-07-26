'use client';

import { Bot, Trash2, User } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface PromptHistoryProps {
  messages: Message[];
  onClearHistory: () => void;
}

export default function PromptHistory({ messages, onClearHistory }: PromptHistoryProps) {
  return (
    <div className="space-y-6">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex gap-4 ${
            message.role === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          {message.role === 'assistant' && (
            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
          )}

          <div
            className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-900'
            }`}
          >
            <div className="text-sm whitespace-pre-wrap leading-relaxed">
              {message.content}
            </div>
          </div>

          {message.role === 'user' && (
            <div className="flex-shrink-0 w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
          )}
        </div>
      ))}

      {messages.length > 0 && (
        <div className="flex justify-center pt-4">
          <button
            onClick={onClearHistory}
            className="flex items-center gap-2 px-4 py-2 text-sm text-gray-500 hover:text-red-600 transition-colors bg-white border border-gray-200 rounded-lg hover:bg-red-50"
          >
            <Trash2 size={14} />
            Clear conversation
          </button>
        </div>
      )}
    </div>
  );
}