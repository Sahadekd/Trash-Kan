import { View, Text, Button, StyleSheet } from 'react-native';
import { Link } from 'expo-router';

export default function Home() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Selecione o tipo de lixo</Text>
      <Link href="/map">
        <Button title="Vidro" />
      </Link>
      <Link href="/map">
        <Button title="Metal" />
      </Link>
      <Link href="/map">
        <Button title="Papel" />
      </Link>
      <Link href="/map">
        <Button title="Plástico" />
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, marginBottom: 20 }
});
