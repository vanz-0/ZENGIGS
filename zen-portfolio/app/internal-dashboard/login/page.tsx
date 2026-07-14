'use client';

import React, { useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { useRouter } from 'next/navigation';
import { Lock, Mail, Loader2, UserPlus, Sparkles } from 'lucide-react';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [magicSent, setMagicSent] = useState(false);
  const router = useRouter();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      router.push('/internal-dashboard/admin');
    }
  }

  async function handleMagicLink() {
    if (!email) { setError('Enter your email first'); return; }
    setLoading(true);
    setError(null);
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/internal-dashboard/admin` },
    });
    if (error) { setError(error.message); setLoading(false); }
    else { setMagicSent(true); setLoading(false); }
  }

  return (
    <main className="min-h-screen bg-black flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute top-[-10%] right-[-10%] w-[50%] h-[50%] bg-primary/20 blur-[120px] rounded-full" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-500/10 blur-[120px] rounded-full" />

      <div className="w-full max-w-md z-10">
        <div className="text-center mb-10">
          <div className="font-mono font-bold text-3xl text-white tracking-tighter mb-2">ZENGIGS.</div>
          <p className="text-gray-400 font-mono text-sm tracking-widest uppercase">Admin Gateway</p>
        </div>

        {magicSent ? (
          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl text-center space-y-4">
            <Sparkles className="mx-auto text-emerald-400" size={40} />
            <h2 className="text-white font-bold text-lg">Magic link sent</h2>
            <p className="text-gray-400 text-sm">Check <span className="text-white">{email}</span></p>
            <p className="text-gray-500 text-xs">Click the link in the email — no password needed.</p>
          </div>
        ) : (
          <form onSubmit={handleLogin} className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl shadow-2xl">
            <div className="space-y-6">
              <div>
                <label className="text-[10px] font-mono text-gray-500 uppercase tracking-widest block mb-2 px-1">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="admin@zengigs.com"
                    required
                    className="w-full bg-black border border-white/10 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-primary transition-all placeholder:text-gray-700"
                  />
                </div>
              </div>

              <div>
                <label className="text-[10px] font-mono text-gray-500 uppercase tracking-widest block mb-2 px-1">Access Key</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full bg-black border border-white/10 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-primary transition-all placeholder:text-gray-700"
                  />
                </div>
              </div>

              {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-500 text-xs py-3 px-4 rounded-xl font-mono">{error}</div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-white text-black font-bold py-4 rounded-2xl hover:bg-primary hover:text-white transition-all flex items-center justify-center gap-2"
              >
                {loading ? <Loader2 className="animate-spin" size={20} /> : 'UNLOCK DASHBOARD'}
              </button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/10" /></div>
                <div className="relative flex justify-center text-xs"><span className="bg-black px-4 text-gray-600 font-mono uppercase">or</span></div>
              </div>

              <button
                type="button"
                disabled={loading}
                onClick={handleMagicLink}
                className="w-full border border-white/10 text-gray-300 font-medium py-4 rounded-2xl hover:bg-white/5 hover:border-emerald-500/50 transition-all flex items-center justify-center gap-2"
              >
                <Sparkles size={18} /> Send Magic Link Instead
              </button>
            </div>
          </form>
        )}

        <a
          href="/internal-dashboard/signup"
          className="flex items-center justify-center gap-1 mt-6 text-gray-500 hover:text-gray-300 font-mono text-xs uppercase tracking-widest transition-colors"
        >
          <UserPlus size={14} /> Get Access
        </a>
        <p className="text-center mt-4 text-gray-700 font-mono text-[10px] uppercase tracking-[0.2em]">
          Authorized Personnel Only
        </p>
      </div>
    </main>
  );
}