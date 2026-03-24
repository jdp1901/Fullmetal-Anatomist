/* API client with SSE streaming support */

const BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  // Settings
  getSettings: () => request<any>('/settings'),
  updateSettings: (data: any) =>
    request<any>('/settings', { method: 'PUT', body: JSON.stringify(data) }),
  testConnection: () =>
    request<any>('/settings/test', { method: 'POST' }),

  // Subjects
  listSubjects: () => request<any[]>('/subjects'),
  createSubject: (name: string) =>
    request<any>('/subjects', { method: 'POST', body: JSON.stringify({ name }) }),

  // Chapters
  createChapter: (data: { subject_id: number; title: string; chapter_number?: number; raw_content: string }) =>
    request<any>('/chapters', { method: 'POST', body: JSON.stringify(data) }),
  uploadChapter: async (file: File, subjectId: number, title?: string) => {
    const form = new FormData();
    form.append('file', file);
    form.append('subject_id', String(subjectId));
    if (title) form.append('title', title);
    const res = await fetch(`${BASE}/chapters/upload`, { method: 'POST', body: form });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },
  getChapter: (id: number) => request<any>(`/chapters/${id}`),
  deleteChapter: (id: number) =>
    request<any>(`/chapters/${id}`, { method: 'DELETE' }),

  // Worksheets
  generateWorksheet: (chapterId: number, difficulty: string) =>
    request<any>('/worksheets/generate', {
      method: 'POST',
      body: JSON.stringify({ chapter_id: chapterId, difficulty }),
    }),
  listWorksheets: () => request<any[]>('/worksheets'),
  getWorksheet: (id: number) => request<any>(`/worksheets/${id}`),
  deleteWorksheet: (id: number) =>
    request<any>(`/worksheets/${id}`, { method: 'DELETE' }),
  regenerateWorksheet: (id: number) =>
    request<any>(`/worksheets/${id}/regenerate`, { method: 'POST' }),
  getPdfUrl: (id: number, answers = false) =>
    `${BASE}/worksheets/${id}/pdf${answers ? '?answers=true' : ''}`,

  // Chat (SSE streaming)
  streamChat: async function* (
    message: string,
    chapterId?: number,
  ): AsyncGenerator<string> {
    const res = await fetch(`${BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, chapter_id: chapterId }),
    });
    if (!res.ok || !res.body) throw new Error('Chat request failed');

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === 'delta') yield data.content;
            if (data.type === 'error') throw new Error(data.content);
            if (data.type === 'done') return;
          } catch (e) {
            if (e instanceof Error) throw e;
            /* skip malformed */
          }
        }
      }
    }
  },
};
