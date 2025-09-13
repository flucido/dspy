import os
from typing import Optional

from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise SystemExit("Set SUPABASE_URL and SUPABASE_ANON_KEY in your environment.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Example: read from a table named `items`
resp = supabase.table("items").select("*").limit(5).execute()
print(resp)
