import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useWorksheet } from '../hooks/useWorksheet';
import { api } from '../api/client';
import FillInBlankQuestion from './FillInBlankQuestion';
import WorksheetActions from './WorksheetActions';
import { calculateScore } from '../utils/scoring';

export default function WorksheetViewer() {
  const { id } = useParams<{ id: string }>();
  const { worksheet, loading } = useWorksheet(id ? Number(id) : null);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [checked, setChecked] = useState(false);

  const score = useMemo(() => {
    if (!worksheet || !checked) return null;
    return calculateScore(answers, worksheet.questions);
  }, [answers, worksheet, checked]);

  if (loading) {
    return <div className="text-center py-20 text-teal-400 animate-pulse">⚗️ Loading worksheet...</div>;
  }

  if (!worksheet) {
    return <div className="text-center py-20 text-gray-400">Worksheet not found</div>;
  }

  // Group questions by section
  const sections = new Map<string, typeof worksheet.questions>();
  for (const q of worksheet.questions) {
    const key = q.section_heading || 'General';
    if (!sections.has(key)) sections.set(key, []);
    sections.get(key)!.push(q);
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="card mb-6">
        <h1 className="text-xl font-bold text-teal-400">{worksheet.title}</h1>
        <div className="flex gap-3 mt-2 text-sm text-gray-400">
          {worksheet.chapter_title && <span>📖 {worksheet.chapter_title}</span>}
          <span className={`badge badge-${worksheet.difficulty}`}>
            {worksheet.difficulty}
          </span>
          <span>{worksheet.questions.length} questions</span>
        </div>
      </div>

      {/* Instructions */}
      <p className="text-sm text-gray-400 mb-4 italic">
        Fill in each blank with the correct term or phrase. Click "Check Answers" when done.
      </p>

      {/* Sections + Questions */}
      {Array.from(sections.entries()).map(([heading, questions]) => (
        <div key={heading} className="mb-6">
          <h2 className="text-teal-400 font-semibold text-sm uppercase tracking-wider
                         border-b border-navy-700 pb-1 mb-3">
            {heading}
          </h2>
          <div className="space-y-2">
            {questions.map(q => (
              <FillInBlankQuestion
                key={q.id}
                question={q}
                value={answers[q.id] || ''}
                onChange={val => setAnswers(prev => ({ ...prev, [q.id]: val }))}
                checked={checked}
              />
            ))}
          </div>
        </div>
      ))}

      {/* Score */}
      {score && (
        <div className="card text-center my-6">
          <p className="text-3xl font-bold">
            <span className={score.percentage >= 70 ? 'text-emerald-400' : 'text-red-400'}>
              {score.correct}
            </span>
            <span className="text-gray-500"> / {score.total}</span>
          </p>
          <p className="text-gray-400">{score.percentage}% correct</p>
        </div>
      )}

      {/* Actions */}
      <WorksheetActions
        worksheetId={worksheet.id}
        checked={checked}
        onCheck={() => setChecked(true)}
        onReset={() => { setChecked(false); setAnswers({}); }}
      />
    </div>
  );
}
