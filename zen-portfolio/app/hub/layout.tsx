import { HubNav } from "@/components/HubNav";
import { MinimalFooter } from "@/components/Footer";

export default function HubLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <HubNav />
      <main className="flex-grow">
        {children}
      </main>
      <MinimalFooter />
    </div>
  );
}
