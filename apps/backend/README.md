### Xish AI Backend (FastAPI)

- FastAPI app with chat, memory, and preferences endpoints
- SSE streaming for typing effect
- Supabase-compatible Postgres schema

Run locally:

```bash
uvicorn app.main:app --reload --port 8000
```

Env:

- See `.env.example`

Database:

- Apply `supabase/schema.sql` to your Postgres/Supabase project
