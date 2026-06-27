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
import Image from "next/image";
import { InteractiveHoverButton } from "./InteractiveHoverButton";

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
  const [roleIndex, setRoleIndex] = React.useState(0);

  const [activeSlide, setActiveSlide] = React.useState(0);
  const slides = [
    {
      title: "YOUR AI OPERATING SYSTEM",
      subtitle: "We build unified digital infrastructure. From AI automations and high-converting web apps, to targeted ads and rigorous data management.",
      imageSrc: "/hero-thumbnail.jpg",
      highlight: "Founder Overview"
    },
    {
      title: "COMPLEX AUTOMATIONS MADE SIMPLE",
      subtitle: "Connect disparate systems with n8n to save hundreds of hours of manual work every week.",
      imageSrc: "/media__1780287107773.png",
      highlight: "n8n Workflows"
    },
    {
      title: "DATA-DRIVEN GROWTH",
      subtitle: "Highlighting ROI tracking across Google Ads, Meta Ads, and blended analytics for precise scaling.",
      imageSrc: "/media__1780287265332.png",
      highlight: "Ads & Analytics"
    },
    {
      title: "PRISTINE DATA MANAGEMENT",
      subtitle: "Showcasing accuracy and organization for large datasets, CRMs, and catalog restructuring.",
      imageSrc: "/media__1780287355326.png",
      highlight: "Data Entry"
    },
    {
      title: "HIGH-CONVERTING INFRASTRUCTURE",
      subtitle: "Building the custom web and mobile applications your business runs on.",
      imageSrc: "/media__1780287419000.png",
      highlight: "Web Development"
    }
  ];

  const currentSlide = slides[activeSlide];

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

  const handleScrollToPortfolio = () => {
    const el = document.getElementById("services");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  const nextSlide = () => setActiveSlide((prev) => (prev + 1) % slides.length);
  const prevSlide = () => setActiveSlide((prev) => (prev - 1 + slides.length) % slides.length);

  return (
    <div ref={ref} className="w-full relative bg-background overflow-hidden min-h-screen flex items-center">
      {/* Animated Grid Pattern */}
      <div className="absolute inset-0 bg-grid-pattern animate-grid-fade" />

      {/* Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-primary/15 rounded-full blur-[150px] animate-float" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-accent/10 rounded-full blur-[120px] animate-float" style={{ animationDelay: '3s' }} />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/8 rounded-full blur-[180px]" />

      <main className="w-full">
        <section className="container py-24 md:py-32 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-8 items-center">

            {/* Left Column: Text & CTAs */}
            <div className="flex flex-col items-center lg:items-start text-center lg:text-left justify-center px-4 lg:pl-10 xl:pl-16">
              
              {/* Badge (H3) */}
              <motion.h3
                initial={{ opacity: 0, y: 20, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.6 }}
                className="inline-flex items-center justify-center lg:justify-start gap-2 px-5 py-2 mb-8 rounded-full glass gradient-border min-w-[300px]"
              >
                <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse shrink-0" />
                <div className="relative h-5 overflow-hidden w-full flex items-center">
                  <span className="text-sm font-mono text-primary font-bold">
                    {currentSlide.highlight}
                  </span>
                </div>
              </motion.h3>

              {/* Title (H1) */}
              <motion.h1
                key={`title-${activeSlide}`}
                initial={{ filter: "blur(10px)", opacity: 0, y: 30 }}
                animate={{ filter: "blur(0px)", opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="relative font-mono text-4xl font-bold md:text-5xl xl:text-6xl leading-[1.1] tracking-tighter uppercase"
              >
                {currentSlide.title}
              </motion.h1>

              {/* Subtitle (H2) */}
              <motion.h2
                key={`subtitle-${activeSlide}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="mt-6 max-w-xl text-lg md:text-xl text-muted-foreground/90 font-mono leading-relaxed"
              >
                {currentSlide.subtitle}
              </motion.h2>

              {/* Slide Navigation Dots */}
              <div className="mt-8 flex items-center gap-2">
                {slides.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setActiveSlide(i)}
                    className={`h-2 rounded-full transition-all duration-300 ${i === activeSlide ? 'w-8 bg-primary' : 'w-2 bg-white/20'}`}
                    aria-label={`Go to slide ${i + 1}`}
                  />
                ))}
              </div>

              {/* Feature Pills */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.6 }}
                className="mt-10 flex flex-wrap justify-center lg:justify-start gap-4"
              >
                {labels.map((feature, index) => (
                  <motion.div
                    key={feature.label}
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
                transition={{ delay: 0.7, duration: 0.6 }}
                className="mt-12 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-6 w-full sm:w-auto"
              >
                <div className="animate-pulse-glow rounded-full w-full sm:w-auto">
                  <a href="#contact" className="block">
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
            </div>

            {/* Right Column: Video Player */}
            <motion.div
              key={`image-${activeSlide}`}
              initial={{ opacity: 0, scale: 0.95, x: 20 }}
              animate={{ opacity: 1, scale: 1, x: 0 }}
              transition={{ duration: 0.5, type: "spring", stiffness: 50 }}
              className="relative w-full max-w-[450px] mx-auto aspect-[9/16] md:aspect-[3/4] lg:aspect-[4/5] rounded-3xl overflow-hidden glass gradient-border group mt-12 lg:mt-0"
            >
              
              <Image 
                src={currentSlide.imageSrc} 
                alt={currentSlide.title}
                fill
                priority
                className="absolute inset-0 w-full h-full object-cover"
              />

              {/* Carousel Arrows */}
              <div className="absolute inset-y-0 left-4 right-4 flex items-center justify-between z-20 pointer-events-none">
                <button onClick={(e) => { e.stopPropagation(); prevSlide(); }} className="w-10 h-10 rounded-full bg-black/50 backdrop-blur-md border border-white/20 flex items-center justify-center pointer-events-auto hover:bg-primary/50 transition-colors">
                  <span className="text-white text-xl leading-none">&lsaquo;</span>
                </button>
                <button onClick={(e) => { e.stopPropagation(); nextSlide(); }} className="w-10 h-10 rounded-full bg-black/50 backdrop-blur-md border border-white/20 flex items-center justify-center pointer-events-auto hover:bg-primary/50 transition-colors">
                  <span className="text-white text-xl leading-none">&rsaquo;</span>
                </button>
              </div>

              {/* Decorative elements around image */}
              <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-primary/20 blur-2xl rounded-full z-0 pointer-events-none" />
              <div className="absolute -top-4 -left-4 w-32 h-32 bg-accent/20 blur-2xl rounded-full z-0 pointer-events-none" />
            </motion.div>

          </div>
        </section>
      </main>
    </div>
  );
}
