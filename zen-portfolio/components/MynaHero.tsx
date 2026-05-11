"use client";

import * as React from "react";
import {
  Activity,
  ArrowRight,
  BarChart,
  Zap,
} from "lucide-react";
import { motion, useAnimation, useInView } from "framer-motion";
import { InteractiveHoverButton } from "./InteractiveHoverButton";

const labels = [
  { icon: Zap, label: "Workflow Automation" },
  { icon: BarChart, label: "Analytics & Strategy" },
  { icon: Activity, label: "24/7 Availability" },
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
    <div className="w-full relative bg-background border-b border-white/10">
      <main>
        <section className="container py-24 md:py-32 relative z-10">
          <div className="flex flex-col items-center text-center">
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="inline-block px-4 py-1 mb-8 rounded-full border border-primary/30 bg-primary/10 text-primary font-mono text-sm"
            >
              Scale Your Operations • Stop Doing $15/hr Tasks
            </motion.div>

            <motion.h1
              initial={{ filter: "blur(10px)", opacity: 0, y: 50 }}
              animate={{ filter: "blur(0px)", opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="relative font-mono text-4xl font-bold md:text-7xl max-w-5xl mx-auto leading-tight tracking-tighter"
            >
              {titleWords.map((text, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ 
                    delay: index * 0.15, 
                    duration: 0.6 
                  }}
                  className={`inline-block mx-2 md:mx-4 ${index === 2 ? 'bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent' : ''}`}
                >
                  {text}
                </motion.span>
              ))}
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.6 }}
              className="mx-auto mt-8 max-w-2xl text-lg md:text-xl text-muted-foreground font-mono"
            >
              Busy founders lose 20+ hours a week to content, admin, and tech setup. I eliminate that bottleneck so you can focus on growth.
            </motion.p>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.2, duration: 0.6 }}
              className="mt-12 flex flex-wrap justify-center gap-6"
            >
              {labels.map((feature, index) => (
                <motion.div
                  key={feature.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ 
                    delay: 1.2 + (index * 0.15), 
                    duration: 0.6,
                    type: "spring",
                    stiffness: 100,
                    damping: 10
                  }}
                  className="flex items-center gap-2 px-6 py-2 rounded-full border border-white/5 bg-white/5 backdrop-blur-sm"
                >
                  <feature.icon className="h-4 w-4 text-primary" />
                  <span className="text-sm font-mono text-foreground/80">{feature.label}</span>
                </motion.div>
              ))}
            </motion.div>

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
              className="mt-12 flex items-center justify-center gap-4"
            >
              <InteractiveHoverButton text="Book a Call" />
            </motion.div>
          </div>
        </section>

        {/* Ambient Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] -z-10 opacity-50" />
      </main>
    </div>
  );
}
