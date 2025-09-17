import { Link } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';

export default function Home() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Selecione o tipo de lixo</Text>
      <View style={styles.buttonsContainer}>
        <Link href="/map" asChild>
          <Pressable style={styles.glassButton}>
            <Text style={styles.buttonText}>Vidro</Text>
          </Pressable>
        </Link>
        <Link href="/map" asChild>
          <Pressable style={styles.metalButton}>
            <Text style={styles.buttonText}>Metal</Text>
          </Pressable>
        </Link>
        <Link href="/map" asChild>
          <Pressable style={styles.paperButton}>
            <Text style={styles.buttonText}>Papel</Text>
          </Pressable>
        </Link>
        <Link href="/map" asChild>
          <Pressable style={styles.plasticButton}>
            <Text style={styles.buttonText}>Plástico</Text>
          </Pressable>
        </Link>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 24,
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    marginBottom: 32,
    color: '#333',
    textAlign: 'center',
  },
  buttonsContainer: {
    width: '100%',
    gap: 18,
  },
  button: {
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 0,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    letterSpacing: 1,
  },
  glassButton: {
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 0,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    backgroundColor: '#0F7B0F',
  },
  metalButton: {
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 0,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    backgroundColor: '#FFB000',
  },
  paperButton: {
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 0,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    backgroundColor: '#1976D2',
  },
  plasticButton: {
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 0,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    backgroundColor: '#DC143C',
  },
});
