"use client";

import { Bot } from "lucide-react";
import Link from "next/link";
import Header from "./Header";
import Sidebar from "./Sidebar";

interface MainLayoutProps {
  children: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      <Sidebar />
      <div className="flex-1 flex flex-col lg:pl-72">
        <Header />
        <main className="flex-1 flex flex-col">
          <div className="flex-1 px-4 sm:px-6 lg:px-8 py-10">{children}</div>
        </main>
      </div>

      {/* Floating Chat Button */}
      <Link
        href="/chat"
        className="fixed bottom-8 right-8 z-50 bg-gradient-to-r from-blue-500 to-purple-600 text-white p-5 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110 group"
        title="Chat with AI Assistant"
      >
        <Bot className="h-7 w-7" />
        <div className="absolute -top-2 -right-2 h-4 w-4 bg-green-500 rounded-full animate-pulse"></div>
        <div className="absolute right-full mr-3 top-1/2 transform -translate-y-1/2 bg-gray-900 text-white text-sm px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
          Ask FinGenie
        </div>
      </Link>
    </div>
  );
}
