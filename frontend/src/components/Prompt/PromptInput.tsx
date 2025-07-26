'use client';

import { Mic, Send } from 'lucide-react';
import { KeyboardEvent, useState } from 'react';

interface PromptInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export default function PromptInput({ onSendMessage, isLoading }: PromptInputProps) {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleVoiceInput = () => {
    // TODO: Implement voice input functionality
    console.log('Voice input not implemented yet');
  };

  return (
    <div className="max-w-4xl mx-auto w-full">
      <div className="relative flex">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message FinGenie..."
          className="w-full px-4 py-3 pr-20 border border-gray-300 rounded-2xl resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
          rows={1}
          style={{ minHeight: '52px', maxHeight: '200px' }}
          disabled={isLoading}
        />

        <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
          <button
            onClick={handleVoiceInput}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100"
            disabled={isLoading}
          >
            <Mic size={18} />
          </button>

          <button
            onClick={handleSend}
            disabled={!message.trim() || isLoading}
            className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            <Send size={18} />
          </button>
        </div>
      </div>

      <div className="text-center mt-3 mb-2">
        <p className="text-xs text-gray-500">
          FinGenie can make mistakes. Consider checking important information.
        </p>
      </div>
    </div>
  );
}