import { useState } from 'react'
import { useGet, post } from '../hooks/useApi'
import TeamCard from '../components/TeamCard'

export default function Teams() {
  const { data: teams, loading } = useGet('/teams/')
  const { data: hackathons } = useGet('/hackathons/')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ hackathon_id: '', team_name: '', college: '', project_idea: '' })

  const handleSubmit = async () => {
    await post('/teams/', { ...form, hackathon_id: Number(form.hackathon_id) })
    setShowForm(false)
    window.location.reload()
  }

  return (
    <div>
      <div className="page-header">
        <h1>Teams</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Register Team'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Register Team</h3>
          <div className="form-group">
            <label>Hackathon</label>
            <select value={form.hackathon_id} onChange={e => setForm({ ...form, hackathon_id: e.target.value })}>
              <option value="">Select hackathon</option>
              {hackathons?.map(h => <option key={h.id} value={h.id}>{h.name}</option>)}
            </select>
          </div>
          {[['team_name', 'Team Name'], ['college', 'College']].map(([key, label]) => (
            <div className="form-group" key={key}>
              <label>{label}</label>
              <input value={form[key]} onChange={e => setForm({ ...form, [key]: e.target.value })} />
            </div>
          ))}
          <div className="form-group">
            <label>Project Idea</label>
            <textarea rows={3} value={form.project_idea} onChange={e => setForm({ ...form, project_idea: e.target.value })} />
          </div>
          <button className="btn btn-primary" onClick={handleSubmit}>Register</button>
        </div>
      )}

      {loading ? <p className="loading">Loading...</p> : (
        <div className="grid-3">
          {teams?.map(t => <TeamCard key={t.id} team={t} />)}
        </div>
      )}
    </div>
  )
}