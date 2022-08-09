CREATE OR REPLACE FUNCTION RefreshMvs() RETURNS INT AS $$
DECLARE
  r RECORD;
BEGIN
  RAISE NOTICE 'Refreshing materialized views';
  FOR r in SELECT * FROM pg_matviews
  LOOP
    EXECUTE 'REFRESH MATERIALIZED VIEW ' || r.schemaname || '.' || r.matviewname;
  END LOOP;
  RETURN 1;
END
$$ LANGUAGE plpgsql;

SELECT RefreshMvs();
