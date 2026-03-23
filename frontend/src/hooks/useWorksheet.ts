import { useCallback, useEffect, useState } from 'react';
import { api } from '../api/client';
import type { WorksheetDetail, WorksheetSummary } from '../types';

export function useWorksheetList() {
  const [worksheets, setWorksheets] = useState<WorksheetSummary[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      setWorksheets(await api.listWorksheets());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { refresh(); }, [refresh]);

  return { worksheets, loading, refresh };
}

export function useWorksheet(id: number | null) {
  const [worksheet, setWorksheet] = useState<WorksheetDetail | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (id == null) { setWorksheet(null); return; }
    setLoading(true);
    api.getWorksheet(id)
      .then(setWorksheet)
      .finally(() => setLoading(false));
  }, [id]);

  return { worksheet, loading };
}
