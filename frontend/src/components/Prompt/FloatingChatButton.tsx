'use client';

import { MessageSquare } from 'lucide-react';

interface FloatingChatButtonProps {
  onClick: () => void;
  isOpen: boolean;
}

export default function FloatingChatButton({ onClick, isOpen }: FloatingChatButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`
        fixed bottom-6 right-6 z-50
        w-14 h-14 rounded-full
        bg-blue-600 hover:bg-blue-700
        text-white shadow-lg
        transition-all duration-300 ease-in-out
        transform hover:scale-110
        ${isOpen ? 'rotate-180' : 'rotate-0'}
        animate-pulse
      `}
      aria-label="Open AI Chat"
    >
      <MessageSquare className="w-6 h-6 mx-auto" />
    </button>
  );
}