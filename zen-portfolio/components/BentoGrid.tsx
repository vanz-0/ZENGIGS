"use client";

import { cn } from "@/lib/utils";
import {
  CheckCircle,
  TrendingUp,
  Video,
  Settings,
  Calendar,
  MessageSquare,
} from "lucide-react";

export interface BentoItem {
  title: string;
  description: string;
  icon: React.ReactNode;
  status?: string;
  tags?: string[];
  meta?: string;
  cta?: string;
  colSpan?: number;
  hasPersistentHover?: boolean;
}

interface BentoGridProps {
  items?: BentoItem[];
}

const itemsSample: BentoItem[] = [
  {
    title: "AI & Automation",
    meta: "Make.com & Zapier",
    description:
      "JSON prompt engineering, API configuration, and chatbot training.",
    icon: <Settings className="w-4 h-4 text-primary" />,
    status: "Core",
    tags: ["Automation", "AI", "Efficiency"],
    colSpan: 2,
    hasPersistentHover: true,
  },
  {
    title: "Social Media Strategy",
    meta: "Multi-platform",
    description: "Content calendar creation, scheduling, and engagement management.",
    icon: <Calendar className="w-4 h-4 text-blue-500" />,
    status: "Growth",
    tags: ["Strategy", "Content"],
  },
  {
    title: "Media Production",
    meta: "Premiere & Canva",
    description: "Short & long-form video editing, thumbnails, and brand kits.",
    icon: <Video className="w-4 h-4 text-purple-500" />,
    tags: ["Video", "Design"],
    colSpan: 2,
  },
  {
    title: "Customer Support",
    meta: "24/7",
    description: "Email management and CRM tracking for inbound leads.",
    icon: <MessageSquare className="w-4 h-4 text-emerald-500" />,
    status: "Active",
    tags: ["Admin", "Inbox"],
  },
];

export function BentoGrid({ items = itemsSample }: BentoGridProps) {
  return (
    <div className="py-24 bg-background relative border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 mb-12 text-center">
        <h2 className="text-3xl md:text-5xl font-mono font-bold mb-4">Core Pillars of Execution</h2>
        <p className="text-muted-foreground font-mono">I don't just complete tasks; I build systems.</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 max-w-7xl mx-auto">
        {items.map((item, index) => (
          <div
            key={index}
            className={cn(
              "group relative p-6 rounded-2xl overflow-hidden transition-all duration-300",
              "border border-white/10 bg-black/40 backdrop-blur-md",
              "hover:-translate-y-1 will-change-transform",
              item.colSpan === 2 ? "md:col-span-2" : "col-span-1",
              {
                "shadow-[0_0_30px_rgba(99,102,241,0.1)] -translate-y-1":
                  item.hasPersistentHover,
              }
            )}
          >
            <div
              className={`absolute inset-0 ${
                item.hasPersistentHover
                  ? "opacity-100"
                  : "opacity-0 group-hover:opacity-100"
              } transition-opacity duration-300`}
            >
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[length:4px_4px]" />
            </div>

            <div className="relative flex flex-col h-full justify-between space-y-4">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-white/5 border border-white/10 group-hover:bg-primary/20 transition-all duration-300">
                    {item.icon}
                  </div>
                  <span
                    className={cn(
                      "text-xs font-mono font-medium px-3 py-1 rounded-full backdrop-blur-sm border border-white/10",
                      "bg-white/5 text-gray-300",
                      "transition-colors duration-300 group-hover:bg-primary/20 group-hover:text-primary"
                    )}
                  >
                    {item.status || "Active"}
                  </span>
                </div>

                <div className="space-y-2">
                  <h3 className="font-mono font-bold text-xl text-gray-100 tracking-tight">
                    {item.title}
                    <span className="block mt-1 text-sm text-primary/80 font-normal">
                      {item.meta}
                    </span>
                  </h3>
                  <p className="text-sm text-gray-400 leading-relaxed font-mono">
                    {item.description}
                  </p>
                </div>
              </div>

              <div className="flex items-center justify-between mt-4 pt-4 border-t border-white/10">
                <div className="flex items-center space-x-2 text-xs text-gray-400 font-mono">
                  {item.tags?.map((tag, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 rounded-md bg-white/5 backdrop-blur-sm transition-all duration-200 hover:bg-white/10"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div
              className={`absolute inset-0 -z-10 rounded-2xl bg-gradient-to-br from-transparent via-primary/5 to-transparent ${
                item.hasPersistentHover
                  ? "opacity-100"
                  : "opacity-0 group-hover:opacity-100"
              } transition-opacity duration-300`}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
