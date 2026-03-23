import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Subject } from '../types';
import { api } from '../api/client';

interface Props {
  subjects: Subject[];
  onRefresh: () => void;
}

export default function Sidebar({ subjects, onRefresh }: Props) {
  const [expanded, setExpanded] = useState<Set<number>>(new Set());
  const [newSubject, setNewSubject] = useState('');
  const [adding, setAdding] = useState(false);

  const toggle = (id: number) => {
    setExpanded(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const handleAdd = async () => {
    if (!newSubject.trim()) return;
    setAdding(true);
    try {
      await api.createSubject(newSubject.trim());
      setNewSubject('');
      onRefresh();
    } finally {
      setAdding(false);
    }
  };

  return (
    <aside className="w-64 bg-navy-800 border-r border-navy-700 overflow-y-auto flex flex-col">
      <div className="p-3 border-b border-navy-700">
        <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
          Subjects
        </h2>
        <div className="flex gap-1">
          <input
            className="input text-sm py-1"
            placeholder="New subject..."
            value={newSubject}
            onChange={e => setNewSubject(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleAdd()}
            aria-label="New subject name"
          />
          <button className="btn-primary text-sm py-1 px-2" onClick={handleAdd} disabled={adding}>
            +
          </button>
        </div>
      </div>

      <nav className="flex-1 p-2 space-y-1" aria-label="Subject navigation">
        {subjects.length === 0 && (
          <p className="text-xs text-gray-500 p-2">No subjects yet. Add one above!</p>
        )}
        {subjects.map(subject => (
          <div key={subject.id}>
            <button
              onClick={() => toggle(subject.id)}
              className="w-full text-left px-2 py-1.5 rounded hover:bg-navy-700
                         text-sm font-medium text-gray-200 flex items-center gap-2"
            >
              <span className={`transform transition-transform ${
                expanded.has(subject.id) ? 'rotate-90' : ''
              }`}>▶</span>
              {subject.name}
              <span className="ml-auto text-xs text-gray-500">
                {subject.chapters.length}
              </span>
            </button>
            {expanded.has(subject.id) && (
              <div className="ml-5 space-y-0.5">
                {subject.chapters.map(ch => (
                  <Link
                    key={ch.id}
                    to={`/?chapter=${ch.id}`}
                    className="block px-2 py-1 text-xs text-gray-400 hover:text-teal-400
                               hover:bg-navy-700 rounded truncate"
                  >
                    {ch.title}
                  </Link>
                ))}
                {subject.chapters.length === 0 && (
                  <p className="text-xs text-gray-600 px-2">No chapters</p>
                )}
              </div>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
