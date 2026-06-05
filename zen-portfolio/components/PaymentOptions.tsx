"use client";

import { motion } from "framer-motion";
import { CreditCard, Wallet, Landmark, DollarSign, Bitcoin, Globe, ShieldCheck } from "lucide-react";

const payments = [
  { name: "Visa & Mastercard", icon: CreditCard, color: "text-indigo-400" },
  { name: "PayPal", icon: Globe, color: "text-blue-500" },
  { name: "M-Pesa", icon: Wallet, color: "text-green-500" },
  { name: "Cryptocurrency", icon: Bitcoin, color: "text-yellow-500" },
  { name: "Stripe", icon: DollarSign, color: "text-purple-500" },
  { name: "Paystack", icon: ShieldCheck, color: "text-cyan-500" },
  { name: "Wise", icon: Globe, color: "text-emerald-400" },
  { name: "Bank Transfer", icon: Landmark, color: "text-zinc-400" },
];

export function PaymentOptions() {
  return (
    <section className="py-24 relative bg-background overflow-hidden border-t border-white/5">
      <div className="absolute inset-0 bg-dot-pattern opacity-10" />
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[300px] bg-primary/5 rounded-[100%] blur-[120px]" />

      <div className="container px-4 mx-auto relative z-10">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-mono font-bold tracking-tight mb-4">
            Flexible <span className="text-gradient">Payments</span>
          </h2>
          <p className="text-muted-foreground font-mono text-sm leading-relaxed">
            We support multiple secure payment gateways and local options to ensure a frictionless checkout process worldwide.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          {payments.map((payment, i) => {
            const Icon = payment.icon;
            return (
              <motion.div
                key={payment.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
                className="glass-card gradient-border rounded-2xl p-6 flex flex-col items-center justify-center text-center gap-3 hover:-translate-y-1 hover:shadow-[0_0_20px_hsla(270,95%,65%,0.15)] transition-all duration-300 group"
              >
                <div className="w-12 h-12 rounded-full bg-white/[0.03] border border-white/5 flex items-center justify-center group-hover:scale-110 group-hover:bg-white/[0.08] transition-all duration-300">
                  <Icon className={`w-5 h-5 ${payment.color}`} />
                </div>
                <span className="font-mono text-sm font-bold text-foreground/80 group-hover:text-foreground transition-colors">
                  {payment.name}
                </span>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
