export type EventName = 'app_open' | 'chat_sent' | 'subscription_click';

export function logEvent(name: EventName, params?: Record<string, any>) {
  // Privacy-friendly placeholder analytics
  console.log('[analytics]', name, params ?? {});
}
