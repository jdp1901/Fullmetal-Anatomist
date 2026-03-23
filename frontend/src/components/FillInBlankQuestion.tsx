import type { QuestionData } from '../types';
import { checkAnswer } from '../utils/scoring';

interface Props {
  question: QuestionData;
  value: string;
  onChange: (val: string) => void;
  checked: boolean;
}

export default function FillInBlankQuestion({ question, value, onChange, checked }: Props) {
  const isCorrect = checked && checkAnswer(value, question.answer_text);
  const isWrong = checked && value.trim() !== '' && !isCorrect;
  const isEmpty = checked && value.trim() === '';

  return (
    <div className={`flex items-start gap-3 p-2 rounded-lg ${
      checked ? (isCorrect ? 'bg-emerald-900/20' : 'bg-red-900/10') : ''
    }`}>
      <span className="text-gray-500 text-sm font-mono w-8 text-right flex-shrink-0 pt-1">
        {question.order}.
      </span>
      <div className="flex-1">
        <p className="text-sm text-gray-200 font-mono leading-relaxed">
          {renderWithBlanks(question.question_text, value, onChange, checked, question.answer_text)}
        </p>
        {checked && (isWrong || isEmpty) && (
          <p className="text-xs text-teal-400 mt-1">
            → {question.answer_text}
            {question.explanation && (
              <span className="text-gray-500 ml-2">({question.explanation})</span>
            )}
          </p>
        )}
      </div>
    </div>
  );
}

function renderWithBlanks(
  text: string,
  value: string,
  onChange: (val: string) => void,
  checked: boolean,
  answer: string,
) {
  const parts = text.split('_____');
  if (parts.length <= 1) {
    // No blank found — render as-is with input at end
    return (
      <>
        {text}{' '}
        <input
          className={`input inline-block w-40 text-sm py-0.5 px-2 mx-1 ${
            checked ? (checkAnswer(value, answer) ? 'border-emerald-500' : 'border-red-500') : ''
          }`}
          value={value}
          onChange={e => onChange(e.target.value)}
          disabled={checked}
          aria-label={`Answer for question`}
        />
      </>
    );
  }

  return (
    <>
      {parts[0]}
      <input
        className={`input inline-block w-40 text-sm py-0.5 px-2 mx-1 ${
          checked ? (checkAnswer(value, answer) ? 'border-emerald-500' : 'border-red-500') : ''
        }`}
        value={value}
        onChange={e => onChange(e.target.value)}
        disabled={checked}
        aria-label={`Fill in the blank`}
      />
      {parts.slice(1).join('_____')}
    </>
  );
}
