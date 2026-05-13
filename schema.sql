-- ZENGIGS Supabase Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Leads Table
CREATE TABLE IF NOT EXISTS public.leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    website TEXT,
    location TEXT,
    niche TEXT,
    status TEXT DEFAULT 'new', -- new, enriched, contacted, bounced, replied, meeting_booked
    source TEXT DEFAULT 'apify_scrape',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Campaigns/Outreach Logs Table
CREATE TABLE IF NOT EXISTS public.outreach_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES public.leads(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    template_used TEXT NOT NULL,
    status TEXT DEFAULT 'sent', -- sent, failed, bounced, opened, clicked, replied
    error_message TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. KPI Tracker Table
CREATE TABLE IF NOT EXISTS public.kpi_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    log_date DATE UNIQUE NOT NULL DEFAULT CURRENT_DATE,
    emails_sent INT DEFAULT 0,
    responses INT DEFAULT 0,
    meetings_booked INT DEFAULT 0,
    leads_scraped INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_leads_status ON public.leads(status);
CREATE INDEX IF NOT EXISTS idx_outreach_logs_lead_id ON public.outreach_logs(lead_id);
CREATE INDEX IF NOT EXISTS idx_kpi_logs_date ON public.kpi_logs(log_date);

-- Trigger to update updated_at on leads
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DO $$ BEGIN
    CREATE TRIGGER update_leads_updated_at
        BEFORE UPDATE ON public.leads
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
