import { View, Text, Pressable } from 'react-native';
import { logEvent } from '../services/analytics';

export function SubscriptionBanner() {
  return (
    <View style={{ borderColor: '#00F0FF', borderWidth: 1, borderRadius: 14, padding: 12, marginVertical: 8 }}>
      <Text style={{ color: 'white', marginBottom: 8 }}>Upgrade to Xish AI Pro for faster responses and custom voices.</Text>
      <Pressable onPress={() => logEvent('subscription_click')}
        style={{ borderColor: '#1DD1A1', borderWidth: 1, borderRadius: 10, paddingVertical: 8, alignItems: 'center' }}>
        <Text style={{ color: '#1DD1A1' }}>See Plans</Text>
      </Pressable>
    </View>
  );
}
