"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { BeforeAfterSlider } from "./BeforeAfterSlider";
import { Play, ArrowRight, Lock, FolderDown, Globe, Video } from "lucide-react";

export const showcaseImages = {
  beforeAfter: {
    beforeSrc: "/media__1780287107773.png",
    beforePos: "50% 10%", // Crop to show the 100 followers area at the top
    afterSrc: "/media__1780287135233.png",
    afterPos: "50% top",   // Crop to show the 8,000 followers area at the top
  },
  automations: { src: "/media__1780287712681.png", pos: "50% 50%" },
  amazonKdp: { src: "/media__1780287782813.png", pos: "50% 50%" },
  localAi: { src: "/media__1780288151493.png", pos: "50% 50%" },
  cosmetics: { src: "/media__1780288225395.png", pos: "50% 50%" },
  digitalNomads: { src: "/media__1780287359382.jpg", pos: "50% 50%" },
  treeSongs: { src: "/media__1780287433411.png", pos: "50% 50%" },
};

export function ClientShowcase() {
  return (
    <section id="work" className="py-24 md:py-32 relative bg-background border-t border-white/5">
      <div className="container px-4 mx-auto">
        
        {/* Section Header */}
        <div className="mb-16 md:mb-24 text-center max-w-3xl mx-auto">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl md:text-5xl font-mono font-bold tracking-tighter mb-6"
          >
            Real <span className="text-gradient">Results</span>
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-muted-foreground font-mono text-lg"
          >
            We don't just post content—we engineer growth. See how we combine massive account scaling, high-quality content creation, and targeted ad copy to build thriving brands.
          </motion.p>
        </div>

        {/* Featured Transformation: Before & After */}
        <div className="mb-24">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="p-1 rounded-3xl bg-gradient-to-b from-white/10 to-transparent"
          >
            <div className="bg-black rounded-[23px] overflow-hidden">
              <BeforeAfterSlider 
                beforeImage={showcaseImages.beforeAfter.beforeSrc}
                beforePosition={showcaseImages.beforeAfter.beforePos}
                afterImage={showcaseImages.beforeAfter.afterSrc}
                afterPosition={showcaseImages.beforeAfter.afterPos}
                beforeLabel="100 Followers"
                afterLabel="8,000 Followers"
              />
            </div>
          </motion.div>
        </div>

        {/* Client Gallery Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Card 1: Automations Workflow */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border"
          >
            <img src={showcaseImages.automations.src} style={{ objectPosition: showcaseImages.automations.pos }} alt="Make.com Workflow" className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
            <div className="absolute bottom-6 left-6 right-6 z-20 flex flex-col gap-2">
              <div className="flex items-start">
                <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-primary/20 text-primary uppercase tracking-wider border border-primary/20 backdrop-blur-sm">SaaS / Agencies</span>
              </div>
              <h3 className="text-white font-bold font-mono text-xl drop-shadow-md leading-tight">Complex AI Automation</h3>
              <p className="text-white/80 font-mono text-sm drop-shadow-md">Audio/video generation pipelines via Make.com</p>
              <a href="#" className="mt-1 inline-flex items-center gap-1.5 text-xs font-mono text-primary hover:text-accent transition-colors w-fit">
                View Project <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </motion.div>

          {/* Card 2: Amazon KDP SEO */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border"
          >
            <img src={showcaseImages.amazonKdp.src} style={{ objectPosition: showcaseImages.amazonKdp.pos }} alt="Amazon KDP SEO" className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
            <div className="absolute bottom-6 left-6 right-6 z-20 flex flex-col gap-2">
              <div className="flex items-start">
                <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-primary/20 text-primary uppercase tracking-wider border border-primary/20 backdrop-blur-sm">Publishing</span>
              </div>
              <h3 className="text-white font-bold font-mono text-xl drop-shadow-md leading-tight">Amazon KDP & SEO</h3>
              <p className="text-white/80 font-mono text-sm drop-shadow-md">Book listings, keyword optimization & SEO strategy</p>
              <a href="#" className="mt-1 inline-flex items-center gap-1.5 text-xs font-mono text-primary hover:text-accent transition-colors w-fit">
                View Project <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </motion.div>

          {/* Card 3: Local AI Infrastructure */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border"
          >
            <img src={showcaseImages.localAi.src} style={{ objectPosition: showcaseImages.localAi.pos }} alt="Local AI Setup" className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
            <div className="absolute bottom-6 left-6 right-6 z-20 flex flex-col gap-2">
              <div className="flex items-start">
                <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-primary/20 text-primary uppercase tracking-wider border border-primary/20 backdrop-blur-sm">Development</span>
              </div>
              <h3 className="text-white font-bold font-mono text-xl drop-shadow-md leading-tight">Local AI & Bolt.diy</h3>
              <p className="text-white/80 font-mono text-sm drop-shadow-md">Self-hosted AI setup and local infrastructure</p>
              <a href="#" className="mt-1 inline-flex items-center gap-1.5 text-xs font-mono text-primary hover:text-accent transition-colors w-fit">
                View Project <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </motion.div>

          {/* Card 4: Cosmetics Data Management */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border"
          >
            <img src={showcaseImages.cosmetics.src} style={{ objectPosition: showcaseImages.cosmetics.pos }} alt="Cosmetics Data Catalog" className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
            <div className="absolute bottom-6 left-6 right-6 z-20 flex flex-col gap-2">
              <div className="flex items-start">
                <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-primary/20 text-primary uppercase tracking-wider border border-primary/20 backdrop-blur-sm">E-Commerce</span>
              </div>
              <h3 className="text-white font-bold font-mono text-xl drop-shadow-md leading-tight">Cosmetics Catalog</h3>
              <p className="text-white/80 font-mono text-sm drop-shadow-md">Data entry, pricing management & catalog design</p>
              <a href="#" className="mt-1 inline-flex items-center gap-1.5 text-xs font-mono text-primary hover:text-accent transition-colors w-fit">
                View Project <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </motion.div>

          {/* Card 5: Digital Nomads Blueprint */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border"
          >
            <img src={showcaseImages.digitalNomads.src} style={{ objectPosition: showcaseImages.digitalNomads.pos }} alt="Digital Nomads Blueprint" className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
            <div className="absolute bottom-6 left-6 right-6 z-20 flex flex-col gap-2">
              <div className="flex items-start">
                <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-primary/20 text-primary uppercase tracking-wider border border-primary/20 backdrop-blur-sm">Info Product</span>
              </div>
              <h3 className="text-white font-bold font-mono text-xl drop-shadow-md leading-tight">Digital Nomads Blueprint</h3>
              <p className="text-white/80 font-mono text-sm drop-shadow-md">High-converting landing page & funnels</p>
              <a href="#" className="mt-1 inline-flex items-center gap-1.5 text-xs font-mono text-primary hover:text-accent transition-colors w-fit">
                View Project <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </motion.div>

          {/* Card 6: TreeSongs Branding */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border"
          >
            <img src={showcaseImages.treeSongs.src} style={{ objectPosition: showcaseImages.treeSongs.pos }} alt="TreeSongs Brand Design" className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
            <div className="absolute bottom-6 left-6 right-6 z-20 flex flex-col gap-2">
              <div className="flex items-start">
                <span className="text-[10px] font-mono font-bold px-2.5 py-1 rounded-full bg-primary/20 text-primary uppercase tracking-wider border border-primary/20 backdrop-blur-sm">Eco-Development</span>
              </div>
              <h3 className="text-white font-bold font-mono text-xl drop-shadow-md leading-tight">TreeSongs</h3>
              <p className="text-white/80 font-mono text-sm drop-shadow-md">Brand design & visual identity auditing</p>
              <a href="#" className="mt-1 inline-flex items-center gap-1.5 text-xs font-mono text-primary hover:text-accent transition-colors w-fit">
                View Project <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </motion.div>

          {/* Card 7: NDA Project */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border flex items-center justify-center text-center p-6"
          >
            <div className="absolute inset-0 bg-black/40 backdrop-blur-md group-hover:bg-black/60 transition-colors duration-500 z-10" />
            <div className="relative z-20 flex flex-col items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center border border-primary/30">
                <Lock className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-white font-bold font-mono text-xl">Enterprise Level</h3>
              <p className="text-white/60 font-mono text-sm max-w-[200px]">Hidden due to NDA & Client Exclusivity.</p>
              <button onClick={() => window.dispatchEvent(new Event('open-lead-gate'))} className="mt-2 px-5 py-2.5 rounded-full border border-primary/50 text-primary font-mono text-xs hover:bg-primary hover:text-primary-foreground transition-all">
                Book call to view
              </button>
            </div>
          </motion.div>

          {/* Card 8: Virtual Events */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border flex items-center justify-center text-center p-6"
          >
            <div className="absolute inset-0 bg-black/40 backdrop-blur-md group-hover:bg-black/60 transition-colors duration-500 z-10" />
            <div className="relative z-20 flex flex-col items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center border border-primary/30">
                <Video className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-white font-bold font-mono text-xl">Virtual Summits</h3>
              <p className="text-white/60 font-mono text-sm max-w-[200px]">End-to-end management for US-based virtual events.</p>
              <button onClick={() => window.dispatchEvent(new Event('open-lead-gate'))} className="mt-2 px-5 py-2.5 rounded-full border border-primary/50 text-primary font-mono text-xs hover:bg-primary hover:text-primary-foreground transition-all">
                View Setup
              </button>
            </div>
          </motion.div>

          {/* Card 9: Global Digital Solutions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="group relative aspect-video rounded-3xl overflow-hidden glass gradient-border flex items-center justify-center text-center p-6"
          >
            <div className="absolute inset-0 bg-black/40 backdrop-blur-md group-hover:bg-black/60 transition-colors duration-500 z-10" />
            <div className="relative z-20 flex flex-col items-center gap-4">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center border border-primary/30">
                <Globe className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-white font-bold font-mono text-xl">Global Digital Solutions</h3>
              <p className="text-white/60 font-mono text-sm max-w-[200px]">Remote workflows and automation for global brands.</p>
              <button onClick={() => window.dispatchEvent(new Event('open-lead-gate'))} className="mt-2 px-5 py-2.5 rounded-full border border-primary/50 text-primary font-mono text-xs hover:bg-primary hover:text-primary-foreground transition-all">
                View Workflows
              </button>
            </div>
          </motion.div>

        </div>

        {/* Google Drive Archive Section */}
        <div className="mt-20">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="w-full rounded-3xl overflow-hidden glass gradient-border p-8 md:p-12 relative flex flex-col md:flex-row items-center justify-between gap-8"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-primary/10 via-transparent to-accent/10 pointer-events-none" />
            
            <div className="flex-1 relative z-10 text-center md:text-left">
              <h3 className="text-2xl md:text-3xl font-bold font-mono text-foreground mb-4">Complete System Archive</h3>
              <p className="text-muted-foreground font-mono text-sm md:text-base max-w-2xl leading-relaxed">
                Get full access to our systematic Google Drive repository. See the entire process documented: from planning and auditing, to the actual work being executed, finished end-products, and final client feedback/results.
              </p>
            </div>

            <div className="relative z-10 shrink-0 flex flex-col md:flex-row gap-4">
              {/* TODO: Replace href with actual Google Drive URL for System Archive */}
              <a 
                href="https://drive.google.com/drive/folders/PLACEHOLDER_SYSTEM_ARCHIVE" 
                target="_blank" 
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-8 py-4 bg-white/5 hover:bg-primary/20 border border-white/10 hover:border-primary/50 rounded-full font-mono text-sm font-bold transition-all duration-300 group shadow-lg"
              >
                <FolderDown className="w-5 h-5 text-primary group-hover:-translate-y-1 transition-transform" />
                System Archive Drive
              </a>

              {/* TODO: Replace href with actual Google Drive URL for Gigs & Proposals */}
              <a 
                href="https://drive.google.com/drive/folders/PLACEHOLDER_GIGS_PROPOSALS" 
                target="_blank" 
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-8 py-4 bg-white/5 hover:bg-accent/20 border border-white/10 hover:border-accent/50 rounded-full font-mono text-sm font-bold transition-all duration-300 group shadow-lg"
              >
                <FolderDown className="w-5 h-5 text-accent group-hover:-translate-y-1 transition-transform" />
                Gigs & Proposals Drive
              </a>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
