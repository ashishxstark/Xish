import { useState } from 'react';
import { View, Text, TextInput, Pressable } from 'react-native';
import { supabase } from '../../src/services/supabase';
import { Link, useRouter } from 'expo-router';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const submit = async () => {
    setError('');
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) setError(error.message); else router.replace('/chat');
  };

  return (
    <View style={{ flex: 1, backgroundColor: '#0A0A0A', padding: 24, gap: 12, paddingTop: 80 }}>
      <Text style={{ color: '#00F0FF', fontSize: 28, fontWeight: '700' }}>Sign in</Text>
      {!!error && <Text style={{ color: 'tomato' }}>{error}</Text>}
      <TextInput value={email} onChangeText={setEmail} placeholder="Email" autoCapitalize='none' keyboardType='email-address' placeholderTextColor='#9CA3AF' style={{ backgroundColor: '#111', color: 'white', borderRadius: 12, padding: 12 }} />
      <TextInput value={password} onChangeText={setPassword} placeholder="Password" secureTextEntry placeholderTextColor='#9CA3AF' style={{ backgroundColor: '#111', color: 'white', borderRadius: 12, padding: 12 }} />
      <Pressable onPress={submit} style={{ backgroundColor: 'transparent', borderColor: '#1DD1A1', borderWidth: 1, borderRadius: 12, padding: 12, alignItems: 'center' }}>
        <Text style={{ color: '#1DD1A1' }}>Sign in</Text>
      </Pressable>
      <Link href="/(auth)/sign-up" style={{ color: '#00F0FF', marginTop: 12 }}>Create an account</Link>
    </View>
  );
}
