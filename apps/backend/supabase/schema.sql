-- Schema for Xish AI backend (Supabase/Postgres)

create table if not exists preferences (
  user_id uuid primary key,
  preferences jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists memory (
  user_id uuid not null,
  key text not null,
  value text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, key)
);

create table if not exists chat_history (
  id uuid primary key,
  user_id uuid not null,
  role text not null check (role in ('user','assistant','system')),
  content text not null,
  model text,
  created_at timestamptz not null default now()
);

-- Recommended row level security policies (enable RLS and add policies as needed)
-- alter table preferences enable row level security;
-- create policy "Users can manage own preferences" on preferences for all using (auth.uid() = user_id);
-- alter table memory enable row level security;
-- create policy "Users can manage own memory" on memory for all using (auth.uid() = user_id);
-- alter table chat_history enable row level security;
-- create policy "Users can manage own chats" on chat_history for all using (auth.uid() = user_id);
