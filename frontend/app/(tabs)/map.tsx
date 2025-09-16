// import React, { useEffect, useState } from 'react';
// import { View, StyleSheet, ActivityIndicator } from 'react-native';
// import MapView, { Marker } from 'react-native-maps';
// import * as Location from 'expo-location';

// export default function MapScreen() {
//   const [location, setLocation] = useState<any>(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     (async () => {
//       let { status } = await Location.requestForegroundPermissionsAsync();
//       if (status !== 'granted') {
//         console.log('Permissão de localização negada');
//         return;
//       }

//       let currentLocation = await Location.getCurrentPositionAsync({});
//       setLocation(currentLocation.coords);
//       setLoading(false);
//     })();
//   }, []);

//   if (loading) {
//     return (
//       <View style={styles.loadingContainer}>
//         <ActivityIndicator size="large" color="green" />
//       </View>
//     );
//   }

//   return (
//     <MapView
//       style={styles.map}
//       initialRegion={{
//         latitude: location.latitude,
//         longitude: location.longitude,
//         latitudeDelta: 0.01,
//         longitudeDelta: 0.01,
//       }}
//     >
//       {/* Marcador do usuário */}
//       <Marker
//         coordinate={{ latitude: location.latitude, longitude: location.longitude }}
//         title="Você está aqui"
//         pinColor="green"
//       />

//       {/* Exemplo de ponto de coleta */}
//       <Marker
//         coordinate={{ latitude: location.latitude + 0.001, longitude: location.longitude + 0.001 }}
//         title="Ponto de Coleta"
//         description="Coleta de vidro"
//       />
//     </MapView>
//   );
// }

// const styles = StyleSheet.create({
//   map: { flex: 1 },
//   loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
// });
