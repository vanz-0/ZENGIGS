-- 1. Enable Row Level Security (RLS) on all tables
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.outreach_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kpi_logs ENABLE ROW LEVEL SECURITY;

-- If there's an old kpi_metrics table, enable it there too
DO $$ 
BEGIN
  IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'kpi_metrics') THEN
    ALTER TABLE public.kpi_metrics ENABLE ROW LEVEL SECURITY;
  END IF;
END $$;

-- 2. Drop any existing "Always True" policies that might be causing warnings
DO $$ 
DECLARE
    pol record;
BEGIN
    FOR pol IN 
        SELECT policyname, tablename 
        FROM pg_policies 
        WHERE schemaname = 'public' 
          AND (tablename = 'leads' OR tablename = 'kpi_metrics' OR tablename = 'kpi_logs' OR tablename = 'outreach_logs')
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON public.%I', pol.policyname, pol.tablename);
    END LOOP;
END $$;

-- 3. Create strict RLS policies
-- Service Role (used by Python scripts) automatically bypasses RLS, so we only need to configure Anon/Authenticated access.

-- Portfolio Frontend (Anon) only needs to READ the kpi_logs for the LiveMetrics component.
CREATE POLICY "Allow public read access to KPI logs" 
ON public.kpi_logs
FOR SELECT 
TO anon, authenticated
USING (true);

-- Explicitly deny all anon access to leads and outreach_logs (Security Best Practice)
-- (By simply enabling RLS and not adding an anon policy, they are implicitly denied, but we can be explicit if we want. Implicit is fine.)

-- 4. Fix Function Search Path Mutable warning
-- This secures the trigger function by explicitly setting its search path to public
ALTER FUNCTION public.update_updated_at_column() SET search_path = public;
