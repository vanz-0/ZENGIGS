'use client';

import React, { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { ThemeToggle } from './ThemeToggle';

export function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleScrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

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
        <button onClick={() => handleScrollTo('services')} className="hover:text-primary transition-colors duration-300 relative group">
          Services
          <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-primary transition-all duration-300 group-hover:w-full" />
        </button>
        <button onClick={() => handleScrollTo('process')} className="hover:text-primary transition-colors duration-300 relative group">
          Process
          <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-primary transition-all duration-300 group-hover:w-full" />
        </button>
        <button onClick={() => handleScrollTo('work')} className="hover:text-primary transition-colors duration-300 relative group">
          Portfolio
          <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-primary transition-all duration-300 group-hover:w-full" />
        </button>

      </div>

      <div className="flex items-center gap-4">
        <ThemeToggle />
        <button
          onClick={() => window.dispatchEvent(new Event('open-lead-gate'))}
          className="px-5 py-2.5 bg-primary text-primary-foreground rounded-full font-mono text-sm font-bold hover:shadow-[0_0_20px_hsla(270,95%,65%,0.4)] hover:scale-105 transition-all duration-300"
        >
          Book a Call
        </button>
      </div>
    </nav>
  );
}
