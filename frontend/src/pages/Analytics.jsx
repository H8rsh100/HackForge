import { useState } from 'react'
import { useGet } from '../hooks/useApi'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import Leaderboard from '../components/Leaderboard'

export default function Analytics() {
  const { data: hackathons } = useGet('/hackathons/')
  const [selectedId, setSelectedId] = useState(1)
  const { data: colleges } = useGet(`/analytics/colleges/${selectedId}`)
  const { data: summary } = useGet(`/analytics/summary/${selectedId}`)
  const s = summary?.[0]

  return (
    <div>
      <div className="page-header">
        <h1>Analytics</h1>
        <select
          value={selectedId}
          onChange={e => setSelectedId(Number(e.target.value))}
          style={{ width: 'auto' }}
        >
          {hackathons?.map(h => <option key={h.id} value={h.id}>{h.name}</option>)}
        </select>
      </div>

      {s && (
        <div className="grid-4" style={{ marginBottom: '2rem' }}>
          {[
            { label: 'Teams', value: s.total_teams },
            { label: 'Participants', value: s.total_participants },
            { label: 'Submissions', value: s.total_submissions },
            { label: 'Prize Pool', value: `₹${s.prize_pool}` },
          ].map(stat => (
            <div className="stat-card" key={stat.label}>
              <div className="label">{stat.label}</div>
              <div className="value" style={{ color: 'var(--accent)', fontSize: '1.5rem' }}>{stat.value}</div>
            </div>
          ))}
        </div>
      )}

      <div className="grid-2" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>College Breakdown</h3>
          {colleges?.length ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={colleges}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="college" tick={{ fill: 'var(--muted)', fontSize: 11 }} />
                <YAxis tick={{ fill: 'var(--muted)', fontSize: 11 }} />
                <Tooltip contentStyle={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8 }} />
                <Bar dataKey="avg_score" fill="var(--accent)" radius={[4, 4, 0, 0]} name="Avg Score" />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="empty">No data yet</p>}
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>Participation by College</h3>
          {colleges?.length ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={colleges}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="college" tick={{ fill: 'var(--muted)', fontSize: 11 }} />
                <YAxis tick={{ fill: 'var(--muted)', fontSize: 11 }} />
                <Tooltip contentStyle={{ background: 'var(--surface2)', border: '1px solid var(--border)', borderRadius: 8 }} />
                <Bar dataKey="total_participants" fill="var(--accent2)" radius={[4, 4, 0, 0]} name="Participants" />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="empty">No data yet</p>}
        </div>
      </div>

      <Leaderboard hackathonId={selectedId} />
    </div>
  )
}