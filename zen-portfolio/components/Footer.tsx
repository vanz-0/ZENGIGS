import {
  GithubIcon,
  InstagramIcon,
  LinkedinIcon,
  TwitterIcon,
  YoutubeIcon,
} from 'lucide-react';

export function MinimalFooter() {
  const year = new Date().getFullYear();

  const socialLinks = [
    {
      icon: <InstagramIcon className="size-4" />,
      link: '#',
    },
    {
      icon: <LinkedinIcon className="size-4" />,
      link: '#',
    },
    {
      icon: <TwitterIcon className="size-4" />,
      link: '#',
    },
    {
      icon: <YoutubeIcon className="size-4" />,
      link: '#',
    },
  ];
  
  return (
    <footer className="relative bg-background overflow-hidden border-t border-white/10">
      <div className="bg-[radial-gradient(35%_80%_at_50%_0%,rgba(99,102,241,0.1),transparent)] mx-auto max-w-5xl py-12 px-4">
        <div className="grid md:grid-cols-2 gap-8 items-center text-center md:text-left">
          
          <div className="flex flex-col gap-4">
            <h2 className="text-2xl font-mono font-bold tracking-tight text-white">ZENGIGS.</h2>
            <p className="text-muted-foreground max-w-sm font-mono text-sm">
              The tech-powered virtual assistant building systems, not just completing tasks.
            </p>
            <div className="flex gap-4 justify-center md:justify-start">
              {socialLinks.map((item, i) => (
                <a
                  key={i}
                  className="hover:bg-white/10 rounded-md border border-white/10 p-2 transition-colors text-gray-400 hover:text-white"
                  target="_blank"
                  href={item.link}
                >
                  {item.icon}
                </a>
              ))}
            </div>
          </div>
          
          <div className="flex flex-col md:items-end gap-2 text-sm font-mono text-muted-foreground">
            <a href="#services" className="hover:text-primary transition-colors">Services</a>
            <a href="#pricing" className="hover:text-primary transition-colors">Pricing</a>
            <a href="https://calendly.com" className="hover:text-primary transition-colors">Book a Call</a>
            <a href="mailto:contact@zengigs.com" className="hover:text-primary transition-colors mt-2">contact@zengigs.com</a>
          </div>

        </div>
        
        <div className="mt-12 pt-6 border-t border-white/10 text-center">
          <p className="text-muted-foreground font-mono text-sm">
            © {year} ZENGIGS. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
