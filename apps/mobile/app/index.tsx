import { Link } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { StatusBar } from 'expo-status-bar';
import { useFonts, Poppins_400Regular, Poppins_600SemiBold, Poppins_700Bold } from '@expo-google-fonts/poppins';
import { Text, View, Pressable } from 'react-native';

export default function Home() {
  const [loaded] = useFonts({ Poppins_400Regular, Poppins_600SemiBold, Poppins_700Bold });
  if (!loaded) return null;

  return (
    <LinearGradient colors={["#0A0A0A", "#0A0A0A"]} style={{ flex: 1 }}>
      <View style={{ flex: 1, padding: 24, justifyContent: 'space-between' }}>
        <View style={{ marginTop: 80 }}>
          <Text style={{ color: '#00F0FF', fontFamily: 'Poppins_700Bold', fontSize: 36 }}>Xish AI ⚡</Text>
          <Text style={{ color: 'white', fontFamily: 'Poppins_400Regular', fontSize: 16, marginTop: 12 }}>
            Your personal AI companion — built by one, made for all.
          </Text>
        </View>

        <View style={{ gap: 16 }}>
          <Link href="/chat" asChild>
            <Pressable style={({ pressed }) => ({
              backgroundColor: pressed ? '#1DD1A1' : 'transparent',
              borderColor: '#1DD1A1',
              borderWidth: 1,
              borderRadius: 14,
              paddingVertical: 16,
              alignItems: 'center',
              shadowColor: '#1DD1A1',
              shadowOpacity: pressed ? 0.8 : 0.4,
              shadowRadius: 10,
            })}>
              <Text style={{ color: '#1DD1A1', fontFamily: 'Poppins_600SemiBold', fontSize: 18 }}>Start Chatting</Text>
            </Pressable>
          </Link>

          <View style={{ alignItems: 'center' }}>
            <Text style={{ color: '#00F0FF', fontFamily: 'Poppins_400Regular' }}>Voice, memory, streaming typing, and more.</Text>
          </View>
        </View>

        <View style={{ marginBottom: 16, opacity: 0.9 }}>
          <Text style={{ color: 'white' }}>GitHub • Instagram • LinkedIn • Contact • Privacy Policy</Text>
        </View>
      </View>
      <StatusBar style="light" />
    </LinearGradient>
  );
}
