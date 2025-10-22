import { ReactNode, createContext, useContext, useEffect, useState } from 'react';
import { supabase } from '../services/supabase';

interface AuthContextValue {
  isAuthed: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthContextValue>({ isAuthed: false, loading: true });

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthed, setAuthed] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      setAuthed(!!data.session);
      setLoading(false);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_event, session) => {
      setAuthed(!!session);
    });
    return () => { sub.subscription.unsubscribe(); };
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthed, loading }}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
