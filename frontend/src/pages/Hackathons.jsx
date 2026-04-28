import { useState } from 'react'
import { useGet, post } from '../hooks/useApi'

export default function Hackathons() {
  const { data: hackathons, loading } = useGet('/hackathons/')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    name: '',
    theme: '',
    description: '',
    venue: '',
    mode: 'offline',
    start_date: '',
    end_date: '',
    max_teams: 50,
    prize_pool: 0,
  })

  const handleSubmit = async () => {
    await post('/hackathons/', {
      ...form,
      max_teams: Number(form.max_teams),
      prize_pool: Number(form.prize_pool),
      start_date: new Date(form.start_date).toISOString(),
      end_date: new Date(form.end_date).toISOString(),
    })
    setShowForm(false)
    window.location.reload()
  }

  const statusColor = {
    upcoming: '#f59e0b',
    ongoing: '#10b981',
    completed: '#6b7280',
  }

  return (
    <div>
      <div className="page-header">
        <h1>Hackathons</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Hackathon'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Create Hackathon</h3>
          <div className="grid-2">
            {[
              ['name', 'Name'],
              ['theme', 'Theme'],
              ['venue', 'Venue'],
            ].map(([key, label]) => (
              <div className="form-group" key={key}>
                <label>{label}</label>
                <input value={form[key]} onChange={e => setForm({ ...form, [key]: e.target.value })} />
              </div>
            ))}
            <div className="form-group">
              <label>Mode</label>
              <select value={form.mode} onChange={e => setForm({ ...form, mode: e.target.value })}>
                <option value="offline">Offline</option>
                <option value="online">Online</option>
                <option value="hybrid">Hybrid</option>
              </select>
            </div>
            <div className="form-group">
              <label>Start Date</label>
              <input type="datetime-local" value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })} />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input type="datetime-local" value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Max Teams</label>
              <input type="number" value={form.max_teams} onChange={e => setForm({ ...form, max_teams: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Prize Pool (₹)</label>
              <input type="number" value={form.prize_pool} onChange={e => setForm({ ...form, prize_pool: e.target.value })} />
            </div>
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea rows={3} value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
          </div>
          <button className="btn btn-primary" onClick={handleSubmit}>Create</button>
        </div>
      )}

      {loading ? (
        <p className="loading">Loading...</p>
      ) : (
        <div className="grid-3">
          {hackathons?.map(h => (
            <div className="card" key={h.id}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                <h3 style={{ margin: 0 }}>{h.name}</h3>
                <span style={{
                  fontSize: '0.7rem',
                  padding: '2px 8px',
                  borderRadius: '12px',
                  background: `${statusColor[h.status]}22`,
                  color: statusColor[h.status],
                  fontWeight: 700,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                }}>
                  {h.status}
                </span>
              </div>
              {h.theme && <p style={{ color: 'var(--accent)', fontSize: '0.85rem', margin: '0 0 0.5rem' }}>🎯 {h.theme}</p>}
              {h.venue && <p style={{ color: 'var(--muted)', fontSize: '0.8rem', margin: '0 0 0.5rem' }}>📍 {h.venue} · {h.mode}</p>}
              {h.description && <p style={{ color: 'var(--muted)', fontSize: '0.82rem', margin: '0 0 0.75rem', lineHeight: 1.5 }}>{h.description}</p>}
              <div style={{ display: 'flex', gap: '1rem', fontSize: '0.8rem', color: 'var(--muted)', marginTop: 'auto' }}>
                <span>👥 Max {h.max_teams} teams</span>
                {h.prize_pool > 0 && <span>🏆 ₹{Number(h.prize_pool).toLocaleString()}</span>}
              </div>
            </div>
          ))}
          {!hackathons?.length && <p className="empty">No hackathons yet. Create one!</p>}
        </div>
      )}
    </div>
  )
}
