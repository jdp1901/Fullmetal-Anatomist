import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useWorksheetList } from '../hooks/useWorksheet';
import { api } from '../api/client';

export default function WorksheetLibrary() {
  const { worksheets, loading, refresh } = useWorksheetList();
  const [filter, setFilter] = useState('');
  const navigate = useNavigate();

  const filtered = worksheets.filter(w =>
    w.title.toLowerCase().includes(filter.toLowerCase()) ||
    (w.chapter_title || '').toLowerCase().includes(filter.toLowerCase())
  );

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this worksheet?')) return;
    await api.deleteWorksheet(id);
    refresh();
  };

  if (loading) {
    return <div className="text-center py-20 text-teal-400 animate-pulse">⚗️ Loading library...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-teal-400">📚 Worksheet Library</h1>
        <input
          className="input w-64"
          placeholder="Search worksheets..."
          value={filter}
          onChange={e => setFilter(e.target.value)}
          aria-label="Search worksheets"
        />
      </div>

      {filtered.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-lg">No worksheets yet.</p>
          <p className="text-sm mt-1">Go to the chat and generate your first one!</p>
          <Link to="/" className="btn-primary inline-block mt-4">Go to Chat</Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map(w => (
            <div key={w.id} className="card hover:border-teal-500/50 transition-colors cursor-pointer"
                 onClick={() => navigate(`/worksheet/${w.id}`)}
                 role="button" tabIndex={0}
                 onKeyDown={e => e.key === 'Enter' && navigate(`/worksheet/${w.id}`)}
            >
              <h3 className="font-semibold text-sm truncate">{w.title}</h3>
              <p className="text-xs text-gray-400 mt-1">{w.chapter_title}</p>
              <div className="flex items-center gap-2 mt-3">
                <span className={`badge badge-${w.difficulty}`}>{w.difficulty}</span>
                <span className="text-xs text-gray-500">{w.question_count} questions</span>
                <span className="text-xs text-gray-600 ml-auto">
                  {new Date(w.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="flex gap-2 mt-3">
                <a
                  href={api.getPdfUrl(w.id)}
                  download
                  className="text-xs text-teal-400 hover:underline"
                  onClick={e => e.stopPropagation()}
                >
                  📥 PDF
                </a>
                <button
                  className="text-xs text-red-400 hover:underline ml-auto"
                  onClick={e => { e.stopPropagation(); handleDelete(w.id); }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
