import AsyncStorage from '@react-native-async-storage/async-storage';
import { Image } from 'expo-image';
import { useRouter } from 'expo-router';
import * as WebBrowser from 'expo-web-browser';
import React, { useState } from 'react';
import {
  ActivityIndicator,
  Alert,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { getRedirectUrl, usePlatform } from '../hooks/usePlatform';

WebBrowser.maybeCompleteAuthSession();
const BACKEND_API_URL = process.env.EXPO_PUBLIC_BACKEND_API_URL;
const FRONTEND_URL = process.env.EXPO_PUBLIC_FRONTEND_URL;

const LoginScreen = () => {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { isWeb, isMobile } = usePlatform();
  
  console.log('Backend API URL:', BACKEND_API_URL);
  console.log('Frontend URL:', FRONTEND_URL);
  console.log('Platform:', isWeb ? 'web' : 'mobile');
  
  const handleGoogleLogin = async () => {
    try {
      setLoading(true);

      const redirectUrl = getRedirectUrl();
      console.log('Using redirect URL:', redirectUrl);

      const response = await fetch(`${BACKEND_API_URL}/auth/login?redirect_url=${encodeURIComponent(redirectUrl)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'ngrok-skip-browser-warning': 'true',
        },
      });

      console.log('Auth request made with redirect URL:', redirectUrl);

      if (!response.ok) {
        throw new Error('Failed to get auth URL');
      }

      const data = await response.json();
      const authUrl = data.auth_url[0]; 

      const result = await WebBrowser.openAuthSessionAsync(
        authUrl,
        redirectUrl
      );

      console.log('WebBrowser result:', result);

      if (result.type === 'success' && result.url) {
        console.log('Callback URL received:', result.url);
        const url = new URL(result.url);
        const token = url.searchParams.get('token');
        const error = url.searchParams.get('error');

        if (error) {
          console.log('Authentication error:', error);
          Alert.alert('Erro de Autenticação', 'Ocorreu um erro durante o login. Tente novamente.');
          return;
        }

        if (token) {
          console.log('Token received, saving to storage');
          await AsyncStorage.setItem('access_token', token);
          router.replace('/home');
        } else {
          console.log('No token found in callback URL');
          Alert.alert('Erro', 'Token de acesso não recebido.');
        }
      } else if (result.type === 'cancel') {
        console.log('User cancelled authentication');
      }

    } catch (error) {
      console.error('Login error:', error);
      Alert.alert('Error', 'Failed to start login process. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = () => {
    Alert.alert('Register', 'Registration feature coming soon!');
  };

  const handleDebugMode = () => {
    Alert.alert('Debug', 'Debug mode activated');
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#000" />
      
      <View style={styles.logoContainer}>

            <Image
              source={require('../assets/images/logo.png')}
              style={styles.logoIcon}
            />
  
        <Text style={styles.title}>Trash Kan</Text>
      </View>

      <Text style={styles.subtitle}>
        Gerencie seus resíduos de forma inteligente e sustentável
      </Text>

      <TouchableOpacity
        style={[styles.googleButton, loading && styles.googleButtonDisabled]}
        onPress={handleGoogleLogin}
        disabled={loading}
      >
        <View style={styles.googleButtonContent}>
          {loading ? (
            <ActivityIndicator size="small" color="#333" style={{ marginRight: 15 }} />
          ) : (
            <Image
              source={{ uri: 'https://developers.google.com/identity/images/g-logo.png' }}
              style={styles.googleIcon}
            />
          )}
          <Text style={styles.googleButtonText}>
            {loading ? 'Conectando...' : 'Continuar com Google'}
          </Text>
        </View>
      </TouchableOpacity>

      <View style={styles.registerContainer}>
        <Text style={styles.registerText}>Não tem uma conta? </Text>
        <TouchableOpacity onPress={handleRegister}>
          <Text style={styles.registerLink}>Cadastre-se</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.debugLink} onPress={handleDebugMode}>
        <Text style={styles.debugLinkText}>Debug Mode</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  logoIcon: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#333',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#fff',
    lineHeight: 50,
  },
  subtitle: {
    fontSize: 16,
    color: '#999',
    marginBottom: 40,
    textAlign: 'center',
  },
  googleButton: {
    width: '100%',
    backgroundColor: '#fff',
    borderRadius: 25,
    paddingVertical: 15,
    marginBottom: 30,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  googleButtonDisabled: {
    backgroundColor: '#f0f0f0',
    opacity: 0.7,
  },
  googleButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  googleIcon: {
    width: 24,
    height: 24,
    marginRight: 15,
  },
  googleButtonText: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
  },
  registerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 40,
  },
  registerText: {
    color: '#999',
    fontSize: 14,
  },
  registerLink: {
    color: '#4CAF50',
    fontSize: 14,
    fontWeight: '500',
  },
  debugLink: {
    marginTop: 20,
  },
  debugLinkText: {
    color: '#666',
    fontSize: 12,
    textDecorationLine: 'underline',
  },
});

export default LoginScreen;
