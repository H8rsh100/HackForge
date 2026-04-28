export default function TeamCard({ team, onClick }) {
  const statusColor = {
    registered: 'var(--muted)',
    submitted: 'var(--success)',
    winner: 'var(--warning)',
    disqualified: 'var(--danger)',
  }

  return (
    <div className="card" onClick={onClick} style={{ cursor: 'pointer', transition: 'border 0.2s' }}
      onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--accent)'}
      onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border)'}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h3 style={{ fontSize: '1rem', marginBottom: '0.25rem' }}>{team.team_name}</h3>
          <p style={{ color: 'var(--muted)', fontSize: '0.8rem' }}>{team.college}</p>
        </div>
        <span style={{ color: statusColor[team.status], fontSize: '0.75rem', fontFamily: 'var(--mono)', fontWeight: 600 }}>
          {team.status}
        </span>
      </div>
      {team.project_idea && (
        <p style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: 'var(--muted)', lineHeight: 1.5 }}>
          {team.project_idea}
        </p>
      )}
    </div>
  )
}