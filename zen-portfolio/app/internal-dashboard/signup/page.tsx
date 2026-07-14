'use client';

import React, { useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { useRouter } from 'next/navigation';
import { Mail, Loader2, ArrowLeft, Sparkles } from 'lucide-react';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);
  const router = useRouter();

  async function handleMagicLink(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/internal-dashboard/admin` },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      setSent(true);
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-black flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute top-[-10%] right-[-10%] w-[50%] h-[50%] bg-emerald-500/20 blur-[120px] rounded-full" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-500/10 blur-[120px] rounded-full" />

      <div className="w-full max-w-md z-10">
        <div className="text-center mb-10">
          <div className="font-mono font-bold text-3xl text-white tracking-tighter mb-2">ZENGIGS.</div>
          <p className="text-gray-400 font-mono text-sm tracking-widest uppercase">Get Access</p>
        </div>

        {sent ? (
          <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl text-center space-y-4">
            <Sparkles className="mx-auto text-emerald-400" size={48} />
            <h2 className="text-white font-bold text-lg">Magic link sent</h2>
            <p className="text-gray-400 text-sm">
              Check <span className="text-white">{email}</span> — we sent you a one-click login link.
            </p>
            <p className="text-gray-500 text-xs">
              No password needed. Click the link and you're in.
            </p>
            <button
              onClick={() => router.push('/internal-dashboard/login')}
              className="w-full bg-white text-black font-bold py-4 rounded-2xl hover:bg-primary transition-all mt-4"
            >
              BACK TO LOGIN
            </button>
          </div>
        ) : (
          <form onSubmit={handleMagicLink} className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-xl shadow-2xl">
            <div className="space-y-6">
              <div>
                <label className="text-[10px] font-mono text-gray-500 uppercase tracking-widest block mb-2 px-1">
                  Your Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@company.com"
                    required
                    className="w-full bg-black border border-white/10 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-emerald-500 transition-all placeholder:text-gray-700"
                  />
                </div>
              </div>

              <p className="text-gray-500 text-xs text-center px-4">
                No password required. We'll email you a one-click login link.
              </p>

              {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-500 text-xs py-3 px-4 rounded-xl font-mono">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-white text-black font-bold py-4 rounded-2xl hover:bg-emerald-500 hover:text-white transition-all flex items-center justify-center gap-2"
              >
                {loading ? <Loader2 className="animate-spin" size={20} /> : 'SEND MAGIC LINK'}
              </button>
            </div>
          </form>
        )}

        <button
          onClick={() => router.push('/internal-dashboard/login')}
          className="flex items-center gap-2 mx-auto mt-6 text-gray-500 hover:text-gray-300 font-mono text-xs uppercase tracking-widest transition-colors"
        >
          <ArrowLeft size={14} /> Already have access?
        </button>
      </div>
    </main>
  );
}