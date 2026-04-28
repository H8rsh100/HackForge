import { useGet } from '../hooks/useApi'
import Leaderboard from '../components/Leaderboard'

export default function Dashboard() {
  const { data: hackathons } = useGet('/hackathons/')
  const { data: teams } = useGet('/teams/')
  const { data: participants } = useGet('/participants/')
  const { data: judges } = useGet('/judges/')

  const active = hackathons?.filter(h => h.status === 'ongoing') || []
  const firstActive = active[0]

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p style={{ color: 'var(--muted)', marginTop: '0.25rem', fontSize: '0.9rem' }}>
            HackForge — Unified Hackathon Engine
          </p>
        </div>
      </div>

      <div className="grid-4" style={{ marginBottom: '2rem' }}>
        {[
          { label: 'Hackathons', value: hackathons?.length ?? '—', sub: `${active.length} ongoing` },
          { label: 'Teams', value: teams?.length ?? '—', sub: 'registered' },
          { label: 'Participants', value: participants?.length ?? '—', sub: 'across all events' },
          { label: 'Judges', value: judges?.length ?? '—', sub: 'panel members' },
        ].map(s => (
          <div className="stat-card" key={s.label}>
            <div className="label">{s.label}</div>
            <div className="value" style={{ color: 'var(--accent)' }}>{s.value}</div>
            <div className="sub">{s.sub}</div>
          </div>
        ))}
      </div>

      {firstActive ? (
        <Leaderboard hackathonId={firstActive.id} />
      ) : (
        <div className="card">
          <p className="empty">No ongoing hackathons. Start one from the Hackathons page.</p>
        </div>
      )}
    </div>
  )
}