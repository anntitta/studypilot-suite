import React from 'react';

export default function Login({ 
  username, 
  setUsername, 
  password, 
  setPassword, 
  onLogin, 
  onNavigateToSignUp 
}) {
  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-indigo-900 via-slate-900 to-purple-950 flex flex-col justify-center items-center font-sans antialiased p-4 selection:bg-pink-500/30">
      <div className="w-full max-w-sm bg-slate-900/90 backdrop-blur-xl rounded-3xl p-8 shadow-[0_0_60px_rgba(129,140,248,0.25)] border-2 border-indigo-500/30 transition-all duration-300 hover:border-pink-500/40 transform hover:scale-[1.01]"> 
        
        <div className="text-center mb-6 relative group">
          <div className="absolute -inset-2 rounded-full bg-gradient-to-r from-pink-500 via-indigo-500 to-cyan-400 blur opacity-40 group-hover:opacity-80 transition duration-500 animate-pulse"></div>
          <img 
            className="w-24 mx-auto relative transform transition duration-500 group-hover:scale-110 group-hover:rotate-6" 
            src="https://img.icons8.com/fluent/344/year-of-tiger.png" 
            alt="StudyPilot Space Tiger"
          />
          <h2 className="mt-4 text-4xl font-black tracking-wider text-white uppercase drop-shadow-[0_2px_8px_rgba(0,0,0,0.5)]">
            StudyPilot
          </h2>
          <p className="text-xs font-black text-yellow-300 tracking-widest mt-2 uppercase drop-shadow-[0_2px_4px_rgba(0,0,0,0.8)]">
            Your Magical Learning Spaceship! 🛸
          </p>
        </div>   
        
        <form onSubmit={onLogin} className="space-y-5">
          <div>
            <label className="block mb-1.5 text-xs font-black uppercase tracking-widest text-yellow-400 drop-shadow-[0_1px_3px_rgba(0,0,0,0.8)]" htmlFor="username">
              🚀 Astronaut Name
            </label>
            <input 
              className="w-full px-4 py-3 text-slate-100 border-2 border-slate-800 rounded-2xl bg-slate-950/80 outline-none focus:border-yellow-400 focus:ring-2 focus:ring-yellow-400/20 transition-all font-bold text-sm placeholder-slate-500 shadow-inner" 
              type="text" 
              id="username"
              placeholder="What should we call you?..."
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          
          <div>
            <label className="block mb-1.5 text-xs font-black uppercase tracking-widest text-white drop-shadow-[0_1px_3px_rgba(0,0,0,0.8)]" htmlFor="password">
              🔑 Secret Launch Code
            </label>
            <input 
              className="w-full px-4 py-3 text-slate-100 border-2 border-slate-800 rounded-2xl bg-slate-950/80 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-400/20 transition-all font-mono text-sm placeholder-slate-600 shadow-inner" 
              type="password" 
              id="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button 
            className="w-full mt-4 relative group overflow-hidden bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-black text-sm tracking-widest py-4 px-4 rounded-2xl transition duration-300 shadow-xl shadow-indigo-500/30 active:scale-[0.97]" 
              type="submit"
          >
            START THE ADVENTURE! 🎮
          </button>
        </form>  
        
        <footer className="mt-6 pt-4 border-t border-slate-800 flex justify-between text-[11px] font-bold px-1">
          <a className="text-slate-300 hover:text-yellow-400 transition-colors drop-shadow" href="#forgot">Lost Password?</a>
          <button 
            type="button"
            onClick={onNavigateToSignUp} 
            className="text-slate-300 hover:text-pink-400 transition-colors drop-shadow"
          >
            New Space Cadet
          </button>
        </footer>   

      </div>
    </div>
  );
}