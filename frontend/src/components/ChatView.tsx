import { useRef, useState } from 'react';
import { useChat } from '../hooks/useChat';
import ChatInput from './ChatInput';
import MessageList from './MessageList';
import FileUploadZone from './FileUploadZone';

export default function ChatView() {
  const { messages, streaming, send, stop } = useChat();
  const [activeChapterId, setActiveChapterId] = useState<number | undefined>();
  const bottomRef = useRef<HTMLDivElement>(null);

  const handleSend = async (text: string) => {
    await send(text, activeChapterId);
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.length === 0 && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">⚗️</div>
            <h2 className="text-2xl font-bold text-teal-400 mb-2">
              Welcome to Fullmetal Anatomist
            </h2>
            <p className="text-gray-400 max-w-md mx-auto">
              Paste textbook content, upload files, or ask me anything about your
              study material. I'll transmute it into worksheets! ✨
            </p>
            <div className="mt-6">
              <FileUploadZone onUploaded={(chId) => setActiveChapterId(chId)} />
            </div>
          </div>
        )}
        <MessageList messages={messages} />
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <ChatInput
        onSend={handleSend}
        onStop={stop}
        streaming={streaming}
      />
    </div>
  );
}
