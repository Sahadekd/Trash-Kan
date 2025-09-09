import { View, Text, Button, StyleSheet } from 'react-native';
import { Link } from 'expo-router';

export default function Login() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>TrashKan</Text>
      <Link href="/(tabs)/home">
        <Button title="Entrar" />
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 32, fontWeight: 'bold' }
});
