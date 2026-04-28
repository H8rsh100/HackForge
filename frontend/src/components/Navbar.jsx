import { Link, useLocation } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/hackathons', label: 'Hackathons' },
  { to: '/teams', label: 'Teams' },
  { to: '/analytics', label: 'Analytics' },
]

export default function Navbar() {
  const { pathname } = useLocation()
  return (
    <nav style={{
      background: 'var(--surface)',
      borderBottom: '1px solid var(--border)',
      padding: '0 2rem',
      display: 'flex',
      alignItems: 'center',
      gap: '2rem',
      height: '60px',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      <span style={{ fontWeight: 700, fontSize: '1.1rem', fontFamily: 'var(--mono)', color: 'var(--accent)' }}>
        ⚡ HackForge
      </span>
      <div style={{ display: 'flex', gap: '0.25rem', flex: 1 }}>
        {links.map(l => (
          <Link key={l.to} to={l.to} style={{
            padding: '0.4rem 1rem',
            borderRadius: '6px',
            textDecoration: 'none',
            fontSize: '0.875rem',
            fontWeight: 500,
            color: pathname === l.to ? 'var(--accent)' : 'var(--muted)',
            background: pathname === l.to ? 'rgba(124,111,255,0.1)' : 'transparent',
            transition: 'all 0.15s',
          }}>{l.label}</Link>
        ))}
      </div>
    </nav>
  )
}