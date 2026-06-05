"use client";

import React, { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { Terminal, ExternalLink, Briefcase, Mail, CheckCircle2, Clock, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface Bid {
  id: string;
  platform: string;
  job_title: string;
  status: string;
  applied_at: string;
  link: string;
}

export function LiveBidsFeed() {
  const [bids, setBids] = useState<Bid[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchBids() {
      const { data, error } = await supabase
        .from("active_bids")
        .select("*")
        .order("applied_at", { ascending: false });

      if (!error && data) {
        setBids(data);
      }
      setLoading(false);
    }
    fetchBids();
  }, []);

  const getPlatformIcon = (platform: string) => {
    switch (platform.toLowerCase()) {
      case "upwork":
        return <span className="text-green-500 font-bold bg-green-500/10 px-1 rounded border border-green-500/20">Up</span>;
      case "fiverr":
        return <span className="text-green-400 font-bold bg-green-400/10 px-1 rounded border border-green-400/20">Fi</span>;
      case "direct":
      case "cold email":
        return <Mail size={16} className="text-blue-400" />;
      default:
        return <Briefcase size={16} className="text-muted-foreground" />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "won":
      case "hired":
        return <CheckCircle2 size={16} className="text-green-500" />;
      case "rejected":
      case "closed":
        return <XCircle size={16} className="text-destructive" />;
      case "interviewing":
      case "active":
        return <span className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse"></span>;
      default: // pending, submitted
        return <Clock size={16} className="text-muted-foreground" />;
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto glass-card rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
      {/* Terminal Header */}
      <div className="bg-black/80 px-4 py-3 flex items-center justify-between border-b border-white/10">
        <div className="flex items-center gap-2">
          <Terminal size={16} className="text-primary" />
          <span className="font-mono text-xs text-muted-foreground uppercase tracking-wider">
            ZENGIGS // live_bids_feed
          </span>
        </div>
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
          <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
        </div>
      </div>

      {/* Terminal Body */}
      <div className="p-6 font-mono text-sm max-h-[600px] overflow-y-auto custom-scrollbar">
        {loading ? (
          <div className="flex items-center gap-2 text-primary">
            <span className="animate-pulse">Loading active bids...</span>
          </div>
        ) : bids.length === 0 ? (
          <div className="text-muted-foreground">
             &gt; No active bids found in the database.
          </div>
        ) : (
          <div className="space-y-4">
            {bids.map((bid, i) => (
              <div 
                key={bid.id} 
                className={cn(
                  "flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded bg-white/5 border border-white/5 hover:border-primary/30 transition-colors gap-4",
                  i === 0 && "border-l-2 border-l-primary"
                )}
              >
                <div className="flex items-center gap-4 overflow-hidden">
                  <div className="flex-shrink-0 w-8 flex justify-center">
                    {getPlatformIcon(bid.platform)}
                  </div>
                  <div className="min-w-0">
                    <p className="text-foreground font-bold truncate pr-4">{bid.job_title}</p>
                    <div className="flex items-center gap-3 text-xs text-muted-foreground mt-1">
                      <span>{new Date(bid.applied_at).toLocaleDateString()}</span>
                      <span className="uppercase text-primary/80">{bid.platform}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between sm:justify-end gap-6 flex-shrink-0">
                  <div className="flex items-center gap-2 px-2 py-1 bg-black/40 rounded border border-white/5">
                    {getStatusIcon(bid.status)}
                    <span className="text-xs uppercase">{bid.status}</span>
                  </div>
                  
                  {bid.link ? (
                    <a href={bid.link} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-primary transition-colors">
                      <ExternalLink size={16} />
                    </a>
                  ) : (
                    <div className="w-4"></div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
