import { Link, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"

function Navbar() {
  const navigate = useNavigate()
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"))

  useEffect(() => {
    const check = () => setIsLoggedIn(!!localStorage.getItem("token"))
    window.addEventListener("storage", check)
    return () => window.removeEventListener("storage", check)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem("token")
    setIsLoggedIn(false)
    navigate("/")
  }

  return (
    <nav className="flex items-center justify-between text-white w-full">
      {/* Logo */}
      <Link to="/" className="font-black text-xl tracking-tight hover:text-blue-300 transition-colors">
        ✈️ AeroBook
      </Link>

      {/* Links */}
      <div className="flex items-center gap-6 text-sm font-semibold">
        {isLoggedIn ? (
          <>
            <Link to="/search" className="text-white/70 hover:text-white transition-colors">Flights</Link>
            <Link to="/my-bookings" className="text-white/70 hover:text-white transition-colors">My Bookings</Link>
            <button
              onClick={handleLogout}
              className="bg-white/10 hover:bg-white/20 border border-white/20 px-4 py-1.5 rounded-xl transition-all text-white/80 hover:text-white"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/" className="text-white/70 hover:text-white transition-colors">Home</Link>
            <Link to="/about" className="text-white/70 hover:text-white transition-colors">About</Link>
            <Link to="/features" className="text-white/70 hover:text-white transition-colors">Features</Link>
            <Link to="/login" className="text-white/70 hover:text-white transition-colors">Login</Link>
            <Link to="/register" className="bg-blue-600 hover:bg-blue-500 px-4 py-1.5 rounded-xl transition-all text-white shadow">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar
