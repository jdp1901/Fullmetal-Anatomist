import { useState } from 'react';
import { api } from '../api/client';
import type { Settings } from '../types';

interface Props {
  settings: Settings;
  onClose: () => void;
}

export default function SettingsModal({ settings, onClose }: Props) {
  const [provider, setProvider] = useState(settings.llm_provider);
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState(settings.model_name);
  const [saving, setSaving] = useState(false);

  const models = settings.model_options[provider] || [];

  const handleSave = async () => {
    setSaving(true);
    try {
      const data: any = { llm_provider: provider, model_name: model };
      if (apiKey) data.api_key = apiKey;
      await api.updateSettings(data);
      onClose();
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
         onClick={onClose} role="dialog" aria-label="Settings">
      <div className="card max-w-md w-full space-y-4" onClick={e => e.stopPropagation()}>
        <h2 className="text-lg font-bold text-teal-400">⚙️ Settings</h2>

        <div>
          <label className="block text-sm text-gray-300 mb-1" htmlFor="s-provider">Provider</label>
          <select id="s-provider" className="input" value={provider}
            onChange={e => { setProvider(e.target.value); setModel(settings.model_options[e.target.value]?.[0] || ''); }}>
            <option value="gemini">Google Gemini</option>
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
          </select>
        </div>

        <div>
          <label className="block text-sm text-gray-300 mb-1" htmlFor="s-key">API Key (leave blank to keep current)</label>
          <input id="s-key" type="password" className="input font-mono" placeholder="••••••••"
            value={apiKey} onChange={e => setApiKey(e.target.value)} />
        </div>

        <div>
          <label className="block text-sm text-gray-300 mb-1" htmlFor="s-model">Model</label>
          <select id="s-model" className="input" value={model}
            onChange={e => setModel(e.target.value)}>
            {models.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>

        <div className="flex gap-3 justify-end">
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn-primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
    </div>
  );
}
