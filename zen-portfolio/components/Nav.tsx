'use client';

import React, { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { cn } from '@/lib/utils';
import { ThemeToggle } from './ThemeToggle';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

export function Nav() {
  const [session, setSession] = useState<any>(null);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={cn(
      "fixed top-0 w-full z-50 flex justify-between items-center px-6 transition-all duration-500",
      scrolled
        ? "py-3 glass shadow-[0_4px_30px_hsla(0,0%,0%,0.3)]"
        : "py-5 bg-transparent"
    )}>
      <a href="#hero" className="font-mono font-bold text-xl text-foreground tracking-tighter hover:text-primary transition-colors">
        ZENGIGS<span className="text-primary">.</span>
      </a>

      <div className="hidden md:flex gap-8 font-mono text-sm text-muted-foreground">
        <a href="#services" className="hover:text-primary transition-colors duration-300 relative group">
          Services
          <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-primary transition-all duration-300 group-hover:w-full" />
        </a>
        <a href="#metrics" className="hover:text-primary transition-colors duration-300 relative group">
          Metrics
          <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-primary transition-all duration-300 group-hover:w-full" />
        </a>
        {session && (
          <a href="/admin" className="text-primary font-bold hover:text-accent transition-colors flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
            Lead Center
          </a>
        )}
      </div>

      <div className="flex items-center gap-4">
        <ThemeToggle />
        {session ? (
          <button
            onClick={() => supabase.auth.signOut()}
            className="text-muted-foreground/50 hover:text-foreground font-mono text-[10px] uppercase tracking-widest transition-colors"
          >
            Logout
          </button>
        ) : (
          <a href="/login" className="text-muted-foreground/40 hover:text-muted-foreground font-mono text-[10px] uppercase tracking-widest transition-colors">
            Login
          </a>
        )}
        <button
          onClick={() => window.dispatchEvent(new Event('open-lead-gate'))}
          className="px-5 py-2.5 bg-primary text-primary-foreground rounded-full font-mono text-sm font-bold hover:shadow-[0_0_20px_hsla(270,95%,65%,0.4)] hover:scale-105 transition-all duration-300"
        >
          Hire Me
        </button>
      </div>
    </nav>
  );
}
