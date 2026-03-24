import { useCallback, useEffect, useState } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import type { Settings, Subject } from '../types';
import { api } from '../api/client';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import SettingsModal from './SettingsModal';

interface Props {
  settings: Settings;
  onSave: (data: any) => Promise<any>;
}

export default function Layout({ settings, onSave }: Props) {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [showSettings, setShowSettings] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const refreshSubjects = useCallback(async () => {
    try {
      setSubjects(await api.listSubjects());
    } catch { /* empty */ }
  }, []);

  useEffect(() => { refreshSubjects(); }, [refreshSubjects]);

  return (
    <div className="min-h-screen flex flex-col">
      <TopBar
        settings={settings}
        onToggleSidebar={() => setSidebarOpen(v => !v)}
        onOpenSettings={() => setShowSettings(true)}
      />
      <div className="flex flex-1 overflow-hidden">
        {sidebarOpen && (
          <Sidebar subjects={subjects} onRefresh={refreshSubjects} />
        )}
        <main className="flex-1 overflow-y-auto p-4">
          <Outlet context={{ refreshSubjects }} />
        </main>
      </div>
      {showSettings && (
        <SettingsModal
          settings={settings}
          onSave={onSave}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  );
}
