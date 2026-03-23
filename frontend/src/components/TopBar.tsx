import { Link } from 'react-router-dom';
import type { Settings } from '../types';

interface Props {
  settings: Settings;
  onToggleSidebar: () => void;
  onOpenSettings: () => void;
}

export default function TopBar({ settings, onToggleSidebar, onOpenSettings }: Props) {
  return (
    <header className="bg-navy-800 border-b border-navy-700 px-4 py-2 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="text-gray-400 hover:text-white p-1"
          aria-label="Toggle sidebar"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <span className="text-teal-400">⚗️</span>
          <span className="hidden sm:inline">Fullmetal Anatomist</span>
        </Link>
      </div>

      <div className="flex items-center gap-3">
        {/* Provider badge */}
        <span className="badge bg-teal-500/20 text-teal-400">
          {settings.llm_provider} · {settings.model_name}
        </span>

        <Link to="/library" className="text-gray-400 hover:text-white text-sm">
          📚 Library
        </Link>

        <button
          onClick={onOpenSettings}
          className="text-gray-400 hover:text-white p-1"
          aria-label="Settings"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
      </div>
    </header>
  );
}
