import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { AuthLayout } from '../components/AuthLayout'
import { useAuth } from '../context/AuthContext'

export function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('Password123!')
  const [error, setError] = useState('')

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      setError('')
      await login(email, password)
      navigate('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to log in.')
    }
  }

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to continue monitoring carbon, biodiversity, and site health."
      footer={
        <>
          <span>Need an account?</span>{' '}
          <Link to="/register">Create one</Link>
        </>
      }
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          <span>Email</span>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <label>
          <span>Password</span>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </label>
        {error ? <p className="form-error">{error}</p> : null}
        <button type="submit">Login</button>
      </form>
    </AuthLayout>
  )
}
