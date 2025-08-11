import { useEffect, useMemo, useState } from 'react'
import { apiRequest, getActivity, getStats, wsUrl } from '../api'
import ActivityChart from '../components/charts/ActivityChart'
import BarHourly from '../components/charts/BarHourly'
import DonutEvents from '../components/charts/DonutEvents'
import StatCard from '../components/kpi/StatCard'

export default function DashboardPage({ token }) {
  const [stats, setStats] = useState({ total: 0, prasanna: 0, random: 0, last_ts: null })
  const [items, setItems] = useState([])
  const [running, setRunning] = useState(false)
  const auth = { headers: { Authorization: `Bearer ${token}` } }

  // initial data
  useEffect(() => {
    (async () => {
      setStats(await getStats(token))
      const { items } = await getActivity(token, 600)
      setItems(items)
      try {
        const r = await apiRequest('/api/monitor/status', auth)
        setRunning(!!r.running)
      } catch {}
    })()
  }, [token])

  // live socket
  useEffect(() => {
    const ws = new WebSocket(wsUrl())
    ws.onopen = () => ws.send('ping')
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data)
      if (d.type === 'event') {
        setItems(prev => [{ ...d, _id: crypto.randomUUID() }, ...prev])
        setStats(s => ({
          ...s,
          total: s.total + 1,
          prasanna: s.prasanna + (d.user === 'prasanna' ? 1 : 0),
          random: s.random + (d.user === 'random' ? 1 : 0),
          last_ts: d.ts
        }))
      }
    }
    return () => ws.close()
  }, [])

  // compute derived metrics/buckets
  const derived = useMemo(() => {
    let p = 0, r = 0, off = 0
    const hourly = {}
    for (const it of items) {
      // event mix
      if (it.event === 'screen_off') off += 1
      if (it.user === 'prasanna' && it.event === 'recognized') p += 1
      if (it.user === 'random'   && it.event === 'recognized') r += 1
      // hourly bucket
      const h = new Date(it.ts).toISOString().slice(0,13)+':00'
      hourly[h] = hourly[h] || { prasanna: 0, random: 0 }
      if (it.user === 'prasanna') hourly[h].prasanna++
      if (it.user === 'random')   hourly[h].random++
    }
    const last = items[0]?.ts ? new Date(items[0].ts).toLocaleString() : '—'
    const last24 = items.filter(it => (Date.now() - new Date(it.ts).getTime()) < 24*3600*1000).length
    return { p, r, off, hourly, last, last24 }
  }, [items])

  return (
    <>
      {/* KPI strip */}
      <div className="kpi-grid">
        <StatCard label="Total Events" value={stats.total} hint={`Last 24h: ${derived.last24}`} />
        <StatCard label="Prasanna Recognized" value={derived.p} />
        <StatCard label="Random Recognized" value={derived.r} />
        <StatCard label="Screen Off" value={derived.off} />
      </div>

      {/* big middle row: line + side panel */}
      <div className="panel-grid">
        <section className="card">
          <div className="panel-title">Activity Trend</div>
          <ActivityChart bucket={derived.hourly} />
        </section>

        <section className="card side">
          <div className="side-title">System</div>
          <div className="side-item">
            <span>Status</span>
            <b className={running ? 'ok' : 'warn'}>{running ? 'Monitoring' : 'Stopped'}</b>
          </div>
          <div className="side-item">
            <span>Last Event</span>
            <b>{derived.last}</b>
          </div>
          <div className="side-item">
            <span>Prasanna / Random</span>
            <b>{derived.p} / {derived.r}</b>
          </div>
          <div className="side-item">
            <span>Total in DB</span>
            <b>{stats.total}</b>
          </div>
        </section>
      </div>

      {/* bottom row: donut + bar */}
      <div className="mini-grid">
        <section className="card">
          <div className="panel-title">Event Mix</div>
          <DonutEvents counts={{ prasanna: derived.p, random: derived.r, screenOff: derived.off }} />
        </section>
        <section className="card">
          <div className="panel-title">Hourly Load (last 12)</div>
          <BarHourly bucket={derived.hourly} />
        </section>
      </div>
    </>
  )
}
