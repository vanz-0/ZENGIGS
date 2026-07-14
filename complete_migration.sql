-- =============================================================================
-- ZENGIGS — Complete Supabase Migration
-- Copy & paste into: https://supabase.com/dashboard/project/tlmzgzxnmatmwpfqrcay/sql/new
-- =============================================================================

-- 1. Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. KPI Logs (daily metric tracking)
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
CREATE INDEX IF NOT EXISTS idx_kpi_logs_date ON public.kpi_logs(log_date);

-- 3. Outreach Logs (sent email tracking)
CREATE TABLE IF NOT EXISTS public.outreach_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES public.leads(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    template_used TEXT NOT NULL,
    status TEXT DEFAULT 'sent',
    error_message TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_outreach_logs_lead_id ON public.outreach_logs(lead_id);

-- 4. Portfolio Projects
CREATE TABLE IF NOT EXISTS portfolio_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tech_stack TEXT[] DEFAULT '{}',
    image_url TEXT,
    live_link TEXT,
    results_metric TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Active Bids
CREATE TABLE IF NOT EXISTS active_bids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform TEXT NOT NULL,
    job_title TEXT NOT NULL,
    client_location TEXT,
    bid_amount NUMERIC,
    status TEXT DEFAULT 'Proposal Submitted',
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    link TEXT
);

-- 6. Blueprints (educational content)
CREATE TABLE IF NOT EXISTS blueprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    summary TEXT NOT NULL,
    markdown_content TEXT NOT NULL,
    difficulty_level TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Workflow Jobs (background job queue)
CREATE TABLE IF NOT EXISTS public.workflow_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    retry_count INT DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_workflow_jobs_status ON public.workflow_jobs(status);

-- 8. Profiles (user metadata — tied to Supabase Auth)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    display_name TEXT,
    role TEXT DEFAULT 'user',
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Auto-create profile on signup (trigger)
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, display_name, role)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'display_name', SPLIT_PART(NEW.email, '@', 1)),
        'user'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DO $$ BEGIN
    CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;


-- =============================================================================
-- Row Level Security (RLS) — public read, authenticated write
-- =============================================================================

-- Portfolio
ALTER TABLE portfolio_projects ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Portfolio" ON portfolio_projects FOR SELECT USING (true);
CREATE POLICY "Auth Write Portfolio" ON portfolio_projects FOR ALL USING (auth.role() = 'authenticated');

-- Active Bids
ALTER TABLE active_bids ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Bids" ON active_bids FOR SELECT USING (true);
CREATE POLICY "Auth Write Bids" ON active_bids FOR ALL USING (auth.role() = 'authenticated');

-- Blueprints
ALTER TABLE blueprints ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Blueprints" ON blueprints FOR SELECT USING (true);
CREATE POLICY "Auth Write Blueprints" ON blueprints FOR ALL USING (auth.role() = 'authenticated');

-- Profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users read own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Service role full access" ON public.profiles FOR ALL USING (auth.role() = 'service_role');


-- =============================================================================
-- Verification (run this separately after the above succeeds)
-- =============================================================================
-- SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public' ORDER BY tablename;
-- Expected: active_bids, blueprints, kpi_logs, leads, outreach_logs, portfolio_projects, profiles, workflow_jobs