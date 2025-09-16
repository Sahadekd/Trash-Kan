import AsyncStorage from '@react-native-async-storage/async-storage';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useEffect } from 'react';
import { ActivityIndicator, Alert, StyleSheet, Text, View } from 'react-native';

const AuthCallbackScreen = () => {
  const router = useRouter();
  const { token, error } = useLocalSearchParams<{
    token?: string;
    error?: string;
  }>();

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        if (error) {
          Alert.alert('Erro de Autenticação', 'Ocorreu um erro durante o login. Tente novamente.');
          router.replace('/login');
          return;
        }

        if (token && typeof token === 'string') {
          await AsyncStorage.setItem('access_token', token);
          
          router.replace('/home');
        } else {
          Alert.alert('Erro', 'Token de acesso não recebido.');
          router.replace('/login');
        }
      } catch (storageError) {
        console.error('Error saving token:', storageError);
        Alert.alert('Erro', 'Falha ao salvar dados de autenticação.');
        router.replace('/login');
      }
    };

    handleAuthCallback();
  }, [token, error, router]);

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#4CAF50" />
      <Text style={styles.text}>Processando autenticação...</Text>
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
  text: {
    color: '#fff',
    fontSize: 16,
    marginTop: 20,
    textAlign: 'center',
  },
});

export default AuthCallbackScreen;