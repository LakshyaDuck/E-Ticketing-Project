import { useEffect, useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import bg from "../assets/frontpage.png"

function Search() {
  const [flights, setFlights] = useState([])
  const [loading, setLoading] = useState(true)
  const [params, setParams] = useSearchParams()
  const navigate = useNavigate()

  const [searchState, setSearchState] = useState({
    fromText: "", fromId: params.get("source_airport_id") || "",
    toText: "", toId: params.get("destination_airport_id") || "",
    date: params.get("date") || ""
  })

  const [suggestions, setSuggestions] = useState({ from: [], to: [] })
  const [activeField, setActiveField] = useState(null)

  const fetchAirports = async (query, field) => {
    if (query.length < 2) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/airports/search?q=${query}`)
      const data = await res.json()
      setSuggestions(prev => ({ ...prev, [field]: data }))
    } catch (err) { console.error(err) }
  }

  useEffect(() => {
    const loadFlights = async () => {
      setLoading(true)
      const sId = params.get("source_airport_id")
      const dId = params.get("destination_airport_id")
      const date = params.get("date")

      let url = `http://localhost:8000/api/v1/flights/search`
      if (sId && dId && date) {
        url += `?source_airport_id=${sId}&destination_airport_id=${dId}&date=${date}`
      }

      try {
        const res = await fetch(url)
        const data = await res.json()
        setFlights(Array.isArray(data) ? data : [])
      } catch (err) { console.error(err) }
      finally { setLoading(false) }
    }
    loadFlights()
  }, [params])

  const handleSearchTrigger = () => {
    setParams({
      source_airport_id: searchState.fromId,
      destination_airport_id: searchState.toId,
      date: searchState.date
    })
  }

  return (
    <div
      className="min-h-screen bg-cover bg-center bg-fixed flex justify-center p-4 relative"
      style={{ backgroundImage: `url(${bg})` }}
    >
      {/* 1. DARK OVERLAY: This makes white text readable regardless of the image */}
      <div className="absolute inset-0 bg-black/40 pointer-events-none" />

      <div className="w-full max-w-6xl mt-10 bg-black/20 backdrop-blur-2xl border border-white/20 rounded-[40px] shadow-2xl p-6 md:p-10 flex flex-col h-fit relative z-10">

        {/* Navigation */}
        <div className="flex flex-col md:flex-row gap-6 items-center mb-10">
          <button
            onClick={() => navigate("/")}
            className="text-white hover:text-blue-300 flex items-center gap-2 font-bold drop-shadow-md transition-colors"
          >
            <span className="text-2xl">←</span> Home
          </button>

          {/* Functional Search Bar */}
          <div className="flex-1 w-full bg-black/40 backdrop-blur-3xl border border-white/20 rounded-3xl p-2 flex flex-wrap md:flex-nowrap items-center gap-2 relative shadow-inner">

            {/* Field Template */}
            {[
              { label: 'From', key: 'fromText', field: 'from', placeholder: 'Origin...' },
              { label: 'To', key: 'toText', field: 'to', placeholder: 'Destination...' }
            ].map((input) => (
              <div key={input.label} className="flex-1 min-w-[180px] px-4 py-2 border-r border-white/10 relative">
                <label className="text-[11px] uppercase text-blue-300 font-black tracking-widest drop-shadow-sm">
                  {input.label}
                </label>
                <input
                  type="text"
                  value={searchState[input.key]}
                  onChange={(e) => {
                    setSearchState({...searchState, [input.key]: e.target.value})
                    fetchAirports(e.target.value, input.field)
                    setActiveField(input.field)
                  }}
                  placeholder={input.placeholder}
                  className="bg-transparent text-white w-full outline-none placeholder:text-white/40 font-semibold text-lg"
                />
                {activeField === input.field && suggestions[input.field].length > 0 && (
                  <div className="absolute top-full left-0 w-full bg-slate-900 border border-white/20 z-50 rounded-2xl mt-2 shadow-2xl overflow-hidden">
                    {suggestions[input.field].map(a => (
                      <div key={a.id} onClick={() => {
                        setSearchState({...searchState, [input.key]: `${a.city} (${a.code})`, [input.field + 'Id']: a.id})
                        setSuggestions({from: [], to: []})
                      }} className="p-4 hover:bg-blue-600 cursor-pointer text-white border-b border-white/5 transition-colors">
                        <p className="font-bold">{a.city}</p>
                        <p className="text-xs opacity-70">{a.name}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}

            <div className="flex-1 min-w-[150px] px-4 py-2">
              <label className="text-[11px] uppercase text-blue-300 font-black tracking-widest">Date</label>
              <input
                type="date" value={searchState.date}
                onChange={(e) => setSearchState({...searchState, date: e.target.value})}
                className="bg-transparent text-white w-full outline-none font-semibold text-lg [color-scheme:dark]"
              />
            </div>

            <button onClick={handleSearchTrigger} className="bg-blue-600 hover:bg-blue-500 p-4 rounded-2xl shadow-lg shadow-blue-900/50 transition-all active:scale-90">
              <span className="text-xl">🔍</span>
            </button>
          </div>
        </div>

        {/* Results Section */}
        <div className="flex justify-between items-end mb-8 border-b border-white/20 pb-4">
          <h2 className="text-white text-4xl font-black tracking-tight drop-shadow-lg">
            {params.get("source_airport_id") ? "Search Results" : "Available Flights"}
          </h2>
          <span className="text-blue-300 font-mono font-bold bg-blue-900/30 px-3 py-1 rounded-lg">
            {flights.length} TOTAL
          </span>
        </div>

        <div className="space-y-4 max-h-[55vh] overflow-y-auto pr-2 custom-scrollbar">
          {loading ? (
             <div className="text-white text-center py-20 animate-pulse text-xl font-bold">Scanning Airspace...</div>
          ) : flights.length > 0 ? (
            flights.map((f) => (
              <div key={f.flight_id} className="bg-black/40 hover:bg-black/60 border border-white/10 rounded-3xl p-6 text-white grid grid-cols-1 md:grid-cols-5 gap-4 items-center transition-all group shadow-xl">
                <div className="md:col-span-1">
                  <p className="text-blue-400 font-black text-xs uppercase tracking-widest mb-1">{f.airline}</p>
                  <p className="text-xl font-bold text-white drop-shadow-md">#{f.flight_id}</p>
                </div>

                <div className="md:col-span-2 flex items-center justify-between px-4">
                  <div className="text-center">
                    <p className="text-2xl font-black">{new Date(f.departure_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                    <p className="text-xs text-white/60 font-bold uppercase">Takeoff</p>
                  </div>
                  <div className="flex-1 border-t-2 border-dashed border-white/20 relative mx-6 h-[1px]">
                    <span className="absolute -top-3 left-1/2 -translate-x-1/2 text-xl drop-shadow-[0_0_8px_rgba(255,255,255,0.8)]">✈️</span>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-black">{new Date(f.arrival_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                    <p className="text-xs text-white/60 font-bold uppercase">Landing</p>
                  </div>
                </div>

                <div className="text-center md:text-right">
                  <p className="text-3xl font-black text-white drop-shadow-md">₹{f.price}</p>
                  <p className={`text-xs font-bold ${f.seats_available < 10 ? 'text-red-400' : 'text-green-400'}`}>
                    {f.seats_available} seats left
                  </p>
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={() => navigate(`/booking/${f.flight_id}`)}
                    className="w-full md:w-auto bg-blue-600 text-white font-black px-10 py-4 rounded-2xl hover:bg-blue-500 transition-all shadow-lg active:scale-95 uppercase tracking-widest"
                  >
                    Select
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-20 bg-black/20 rounded-3xl border border-dashed border-white/20">
               <p className="text-white font-bold text-xl drop-shadow-md">No flights currently in the air.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Search