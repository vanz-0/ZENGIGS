"use client";

import * as React from "react";
import {
  Activity,
  Zap,
  BarChart,
  Shield,
  ArrowRight
} from "lucide-react";
import { motion, useAnimation, useInView } from "framer-motion";
import { InteractiveHoverButton } from "./InteractiveHoverButton";

const labels = [
  { icon: Zap, label: "Workflow Automation" },
  { icon: BarChart, label: "Analytics & Strategy" },
  { icon: Activity, label: "24/7 Availability" },
  { icon: Shield, label: "Enterprise Security" },
];

export function MynaHero() {
  const controls = useAnimation();
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.1 });

  React.useEffect(() => {
    if (isInView) {
      controls.start("visible");
    }
  }, [controls, isInView]);

  const titleWords = [
    "TECH-POWERED",
    "VIRTUAL",
    "ASSISTANT",
  ];

  return (
    <div ref={ref} className="w-full relative bg-background overflow-hidden">
      {/* Animated Grid Pattern */}
      <div className="absolute inset-0 bg-grid-pattern animate-grid-fade" />

      {/* Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-primary/15 rounded-full blur-[150px] animate-float" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-accent/10 rounded-full blur-[120px] animate-float" style={{ animationDelay: '3s' }} />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/8 rounded-full blur-[180px]" />

      <main>
        <section className="container py-28 md:py-40 relative z-10">
          <div className="flex flex-col items-center text-center">

            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-5 py-2 mb-10 rounded-full glass gradient-border"
            >
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
              <span className="text-sm font-mono text-foreground/80">
                Scale Your Operations • Stop Doing $15/hr Tasks
              </span>
            </motion.div>

            {/* Title */}
            <motion.h1
              initial={{ filter: "blur(10px)", opacity: 0, y: 50 }}
              animate={{ filter: "blur(0px)", opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="relative font-mono text-5xl font-bold md:text-8xl max-w-5xl mx-auto leading-[1.1] tracking-tighter"
            >
              {titleWords.map((text, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    delay: 0.1 + index * 0.15,
                    duration: 0.7,
                    type: "spring",
                    stiffness: 80,
                  }}
                  className={`inline-block mx-2 md:mx-4 ${index === 2 ? 'text-gradient' : ''}`}
                >
                  {text}
                </motion.span>
              ))}
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.6 }}
              className="mx-auto mt-8 max-w-2xl text-lg md:text-xl text-muted-foreground/90 font-mono leading-relaxed"
            >
              Busy founders lose 20+ hours a week to content, admin, and tech setup.
              I eliminate that bottleneck so you can focus on growth.
            </motion.p>

            {/* Feature Pills */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.2, duration: 0.6 }}
              className="mt-12 flex flex-wrap justify-center gap-4"
            >
              {labels.map((feature, index) => (
                <motion.div
                  key={feature.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    delay: 1.2 + (index * 0.12),
                    duration: 0.6,
                    type: "spring",
                    stiffness: 100,
                    damping: 10
                  }}
                  className="flex items-center gap-2.5 px-5 py-2.5 rounded-full glass-card hover:bg-white/[0.08] transition-all duration-300 cursor-default group"
                >
                  <feature.icon className="h-4 w-4 text-primary group-hover:text-accent transition-colors duration-300" />
                  <span className="text-sm font-mono text-foreground/70 group-hover:text-foreground/90 transition-colors duration-300">{feature.label}</span>
                </motion.div>
              ))}
            </motion.div>

            {/* CTA */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: 1.8,
                duration: 0.6,
                type: "spring",
                stiffness: 100,
                damping: 10
              }}
              className="mt-14 flex flex-col sm:flex-row items-center justify-center gap-6"
            >
              <div className="animate-pulse-glow rounded-full">
                <InteractiveHoverButton text="Book a Call" />
              </div>
              <button
                onClick={() => window.dispatchEvent(new Event('open-lead-gate'))}
                className="px-6 py-3 rounded-full font-mono font-semibold border border-white/20 hover:bg-white/5 hover:border-primary/50 text-foreground transition-all flex items-center gap-2 group"
              >
                View Full Portfolio
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform text-primary" />
              </button>
            </motion.div>

            {/* Trust bar */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 2.2, duration: 0.8 }}
              className="mt-16 flex items-center gap-6 text-muted-foreground/40 font-mono text-xs uppercase tracking-[0.2em]"
            >
              <span>Trusted by 50+ founders</span>
              <span className="w-1 h-1 rounded-full bg-muted-foreground/30" />
              <span>SOC 2 Compliant</span>
              <span className="w-1 h-1 rounded-full bg-muted-foreground/30" />
              <span>NDA Protected</span>
            </motion.div>
          </div>
        </section>
      </main>
    </div>
  );
}
