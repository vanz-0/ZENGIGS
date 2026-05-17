"use client";

import { cn } from "@/lib/utils";
import {
  Settings,
  Calendar,
  Video,
  MessageSquare,
} from "lucide-react";
import { motion } from "framer-motion";

export interface BentoItem {
  title: string;
  description: string;
  icon: React.ReactNode;
  status?: string;
  tags?: string[];
  meta?: string;
  colSpan?: number;
  hasPersistentHover?: boolean;
  gradient?: string;
}

const itemsSample: BentoItem[] = [
  {
    title: "AI & Automation",
    meta: "Make.com & Zapier",
    description:
      "JSON prompt engineering, API configuration, and chatbot training. I build systems that run while you sleep.",
    icon: <Settings className="w-5 h-5" />,
    status: "Core",
    tags: ["Automation", "AI", "Efficiency"],
    colSpan: 2,
    hasPersistentHover: true,
    gradient: "from-violet-500/20 via-purple-500/10 to-transparent",
  },
  {
    title: "Social Media Strategy",
    meta: "Multi-platform",
    description: "Content calendar creation, scheduling, and engagement management across all channels.",
    icon: <Calendar className="w-5 h-5" />,
    status: "Growth",
    tags: ["Strategy", "Content"],
    gradient: "from-blue-500/20 via-cyan-500/10 to-transparent",
  },
  {
    title: "Media Production",
    meta: "Premiere & Canva",
    description: "Short & long-form video editing, thumbnails, brand kits, and everything visual.",
    icon: <Video className="w-5 h-5" />,
    tags: ["Video", "Design"],
    colSpan: 2,
    gradient: "from-fuchsia-500/20 via-pink-500/10 to-transparent",
  },
  {
    title: "Customer Support",
    meta: "24/7 Coverage",
    description: "Email management, CRM tracking, and inbound lead qualification around the clock.",
    icon: <MessageSquare className="w-5 h-5" />,
    status: "Active",
    tags: ["Admin", "Inbox"],
    gradient: "from-emerald-500/20 via-green-500/10 to-transparent",
  },
];

interface BentoGridProps {
  items?: BentoItem[];
}

export function BentoGrid({ items = itemsSample }: BentoGridProps) {
  return (
    <div className="py-28 bg-background relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-dot-pattern opacity-30" />

      <div className="max-w-7xl mx-auto px-4 mb-16 text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <span className="inline-block px-4 py-1.5 mb-6 rounded-full text-xs font-mono tracking-widest uppercase text-primary/80 glass-card">
            What I Do
          </span>
          <h2 className="text-4xl md:text-6xl font-mono font-bold mb-5 tracking-tight">
            Core Pillars of{" "}
            <span className="text-gradient">Execution</span>
          </h2>
          <p className="text-muted-foreground font-mono text-lg max-w-xl mx-auto">
            I don&apos;t just complete tasks — I build systems that scale.
          </p>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 p-4 max-w-7xl mx-auto relative z-10">
        {items.map((item, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
            viewport={{ once: true }}
            className={cn(
              "group relative p-7 rounded-2xl overflow-hidden transition-all duration-500",
              "glass-card",
              "hover:-translate-y-2 hover:shadow-[0_20px_60px_-10px_hsla(270,95%,65%,0.15)] will-change-transform",
              item.colSpan === 2 ? "md:col-span-2" : "col-span-1",
              {
                "shadow-[0_0_40px_rgba(139,92,246,0.1)] -translate-y-1 gradient-border":
                  item.hasPersistentHover,
              }
            )}
          >
            {/* Hover gradient overlay */}
            <div
              className={cn(
                "absolute inset-0 bg-gradient-to-br transition-opacity duration-500",
                item.gradient || "from-primary/10 to-transparent",
                item.hasPersistentHover
                  ? "opacity-100"
                  : "opacity-0 group-hover:opacity-100"
              )}
            />

            {/* Content */}
            <div className="relative flex flex-col h-full justify-between space-y-5">
              <div>
                <div className="flex items-center justify-between mb-5">
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center bg-primary/10 text-primary border border-primary/20 group-hover:bg-primary/20 group-hover:scale-110 transition-all duration-300">
                    {item.icon}
                  </div>
                  <span
                    className={cn(
                      "text-[10px] font-mono font-bold px-3 py-1.5 rounded-full uppercase tracking-widest",
                      "glass-card text-primary/80",
                      "transition-all duration-300 group-hover:text-primary group-hover:bg-primary/10"
                    )}
                  >
                    {item.status || "Active"}
                  </span>
                </div>

                <div className="space-y-3">
                  <h3 className="font-mono font-bold text-xl text-foreground tracking-tight">
                    {item.title}
                    <span className="block mt-1.5 text-sm text-primary/70 font-normal">
                      {item.meta}
                    </span>
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed font-mono">
                    {item.description}
                  </p>
                </div>
              </div>

              <div className="flex items-center justify-between mt-4 pt-4 border-t border-white/[0.06]">
                <div className="flex items-center space-x-2 text-xs text-muted-foreground/70 font-mono">
                  {item.tags?.map((tag, i) => (
                    <span
                      key={i}
                      className="px-2.5 py-1 rounded-lg bg-white/[0.04] transition-all duration-300 hover:bg-primary/10 hover:text-primary"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
