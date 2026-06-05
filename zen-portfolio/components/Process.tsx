"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, PenTool, Zap, CheckSquare, Rocket } from "lucide-react";

const steps = [
  {
    num: "01",
    title: "Audit & Analyze",
    description:
      "Book a call to analyze your core issues, identify bottlenecks, and define your exact operational needs.",
    icon: Search,
    color: "hsl(270, 95%, 65%)",
  },
  {
    num: "02",
    title: "Strategic Planning",
    description:
      "We create a detailed implementation plan, discuss the strategy with you, and agree on the deliverables.",
    icon: PenTool,
    color: "hsl(280, 90%, 60%)",
  },
  {
    num: "03",
    title: "Implementation",
    description:
      "Our team executes the agreed-upon systems — automations, sites, ads, and pipelines.",
    icon: Zap,
    color: "hsl(290, 85%, 55%)",
  },
  {
    num: "04",
    title: "Review & Feedback",
    description:
      "We check the end product together, gather your feedback, and make any final operational tweaks.",
    icon: CheckSquare,
    color: "hsl(300, 80%, 60%)",
  },
  {
    num: "05",
    title: "Delivery & Scaling",
    description:
      "Final handover of the finished product. The system runs, and we monitor for optimization.",
    icon: Rocket,
    color: "hsl(260, 95%, 65%)",
  },
];

// Positions around a circle (top-center start, clockwise)
const nodeAngles = [-90, -18, 54, 126, 198]; // degrees

function polarToXY(angleDeg: number, radius: number, cx: number, cy: number) {
  const rad = (angleDeg * Math.PI) / 180;
  return { x: cx + radius * Math.cos(rad), y: cy + radius * Math.sin(rad) };
}

