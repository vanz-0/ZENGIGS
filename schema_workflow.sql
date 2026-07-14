-- ZENGIGS Workflow Jobs Schema

CREATE TABLE IF NOT EXISTS public.workflow_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_type TEXT NOT NULL, -- e.g., 'scrape', 'outreach'
    status TEXT DEFAULT 'pending', -- pending, running, completed, failed
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    retry_count INT DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index to quickly find pending jobs
CREATE INDEX IF NOT EXISTS idx_workflow_jobs_status ON public.workflow_jobs(status);

-- Trigger to update updated_at
DO $$ BEGIN
    CREATE TRIGGER update_workflow_jobs_updated_at
        BEFORE UPDATE ON public.workflow_jobs
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
