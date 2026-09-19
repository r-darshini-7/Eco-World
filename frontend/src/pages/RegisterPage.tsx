import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { AuthLayout } from '../components/AuthLayout'
import { useAuth } from '../context/AuthContext'

export function RegisterPage() {
  const navigate = useNavigate()
  const { register } = useAuth()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      setError('')
      await register(email, password, fullName)
      navigate('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to register.')
    }
  }

  return (
    <AuthLayout
      title="Create account"
      subtitle="Register a new admin account for project oversight and environmental monitoring."
      footer={
        <>
          <span>Already registered?</span>{' '}
          <Link to="/login">Sign in</Link>
        </>
      }
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          <span>Full name</span>
          <input value={fullName} onChange={(event) => setFullName(event.target.value)} required />
        </label>
        <label>
          <span>Email</span>
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        </label>
        <label>
          <span>Password</span>
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
        </label>
        {error ? <p className="form-error">{error}</p> : null}
        <button type="submit">Register</button>
      </form>
    </AuthLayout>
  )
}
