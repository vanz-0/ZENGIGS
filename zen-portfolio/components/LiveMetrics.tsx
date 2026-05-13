"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

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
    <div className="w-full max-w-5xl mx-auto py-12 px-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-mono font-bold text-white mb-4">Live System Metrics</h2>
        <p className="text-gray-400 font-mono text-sm">Real-time stats from the ZENGIGS Second Brain pipeline.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-black/50 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-center">
          <div className="text-primary text-4xl font-mono font-bold mb-2">{metrics.leads_scraped}</div>
          <div className="text-gray-400 text-sm font-mono uppercase tracking-wider">Leads Sourced</div>
        </div>
        <div className="bg-black/50 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-center">
          <div className="text-primary text-4xl font-mono font-bold mb-2">{metrics.emails_sent}</div>
          <div className="text-gray-400 text-sm font-mono uppercase tracking-wider">Automated Emails Sent</div>
        </div>
        <div className="bg-black/50 border border-white/10 rounded-xl p-6 backdrop-blur-sm text-center">
          <div className="text-primary text-4xl font-mono font-bold mb-2">{metrics.meetings_booked}</div>
          <div className="text-gray-400 text-sm font-mono uppercase tracking-wider">Meetings Booked</div>
        </div>
      </div>
    </div>
  );
}
