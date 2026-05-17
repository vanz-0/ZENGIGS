import { Nav } from "@/components/Nav";
import { MynaHero } from "@/components/MynaHero";
import { BentoGrid } from "@/components/BentoGrid";
import { CorePillars } from "@/components/CorePillars";
import { MinimalFooter } from "@/components/Footer";
import { LiveMetrics } from "@/components/LiveMetrics";
import { LeadGateModal } from "@/components/LeadGateModal";

export default function Home() {
  return (
    <main className="min-h-screen bg-background relative overflow-hidden">
      {/* Navigation */}
      <Nav />
      
      <div id="hero" className="relative">
        <MynaHero />
      </div>

      <div id="services">
        <BentoGrid />
      </div>

      <div id="pillars">
        <CorePillars />
      </div>

      <div id="metrics">
        <LiveMetrics />
      </div>

      <MinimalFooter />

      {/* Global Modal Gate triggered by interactive elements */}
      <LeadGateModal />
    </main>
  );
}
