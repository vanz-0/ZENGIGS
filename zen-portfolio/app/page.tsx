import { Nav } from "@/components/Nav";
import { MynaHero } from "@/components/MynaHero";
import { BentoGrid } from "@/components/BentoGrid";
import { Pricing } from "@/components/Pricing";
import { MinimalFooter } from "@/components/Footer";
import { LiveMetrics } from "@/components/LiveMetrics";

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      {/* Navigation */}
      <Nav />
      
      <div id="hero">
        <MynaHero />
      </div>
...


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
