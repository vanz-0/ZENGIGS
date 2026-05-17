"use client";

import React from 'react';
import { cn } from '@/lib/utils';
import { Check, Sparkles } from 'lucide-react';
import { InteractiveHoverButton } from './InteractiveHoverButton';
import { motion } from 'framer-motion';

function Card({ className, children, featured = false, ...props }: React.ComponentProps<'div'> & { featured?: boolean }) {
  return (
    <div
      className={cn(
        'relative w-full rounded-2xl overflow-hidden',
        'p-[1px] transition-all duration-500 hover:-translate-y-2',
        featured
          ? 'bg-gradient-to-b from-primary/60 via-primary/20 to-accent/30 shadow-[0_0_50px_hsla(270,95%,65%,0.15)]'
          : 'bg-gradient-to-b from-white/10 via-white/5 to-transparent hover:shadow-[0_20px_60px_-10px_hsla(270,95%,65%,0.1)]',
        className,
      )}
      {...props}
    >
      <div className="bg-card rounded-[calc(1rem-1px)] h-full">
        {children}
      </div>
    </div>
  );
}

function Header({
  className,
  children,
  ...props
}: React.ComponentProps<'div'>) {
  return (
    <div
      className={cn(
        'relative p-7 pb-6',
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

function PlanName({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      className={cn(
        "text-muted-foreground flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-[0.2em] mb-5",
        className,
      )}
      {...props}
    />
  );
}

function Price({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div className={cn('mb-3 flex items-end gap-1', className)} {...props} />
  );
}

function MainPrice({ className, ...props }: React.ComponentProps<'span'>) {
  return (
    <span
      className={cn('text-5xl font-extrabold tracking-tight font-mono text-foreground', className)}
      {...props}
    />
  );
}

function Period({ className, ...props }: React.ComponentProps<'span'>) {
  return (
    <span
      className={cn('text-muted-foreground pb-1.5 text-sm font-mono', className)}
      {...props}
    />
  );
}

function Description({ className, ...props }: React.ComponentProps<'p'>) {
  return (
    <p className={cn('text-muted-foreground/70 text-sm font-mono leading-relaxed', className)} {...props} />
  );
}

function Body({ className, ...props }: React.ComponentProps<'div'>) {
  return <div className={cn('space-y-6 p-7 pt-0', className)} {...props} />;
}

function List({ className, ...props }: React.ComponentProps<'ul'>) {
  return <ul className={cn('space-y-4', className)} {...props} />;
}

function ListItem({ className, children, featured = false, ...props }: React.ComponentProps<'li'> & { featured?: boolean }) {
  return (
    <li
      className={cn(
        'flex items-start gap-3 text-sm font-mono',
        featured ? 'text-foreground/90' : 'text-muted-foreground',
        className,
      )}
      {...props}
    >
      <div className={cn(
        "w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5",
        featured ? "bg-primary/20" : "bg-white/5"
      )}>
        <Check className={cn("w-3 h-3", featured ? "text-primary" : "text-muted-foreground/70")} />
      </div>
      <span>{children}</span>
    </li>
  );
}

export function Pricing() {
  return (
    <section className="py-28 bg-background relative overflow-hidden" id="pricing">
      {/* Background */}
      <div className="absolute inset-0 bg-dot-pattern opacity-20" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-primary/8 rounded-[100%] blur-[150px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
        className="max-w-7xl mx-auto px-4 mb-16 text-center relative z-10"
      >
        <span className="inline-block px-4 py-1.5 mb-6 rounded-full text-xs font-mono tracking-widest uppercase text-primary/80 glass-card">
          Pricing
        </span>
        <h2 className="text-4xl md:text-6xl font-mono font-bold mb-5 tracking-tight">
          Ready to reclaim your <span className="text-gradient">time</span>?
        </h2>
        <p className="text-muted-foreground font-mono text-lg max-w-2xl mx-auto">
          Choose a plan that fits your growth stage. Transparent pricing, no hidden fees.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto px-4 relative z-10">

        {/* Starter Pack */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ delay: 0, duration: 0.5 }}
          viewport={{ once: true }}
        >
          <Card>
            <Header>
              <PlanName>Starter Pack</PlanName>
              <Price>
                <MainPrice>$480</MainPrice>
                <Period>/mo</Period>
              </Price>
              <Description>Perfect for solopreneurs needing baseline operational support.</Description>
            </Header>
            <div className="mx-7 border-t border-white/[0.06]" />
            <Body>
              <List>
                <ListItem>20 Hours per month</ListItem>
                <ListItem>Basic Inbox Management</ListItem>
                <ListItem>Weekly Social Media Scheduling</ListItem>
                <ListItem>Light Data Entry & CRM Admin</ListItem>
              </List>
              <div className="mt-8 flex justify-center">
                <InteractiveHoverButton text="Get Started" className="w-full" />
              </div>
            </Body>
          </Card>
        </motion.div>

        {/* Growth Pack (Popular) */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          viewport={{ once: true }}
        >
          <Card featured>
            <div className="absolute -top-[1px] inset-x-0 flex justify-center z-10">
              <span className="bg-gradient-to-r from-primary to-accent text-white text-[10px] font-mono font-bold px-4 py-1.5 rounded-b-xl uppercase tracking-[0.2em] flex items-center gap-1.5">
                <Sparkles className="w-3 h-3" />
                Most Popular
              </span>
            </div>
            <Header className="pt-10">
              <PlanName className="text-primary">Growth Pack</PlanName>
              <Price>
                <MainPrice className="text-gradient">$940</MainPrice>
                <Period>/mo</Period>
              </Price>
              <Description>For growing teams needing advanced automation and media production.</Description>
            </Header>
            <div className="mx-7 border-t border-primary/10" />
            <Body>
              <List>
                <ListItem featured>40 Hours per month</ListItem>
                <ListItem featured>Advanced Zapier/Make Automation</ListItem>
                <ListItem featured>Short-form Video Editing (TikTok/Reels)</ListItem>
                <ListItem featured>Proactive Lead Generation</ListItem>
                <ListItem featured>Weekly Strategy Calls</ListItem>
              </List>
              <div className="mt-8 flex justify-center">
                <InteractiveHoverButton text="Scale Now" className="w-full !bg-primary border-primary/50" />
              </div>
            </Body>
          </Card>
        </motion.div>

        {/* Premium Pack */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          viewport={{ once: true }}
        >
          <Card>
            <Header>
              <PlanName>Premium 24/7</PlanName>
              <Price>
                <MainPrice>$1,800</MainPrice>
                <Period>/mo</Period>
              </Price>
              <Description>Institutional-grade support for established businesses.</Description>
            </Header>
            <div className="mx-7 border-t border-white/[0.06]" />
            <Body>
              <List>
                <ListItem>80 Hours per month</ListItem>
                <ListItem>Dedicated 24/7 Availability</ListItem>
                <ListItem>Full Social Media Strategy & Production</ListItem>
                <ListItem>Custom AI Chatbot Integration</ListItem>
                <ListItem>End-to-end Project Management</ListItem>
              </List>
              <div className="mt-8 flex justify-center">
                <InteractiveHoverButton text="Go Premium" className="w-full" />
              </div>
            </Body>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}
