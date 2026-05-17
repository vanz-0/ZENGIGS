'use client';

import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';
import { 
  Play, 
  Search, 
  MapPin, 
  Filter, 
  RefreshCw, 
  CheckCircle2, 
  AlertCircle,
  ExternalLink,
  Users
} from 'lucide-react';

// Initialize Supabase Client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

const NICHES = [
  "SaaS Founders",
  "E-commerce Owners",
  "Life Coaches",
  "Digital Marketing Agencies",
  "Real Estate Agents",
  "YouTubers",
  "Video Production Companies"
];

const LOCATIONS = [
  "United States",
  "United Kingdom",
  "London",
  "New York",
  "Global"
];

export function LeadCenter() {
  const [leads, setLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  
  // Form State
  const [niche, setNiche] = useState(NICHES[0]);
  const [location, setLocation] = useState(LOCATIONS[1]);
  const [mode, setMode] = useState("test");

  useEffect(() => {
    fetchLeads();
    
    // Subscribe to changes
    const channel = supabase
      .channel('leads-all')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'leads' }, () => {
        fetchLeads();
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  async function fetchLeads() {
    setLoading(true);
    const { data, error } = await supabase
      .from('leads')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(10);
    
    if (data) setLeads(data);
    setLoading(false);
  }

  async function startPipeline() {
    setRunning(true);
    try {
      const res = await fetch('/api/pipeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'scrape',
          query: niche,
          location: location,
          mode: mode
        })
      });
      
      if (res.ok) {
        alert("Pipeline started! Check the logs or refresh in a minute.");
      } else {
        const err = await res.json();
        alert(`Error: ${err.error}`);
      }
    } catch (e) {
      alert("Failed to start pipeline.");
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="flex flex-col gap-8 p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-foreground tracking-tight">Lead Center</h1>
          <p className="text-muted-foreground mt-2 font-mono">ZENGIGS Automation Command Center</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-full flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-xs font-mono text-green-500">SYSTEM LIVE</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Control Panel */}
        <div className="lg:col-span-1 bg-white/5 border border-white/10 rounded-3xl p-6 backdrop-blur-xl">
          <div className="flex items-center gap-2 mb-6 text-primary">
            <Filter size={20} />
            <h2 className="font-bold uppercase tracking-widest text-sm">Control Panel</h2>
          </div>

          <div className="space-y-6">
            <div>
              <label className="text-xs font-mono text-muted-foreground block mb-2">TARGET NICHE</label>
              <select 
                value={niche} 
                onChange={(e) => setNiche(e.target.value)}
                className="w-full bg-black border border-white/20 rounded-xl px-4 py-3 text-foreground focus:outline-none focus:border-primary transition-colors"
              >
                {NICHES.map(n => <option key={n} value={n}>{n}</option>)}
              </select>
            </div>

            <div>
              <label className="text-xs font-mono text-muted-foreground block mb-2">LOCATION</label>
              <select 
                value={location} 
                onChange={(e) => setLocation(e.target.value)}
                className="w-full bg-black border border-white/20 rounded-xl px-4 py-3 text-foreground focus:outline-none focus:border-primary transition-colors"
              >
                {LOCATIONS.map(l => <option key={l} value={l}>{l}</option>)}
              </select>
            </div>

            <div>
              <label className="text-xs font-mono text-muted-foreground block mb-2">SCRAPE MODE</label>
              <div className="grid grid-cols-2 gap-2 p-1 bg-black rounded-xl border border-white/10">
                <button 
                  onClick={() => setMode("test")}
                  className={`py-2 text-xs font-bold rounded-lg transition-all ${mode === "test" ? "bg-primary text-foreground" : "text-muted-foreground hover:text-foreground"}`}
                >
                  TEST (1 Lead)
                </button>
                <button 
                  onClick={() => setMode("active")}
                  className={`py-2 text-xs font-bold rounded-lg transition-all ${mode === "active" ? "bg-primary text-foreground" : "text-muted-foreground hover:text-foreground"}`}
                >
                  ACTIVE (Batch)
                </button>
              </div>
            </div>

            <button 
              onClick={startPipeline}
              disabled={running}
              className="w-full bg-white text-background font-bold py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-primary hover:text-foreground transition-all disabled:opacity-50 group"
            >
              {running ? <RefreshCw className="animate-spin" /> : <Play fill="currentColor" size={20} />}
              {running ? "SCRAPING..." : "START PIPELINE"}
            </button>
          </div>
        </div>

        {/* Lead Table */}
        <div className="lg:col-span-2 bg-white/5 border border-white/10 rounded-3xl overflow-hidden backdrop-blur-xl">
          <div className="p-6 border-b border-white/10 flex justify-between items-center">
            <div className="flex items-center gap-2 text-primary">
              <Users size={20} />
              <h2 className="font-bold uppercase tracking-widest text-sm">Recent Leads</h2>
            </div>
            <button onClick={fetchLeads} className="text-muted-foreground hover:text-foreground transition-colors">
              <RefreshCw size={16} />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-white/5 text-[10px] font-mono text-muted-foreground uppercase">
                  <th className="px-6 py-4">Lead</th>
                  <th className="px-6 py-4">Company</th>
                  <th className="px-6 py-4">Niche</th>
                  <th className="px-6 py-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {leads.map((lead) => (
                  <tr key={lead.id} className="hover:bg-white/[0.02] transition-colors group">
                    <td className="px-6 py-4">
                      <div className="font-bold text-foreground text-sm">{lead.first_name} {lead.last_name}</div>
                      <div className="text-xs text-muted-foreground">{lead.email}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-foreground">{lead.company}</div>
                      <a href={lead.website} target="_blank" className="text-[10px] text-primary flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <ExternalLink size={10} /> Visit Site
                      </a>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-[10px] font-mono px-2 py-1 bg-white/10 rounded-full text-muted-foreground border border-white/10">
                        {lead.niche}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      {lead.status === 'new' ? (
                        <div className="flex items-center justify-end gap-1 text-primary text-xs font-bold">
                          <CheckCircle2 size={14} /> NEW
                        </div>
                      ) : (
                        <div className="flex items-center justify-end gap-1 text-muted-foreground text-xs">
                          <AlertCircle size={14} /> {lead.status.toUpperCase()}
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
                {leads.length === 0 && !loading && (
                  <tr>
                    <td colSpan={4} className="px-6 py-12 text-center text-muted-foreground font-mono text-sm">
                      No leads found. Start a pipeline to populate this list.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
