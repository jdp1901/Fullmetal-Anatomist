import type { ChatMessage } from '../types';

interface Props {
  messages: ChatMessage[];
}

export default function MessageList({ messages }: Props) {
  return (
    <div className="space-y-3">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex ${
            msg.role === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          <div
            className={`max-w-[80%] rounded-xl px-4 py-3 ${
              msg.role === 'user'
                ? 'bg-teal-500/20 text-teal-100'
                : 'bg-navy-800 border border-navy-700 text-gray-200'
            }`}
          >
            {msg.role === 'assistant' && (
              <span className="text-teal-400 text-xs font-semibold block mb-1">
                ⚗️ Fullmetal Anatomist
              </span>
            )}
            <div className="whitespace-pre-wrap text-sm font-mono leading-relaxed">
              {msg.content}
              {msg.role === 'assistant' && msg.content === '' && (
                <span className="animate-pulse">█</span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
