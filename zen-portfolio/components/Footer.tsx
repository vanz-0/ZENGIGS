import {
  InstagramIcon,
  LinkedinIcon,
  TwitterIcon,
  YoutubeIcon,
} from 'lucide-react';

export function MinimalFooter() {
  const year = new Date().getFullYear();

  const socialLinks = [
    { icon: <InstagramIcon className="size-4" />, link: '#' },
    { icon: <LinkedinIcon className="size-4" />, link: '#' },
    { icon: <TwitterIcon className="size-4" />, link: '#' },
    { icon: <YoutubeIcon className="size-4" />, link: '#' },
  ];

  return (
    <footer className="relative bg-background overflow-hidden">
      {/* Gradient divider */}
      <div className="h-[1px] bg-gradient-to-r from-transparent via-primary/40 to-transparent" />

      <div className="mx-auto max-w-6xl py-16 px-6">
        <div className="grid md:grid-cols-2 gap-10 items-center text-center md:text-left">

          <div className="flex flex-col gap-5">
            <h2 className="text-2xl font-mono font-bold tracking-tighter text-foreground">
              ZENGIGS<span className="text-primary">.</span>
            </h2>
            <p className="text-muted-foreground/70 max-w-sm font-mono text-sm leading-relaxed">
              The tech-powered virtual assistant building systems, not just completing tasks.
            </p>
            <div className="flex gap-3 justify-center md:justify-start">
              {socialLinks.map((item, i) => (
                <a
                  key={i}
                  className="glass-card rounded-lg p-2.5 transition-all duration-300 text-muted-foreground/50 hover:text-primary hover:bg-primary/10 hover:scale-110"
                  target="_blank"
                  href={item.link}
                >
                  {item.icon}
                </a>
              ))}
            </div>
          </div>

          <div className="flex flex-col md:items-end gap-3 text-sm font-mono text-muted-foreground/60">
            <a href="#services" className="hover:text-primary transition-colors duration-300">Services</a>
            <a href="/hub/portfolio" className="hover:text-primary transition-colors duration-300">Portfolio</a>
            <a href="https://calendly.com" className="hover:text-primary transition-colors duration-300">Book a Call</a>
            <a href="mailto:contact@zengigs.com" className="hover:text-primary transition-colors duration-300 mt-1 text-primary/60">
              contact@zengigs.com
            </a>
          </div>

        </div>

        <div className="mt-14 pt-6 border-t border-white/[0.04] flex flex-col md:flex-row justify-between items-center gap-4 text-center">
          <p className="text-muted-foreground/40 font-mono text-xs tracking-wider">
            © {year} ZENGIGS. All rights reserved.
          </p>
          <p className="text-muted-foreground/25 font-mono text-[10px] tracking-[0.2em] uppercase">
            Built with precision
          </p>
        </div>
      </div>
    </footer>
  );
}
