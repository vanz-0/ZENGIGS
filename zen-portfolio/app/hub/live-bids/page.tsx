import { LiveBidsFeed } from "@/components/LiveBidsFeed";

export default function LiveBidsPage() {
  return (
    <div className="container mx-auto px-6 py-12">
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tighter text-foreground mb-4">
          Active <span className="text-primary">Pipeline.</span>
        </h1>
        <p className="text-muted-foreground font-mono max-w-2xl">
          Live feed of my current freelance proposals, outreach, and applications across platforms like Upwork and Fiverr.
        </p>
      </div>

      <LiveBidsFeed />
    </div>
  );
}
