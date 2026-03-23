/* Types for Fullmetal Anatomist */

export interface Settings {
  llm_provider: string;
  model_name: string;
  has_api_key: boolean;
  model_options: Record<string, string[]>;
}

export interface Subject {
  id: number;
  name: string;
  created_at: string;
  chapters: ChapterSummary[];
}

export interface ChapterSummary {
  id: number;
  title: string;
  chapter_number: number;
}

export interface Chapter {
  id: number;
  subject_id: number;
  title: string;
  chapter_number: number;
  raw_content: string;
  summary: string | null;
  created_at: string;
}

export interface WorksheetSummary {
  id: number;
  title: string;
  difficulty: string;
  status: string;
  question_count: number;
  chapter_title: string | null;
  created_at: string;
}

export interface WorksheetDetail {
  id: number;
  title: string;
  difficulty: string;
  status: string;
  created_at: string;
  chapter_title: string | null;
  questions: QuestionData[];
}

export interface QuestionData {
  id: number;
  order: number;
  question_text: string;
  answer_text: string;
  explanation: string;
  section_heading: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}
