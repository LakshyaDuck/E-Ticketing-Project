import Navbar from "../components/Navbar"
import Firstpageelement from "../components/HomeHero"
import bg from "../assets/frontpage.png"

const destinations = [
  { code: "NYC", name: "New York" },
  { code: "DXB", name: "Dubai" },
  { code: "TYO", name: "Tokyo" },
  { code: "PAR", name: "Paris" },
  { code: "SYD", name: "Sydney" },
  { code: "LON", name: "London" },
]

function Home() {
  return (
    <div
      className="h-screen w-screen overflow-hidden bg-cover bg-center flex items-center justify-center relative"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <style>{`
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(24px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to   { opacity: 1; }
        }
        @keyframes float1 {
          0%, 100% { transform: translateY(0px) translateX(0px); }
          33%       { transform: translateY(-18px) translateX(8px); }
          66%       { transform: translateY(10px) translateX(-6px); }
        }
        @keyframes float2 {
          0%, 100% { transform: translateY(0px) translateX(0px); }
          33%       { transform: translateY(14px) translateX(-10px); }
          66%       { transform: translateY(-8px) translateX(12px); }
        }
        @keyframes float3 {
          0%, 100% { transform: translateY(0px); }
          50%       { transform: translateY(-22px); }
        }
        @keyframes shimmer {
          0%   { background-position: -200% center; }
          100% { background-position: 200% center; }
        }
        @keyframes scanline {
          0%   { transform: translateY(-100%); }
          100% { transform: translateY(100vh); }
        }
        @keyframes orbitDot {
          from { transform: rotate(0deg) translateX(110px) rotate(0deg); }
          to   { transform: rotate(360deg) translateX(110px) rotate(-360deg); }
        }
        @keyframes pulseLine {
          0%, 100% { opacity: 0.3; }
          50%       { opacity: 0.8; }
        }
        @keyframes tagFloat {
          0%, 100% { transform: translateY(0); }
          50%       { transform: translateY(-6px); }
        }
        .shimmer-text {
          background: linear-gradient(
            120deg,
            #ffffff 0%,
            #ffffff 35%,
            #93c5fd 45%,
            #e0f2fe 55%,
            #ffffff 65%,
            #ffffff 100%
          );
          background-size: 200% auto;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          animation: shimmer 4s linear infinite;
        }
      `}</style>

      {/* ── Layered overlays ── */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/35 to-black/65" />
      <div className="absolute inset-0 bg-gradient-to-r from-blue-950/30 via-transparent to-blue-950/20" />

      {/* ── Scanline sweep ── */}
      <div
        className="absolute inset-x-0 h-32 pointer-events-none"
        style={{
          background: "linear-gradient(to bottom, transparent, rgba(96,165,250,0.03), transparent)",
          animation: "scanline 8s linear infinite",
        }}
      />

      {/* ── Floating glow orbs ── */}
      <div className="absolute w-[500px] h-[500px] rounded-full pointer-events-none"
        style={{ top: "10%", left: "5%", background: "radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%)", animation: "float1 9s ease-in-out infinite" }} />
      <div className="absolute w-[350px] h-[350px] rounded-full pointer-events-none"
        style={{ bottom: "5%", right: "8%", background: "radial-gradient(circle, rgba(96,165,250,0.10) 0%, transparent 70%)", animation: "float2 11s ease-in-out infinite" }} />
      <div className="absolute w-[200px] h-[200px] rounded-full pointer-events-none"
        style={{ top: "40%", right: "20%", background: "radial-gradient(circle, rgba(147,197,253,0.08) 0%, transparent 70%)", animation: "float3 7s ease-in-out infinite" }} />

      {/* ── Floating destination tags ── */}
      {destinations.map((d, i) => {
        const positions = [
          { top: "12%", left: "3%" },
          { top: "22%", right: "2%" },
          { bottom: "28%", left: "1%" },
          { bottom: "18%", right: "3%" },
          { top: "55%", left: "2%" },
          { top: "45%", right: "1%" },
        ]
        const delays = [0, 0.8, 1.4, 0.4, 1.8, 1.1]
        const floatAnims = ["float1", "float2", "float3", "float2", "float1", "float3"]
        const pos = positions[i]
        return (
          <div
            key={d.code}
            className="absolute hidden xl:flex items-center gap-2 px-3 py-1.5 rounded-xl border border-white/10 pointer-events-none"
            style={{
              ...pos,
              background: "rgba(255,255,255,0.04)",
              backdropFilter: "blur(8px)",
              opacity: 0,
              animation: `fadeIn 0.6s ease ${0.8 + delays[i]}s forwards, tagFloat ${5 + i}s ease-in-out ${delays[i]}s infinite`,
            }}
          >
            <div className="w-1.5 h-1.5 rounded-full bg-blue-400" style={{ animation: "pulseLine 2s ease-in-out infinite" }} />
            <span className="text-blue-300 font-black text-xs">{d.code}</span>
            <span className="text-white/40 text-xs">{d.name}</span>
          </div>
        )
      })}

      {/* ── Main card ── */}
      <div
        className="relative z-10 w-full mx-6 flex flex-col overflow-hidden"
        style={{
          maxWidth: "1100px",
          height: "min(640px, calc(100vh - 48px))",
          background: "linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.03) 100%)",
          backdropFilter: "blur(20px)",
          borderRadius: "28px",
          border: "1px solid rgba(255,255,255,0.12)",
          boxShadow: "0 0 0 1px rgba(255,255,255,0.04), 0 32px 80px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.12)",
        }}
      >
        {/* Top shimmer line */}
        <div style={{ height: "1px", background: "linear-gradient(90deg, transparent 0%, rgba(96,165,250,0.8) 40%, rgba(167,139,250,0.6) 60%, transparent 100%)" }} />

        {/* Navbar */}
        <div className="px-8 pt-5" style={{ opacity: 0, animation: "fadeUp 0.5s ease 0.05s forwards" }}>
          <Navbar />
        </div>

        {/* ── Body ── */}
        <div className="flex-1 flex min-h-0">

          {/* Left stats panel */}
          <div className="hidden lg:flex flex-col justify-between py-8 px-7 border-r"
            style={{ minWidth: "175px", borderColor: "rgba(255,255,255,0.08)" }}>

            <div className="space-y-7">
              {[
                { n: "180+", l: "Destinations" },
                { n: "50+",  l: "Airlines" },
                { n: "24/7", l: "Support" },
              ].map((s, i) => (
                <div key={s.l} style={{ opacity: 0, animation: `fadeUp 0.55s ease ${0.25 + i * 0.12}s forwards` }}>
                  <p className="font-black text-2xl leading-none"
                    style={{ background: "linear-gradient(135deg,#fff,#93c5fd)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
                    {s.n}
                  </p>
                  <p className="text-xs uppercase tracking-widest mt-1" style={{ color: "rgba(255,255,255,0.35)" }}>{s.l}</p>
                </div>
              ))}
            </div>

            {/* Animated vertical route line */}
            <div className="flex flex-col items-center gap-1" style={{ opacity: 0, animation: "fadeIn 1s ease 1s forwards" }}>
              <div className="w-1.5 h-1.5 rounded-full bg-blue-400" />
              <div className="w-px flex-1 min-h-[60px]"
                style={{ background: "linear-gradient(to bottom, rgba(96,165,250,0.8), rgba(167,139,250,0.4))", animation: "pulseLine 2.5s ease-in-out infinite" }} />
              <div className="w-1.5 h-1.5 rounded-full" style={{ background: "rgba(167,139,250,0.8)" }} />
              <p className="text-xs uppercase tracking-[0.25em] mt-2" style={{ color: "rgba(255,255,255,0.18)", writingMode: "vertical-rl", transform: "rotate(180deg)" }}>
                Fly Anywhere
              </p>
            </div>
          </div>

          {/* Main content */}
          <div className="flex-1 flex flex-col justify-between p-8 relative overflow-hidden">

            {/* Giant watermark ✈ */}
            <div className="absolute pointer-events-none select-none"
              style={{ fontSize: "280px", lineHeight: 1, right: "-20px", bottom: "-40px", color: "rgba(255,255,255,0.025)", fontWeight: 900 }}>
              ✈
            </div>

            {/* Corner orbit decoration */}
            <div className="absolute top-6 right-6 pointer-events-none" style={{ width: "60px", height: "60px" }}>
              <div className="absolute inset-0 rounded-full border border-white/8" />
              <div className="absolute inset-3 rounded-full border border-blue-400/15" />
              <div className="absolute w-2 h-2 rounded-full bg-blue-400/60"
                style={{ top: "50%", left: "50%", marginTop: "-4px", marginLeft: "-4px", animation: "orbitDot 4s linear infinite" }} />
            </div>

            {/* Hero text */}
            <div className="text-right" style={{ opacity: 0, animation: "fadeUp 0.65s ease 0.15s forwards" }}>
              <div className="flex items-center justify-end gap-3 mb-3">
                <div style={{ height: "1px", width: "40px", background: "linear-gradient(90deg, transparent, rgba(96,165,250,0.8))" }} />
                <span className="text-xs uppercase font-bold tracking-[0.2em]" style={{ color: "rgba(96,165,250,0.9)" }}>
                  Premium Flight Booking
                </span>
              </div>

              <h1 className="font-black leading-[0.95] mb-4 shimmer-text"
                style={{ fontSize: "clamp(2.4rem, 4.5vw, 3.8rem)", letterSpacing: "-0.03em" }}>
                your ticket to<br />
                explore the world
              </h1>

              <p className="text-sm leading-relaxed ml-auto max-w-xs"
                style={{ color: "rgba(255,255,255,0.5)" }}>
                Discover the world at your fingertips — hundreds of routes, real-time seats, instant confirmation.
              </p>

              {/* Trust chips */}
              <div className="flex items-center justify-end gap-2 mt-4">
                {["✓ No hidden fees", "✓ Instant tickets", "✓ 180+ routes"].map((t, i) => (
                  <span key={t}
                    className="text-xs px-2.5 py-1 rounded-full border"
                    style={{
                      color: "rgba(147,197,253,0.9)",
                      borderColor: "rgba(96,165,250,0.2)",
                      background: "rgba(59,130,246,0.08)",
                      opacity: 0,
                      animation: `fadeUp 0.4s ease ${0.5 + i * 0.1}s forwards`
                    }}>
                    {t}
                  </span>
                ))}
              </div>
            </div>

            {/* Search bar */}
            <div style={{ opacity: 0, animation: "fadeUp 0.65s ease 0.4s forwards" }}>
              <Firstpageelement />
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="px-8 py-2.5 flex items-center justify-between"
          style={{ borderTop: "1px solid rgba(255,255,255,0.06)", opacity: 0, animation: "fadeIn 0.6s ease 0.8s forwards" }}>
          <div className="flex items-center gap-5">
            {["Dubai", "Tokyo", "Paris", "New York", "Sydney"].map((city, i) => (
              <span key={city} className="text-xs"
                style={{
                  color: "rgba(255,255,255,0.25)",
                  opacity: 0,
                  animation: `fadeIn 0.4s ease ${1 + i * 0.08}s forwards`
                }}>
                {city}
              </span>
            ))}
          </div>
          <p className="text-xs" style={{ color: "rgba(255,255,255,0.18)" }}>AeroBook © 2024</p>
        </div>

        {/* Bottom shimmer line */}
        <div style={{ height: "1px", background: "linear-gradient(90deg, transparent 0%, rgba(167,139,250,0.5) 50%, transparent 100%)" }} />
      </div>
    </div>
  )
}

export default Home
