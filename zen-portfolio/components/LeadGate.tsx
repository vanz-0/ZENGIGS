"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Mail, ArrowRight, Lock, CheckCircle } from "lucide-react";

export function LeadGate() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sent, setSent] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (document.cookie.includes("hub_unlocked=true")) {
      router.push("/hub");
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setLoading(true);
    setError("");

    try {
      // 1. Save to Supabase
      await supabase.from("leads").insert([
        { email, first_name: "Guide", last_name: "Lead", company: "Unknown", niche: "Free Guide", status: "new" }
      ]);

      // 2. Send free PDF guide via Brevo
      await fetch("/api/send-guide", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      // 3. Set cookie + redirect
      document.cookie = "hub_unlocked=true; path=/; max-age=" + 60 * 60 * 24 * 30;
      setSent(true);
      setTimeout(() => router.push("/hub"), 2000);
    } catch (err: any) {
      console.error("LeadGate error:", err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] relative z-20">
      <div className="glass-card max-w-md w-full p-8 rounded-2xl border border-white/10 shadow-2xl relative overflow-hidden group">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-accent/5 opacity-50"></div>

        <div className="relative z-10 flex flex-col items-center text-center">
          {sent ? (
            <div className="py-4 space-y-3">
              <CheckCircle className="mx-auto text-emerald-400" size={48} />
              <h2 className="text-2xl font-bold text-foreground">Check your inbox!</h2>
              <p className="text-muted-foreground text-sm">
                Your free <strong className="text-white">0 to 100: Selling PDFs</strong> guide is on its way to {email}.
              </p>
              <p className="text-muted-foreground text-xs">Redirecting you to the hub...</p>
            </div>
          ) : (
            <>
              <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mb-6 border border-primary/30 text-primary">
                <Lock className="w-8 h-8" />
              </div>

              <h2 className="text-2xl font-bold text-foreground mb-2">Get Your Free Guide</h2>
              <p className="text-muted-foreground mb-8 text-sm">
                Enter your email to unlock the ZENGIGS hub and get the free guide{" "}
                <strong className="text-amber-400">0 to 100: Selling PDFs</strong> — delivered straight to your inbox.
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
                    className="w-full bg-background/50 border border-border rounded-xl py-3 pl-12 pr-4 text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                  />
                </div>

                {error && <p className="text-destructive text-sm font-semibold">{error}</p>}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-primary to-accent text-white font-bold py-3 rounded-xl hover:shadow-[0_0_20px_hsla(270,95%,65%,0.4)] transition-all flex items-center justify-center gap-2 group/btn"
                >
                  {loading ? (
                    <span className="animate-pulse">Sending guide...</span>
                  ) : (
                    <>
                      Unlock & Get Free Guide
                      <ArrowRight className="w-5 h-5 group-hover/btn:translate-x-1 transition-transform" />
                    </>
                  )}
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}