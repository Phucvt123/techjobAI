import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useApp } from '../context/AppContext'

/** Redirect authenticated users away from login/register pages */
export default function GuestRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  const { profile, profileReady } = useApp()

  if (loading || (isAuthenticated && !profileReady)) {
    return (
      <div className="min-h-screen bg-bg flex items-center justify-center">
        <div className="w-10 h-10 rounded-xl bg-indigo flex items-center justify-center animate-pulse">
          <span className="text-white text-sm font-black">T</span>
        </div>
      </div>
    )
  }

  if (isAuthenticated) {
    if (profile?.onboardingCompleted === false) {
      return <Navigate to="/onboarding" replace />
    }
    return <Navigate to="/dashboard" replace />
  }

  return children
}
