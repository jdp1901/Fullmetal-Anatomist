import { api } from '../api/client';

interface Props {
  worksheetId: number;
  checked: boolean;
  onCheck: () => void;
  onReset: () => void;
}

export default function WorksheetActions({ worksheetId, checked, onCheck, onReset }: Props) {
  return (
    <div className="flex flex-wrap gap-3 py-4 border-t border-navy-700">
      {!checked ? (
        <button className="btn-primary" onClick={onCheck}>
          ✅ Check Answers
        </button>
      ) : (
        <button className="btn-secondary" onClick={onReset}>
          🔄 Reset
        </button>
      )}

      <a
        href={api.getPdfUrl(worksheetId, false)}
        download
        className="btn-secondary inline-block"
      >
        📥 Download PDF
      </a>

      <a
        href={api.getPdfUrl(worksheetId, true)}
        download
        className="btn-secondary inline-block"
      >
        📥 Answer Key PDF
      </a>

      <button
        className="btn-secondary"
        onClick={() => window.print()}
      >
        🖨️ Print
      </button>
    </div>
  );
}
