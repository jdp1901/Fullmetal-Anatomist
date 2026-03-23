import { useState } from 'react';
import type { Settings } from '../types';

interface Props {
  settings: Settings;
  onSave: (data: any) => Promise<any>;
  onTest: () => Promise<any>;
}

export default function SetupWizard({ settings, onSave, onTest }: Props) {
  const [provider, setProvider] = useState(settings.llm_provider);
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState(settings.model_name);
  const [testResult, setTestResult] = useState<string | null>(null);
  const [testing, setTesting] = useState(false);
  const [saving, setSaving] = useState(false);

  const models = settings.model_options[provider] || [];

  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      // Save first so test uses the right key
      await onSave({ llm_provider: provider, api_key: apiKey, model_name: model });
      const result = await onTest();
      setTestResult(result.success ? '✅ Connection successful!' : `❌ ${result.message}`);
    } catch (e: any) {
      setTestResult(`❌ ${e.message}`);
    } finally {
      setTesting(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await onSave({ llm_provider: provider, api_key: apiKey, model_name: model });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="card max-w-lg w-full space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold">
            <span className="text-teal-400">⚗️</span> Fullmetal Anatomist
          </h1>
          <p className="text-gray-400 mt-2">Configure your LLM provider to get started</p>
        </div>

        {/* Provider */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1" htmlFor="provider">
            LLM Provider
          </label>
          <select
            id="provider"
            className="input"
            value={provider}
            onChange={e => {
              setProvider(e.target.value);
              setModel(settings.model_options[e.target.value]?.[0] || '');
            }}
          >
            <option value="gemini">Google Gemini</option>
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
          </select>
        </div>

        {/* API Key */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1" htmlFor="api-key">
            API Key
          </label>
          <input
            id="api-key"
            type="password"
            className="input font-mono"
            placeholder="Paste your API key here"
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
          />
        </div>

        {/* Model */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1" htmlFor="model">
            Model
          </label>
          <select
            id="model"
            className="input"
            value={model}
            onChange={e => setModel(e.target.value)}
          >
            {models.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>

        {/* Test result */}
        {testResult && (
          <p className={`text-sm ${testResult.startsWith('✅') ? 'text-emerald-400' : 'text-red-400'}`}>
            {testResult}
          </p>
        )}

        {/* Buttons */}
        <div className="flex gap-3">
          <button
            className="btn-secondary flex-1"
            onClick={handleTest}
            disabled={!apiKey || testing}
          >
            {testing ? 'Testing...' : 'Test Connection'}
          </button>
          <button
            className="btn-primary flex-1"
            onClick={handleSave}
            disabled={!apiKey || saving}
          >
            {saving ? 'Saving...' : 'Save & Start ⚗️'}
          </button>
        </div>
      </div>
    </div>
  );
}
