import { useEffect, useRef, useState } from 'react';
import { View, Text, TextInput, Pressable, FlatList } from 'react-native';
import { SubscriptionBanner } from '../src/components/SubscriptionBanner';
import { StatusBar } from 'expo-status-bar';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { EventSourcePolyfill } from 'event-source-polyfill';
import * as Speech from 'expo-speech';

interface Message { id: string; role: 'user' | 'assistant'; content: string }

const API_BASE = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

export default function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const listRef = useRef<FlatList>(null);

  useEffect(() => {
    (async () => {
      const cached = await AsyncStorage.getItem('chat_cache');
      if (cached) setMessages(JSON.parse(cached));
    })();
  }, []);

  useEffect(() => {
    AsyncStorage.setItem('chat_cache', JSON.stringify(messages));
  }, [messages]);

  const send = async () => {
    const prompt = input.trim();
    if (!prompt) return;
    setInput('');
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: prompt };
    setMessages(prev => [...prev, userMsg]);

    // Streaming via SSE
    setIsTyping(true);
    const assistantId = `${Date.now()}-ai`;
    setMessages(prev => [...prev, { id: assistantId, role: 'assistant', content: '' }]);

    try {
      const es = new EventSourcePolyfill(`${API_BASE}/chat`, {
        headers: { 'Content-Type': 'application/json' },
        payload: JSON.stringify({ message: prompt, stream: true }),
        method: 'POST',
      } as any);
      es.onmessage = (ev) => {
        setMessages(prev => prev.map(m => m.id === assistantId ? { ...m, content: (m.content + ev.data) } : m));
      };
      es.onerror = async () => {
        es.close();
        // Fallback non-streaming
        const r = await fetch(`${API_BASE}/chat`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: prompt, stream: false }),
        });
        const j = await r.json();
        setMessages(prev => prev.map(m => m.id === assistantId ? { ...m, content: j.content } : m));
        setIsTyping(false);
        Speech.speak(j.content, { language: 'en' });
      };
      es.addEventListener('end', () => {
        es.close();
        setIsTyping(false);
      });
    } catch (e) {
      // hard fallback
      const r = await fetch(`${API_BASE}/chat`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: prompt, stream: false }),
      });
      const j = await r.json();
      setMessages(prev => prev.map(m => m.id === assistantId ? { ...m, content: j.content } : m));
      setIsTyping(false);
      Speech.speak(j.content, { language: 'en' });
    }
  };

  return (
    <LinearGradient colors={["#0A0A0A", "#0A0A0A"]} style={{ flex: 1 }}>
      <View style={{ flex: 1, padding: 16, paddingTop: 48 }}>
        <FlatList
          ref={listRef}
          data={messages}
          keyExtractor={item => item.id}
          renderItem={({ item }) => (
            <View style={{
              alignSelf: item.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: item.role === 'user' ? '#1DD1A1' : '#00F0FF',
              borderRadius: 16,
              padding: 12,
              marginVertical: 6,
              maxWidth: '85%'
            }}>
              <Text style={{ color: '#0A0A0A' }}>{item.content}</Text>
            </View>
          )}
          onContentSizeChange={() => listRef.current?.scrollToEnd({ animated: true })}
          onLayout={() => listRef.current?.scrollToEnd({ animated: true })}
        />

        <SubscriptionBanner />

        {isTyping && (
          <Text style={{ color: '#00F0FF', marginBottom: 8 }}>Xish AI is typing...</Text>
        )}

        <View style={{ flexDirection: 'row', gap: 8, alignItems: 'center' }}>
          <TextInput
            value={input}
            onChangeText={setInput}
            placeholder="Type a message"
            placeholderTextColor="#9CA3AF"
            style={{
              flex: 1,
              backgroundColor: '#111',
              color: 'white',
              borderRadius: 12,
              paddingHorizontal: 12,
              paddingVertical: 10,
              borderColor: '#1DD1A1',
              borderWidth: 1,
            }}
          />
          <Pressable onPress={send} style={({ pressed }) => ({
            backgroundColor: pressed ? '#1DD1A1' : 'transparent',
            borderColor: '#1DD1A1', borderWidth: 1, borderRadius: 12, paddingHorizontal: 16, paddingVertical: 10,
          })}>
            <Text style={{ color: '#1DD1A1' }}>Send</Text>
          </Pressable>
        </View>
      </View>
      <StatusBar style="light" />
    </LinearGradient>
  );
}
