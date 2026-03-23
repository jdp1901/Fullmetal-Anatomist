import { useCallback, useRef, useState } from 'react';
import { api } from '../api/client';

interface Props {
  onUploaded: (chapterId: number) => void;
}

export default function FileUploadZone({ onUploaded }: Props) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      // Ensure a default subject exists
      let subjects = await api.listSubjects();
      let subjectId: number;
      if (subjects.length === 0) {
        const created = await api.createSubject('General');
        subjectId = created.id;
      } else {
        subjectId = subjects[0].id;
      }
      const chapter = await api.uploadChapter(file, subjectId, file.name);
      onUploaded(chapter.id);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setUploading(false);
    }
  }, [onUploaded]);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors
        ${dragging ? 'border-teal-400 bg-teal-500/5' : 'border-navy-700 hover:border-navy-600'}`}
      onDragOver={e => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
    >
      {uploading ? (
        <p className="text-teal-400 animate-pulse">Uploading & extracting text...</p>
      ) : (
        <>
          <p className="text-gray-400 mb-2">
            Drag & drop a file here, or{' '}
            <button
              className="text-teal-400 underline"
              onClick={() => inputRef.current?.click()}
            >
              browse
            </button>
          </p>
          <p className="text-xs text-gray-600">.txt, .pdf, .docx supported</p>
          {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
        </>
      )}
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".txt,.pdf,.docx"
        onChange={e => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
        }}
        aria-label="Upload file"
      />
    </div>
  );
}
