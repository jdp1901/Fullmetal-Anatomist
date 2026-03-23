/** Scoring utility for fill-in-the-blank answers. */

export function normalizeAnswer(answer: string): string {
  return answer.trim().toLowerCase().replace(/[^a-z0-9\s]/g, '');
}

export function checkAnswer(userAnswer: string, correctAnswer: string): boolean {
  return normalizeAnswer(userAnswer) === normalizeAnswer(correctAnswer);
}

export function calculateScore(
  answers: Record<number, string>,
  questions: { id: number; answer_text: string }[],
): { correct: number; total: number; percentage: number } {
  let correct = 0;
  for (const q of questions) {
    if (answers[q.id] && checkAnswer(answers[q.id], q.answer_text)) {
      correct++;
    }
  }
  const total = questions.length;
  return { correct, total, percentage: total > 0 ? Math.round((correct / total) * 100) : 0 };
}
