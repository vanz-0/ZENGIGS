"use client";

import React from "react";
import { motion } from "framer-motion";
import { FolderArchive, Cpu, Radio, BookOpen, ArrowRight } from "lucide-react";

const pillars = [
  {
    title: "AI Operating System Specialists",
    subtitle: "The Central Nervous System.",
    description:
      "We don't just add AI for the sake of it; we build a central nervous system for your business. By integrating intelligent agents and autonomous workflows, we automate repetitive decision-making, customer routing, and internal operations.",
    icon: Cpu,
    href: "#email-collection",
    accent: "from-violet-500/20 to-purple-600/10",
    borderAccent: "border-violet-500/30",
    features: ["Agentic Workflows", "Customer Routing", "Autonomous Ops", "AI Integration"],
    ctaText: "Audit My Workflows"
  },
  {
    title: "Ads & Social Media Experts",
    subtitle: "Data-Driven Growth.",
    description:
      "Traffic means nothing without conversion. We architect omni-channel campaigns across Google, Meta, and emerging platforms, backed by rigorous analytics and A/B testing to ensure every dollar spent drives measurable revenue.",
    icon: Radio,
    href: "#book-call",
    accent: "from-blue-500/20 to-cyan-600/10",
    borderAccent: "border-blue-500/30",
    features: ["Omni-channel Campaigns", "A/B Testing", "ROI Tracking", "Meta & Google Ads"],
    ctaText: "Get a Free Ad Audit"
  },
  {
    title: "Web & App Developers",
    subtitle: "High-Converting Infrastructure.",
    description:
      "Your digital storefront needs to be fast, secure, and intuitive. We build scalable web applications and mobile experiences using modern frameworks that not only look stunning but are engineered to convert visitors into loyal customers.",
    icon: BookOpen,
    href: "#services",
    accent: "from-emerald-500/20 to-green-600/10",
    borderAccent: "border-emerald-500/30",
    features: ["Next.js & React", "Mobile Apps", "Custom UI/UX", "Secure Architecture"],
    ctaText: "View Tech Stack"
  },
  {
    title: "Data & Catalog Managers",
    subtitle: "Pristine Data Architecture.",
    description:
      "Clean data is the foundation of scale. We handle massive data entry, catalog organization, and database structuring, ensuring your inventory, CRM, and analytics platforms are always synchronized and perfectly accurate.",
    icon: FolderArchive,
    href: "#email-collection",
    accent: "from-amber-500/20 to-orange-600/10",
    borderAccent: "border-amber-500/30",
    features: ["Data Entry", "Catalog Org", "Database Structuring", "CRM Sync"],
    ctaText: "Organize My Data"
  },
];

export function CorePillars() {
  return (
    <section className="py-24 md:py-32 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-grid-pattern opacity-30" />
      <div className="absolute top-1/3 right-0 w-[400px] h-[400px] bg-primary/8 rounded-full blur-[150px]" />
      <div className="absolute bottom-1/3 left-0 w-[300px] h-[300px] bg-accent/5 rounded-full blur-[120px]" />

      <div className="container mx-auto px-6 relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.7 }}
          className="text-center mb-20"
        >
          <span className="text-primary font-mono text-sm uppercase tracking-[0.3em] mb-4 block">
            Inside the Hub
          </span>
          <h2 className="text-4xl md:text-6xl font-bold tracking-tighter text-foreground">
            Four <span className="text-gradient">Pillars.</span>
          </h2>
          <p className="text-muted-foreground font-mono mt-4 max-w-lg mx-auto">
            Everything you need to evaluate, hire, and track — organized into one gated system.
          </p>
        </motion.div>

        {/* Zig-Zag Pillars */}
        <div className="flex flex-col gap-24 md:gap-32">
          {pillars.map((pillar, index) => {
            const isEven = index % 2 === 0;
            const Icon = pillar.icon;

            return (
              <motion.div
                key={pillar.title}
                initial={{ opacity: 0, y: 60 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.8, delay: 0.1 }}
                className={`flex flex-col ${isEven ? "md:flex-row" : "md:flex-row-reverse"} items-center gap-12 md:gap-16`}
              >
                {/* Text Side */}
                <div className="flex-1 space-y-6">
                  <div className="flex items-center gap-3">
                    <div className={`p-3 rounded-xl bg-gradient-to-br ${pillar.accent} border ${pillar.borderAccent}`}>
                      <Icon className="w-6 h-6 text-foreground" />
                    </div>
                    <span className="font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground">
                      0{index + 1}
                    </span>
                  </div>

                  <div>
                    <p className="text-primary font-mono text-sm font-bold uppercase tracking-wider mb-1">
                      {pillar.subtitle}
                    </p>
                    <h3 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
                      {pillar.title}
                    </h3>
                  </div>

                  <p className="text-muted-foreground leading-relaxed max-w-md">
                    {pillar.description}
                  </p>

                  <a
                    href={pillar.href}
                    className="inline-flex items-center gap-2 text-primary font-mono font-bold text-sm hover:gap-3 transition-all group"
                  >
                    {pillar.ctaText}
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </a>
                </div>

                {/* Frame Side */}
                <div className="flex-1 w-full max-w-md">
                  <div className={`glass-card rounded-2xl border ${pillar.borderAccent} p-8 relative overflow-hidden group hover:border-primary/40 transition-colors duration-500`}>
                    {/* Gradient overlay */}
                    <div className={`absolute inset-0 bg-gradient-to-br ${pillar.accent} opacity-40 group-hover:opacity-60 transition-opacity duration-500`} />

                    {/* Content inside frame */}
                    <div className="relative z-10">
                      <div className="flex items-center gap-2 mb-6">
                        <div className="w-3 h-3 rounded-full bg-red-500/60" />
                        <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
                        <div className="w-3 h-3 rounded-full bg-green-500/60" />
                        <span className="ml-2 font-mono text-[10px] text-muted-foreground/60 uppercase tracking-wider">
                          {pillar.title.toLowerCase()}.panel
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        {pillar.features.map((feature) => (
                          <div
                            key={feature}
                            className="flex items-center gap-2 px-3 py-2.5 bg-white/5 rounded-lg border border-white/5 hover:border-primary/20 transition-colors"
                          >
                            <span className="w-1.5 h-1.5 rounded-full bg-primary flex-shrink-0" />
                            <span className="text-xs font-mono text-foreground/80">{feature}</span>
                          </div>
                        ))}
                      </div>

                      <div className="mt-6 pt-4 border-t border-white/10 flex items-center justify-between">
                        <span className="text-[10px] font-mono text-muted-foreground/50 uppercase tracking-widest">
                          Status: Active
                        </span>
                        <span className="flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                          <span className="text-[10px] font-mono text-green-500/80">Online</span>
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
