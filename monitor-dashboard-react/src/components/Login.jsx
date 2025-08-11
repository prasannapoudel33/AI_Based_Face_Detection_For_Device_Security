import { useState } from 'react'
import { login } from '../api'

export default function Login({ onLogin }) {
  const [u, setU] = useState('admin')        // prefill if you like
  const [p, setP] = useState('letmein123!')
  const [msg, setMsg] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setMsg('')
    setLoading(true)
    try {
      const res = await login(u, p)
      onLogin(res.access_token)
    } catch {
      setMsg('Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-wrap">
      <div className="login-ring">
        <section className="login-card" role="dialog" aria-labelledby="login-title">
          <h1 id="login-title" className="login-title">Login</h1>

          <form onSubmit={submit} className="login-form">
            <input
              className="login-input"
              placeholder="Email or Username"
              autoComplete="username"
              value={u}
              onChange={e => setU(e.target.value)}
            />
            <input
              className="login-input"
              type="password"
              placeholder="Password"
              autoComplete="current-password"
              value={p}
              onChange={e => setP(e.target.value)}
            />
            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? 'Signing in…' : 'Login'}
            </button>
            {msg && <p className="login-msg" role="alert">{msg}</p>}
          </form>
        </section>
      </div>
    </div>
  )
}

