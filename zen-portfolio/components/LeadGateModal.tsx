"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Mail, ArrowRight, Lock, X } from "lucide-react";

export function LeadGateModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  // Listen for custom event to open modal
  useEffect(() => {
    const handleOpenModal = () => setIsOpen(true);
    window.addEventListener("open-lead-gate", handleOpenModal);
    
    // Check if unlocked
    if (document.cookie.includes("hub_unlocked=true")) {
      // already unlocked, but we don't automatically redirect from the landing page
      // unless they specifically click "View Hub"
    }

    return () => window.removeEventListener("open-lead-gate", handleOpenModal);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setLoading(true);
    setError("");

    try {
      // 1. Save to Supabase Leads
      const { error: dbError } = await supabase.from("leads").insert([
        { 
          email, 
          first_name: "Portfolio", 
          last_name: "Visitor",
          company: "Unknown",
          niche: "Lead Gate",
          status: "new"
        }
      ]);

      if (dbError) throw dbError;

      // 2. Set Cookie (Expires in 30 days)
      document.cookie = "hub_unlocked=true; path=/; max-age=" + 60 * 60 * 24 * 30;

      // 3. Redirect to Hub
      router.push("/hub/portfolio");
    } catch (err: any) {
      console.error("Failed to unlock hub:", err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-background/80 backdrop-blur-md"
      onClick={(e) => {
        if (e.target === e.currentTarget) setIsOpen(false);
      }}
    >
      <div className="glass-card max-w-md w-full p-8 rounded-2xl border border-white/10 shadow-2xl relative overflow-hidden animate-fade-in-up">
        <button 
          onClick={() => setIsOpen(false)}
          className="absolute top-4 right-4 text-muted-foreground hover:text-foreground transition-colors z-20"
        >
          <X size={20} />
        </button>

        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-accent/5 opacity-50"></div>
        
        <div className="relative z-10 flex flex-col items-center text-center">
          <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mb-6 border border-primary/30 text-primary">
            <Lock className="w-8 h-8" />
          </div>
          
          <h2 className="text-2xl font-bold text-foreground mb-2">Unlock the Freelance Hub</h2>
          <p className="text-muted-foreground mb-8 text-sm">
            Enter your email to view my complete portfolio, live platform bids, and access the freelancer blueprints.
          </p>

          <form onSubmit={handleSubmit} className="w-full flex flex-col gap-4">
            <div className="relative w-full">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your best email..."
                className="w-full bg-background border border-border rounded-xl py-3 pl-12 pr-4 text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              />
            </div>
            
            {error && <p className="text-destructive text-sm font-semibold">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-primary to-accent text-white font-bold py-3 rounded-xl hover:shadow-[0_0_20px_hsla(270,95%,65%,0.4)] transition-all flex items-center justify-center gap-2 group/btn"
            >
              {loading ? (
                <span className="animate-pulse">Unlocking...</span>
              ) : (
                <>
                  Unlock Access
                  <ArrowRight className="w-5 h-5 group-hover/btn:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
