import { BentoGrid } from "@/components/BentoGrid";

export default function ServicesPage() {
  return (
    <div className="container mx-auto px-6 py-12">
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tighter text-foreground mb-4">
          Capabilities <span className="text-primary">& Engine.</span>
        </h1>
        <p className="text-muted-foreground font-mono max-w-2xl">
          Core services and automated workflows designed to scale your operations. 
          Available via direct contract or freelance platforms.
        </p>
      </div>

      <BentoGrid />
    </div>
  );
}
