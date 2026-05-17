"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { createClient } from "@supabase/supabase-js";
import { cn } from "@/lib/utils";
import { ThemeToggle } from "./ThemeToggle";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";
const supabase = createClient(supabaseUrl, supabaseKey);

export function HubNav() {
  const pathname = usePathname();
  const router = useRouter();
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    // Localhost gets full access — no gate
    const isLocalhost = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    if (!isLocalhost && !document.cookie.includes("hub_unlocked=true")) {
      router.push("/");
    }

    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });
  }, [router]);

  const navItems = [
    { name: "Archive (Done)", path: "/hub/portfolio" },
    { name: "Engine (Can Do)", path: "/hub/services" },
    { name: "Live Feed (Bids)", path: "/hub/live-bids" },
    { name: "Blueprints", path: "/hub/blueprints" },
  ];

  return (
    <nav className="sticky top-0 w-full z-50 glass border-b border-white/10 px-6 py-4 flex justify-between items-center shadow-[0_4px_30px_hsla(0,0%,0%,0.3)]">
      <Link href="/hub/portfolio" className="font-mono font-bold text-xl text-foreground tracking-tighter hover:text-primary transition-colors">
        ZENGIGS<span className="text-primary">.HUB</span>
      </Link>

      <div className="hidden md:flex gap-8 font-mono text-sm">
        {navItems.map((item) => {
          const isActive = pathname === item.path;
          return (
            <Link
              key={item.name}
              href={item.path}
              className={cn(
                "transition-colors duration-300 relative group",
                isActive ? "text-primary font-bold" : "text-muted-foreground hover:text-foreground"
              )}
            >
              {item.name}
              <span 
                className={cn(
                  "absolute -bottom-1 left-0 h-[2px] bg-primary transition-all duration-300",
                  isActive ? "w-full" : "w-0 group-hover:w-full"
                )} 
              />
            </Link>
          );
        })}

        {session && (
          <Link href="/admin" className="text-primary font-bold hover:text-accent transition-colors flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
            Lead Center
          </Link>
        )}
      </div>

      <div className="flex items-center gap-4">
        <ThemeToggle />
        {session ? (
          <button
            onClick={() => supabase.auth.signOut()}
            className="text-muted-foreground/50 hover:text-foreground font-mono text-[10px] uppercase tracking-widest transition-colors"
          >
            Logout
          </button>
        ) : (
          <Link href="/login" className="text-muted-foreground/40 hover:text-muted-foreground font-mono text-[10px] uppercase tracking-widest transition-colors">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}
