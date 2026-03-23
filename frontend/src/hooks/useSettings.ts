import { useCallback, useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Settings } from '../types';

export function useSettings() {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getSettings();
      setSettings(data);
    } catch (err) {
      console.error('Failed to load settings', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { refresh(); }, [refresh]);

  const update = async (data: any) => {
    const updated = await api.updateSettings(data);
    setSettings(updated);
    return updated;
  };

  const testConnection = async () => api.testConnection();

  return { settings, loading, update, testConnection, refresh };
}
