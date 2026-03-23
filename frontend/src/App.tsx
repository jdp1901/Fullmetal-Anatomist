import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { useSettings } from './hooks/useSettings';
import Layout from './components/Layout';
import SetupWizard from './components/SetupWizard';
import ChatView from './components/ChatView';
import WorksheetViewer from './components/WorksheetViewer';
import WorksheetLibrary from './components/WorksheetLibrary';

export default function App() {
  const { settings, loading, update, testConnection, refresh } = useSettings();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-teal-400 text-2xl animate-pulse">⚗️ Loading...</div>
      </div>
    );
  }

  // First-run: no API key configured
  if (settings && !settings.has_api_key) {
    return (
      <SetupWizard
        settings={settings}
        onSave={async (data) => { await update(data); refresh(); }}
        onTest={testConnection}
      />
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/setup" element={
          <SetupWizard
            settings={settings!}
            onSave={async (data) => { await update(data); refresh(); }}
            onTest={testConnection}
          />
        } />
        <Route element={<Layout settings={settings!} />}>
          <Route path="/" element={<ChatView />} />
          <Route path="/worksheet/:id" element={<WorksheetViewer />} />
          <Route path="/library" element={<WorksheetLibrary />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
