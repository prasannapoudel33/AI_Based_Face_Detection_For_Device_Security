import { useEffect, useState } from 'react';
import { apiRequest } from '../api';

export default function MonitoringPage({ token }) {
  const [running, setRunning] = useState(false)
  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

  async function refresh(){ const r = await apiRequest('/api/monitor/status', { headers }); setRunning(r.running) }
  useEffect(() => { refresh() }, [])

  async function start(){ await apiRequest('/api/monitor/start', { method:'POST', headers }); refresh() }
  async function stop(){ await apiRequest('/api/monitor/stop', { method:'POST', headers }); refresh() }

  return (
    <section className="card">
      <h2>Monitoring Control</h2>
      <p>Status: <b>{running ? 'Running' : 'Stopped'}</b></p>
      <div style={{display:'flex', gap:12}}>
        <button onClick={start} disabled={running}>Start Monitoring</button>
        <button className="ghost" onClick={stop} disabled={!running}>Stop</button>
      </div>
    </section>
  )
}
