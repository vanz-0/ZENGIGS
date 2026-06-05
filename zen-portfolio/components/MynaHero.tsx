"use client";

import * as React from "react";
import {
  Zap,
  Globe,
  Megaphone,
  Database,
  ArrowRight,
  Play
} from "lucide-react";
import { motion, useAnimation, useInView, AnimatePresence } from "framer-motion";
import { InteractiveHoverButton } from "./InteractiveHoverButton";
import { VideoModal } from "./VideoModal";

const roles = [
  "AI Operating System Specialists",
  "Ads & Social Media Experts",
  "Web & App Developers",
  "Data & Catalog Managers",
];

const labels = [
  { icon: Zap, label: "AI & Automations" },
  { icon: Megaphone, label: "Ads & Social Media" },
  { icon: Globe, label: "Web & App Dev" },
  { icon: Database, label: "Data & Catalogs" },
];

export function MynaHero() {
  const controls = useAnimation();
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, amount: 0.1 });
  const [isVideoModalOpen, setIsVideoModalOpen] = React.useState(false);
  const [roleIndex, setRoleIndex] = React.useState(0);

  React.useEffect(() => {
    if (isInView) {
      controls.start("visible");
    }
  }, [controls, isInView]);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setRoleIndex((prev) => (prev + 1) % roles.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const titleWords = [
    "YOUR",
    "AI",
    "OPERATING",
    "SYSTEM",
  ];

  const handleScrollToPortfolio = () => {
    const el = document.getElementById("services");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div ref={ref} className="w-full relative bg-background overflow-hidden min-h-screen flex items-center">
      {/* Animated Grid Pattern */}
      <div className="absolute inset-0 bg-grid-pattern animate-grid-fade" />

      {/* Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-primary/15 rounded-full blur-[150px] animate-float" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-accent/10 rounded-full blur-[120px] animate-float" style={{ animationDelay: '3s' }} />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/8 rounded-full blur-[180px]" />

      <main className="w-full">
        <section className="container py-28 md:py-32 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-8 items-center">

            {/* Left Column: Text & CTAs */}
            <div className="flex flex-col items-start text-left">
              {/* Badge */}
              <motion.div
                initial={{ opacity: 0, y: 20, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6 }}
                className="inline-flex items-center gap-2 px-5 py-2 mb-8 rounded-full glass gradient-border min-w-[300px]"
              >
                <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse shrink-0" />
                <div className="relative h-5 overflow-hidden w-full flex items-center">
                  <AnimatePresence mode="popLayout">
                    <motion.span
                      key={roleIndex}
                      initial={{ y: 20, opacity: 0 }}
                      animate={{ y: 0, opacity: 1 }}
                      exit={{ y: -20, opacity: 0 }}
                      transition={{ duration: 0.5, ease: "easeInOut" }}
                      className="text-sm font-mono text-foreground/80 absolute whitespace-nowrap"
                    >
                      {roles[roleIndex]}
                    </motion.span>
                  </AnimatePresence>
                </div>
              </motion.div>

              {/* Title */}
              <motion.h1
                initial={{ filter: "blur(10px)", opacity: 0, y: 30 }}
                animate={{ filter: "blur(0px)", opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="relative font-mono text-5xl font-bold md:text-7xl xl:text-8xl leading-[1.1] tracking-tighter"
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
                    className={`block ${index === 2 ? 'text-gradient' : ''}`}
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
                className="mt-8 max-w-xl text-lg md:text-xl text-muted-foreground/90 font-mono leading-relaxed"
              >
                We build unified digital infrastructure. From AI automations and high-converting web apps, to targeted ads and rigorous data management — everything operates as one cohesive system.
              </motion.p>

              {/* Feature Pills */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.2, duration: 0.6 }}
                className="mt-10 flex flex-wrap gap-4"
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
                    className="flex items-center gap-2.5 px-4 py-2 rounded-full glass-card hover:bg-white/[0.08] transition-all duration-300 cursor-default group"
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
                className="mt-12 flex flex-col sm:flex-row items-center gap-6 w-full sm:w-auto"
              >
                <div className="animate-pulse-glow rounded-full w-full sm:w-auto">
                  <a href="#book-call" className="block">
                    <InteractiveHoverButton text="Book a Strategy Call" />
                  </a>
                </div>
                <button
                  onClick={handleScrollToPortfolio}
                  className="px-6 py-3 rounded-full font-mono font-semibold border border-white/20 hover:bg-white/5 hover:border-primary/50 text-foreground transition-all flex items-center justify-center gap-2 group w-full sm:w-auto"
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
                className="mt-14 flex flex-wrap items-center gap-4 text-muted-foreground/40 font-mono text-xs uppercase tracking-[0.2em]"
              >
                <span>Trusted by 50+ founders</span>
                <span className="w-1 h-1 rounded-full bg-muted-foreground/30 hidden sm:block" />
                <span>SOC 2 Compliant</span>
                <span className="w-1 h-1 rounded-full bg-muted-foreground/30 hidden sm:block" />
                <span>NDA Protected</span>
              </motion.div>
            </div>

            {/* Right Column: Video Player */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95, x: 20 }}
              animate={{ opacity: 1, scale: 1, x: 0 }}
              transition={{ delay: 1.0, duration: 0.8, type: "spring", stiffness: 50 }}
              className="relative w-full aspect-[9/16] md:aspect-video lg:aspect-[4/5] rounded-3xl overflow-hidden glass gradient-border group"
            >
              {/* Video Overlay / Play Button Indicator */}
              <div 
                className="absolute inset-0 bg-black/10 hover:bg-black/30 transition-colors duration-500 z-10 flex items-center justify-center cursor-pointer group/play"
                onClick={() => setIsVideoModalOpen(true)}
              >
                 <div className="w-16 h-16 rounded-full bg-primary/80 flex items-center justify-center backdrop-blur-sm shadow-lg scale-90 group-hover/play:scale-110 transition-transform">
                   <Play className="w-6 h-6 text-white ml-1" />
                 </div>
              </div>
              
              <video 
                src="/hero-video.mp4" 
                autoPlay 
                loop 
                muted 
                playsInline
                className="absolute inset-0 w-full h-full object-cover"
              >
                Your browser does not support the video tag.
              </video>

              {/* Decorative elements around video */}
              <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-primary/20 blur-2xl rounded-full z-0" />
              <div className="absolute -top-4 -left-4 w-32 h-32 bg-accent/20 blur-2xl rounded-full z-0" />
            </motion.div>

          </div>
        </section>
      </main>

      <VideoModal 
        isOpen={isVideoModalOpen} 
        onClose={() => setIsVideoModalOpen(false)} 
        videoSrc="/hero-video.mp4" 
      />
    </div>
  );
}
