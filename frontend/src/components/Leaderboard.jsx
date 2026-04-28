import { useGet } from '../hooks/useApi'

export default function Leaderboard({ hackathonId }) {
  const { data, loading } = useGet(`/analytics/leaderboard/${hackathonId}`)

  if (loading) return <p className="loading">Loading leaderboard...</p>
  if (!data?.length) return <p className="empty">No scores yet.</p>

  const medals = ['🥇', '🥈', '🥉']

  return (
    <div className="card">
      <h3 style={{ marginBottom: '1rem' }}>Live Leaderboard</h3>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Team</th>
            <th>College</th>
            <th>Score</th>
            <th>Judges</th>
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.team_id}>
              <td style={{ fontFamily: 'var(--mono)', fontWeight: 700 }}>
                {medals[row.team_rank - 1] || `#${row.team_rank}`}
              </td>
              <td style={{ fontWeight: 600 }}>{row.team_name}</td>
              <td style={{ color: 'var(--muted)' }}>{row.college}</td>
              <td style={{ fontFamily: 'var(--mono)', color: 'var(--accent)' }}>{row.weighted_score}</td>
              <td style={{ color: 'var(--muted)' }}>{row.judges_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}