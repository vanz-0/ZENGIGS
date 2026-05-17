import { PortfolioGallery } from "@/components/PortfolioGallery";

export default function PortfolioPage() {
  return (
    <div className="container mx-auto px-6 py-12">
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tighter text-foreground mb-4">
          Work <span className="text-primary">Done.</span>
        </h1>
        <p className="text-muted-foreground font-mono max-w-2xl">
          The Archive. High-fidelity case studies demonstrating technical execution, 
          problem-solving, and measurable ROI for institutional clients.
        </p>
      </div>

      <PortfolioGallery />
    </div>
  );
}
