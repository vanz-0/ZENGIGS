-- ZENGIGS Supabase Migration V2
-- Adds tables for Portfolio Projects, Active Bids, and Blueprints

-- 1. Portfolio Projects (Work Done)
CREATE TABLE IF NOT EXISTS portfolio_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tech_stack TEXT[] DEFAULT '{}',
    image_url TEXT,
    live_link TEXT,
    results_metric TEXT, -- e.g., "Increased ROI by 50%"
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Active Bids (Work Applied For)
CREATE TYPE bid_status AS ENUM ('Draft', 'Proposal Submitted', 'Interviewing', 'Closed', 'Won');

CREATE TABLE IF NOT EXISTS active_bids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform TEXT NOT NULL, -- 'Upwork', 'Fiverr', 'Direct', etc.
    job_title TEXT NOT NULL,
    client_location TEXT,
    bid_amount NUMERIC,
    status bid_status DEFAULT 'Proposal Submitted',
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    link TEXT -- Link to the job posting
);

-- 3. Blueprints (Educational Content)
CREATE TABLE IF NOT EXISTS blueprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    category TEXT NOT NULL, -- e.g., 'Upwork', 'Fiverr', 'Cold Email'
    summary TEXT NOT NULL,
    markdown_content TEXT NOT NULL,
    difficulty_level TEXT, -- 'Easy', 'Medium', 'Hard'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security (RLS)

-- Portfolio Projects: Anyone can view, only authenticated can modify
ALTER TABLE portfolio_projects ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Portfolio" ON portfolio_projects FOR SELECT USING (true);
CREATE POLICY "Auth Write Portfolio" ON portfolio_projects FOR ALL USING (auth.role() = 'authenticated');

-- Active Bids: Anyone can view, only authenticated can modify
ALTER TABLE active_bids ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Active Bids" ON active_bids FOR SELECT USING (true);
CREATE POLICY "Auth Write Active Bids" ON active_bids FOR ALL USING (auth.role() = 'authenticated');

-- Blueprints: Anyone can view (we gate the markdown content at the application layer)
ALTER TABLE blueprints ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Blueprints" ON blueprints FOR SELECT USING (true);
CREATE POLICY "Auth Write Blueprints" ON blueprints FOR ALL USING (auth.role() = 'authenticated');
