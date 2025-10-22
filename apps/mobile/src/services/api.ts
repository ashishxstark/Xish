import { supabase } from './supabase';

const API_BASE = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiFetch<T = any>(path: string, init?: RequestInit): Promise<T> {
  const session = (await supabase.auth.getSession()).data.session;
  const headers = new Headers(init?.headers);
  headers.set('Content-Type', 'application/json');
  if (session?.access_token) headers.set('Authorization', `Bearer ${session.access_token}`);
  const res = await fetch(`${API_BASE}${path}`, { ...init, headers });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export function apiSSE(path: string, body: any): EventSourceInit & { url: string } {
  const url = `${API_BASE}${path}`;
  const init: any = { method: 'POST', headers: { 'Content-Type': 'application/json' }, payload: JSON.stringify(body) };
  // NOTE: Authorization header for SSE requires polyfill supporting headers
  return { url, ...init } as any;
}
