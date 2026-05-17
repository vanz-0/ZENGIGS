"use client";

import React, { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { FileText, BookOpen, Lock, ArrowRight } from "lucide-react";

interface Blueprint {
  id: string;
  title: string;
  category: string;
  difficulty_level: string;
}

export default function BlueprintsPage() {
  const [blueprints, setBlueprints] = useState<Blueprint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchBlueprints() {
      const { data, error } = await supabase
        .from("blueprints")
        .select("id, title, category, difficulty_level")
        .order("created_at", { ascending: false });

      if (!error && data) {
        setBlueprints(data);
      }
      setLoading(false);
    }
    fetchBlueprints();
  }, []);

  return (
    <div className="container mx-auto px-6 py-12">
      <div className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tighter text-foreground mb-4">
          The <span className="text-primary">Blueprints.</span>
        </h1>
        <p className="text-muted-foreground font-mono max-w-2xl">
          Step-by-step documentation, automation SOPs, and freelance guides.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {loading ? (
          <div className="col-span-full py-12 flex justify-center text-primary">
            <span className="animate-pulse">Loading blueprints...</span>
          </div>
        ) : blueprints.length === 0 ? (
          <div className="col-span-full py-20 text-center border border-dashed border-white/20 rounded-2xl glass-card">
            <BookOpen className="mx-auto h-12 w-12 text-muted-foreground/50 mb-4" />
            <p className="text-muted-foreground font-mono">No blueprints published yet.</p>
          </div>
        ) : (
          blueprints.map((bp) => (
            <div key={bp.id} className="glass-card p-6 rounded-2xl border border-white/10 hover:border-primary/50 transition-colors group cursor-pointer flex flex-col">
              <div className="flex justify-between items-start mb-4">
                <div className="p-3 rounded-xl bg-primary/10 text-primary">
                  <FileText size={24} />
                </div>
                <span className="text-[10px] uppercase font-mono px-2 py-1 bg-white/5 rounded text-muted-foreground">
                  {bp.difficulty_level}
                </span>
              </div>
              
              <h3 className="text-xl font-bold text-foreground mb-2 group-hover:text-primary transition-colors">{bp.title}</h3>
              
              <div className="mt-auto pt-4 flex items-center justify-between">
                <span className="text-xs font-mono text-muted-foreground">{bp.category}</span>
                <span className="text-xs text-primary flex items-center gap-1 font-bold">
                  Read <ArrowRight className="w-3 h-3 group-hover:translate-x-1 transition-transform" />
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
