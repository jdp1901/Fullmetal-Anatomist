import { useCallback, useRef, useState } from 'react';
import { api } from '../api/client';
import type { ChatMessage } from '../types';

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const abortRef = useRef(false);

  const send = useCallback(async (text: string, chapterId?: number) => {
    abortRef.current = false;
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setStreaming(true);

    let assistantContent = '';
    setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

    try {
      for await (const chunk of api.streamChat(text, chapterId)) {
        if (abortRef.current) break;
        assistantContent += chunk;
        setMessages(prev => {
          const copy = [...prev];
          copy[copy.length - 1] = { role: 'assistant', content: assistantContent };
          return copy;
        });
      }
    } catch (err) {
      assistantContent += '\n\n⚠️ Error: Could not reach the assistant.';
      setMessages(prev => {
        const copy = [...prev];
        copy[copy.length - 1] = { role: 'assistant', content: assistantContent };
        return copy;
      });
    } finally {
      setStreaming(false);
    }
  }, []);

  const stop = useCallback(() => { abortRef.current = true; }, []);
  const clear = useCallback(() => { setMessages([]); }, []);

  return { messages, streaming, send, stop, clear };
}
