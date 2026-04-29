import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';

// Use the variables exactly as they appear in your .env.local
const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL, 
  import.meta.env.VITE_SUPABASE_ANON_KEY
);

export default function History({ refreshKey }) {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    setLoading(true);
    const { data, error } = await supabase
      .from('carbon_logs')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(5);

    if (!error) {
      setLogs(data);
    } else {
      console.error("Error fetching logs:", error.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchLogs();
  }, [refreshKey]);

  return (
    <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ddd', borderRadius: '10px' }}>
      <h3>📊 Recent History</h3>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {logs.map((log) => (
            <li key={log.id} style={{ marginBottom: '10px', padding: '10px', background: '#f9f9f9', borderRadius: '5px' }}>
              <strong>{log.consumption_value} kWh</strong> - {log.co2_emitted_kg} kg CO₂
              <br />
              <small>{new Date(log.created_at).toLocaleDateString()}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}