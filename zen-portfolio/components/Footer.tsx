'use client';

import {
  InstagramIcon,
  LinkedinIcon,
  TwitterIcon,
  YoutubeIcon,
  Mail,
  Phone,
  ArrowUpRight,
} from 'lucide-react';

export function MinimalFooter() {
  const year = new Date().getFullYear();

  const socialLinks = [
    { icon: <InstagramIcon className="size-4" />, link: '#', label: 'Instagram' },
    { icon: <LinkedinIcon className="size-4" />, link: '#', label: 'LinkedIn' },
    { icon: <TwitterIcon className="size-4" />, link: '#', label: 'Twitter' },
    { icon: <YoutubeIcon className="size-4" />, link: '#', label: 'YouTube' },
  ];

  const handleScrollTo = (id: string) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <footer className="relative bg-background overflow-hidden">
      {/* Full-width CTA Banner */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/15 via-accent/10 to-primary/15" />
        <div className="absolute inset-0 bg-dot-pattern opacity-10" />
        <div className="relative max-w-6xl mx-auto py-16 px-6 flex flex-col items-center text-center gap-6">
          <h3 className="text-3xl md:text-4xl font-mono font-bold tracking-tight text-foreground">
            Ready to build your <span className="text-gradient">AI Operating System</span>?
          </h3>
          <p className="text-muted-foreground font-mono text-sm max-w-lg">
            Book a free audit call. We&apos;ll analyze your workflows, identify bottlenecks, and deliver a strategic plan.
          </p>
          <div className="flex flex-col md:flex-row gap-8 w-full max-w-4xl mx-auto mt-6">
            {/* Call Booking Options */}
            <div className="flex-1 glass p-6 rounded-2xl flex flex-col items-center gap-4 border border-white/10">
              <h4 className="font-mono font-bold text-foreground">Book a Direct Call</h4>
              <p className="text-xs text-muted-foreground font-mono">Skip the line and speak with us directly.</p>
              <div className="flex flex-col sm:flex-row gap-3 w-full">
                <a
                  href="mailto:merchzenith@gmail.com?subject=Google%20Meet%20Call%20Request"
                  className="flex-1 py-3 bg-primary/20 text-primary rounded-xl font-mono text-sm font-bold border border-primary/30 hover:bg-primary hover:text-primary-foreground transition-all flex items-center justify-center gap-2"
                >
                  <ArrowUpRight className="w-4 h-4" />
                  Google Meet
                </a>
                <a
                  href="tel:+1234567890"
                  className="flex-1 py-3 bg-white/5 text-foreground rounded-xl font-mono text-sm font-bold border border-white/10 hover:bg-white/10 transition-all flex items-center justify-center gap-2"
                >
                  <Phone className="w-4 h-4" />
                  Phone Call
                </a>
              </div>
            </div>

            {/* Email Sequence Form */}
            <div className="flex-1 glass p-6 rounded-2xl flex flex-col items-center gap-4 border border-white/10">
              <h4 className="font-mono font-bold text-foreground">Get the Free Value Sequence</h4>
              <p className="text-xs text-muted-foreground font-mono">Not ready for a call? Get our best strategies via email.</p>
              <form 
                className="w-full flex flex-col gap-2"
                onSubmit={(e) => { e.preventDefault(); alert("Brevo API integration coming soon!"); }}
              >
                <input 
                  type="email" 
                  placeholder="Enter your email" 
                  required
                  className="w-full bg-black/50 border border-white/20 rounded-xl px-4 py-3 text-sm font-mono text-foreground focus:outline-none focus:border-primary transition-colors"
                />
                <button 
                  type="submit"
                  className="w-full py-3 bg-primary text-primary-foreground rounded-xl font-mono text-sm font-bold hover:shadow-[0_0_20px_hsla(270,95%,65%,0.3)] transition-all flex items-center justify-center gap-2"
                >
                  <Mail className="w-4 h-4" />
                  Send Me the Guide
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      {/* Gradient divider */}
      <div className="h-[1px] bg-gradient-to-r from-transparent via-primary/40 to-transparent" />

      <div className="mx-auto max-w-6xl py-16 px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 md:gap-8">

          {/* Brand Column */}
          <div className="md:col-span-2 flex flex-col gap-5">
            <h2 className="text-2xl font-mono font-bold tracking-tighter text-foreground">
              ZENGIGS<span className="text-primary">.</span>
            </h2>
            <p className="text-muted-foreground/70 max-w-sm font-mono text-sm leading-relaxed">
              AI Operating System Specialists. We build unified AI infrastructure — automations, ads, web systems, and data pipelines — that work together as one system.
            </p>
            <div className="flex gap-3">
              {socialLinks.map((item, i) => (
                <a
                  key={i}
                  className="glass-card rounded-lg p-2.5 transition-all duration-300 text-muted-foreground/50 hover:text-primary hover:bg-primary/10 hover:scale-110"
                  target="_blank"
                  rel="noreferrer"
                  href={item.link}
                  aria-label={item.label}
                >
                  {item.icon}
                </a>
              ))}
            </div>
          </div>

          {/* Navigation Column */}
          <div className="flex flex-col gap-4">
            <h4 className="font-mono font-bold text-xs uppercase tracking-[0.2em] text-foreground/60 mb-1">Navigate</h4>
            <button onClick={() => handleScrollTo('services')} className="text-left text-sm font-mono text-muted-foreground/60 hover:text-primary transition-colors duration-300">Services</button>
            <button onClick={() => handleScrollTo('process')} className="text-left text-sm font-mono text-muted-foreground/60 hover:text-primary transition-colors duration-300">Process</button>
            <button onClick={() => handleScrollTo('work')} className="text-left text-sm font-mono text-muted-foreground/60 hover:text-primary transition-colors duration-300">Portfolio</button>

          </div>

          {/* Contact Column */}
          <div className="flex flex-col gap-4">
            <h4 className="font-mono font-bold text-xs uppercase tracking-[0.2em] text-foreground/60 mb-1">Contact</h4>
            <a href="mailto:hello@zengigs.com" className="text-sm font-mono text-muted-foreground/60 hover:text-primary transition-colors duration-300 flex items-center gap-2">
              <Mail className="w-3.5 h-3.5" />
              hello@zengigs.com
            </a>
            <button
              onClick={() => window.dispatchEvent(new Event('open-lead-gate'))}
              className="text-left text-sm font-mono text-muted-foreground/60 hover:text-primary transition-colors duration-300 flex items-center gap-2"
            >
              <Phone className="w-3.5 h-3.5" />
              Book a Call
            </button>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="mt-14 pt-6 border-t border-white/[0.04] flex flex-col md:flex-row justify-between items-center gap-4 text-center">
          <p className="text-muted-foreground/40 font-mono text-xs tracking-wider">
            © {year} ZENGIGS. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <span className="text-muted-foreground/25 font-mono text-[10px] tracking-[0.2em] uppercase">
              AI Operating System Specialists
            </span>
            <span className="text-muted-foreground/15 font-mono text-[10px]">|</span>
            <span className="text-muted-foreground/25 font-mono text-[10px] tracking-[0.2em] uppercase">
              Licensed & Operational
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
