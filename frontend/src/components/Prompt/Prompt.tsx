// frontend/src/components/Prompt/Prompt.tsx
import React, { useState } from 'react';

const Prompt: React.FC = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to the chat
    setMessages([...messages, `You: ${input}`]);

    // Send the prompt to the backend
    const response = await fetch('/api/prompt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: input }),
    });

    const data = await response.json();

    // Add the response from the backend to the chat
    setMessages([...messages, `You: ${input}`, `AI: ${data.response}`]);
    setInput('');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', justifyContent: 'space-between', margin: 'auto', maxWidth: '768px' }}>
      <div style={{ flexGrow: 1, overflowY: 'auto', padding: '1rem' }}>
        {messages.map((message, index) => (
          <div key={index} style={{ marginBottom: '1rem' }}>
            {message}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} style={{ display: 'flex', padding: '1rem' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ flexGrow: 1, padding: '0.5rem', marginRight: '0.5rem' }}
          placeholder="Ask me anything..."
        />
        <button type="submit" style={{ padding: '0.5rem 1rem' }}>
          Send
        </button>
      </form>
    </div>
  );
};

export default Prompt;
