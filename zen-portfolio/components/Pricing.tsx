import React from 'react';
import { cn } from '@/lib/utils';
import { Check } from 'lucide-react';
import { InteractiveHoverButton } from './InteractiveHoverButton';

function Card({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      className={cn(
        'bg-black/40 relative w-full rounded-2xl border border-white/10',
        'p-1.5 shadow-xl backdrop-blur-xl transition-transform hover:-translate-y-1 duration-300',
        className,
      )}
      {...props}
    />
  );
}

function Header({
  className,
  children,
  glassEffect = true,
  ...props
}: React.ComponentProps<'div'> & {
  glassEffect?: boolean;
}) {
  return (
    <div
      className={cn(
        'bg-white/5 relative mb-4 rounded-xl border border-white/5 p-6',
        className,
      )}
      {...props}
    >
      {glassEffect && (
        <div
          aria-hidden="true"
          className="absolute inset-x-0 top-0 h-48 rounded-[inherit] pointer-events-none"
          style={{
            background:
              'linear-gradient(180deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 40%, rgba(0,0,0,0) 100%)',
          }}
        />
      )}
      {children}
    </div>
  );
}

function PlanName({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      className={cn(
        "text-gray-300 flex items-center gap-2 text-sm font-mono font-medium uppercase tracking-wider mb-4",
        className,
      )}
      {...props}
    />
  );
}

function Price({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div className={cn('mb-2 flex items-end gap-1', className)} {...props} />
  );
}

function MainPrice({ className, ...props }: React.ComponentProps<'span'>) {
  return (
    <span
      className={cn('text-4xl font-extrabold tracking-tight font-mono text-white', className)}
      {...props}
    />
  );
}

function Period({ className, ...props }: React.ComponentProps<'span'>) {
  return (
    <span
      className={cn('text-gray-400 pb-1 text-sm font-mono', className)}
      {...props}
    />
  );
}

function Description({ className, ...props }: React.ComponentProps<'p'>) {
  return (
    <p className={cn('text-gray-400 text-sm font-mono leading-relaxed', className)} {...props} />
  );
}

function Body({ className, ...props }: React.ComponentProps<'div'>) {
  return <div className={cn('space-y-6 p-6', className)} {...props} />;
}

function List({ className, ...props }: React.ComponentProps<'ul'>) {
  return <ul className={cn('space-y-4', className)} {...props} />;
}

function ListItem({ className, children, ...props }: React.ComponentProps<'li'>) {
  return (
    <li
      className={cn(
        'text-gray-300 flex items-start gap-3 text-sm font-mono',
        className,
      )}
      {...props}
    >
      <Check className="w-5 h-5 text-primary shrink-0" />
      <span>{children}</span>
    </li>
  );
}

export function Pricing() {
  return (
    <section className="py-24 bg-background relative overflow-hidden border-b border-white/10" id="pricing">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-primary/10 rounded-[100%] blur-[120px] -z-10 pointer-events-none" />
      
      <div className="max-w-7xl mx-auto px-4 mb-16 text-center">
        <h2 className="text-3xl md:text-5xl font-mono font-bold mb-4">Ready to reclaim your time?</h2>
        <p className="text-muted-foreground font-mono max-w-2xl mx-auto">Choose a plan that fits your growth stage. Transparent pricing, no hidden fees.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto px-4">
        
        {/* Starter Pack */}
        <Card>
          <Header>
            <PlanName>Starter Pack</PlanName>
            <Price>
              <MainPrice>$480</MainPrice>
              <Period>/mo</Period>
            </Price>
            <Description>Perfect for solopreneurs needing baseline operational support.</Description>
          </Header>
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

        {/* Growth Pack (Popular) */}
        <Card className="border-primary/50 shadow-[0_0_30px_rgba(99,102,241,0.1)] relative">
          <div className="absolute -top-3 inset-x-0 flex justify-center z-10">
            <span className="bg-primary text-white text-xs font-mono font-bold px-3 py-1 rounded-full border border-white/20">MOST POPULAR</span>
          </div>
          <Header className="bg-primary/5 border-primary/20">
            <PlanName className="text-primary">Growth Pack</PlanName>
            <Price>
              <MainPrice>$940</MainPrice>
              <Period>/mo</Period>
            </Price>
            <Description>For growing teams needing advanced automation and media.</Description>
          </Header>
          <Body>
            <List>
              <ListItem>40 Hours per month</ListItem>
              <ListItem>Advanced Zapier/Make Automation</ListItem>
              <ListItem>Short-form Video Editing (TikTok/Reels)</ListItem>
              <ListItem>Proactive Lead Generation</ListItem>
              <ListItem>Weekly Strategy Calls</ListItem>
            </List>
            <div className="mt-8 flex justify-center">
              <InteractiveHoverButton text="Scale Now" className="w-full !bg-primary border-primary/50" />
            </div>
          </Body>
        </Card>

        {/* Premium Pack */}
        <Card>
          <Header>
            <PlanName>Premium 24/7</PlanName>
            <Price>
              <MainPrice>$1,800</MainPrice>
              <Period>/mo</Period>
            </Price>
            <Description>Institutional-grade support for established businesses.</Description>
          </Header>
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

      </div>
    </section>
  );
}
