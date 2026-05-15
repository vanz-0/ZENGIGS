'use client';

import React, { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

export function Nav() {
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  return (
    <nav className="fixed top-0 w-full z-50 flex justify-between items-center px-6 py-4 bg-black/50 backdrop-blur-md border-b border-white/10">
      <div className="font-mono font-bold text-xl text-white tracking-tighter">ZENGIGS.</div>
      <div className="hidden md:flex gap-8 font-mono text-sm text-gray-300">
        <a href="#services" className="hover:text-primary transition-colors">Services</a>
        <a href="#pricing" className="hover:text-primary transition-colors">Pricing</a>
        
        {session && (
          <a href="/admin" className="text-primary font-bold hover:text-white transition-colors flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
            Lead Center
          </a>
        )}
      </div>
      
      <div className="flex items-center gap-4">
        {session ? (
          <button 
            onClick={() => supabase.auth.signOut()}
            className="text-gray-500 hover:text-white font-mono text-[10px] uppercase tracking-widest transition-colors"
          >
            Logout
          </button>
        ) : (
          <a href="/login" className="text-gray-700 hover:text-gray-400 font-mono text-[10px] uppercase tracking-widest transition-colors">
            Login
          </a>
        )}
        <a href="#pricing" className="px-4 py-2 bg-primary text-white rounded-full font-mono text-sm font-bold hover:bg-primary/90 transition-colors">
          Hire Me
        </a>
      </div>
    </nav>
  );
}
