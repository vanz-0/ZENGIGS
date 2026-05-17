"use client";

import { useEffect, useState, useRef } from "react";
import { supabase } from "@/lib/supabase";
import { motion, useInView } from "framer-motion";
import { TrendingUp, Mail, Users, CalendarCheck } from "lucide-react";

function AnimatedCounter({ value, duration = 2000 }: { value: number; duration?: number }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (!isInView || value === 0) return;

    let start = 0;
    const step = Math.ceil(value / (duration / 16));
    const timer = setInterval(() => {
      start += step;
      if (start >= value) {
        setCount(value);
        clearInterval(timer);
      } else {
        setCount(start);
      }
    }, 16);

    return () => clearInterval(timer);
  }, [isInView, value, duration]);

  return (
    <div ref={ref} className="text-5xl md:text-6xl font-mono font-bold tabular-nums">
      {count.toLocaleString()}
    </div>
  );
}

const metricConfig = [
  {
    key: "leads_scraped",
    label: "Leads Sourced",
    icon: Users,
    gradient: "from-violet-500 to-purple-600",
    glowColor: "hsla(270, 95%, 65%, 0.15)",
  },
  {
    key: "emails_sent",
    label: "Emails Sent",
    icon: Mail,
    gradient: "from-blue-500 to-cyan-500",
    glowColor: "hsla(210, 90%, 60%, 0.15)",
  },
  {
    key: "meetings_booked",
    label: "Meetings Booked",
    icon: CalendarCheck,
    gradient: "from-amber-400 to-orange-500",
    glowColor: "hsla(38, 92%, 60%, 0.15)",
  },
];

export function LiveMetrics() {
  const [metrics, setMetrics] = useState({
    emails_sent: 0,
    meetings_booked: 0,
    leads_scraped: 0,
  });

  useEffect(() => {
    async function fetchKPIs() {
      try {
        const { data, error } = await supabase
          .from("kpi_logs")
          .select("emails_sent, meetings_booked, leads_scraped");

        if (error) {
          console.error("Error fetching KPIs:", error);
          return;
        }

        if (data && data.length > 0) {
          const totals = data.reduce(
            (acc, curr) => ({
              emails_sent: acc.emails_sent + (curr.emails_sent || 0),
              meetings_booked: acc.meetings_booked + (curr.meetings_booked || 0),
              leads_scraped: acc.leads_scraped + (curr.leads_scraped || 0),
            }),
            { emails_sent: 0, meetings_booked: 0, leads_scraped: 0 }
          );
          setMetrics(totals);
        }
      } catch (err) {
        console.error("Exception fetching KPIs:", err);
      }
    }

    fetchKPIs();
  }, []);

  return (
    <div className="w-full py-28 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-grid-pattern opacity-30" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-primary/5 rounded-full blur-[150px]" />

      <div className="max-w-6xl mx-auto px-6 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-6 rounded-full glass-card">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs font-mono text-green-400 uppercase tracking-widest">Live Pipeline Data</span>
          </div>
          <h2 className="text-4xl md:text-6xl font-mono font-bold mb-5 tracking-tight">
            System <span className="text-gradient">Metrics</span>
          </h2>
          <p className="text-muted-foreground font-mono text-lg max-w-xl mx-auto">
            Real-time stats from the ZENGIGS automation pipeline.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {metricConfig.map((metric, index) => {
            const value = metrics[metric.key as keyof typeof metrics];
            const Icon = metric.icon;

            return (
              <motion.div
                key={metric.key}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.15, duration: 0.5 }}
                viewport={{ once: true }}
                className="group glass-card rounded-2xl p-8 text-center hover:-translate-y-2 transition-all duration-500 relative overflow-hidden"
                style={{
                  boxShadow: `0 0 40px ${metric.glowColor}`,
                }}
              >
                {/* Gradient accent line */}
                <div className={`absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r ${metric.gradient} opacity-60 group-hover:opacity-100 transition-opacity duration-300`} />

                {/* Icon */}
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br ${metric.gradient} mb-6 opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-300`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>

                {/* Counter */}
                <div className="text-foreground mb-3">
                  <AnimatedCounter value={value} />
                </div>

                {/* Label */}
                <div className="text-muted-foreground text-sm font-mono uppercase tracking-[0.2em]">
                  {metric.label}
                </div>

                {/* Subtle trend indicator */}
                <div className="mt-4 inline-flex items-center gap-1 text-xs font-mono text-green-400/70">
                  <TrendingUp className="w-3 h-3" />
                  <span>Live</span>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
