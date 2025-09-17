import Constants from 'expo-constants';
import { Platform } from 'react-native';

export const usePlatform = () => {
  const isWeb = Platform.OS === 'web';
  const isMobile = Platform.OS === 'ios' || Platform.OS === 'android';
  
  return {
    isWeb,
    isMobile,
    platform: Platform.OS
  };
};

export const getRedirectUrl = () => {
  if (Platform.OS === 'web') {
    // Para web, usa localhost
    return `${process.env.EXPO_PUBLIC_FRONTEND_URL}/auth-callback`;
  } else {
    // Para mobile, verificar se é Expo Go ou development build
    const isExpoGo = Constants.appOwnership === 'expo';

    if (isExpoGo) {
      // No Expo Go, usar o scheme expo padrão com IP do manifest
      const manifest = Constants.expoConfig || Constants.manifest;
      const hostname = manifest?.hostUri?.split(':')[0] || '192.168.0.121';
      const redirectUrl = `exp://${hostname}:8081/--/auth-callback`;
      console.log('Using Expo Go redirect URL:', redirectUrl);
      return redirectUrl;
    } else {
      const redirectUrl = 'trashkan://auth-callback';
      console.log('Using custom scheme redirect URL:', redirectUrl);
      return redirectUrl;
    }
  }
};