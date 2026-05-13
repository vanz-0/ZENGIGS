import { MynaHero } from "@/components/MynaHero";
import { BentoGrid } from "@/components/BentoGrid";
import { Pricing } from "@/components/Pricing";
import { MinimalFooter } from "@/components/Footer";
import { LiveMetrics } from "@/components/LiveMetrics";

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 flex justify-between items-center px-6 py-4 bg-black/50 backdrop-blur-md border-b border-white/10">
        <div className="font-mono font-bold text-xl text-white tracking-tighter">ZENGIGS.</div>
        <div className="hidden md:flex gap-8 font-mono text-sm text-gray-300">
          <a href="#services" className="hover:text-primary transition-colors">Services</a>
          <a href="#pricing" className="hover:text-primary transition-colors">Pricing</a>
        </div>
        <a href="#pricing" className="px-4 py-2 bg-primary text-white rounded-full font-mono text-sm font-bold hover:bg-primary/90 transition-colors">Hire Me</a>
      </nav>

      <div id="hero">
        <MynaHero />
      </div>

      <div id="services">
        <BentoGrid />
      </div>

      <div id="metrics">
        <LiveMetrics />
      </div>

      <div id="pricing">
        <Pricing />
      </div>

      <MinimalFooter />
    </main>
  );
}
