import { useState, useRef, type KeyboardEvent } from 'react';

interface Props {
  onSend: (text: string) => void;
  onStop: () => void;
  streaming: boolean;
}

export default function ChatInput({ onSend, onStop, streaming }: Props) {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || streaming) return;
    onSend(trimmed);
    setText('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = () => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = 'auto';
      ta.style.height = Math.min(ta.scrollHeight, 200) + 'px';
    }
  };

  return (
    <div className="border-t border-navy-700 bg-navy-800 p-3">
      <div className="flex gap-2 items-end">
        <textarea
          ref={textareaRef}
          className="input resize-none text-sm font-mono"
          rows={1}
          placeholder="Paste textbook content or ask a question..."
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          aria-label="Chat message input"
        />
        {streaming ? (
          <button className="btn-danger text-sm py-2 px-3" onClick={onStop}>
            Stop
          </button>
        ) : (
          <button
            className="btn-primary text-sm py-2 px-3"
            onClick={handleSubmit}
            disabled={!text.trim()}
          >
            Send
          </button>
        )}
      </div>
      <p className="text-xs text-gray-600 mt-1">
        Shift+Enter for newline · Supports .txt, .pdf, .docx uploads
      </p>
    </div>
  );
}
