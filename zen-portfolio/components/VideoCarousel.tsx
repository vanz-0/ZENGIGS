"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Volume2,
  VolumeX,
  ChevronLeft,
  ChevronRight,
  ArrowRight,
  Zap,
} from "lucide-react";
import { videos, categoryColors, type VideoCategory } from "@/lib/videoData";

const SLIDE_DURATION = 35; // seconds before auto-advance

export function VideoCarousel() {
  const [activeIndex, setActiveIndex] = React.useState(0);
  const [isMuted, setIsMuted] = React.useState(true);
  const [progress, setProgress] = React.useState(0);
  const [direction, setDirection] = React.useState<1 | -1>(1);

  const videoRef = React.useRef<HTMLVideoElement>(null);
  const autoAdvanceRef = React.useRef<ReturnType<typeof setTimeout>>();
  const progressRef = React.useRef<ReturnType<typeof setInterval>>();
  const startTimeRef = React.useRef<number>(Date.now());

  const goTo = React.useCallback(
    (index: number, dir: 1 | -1) => {
      const next = ((index % videos.length) + videos.length) % videos.length;
      setDirection(dir);
      setActiveIndex(next);
      setProgress(0);
      startTimeRef.current = Date.now();
    },
    []
  );

  const goNext = React.useCallback(() => goTo(activeIndex + 1, 1), [activeIndex, goTo]);
  const goPrev = React.useCallback(() => goTo(activeIndex - 1, -1), [activeIndex, goTo]);

  // Auto-advance timer
  React.useEffect(() => {
    clearTimeout(autoAdvanceRef.current);
    autoAdvanceRef.current = setTimeout(goNext, SLIDE_DURATION * 1000);
    return () => clearTimeout(autoAdvanceRef.current);
  }, [activeIndex, goNext]);

  // Progress bar
  React.useEffect(() => {
    clearInterval(progressRef.current);
    startTimeRef.current = Date.now();
    progressRef.current = setInterval(() => {
      const elapsed = (Date.now() - startTimeRef.current) / 1000;
      setProgress(Math.min((elapsed / SLIDE_DURATION) * 100, 100));
    }, 80);
    return () => clearInterval(progressRef.current);
  }, [activeIndex]);

  // Sync mute to video element
  React.useEffect(() => {
    if (videoRef.current) {
      videoRef.current.muted = isMuted;
      if (!isMuted) videoRef.current.play().catch(() => {});
    }
  }, [isMuted, activeIndex]);

  // Keyboard navigation
  React.useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") goPrev();
      if (e.key === "ArrowRight") goNext();
      if (e.key === "m") setIsMuted((v) => !v);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [goNext, goPrev]);

  const current = videos[activeIndex];
  const prevIndex = ((activeIndex - 1) + videos.length) % videos.length;
  const nextIndex = (activeIndex + 1) % videos.length;

  const slideVariants = {
    enter: (dir: number) => ({ x: dir > 0 ? 80 : -80, opacity: 0, scale: 0.95 }),
    center: { x: 0, opacity: 1, scale: 1 },
    exit: (dir: number) => ({ x: dir > 0 ? -80 : 80, opacity: 0, scale: 0.95 }),
  };

  const textVariants = {
    enter: { y: 16, opacity: 0 },
    center: { y: 0, opacity: 1 },
    exit: { y: -16, opacity: 0 },
  };

  const badgeColor = categoryColors[current.category as VideoCategory] ?? "bg-white/10 text-white/60 border-white/20";

  return (
    <section
      id="video-showcase"
      className="py-24 md:py-32 relative bg-background border-t border-white/5 overflow-hidden"
    >
      {/* Ambient glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[900px] h-[900px] bg-primary/5 rounded-full blur-[220px] pointer-events-none" />
      <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-accent/5 rounded-full blur-[150px] pointer-events-none" />

      <div className="container px-4 mx-auto">
        {/* ── Section Header ─────────────────────────────────── */}
        <div className="text-center mb-16 max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass gradient-border text-xs font-mono text-primary mb-6"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
            26 Real Business Problems — Solved Live
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-3xl md:text-5xl font-mono font-bold tracking-tighter mb-6"
          >
            Watch the Problem.{" "}
            <span className="text-gradient">Get the Fix. Free.</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-muted-foreground font-mono text-base md:text-lg"
          >
            Each clip is a real scenario we solve for clients. Find your problem,
            claim a free solution — no strings attached.
          </motion.p>
        </div>

        {/* ── Carousel ───────────────────────────────────────── */}
        <div className="flex items-center justify-center gap-3 md:gap-6">
          {/* Prev arrow */}
          <button
            id="carousel-prev"
            onClick={goPrev}
            aria-label="Previous video"
            className="shrink-0 w-10 h-10 md:w-12 md:h-12 rounded-full glass-card border border-white/10 flex items-center justify-center hover:bg-primary/20 hover:border-primary/40 transition-all duration-300 group z-10"
          >
            <ChevronLeft className="w-5 h-5 text-foreground/60 group-hover:text-primary transition-colors" />
          </button>

          {/* ── Video cards ──────────────────────────────────── */}
          <div className="flex items-center gap-3 md:gap-4">
            {/* Left peek card */}
            <motion.div
              key={`prev-${prevIndex}`}
              className="hidden lg:block relative w-40 xl:w-48 rounded-2xl overflow-hidden cursor-pointer shrink-0"
              style={{ aspectRatio: "9/16" }}
              onClick={goPrev}
              whileHover={{ scale: 1.03 }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
              <div className="absolute inset-0 bg-black/50 z-10 hover:bg-black/30 transition-colors" />
              <video
                src={`/videos/${videos[prevIndex].id}.mp4`}
                muted
                loop
                playsInline
                className="w-full h-full object-cover"
              />
              {/* Category badge */}
              <div className="absolute top-3 left-3 z-20">
                <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded-full border backdrop-blur-sm ${categoryColors[videos[prevIndex].category as VideoCategory]}`}>
                  {videos[prevIndex].category}
                </span>
              </div>
            </motion.div>

            {/* ── Active Card ───────────────────────────────── */}
            <div className="relative flex flex-col items-center">
              <AnimatePresence mode="wait" custom={direction}>
                <motion.div
                  key={activeIndex}
                  custom={direction}
                  variants={slideVariants}
                  initial="enter"
                  animate="center"
                  exit="exit"
                  transition={{ type: "spring", stiffness: 260, damping: 28 }}
                  className="relative w-64 sm:w-72 md:w-80 rounded-3xl overflow-hidden glass gradient-border shadow-2xl shadow-primary/10"
                  style={{ aspectRatio: "9/16" }}
                >
                  {/* Video */}
                  <video
                    ref={videoRef}
                    key={`video-${activeIndex}`}
                    src={`/videos/${current.id}.mp4`}
                    autoPlay
                    loop
                    muted={isMuted}
                    playsInline
                    className="absolute inset-0 w-full h-full object-cover"
                  />

                  {/* Top gradient */}
                  <div className="absolute top-0 left-0 right-0 h-28 bg-gradient-to-b from-black/70 to-transparent z-10" />

                  {/* Bottom gradient */}
                  <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black/90 via-black/40 to-transparent z-10" />

                  {/* Category badge */}
                  <div className="absolute top-4 left-4 z-20">
                    <span className={`text-[10px] font-mono font-bold px-2.5 py-1 rounded-full border backdrop-blur-sm ${badgeColor}`}>
                      {current.category}
                    </span>
                  </div>

                  {/* Mute button */}
                  <div className="absolute top-4 right-4 z-20 flex items-center gap-2">
                    <button
                      id="carousel-mute-toggle"
                      onClick={() => setIsMuted((v) => !v)}
                      aria-label={isMuted ? "Unmute video" : "Mute video"}
                      className="w-8 h-8 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center border border-white/10 hover:bg-primary/30 hover:border-primary/40 transition-all"
                    >
                      {isMuted ? (
                        <VolumeX className="w-3.5 h-3.5 text-white/70" />
                      ) : (
                        <Volume2 className="w-3.5 h-3.5 text-primary" />
                      )}
                    </button>
                  </div>

                  {/* Muted hint pill (shows briefly then fades) */}
                  {isMuted && (
                    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
                      <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-black/60 backdrop-blur-sm border border-white/10">
                        <VolumeX className="w-3 h-3 text-white/50" />
                        <span className="text-white/50 font-mono text-[10px]">Tap 🔇 to unmute</span>
                      </div>
                    </div>
                  )}

                  {/* Progress bar */}
                  <div className="absolute bottom-0 left-0 right-0 h-[3px] bg-white/10 z-30">
                    <div
                      className="h-full bg-primary transition-none rounded-full"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                </motion.div>
              </AnimatePresence>
            </div>

            {/* Right peek card */}
            <motion.div
              key={`next-${nextIndex}`}
              className="hidden lg:block relative w-40 xl:w-48 rounded-2xl overflow-hidden cursor-pointer shrink-0"
              style={{ aspectRatio: "9/16" }}
              onClick={goNext}
              whileHover={{ scale: 1.03 }}
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
            >
              <div className="absolute inset-0 bg-black/50 z-10 hover:bg-black/30 transition-colors" />
              <video
                src={`/videos/${videos[nextIndex].id}.mp4`}
                muted
                loop
                playsInline
                className="w-full h-full object-cover"
              />
              <div className="absolute top-3 left-3 z-20">
                <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded-full border backdrop-blur-sm ${categoryColors[videos[nextIndex].category as VideoCategory]}`}>
                  {videos[nextIndex].category}
                </span>
              </div>
            </motion.div>
          </div>

          {/* Next arrow */}
          <button
            id="carousel-next"
            onClick={goNext}
            aria-label="Next video"
            className="shrink-0 w-10 h-10 md:w-12 md:h-12 rounded-full glass-card border border-white/10 flex items-center justify-center hover:bg-primary/20 hover:border-primary/40 transition-all duration-300 group z-10"
          >
            <ChevronRight className="w-5 h-5 text-foreground/60 group-hover:text-primary transition-colors" />
          </button>
        </div>

        {/* ── Problem / Solution / CTA ────────────────────────── */}
        <div className="mt-10 max-w-lg mx-auto text-center min-h-[140px] flex flex-col items-center justify-start">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeIndex}
              variants={textVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.3, ease: "easeOut" }}
              className="flex flex-col items-center gap-3 w-full"
            >
              {/* Problem */}
              <h3 className="text-lg md:text-xl font-mono font-bold text-foreground leading-snug">
                {current.problem}
              </h3>

              {/* Solution */}
              <p className="text-sm font-mono text-muted-foreground flex items-start gap-2">
                <span className="text-primary mt-0.5 shrink-0">✓</span>
                <span>{current.solution}</span>
              </p>

              {/* Free Offer */}
              <div className="mt-1 p-3 rounded-xl bg-primary/10 border border-primary/20 text-xs font-mono text-primary-foreground/90 flex flex-col items-center gap-1 w-full text-center">
                <span className="font-bold text-primary tracking-wider uppercase text-[10px]">The Free Fix</span>
                <span>{current.freeOffer}</span>
              </div>

              {/* CTA */}
              <a
                href="#email-collection"
                id="carousel-cta"
                className="mt-2 inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-primary/10 hover:bg-primary/20 border border-primary/30 hover:border-primary/50 text-primary font-mono text-sm font-semibold transition-all duration-300 group"
              >
                <Zap className="w-3.5 h-3.5" />
                Get This Fixed — Free
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </a>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* ── Dot navigation ──────────────────────────────────── */}
        <div
          className="mt-8 flex items-center justify-center flex-wrap gap-1.5"
          role="tablist"
          aria-label="Video navigation"
        >
          {videos.map((v, i) => (
            <button
              key={v.id}
              id={`carousel-dot-${i + 1}`}
              role="tab"
              aria-selected={i === activeIndex}
              aria-label={`Video ${i + 1}`}
              onClick={() => goTo(i, i > activeIndex ? 1 : -1)}
              className={`rounded-full transition-all duration-300 ${
                i === activeIndex
                  ? "w-6 h-2 bg-primary"
                  : "w-2 h-2 bg-white/20 hover:bg-white/40"
              }`}
            />
          ))}
        </div>

        {/* ── Category filter pills ───────────────────────────── */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-2">
          {(Object.keys(categoryColors) as VideoCategory[]).map((cat) => {
            const firstMatch = videos.findIndex((v) => v.category === cat);
            const isActive = videos[activeIndex].category === cat;
            return (
              <button
                key={cat}
                onClick={() => goTo(firstMatch, firstMatch > activeIndex ? 1 : -1)}
                className={`text-[10px] font-mono font-bold px-3 py-1 rounded-full border backdrop-blur-sm transition-all duration-300 ${
                  isActive
                    ? categoryColors[cat]
                    : "bg-white/5 text-white/40 border-white/10 hover:bg-white/10 hover:text-white/60"
                }`}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
