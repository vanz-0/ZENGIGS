"use client";

import React, { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { ExternalLink, Code2, ArrowRight } from "lucide-react";

interface Project {
  id: string;
  title: string;
  description: string;
  image_url: string;
  tech_stack: string[];
  live_link: string;
  results_metric: string;
}

export function PortfolioGallery() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProjects() {
      const { data, error } = await supabase
        .from("portfolio_projects")
        .select("*")
        .order("created_at", { ascending: false });

      if (error) {
        console.error("Error fetching projects:", error);
      } else {
        setProjects(data || []);
      }
      setLoading(false);
    }

    fetchProjects();
  }, []);

  if (loading) {
    return (
      <div className="w-full h-64 flex items-center justify-center">
        <div className="w-8 h-8 rounded-full border-2 border-primary border-t-transparent animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {projects.length === 0 ? (
        <div className="col-span-full py-20 text-center border border-dashed border-white/20 rounded-2xl glass-card">
          <p className="text-muted-foreground font-mono">No projects in the archive yet.</p>
        </div>
      ) : (
        projects.map((project) => (
          <div key={project.id} className="glass-card rounded-2xl overflow-hidden group border border-white/10 hover:border-primary/50 transition-colors duration-500 flex flex-col h-full">
            {/* Image Placeholder or Actual Image */}
            <div className="h-48 w-full bg-black/50 relative overflow-hidden">
              {project.image_url ? (
                <img 
                  src={project.image_url} 
                  alt={project.title} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
                />
              ) : (
                <div className="absolute inset-0 flex items-center justify-center text-muted-foreground/30">
                  <Code2 size={48} />
                </div>
              )}
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
            </div>

            {/* Content */}
            <div className="p-6 flex-grow flex flex-col">
              <h3 className="text-xl font-bold text-foreground mb-2">{project.title}</h3>
              <p className="text-sm text-muted-foreground mb-4 line-clamp-3 flex-grow">{project.description}</p>
              
              <div className="mb-6">
                <div className="flex flex-wrap gap-2">
                  {project.tech_stack && project.tech_stack.map((tech) => (
                    <span key={tech} className="text-[10px] font-mono px-2 py-1 bg-white/5 border border-white/10 rounded-md text-muted-foreground">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>

              {/* Results & Link */}
              <div className="flex items-center justify-between mt-auto pt-4 border-t border-white/10">
                <div className="text-xs font-bold text-primary max-w-[70%] truncate">
                  {project.results_metric}
                </div>
                {project.live_link && (
                  <a 
                    href={project.live_link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="p-2 rounded-full bg-white/5 hover:bg-primary text-foreground transition-colors"
                  >
                    <ExternalLink size={16} />
                  </a>
                )}
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