export function Process() {
  const [active, setActive] = useState<number | null>(null);

  const size = 500;
  const cx = size / 2;
  const cy = size / 2;
  const orbitR = 190;
  const nodeR = 38;

  return (
    <section
      id="process"
      className="py-24 md:py-32 relative bg-background overflow-hidden border-t border-white/5"
    >
      {/* Backgrounds */}
      <div className="absolute inset-0 bg-grid-pattern opacity-10" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-primary/5 rounded-full blur-[180px]" />

      <div className="container px-4 mx-auto relative z-10">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="inline-block px-4 py-1.5 mb-6 rounded-full text-xs font-mono tracking-widest uppercase text-primary/80 glass-card">
            How We Work
          </span>
          <h2 className="text-4xl md:text-6xl font-mono font-bold tracking-tight mb-6">
            The <span className="text-gradient">System</span>
          </h2>
          <p className="text-muted-foreground font-mono text-lg">
            A circular, repeatable process — from audit to scale. Hover each
            step to learn more.
          </p>
        </div>

        {/* ===== DESKTOP: Circular Orbital ===== */}
        <div className="hidden md:flex justify-center items-center relative">
          <div style={{ width: size, height: size }} className="relative">
            {/* SVG orbit ring + traveling dot */}
            <svg
              viewBox={`0 0 ${size} ${size}`}
              className="absolute inset-0 w-full h-full"
              style={{ overflow: "visible" }}
            >
              {/* Dashed orbit ring */}
              <circle
                cx={cx}
                cy={cy}
                r={orbitR}
                fill="none"
                stroke="currentColor"
                className="text-white/[0.06]"
                strokeWidth={1.5}
                strokeDasharray="6 6"
              />

              {/* Animated glowing ring */}
              <circle
                cx={cx}
                cy={cy}
                r={orbitR}
                fill="none"
                stroke="url(#orbitGradient)"
                strokeWidth={2}
                strokeDasharray="60 1140"
                strokeLinecap="round"
                className="origin-center animate-[spin_8s_linear_infinite]"
              />

              {/* Traveling dot */}
              <g className="origin-center animate-[spin_8s_linear_infinite]">
                <circle cx={cx + orbitR} cy={cy} r={5} fill="hsl(270, 95%, 65%)" />
                <circle cx={cx + orbitR} cy={cy} r={12} fill="hsl(270, 95%, 65%)" opacity={0.2} />
              </g>

              {/* Connecting lines from center to each node */}
              {nodeAngles.map((angle, i) => {
                const pos = polarToXY(angle, orbitR, cx, cy);
                return (
                  <line
                    key={i}
                    x1={cx}
                    y1={cy}
                    x2={pos.x}
                    y2={pos.y}
                    stroke="currentColor"
                    className="text-white/[0.04]"
                    strokeWidth={1}
                  />
                );
              })}

              <defs>
                <linearGradient
                  id="orbitGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="0%"
                >
                  <stop offset="0%" stopColor="hsl(270, 95%, 65%)" stopOpacity={0.8} />
                  <stop offset="100%" stopColor="hsl(300, 80%, 60%)" stopOpacity={0.2} />
                </linearGradient>
              </defs>
            </svg>

            {/* Center hub */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-28 h-28 rounded-full bg-background border border-white/10 flex flex-col items-center justify-center z-20 shadow-[0_0_60px_hsla(270,95%,65%,0.15)]">
              <span className="text-primary font-mono font-bold text-lg">ZEN</span>
              <span className="text-muted-foreground font-mono text-[10px] uppercase tracking-widest">
                System
              </span>
            </div>

            {/* Step nodes */}
            {steps.map((step, i) => {
              const pos = polarToXY(nodeAngles[i], orbitR, cx, cy);
              const Icon = step.icon;
              const isActive = active === i;

              return (
                <div
                  key={step.num}
                  className="absolute z-30"
                  style={{
                    left: pos.x - nodeR,
                    top: pos.y - nodeR,
                    width: nodeR * 2,
                    height: nodeR * 2,
                  }}
                  onMouseEnter={() => setActive(i)}
                  onMouseLeave={() => setActive(null)}
                >
                  <motion.div
                    className="w-full h-full rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 border"
                    style={{
                      background: isActive
                        ? `linear-gradient(135deg, ${step.color}30, ${step.color}10)`
                        : "hsl(var(--background))",
                      borderColor: isActive ? step.color : "hsla(0,0%,100%,0.1)",
                      boxShadow: isActive
                        ? `0 0 30px ${step.color}40`
                        : "none",
                    }}
                    animate={{ scale: isActive ? 1.15 : 1 }}
                    transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  >
                    <Icon
                      className="w-5 h-5"
                      style={{ color: isActive ? step.color : "hsl(var(--muted-foreground))" }}
                    />
                  </motion.div>

                  {/* Step number badge */}
                  <span
                    className="absolute -top-1 -right-1 w-5 h-5 rounded-full text-[10px] font-mono font-bold flex items-center justify-center"
                    style={{
                      background: step.color,
                      color: "#000",
                    }}
                  >
                    {step.num}
                  </span>

                  {/* Tooltip */}
                  <AnimatePresence>
                    {isActive && (
                      <motion.div
                        initial={{ opacity: 0, y: 8, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 8, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                        className="absolute z-50 w-64 glass-card rounded-xl p-4 shadow-2xl pointer-events-none"
                        style={{
                          left: "50%",
                          transform: "translateX(-50%)",
                          top: nodeR * 2 + 12,
                          borderColor: `${step.color}30`,
                          borderWidth: 1,
                        }}
                      >
                        <div
                          className="text-xs font-mono font-bold uppercase tracking-wider mb-1"
                          style={{ color: step.color }}
                        >
                          Step {step.num}
                        </div>
                        <h4 className="text-foreground font-mono font-bold text-sm mb-1.5">
                          {step.title}
                        </h4>
                        <p className="text-muted-foreground font-mono text-xs leading-relaxed">
                          {step.description}
                        </p>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              );
            })}
          </div>
        </div>

        {/* ===== MOBILE: Vertical circular flow ===== */}
        <div className="md:hidden flex flex-col items-center gap-0">
          {steps.map((step, i) => {
            const Icon = step.icon;
            return (
              <React.Fragment key={step.num}>
                {/* Connecting line */}
                {i > 0 && (
                  <div className="w-px h-10 bg-gradient-to-b from-primary/30 to-primary/10" />
                )}
                <motion.div
                  initial={{ opacity: 0, x: i % 2 === 0 ? -30 : 30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, amount: 0.5 }}
                  transition={{ duration: 0.4, delay: i * 0.1 }}
                  className="w-full max-w-sm glass-card rounded-2xl p-5 gradient-border flex items-start gap-4"
                >
                  <div
                    className="shrink-0 w-12 h-12 rounded-full flex items-center justify-center border"
                    style={{
                      background: `${step.color}15`,
                      borderColor: `${step.color}40`,
                    }}
                  >
                    <Icon className="w-5 h-5" style={{ color: step.color }} />
                  </div>
                  <div className="flex-1">
                    <div
                      className="text-[10px] font-mono font-bold uppercase tracking-widest mb-1"
                      style={{ color: step.color }}
                    >
                      Step {step.num}
                    </div>
                    <h3 className="text-base font-bold font-mono text-foreground mb-1">
                      {step.title}
                    </h3>
                    <p className="text-muted-foreground font-mono text-xs leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                </motion.div>
              </React.Fragment>
            );
          })}
        </div>

        {/* CTA */}
        <div className="mt-16 flex justify-center">
          <button
            onClick={() =>
              window.dispatchEvent(new Event("open-lead-gate"))
            }
            className="px-8 py-4 bg-primary text-primary-foreground rounded-full font-mono font-bold hover:shadow-[0_0_30px_hsla(270,95%,65%,0.4)] hover:-translate-y-1 transition-all duration-300"
          >
            Start the Process — Book an Audit
          </button>
        </div>
      </div>
    </section>
  );
}
