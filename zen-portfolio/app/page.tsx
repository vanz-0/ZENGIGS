import { Nav } from "@/components/Nav";
import { MynaHero } from "@/components/MynaHero";
import { BentoGrid } from "@/components/BentoGrid";
import { CorePillars } from "@/components/CorePillars";
import { MinimalFooter } from "@/components/Footer";
import { LiveMetrics } from "@/components/LiveMetrics";
import { ClientShowcase } from "@/components/ClientShowcase";
import { Process } from "@/components/Process";

import { PaymentOptions } from "@/components/PaymentOptions";
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

      <ClientShowcase />

      <Process />

      <div id="metrics">
        <LiveMetrics />
      </div>


      <div id="payments">
        <PaymentOptions />
      </div>
      <MinimalFooter />

    </main>
  );
}
