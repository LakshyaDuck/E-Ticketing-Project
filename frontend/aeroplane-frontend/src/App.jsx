import { Routes, Route } from "react-router-dom"

import Home from "./pages/home"
import Login from "./pages/login"
import Register from "./pages/register"
import Search from "./pages/search.jsx";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
        <Route path="/search" element={<Search />} />
    </Routes>
  )
}

export default App