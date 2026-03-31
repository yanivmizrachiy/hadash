import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Image, TextInput, Dimensions, TouchableWithoutFeedback, ScrollView } from 'react-native';

const PC_IP = "10.100.102.10";

export default function App() {
  const [screenUrl, setScreenUrl] = useState(`http://${PC_IP}:5000/screen`);
  const [text, setText] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      setScreenUrl(`http://${PC_IP}:5000/screen?t=${Date.now()}`);
    }, 350);
    return () => clearInterval(interval);
  }, []);

  const run = (cmd, extra = {}) => {
    fetch(`http://${PC_IP}:5000/action`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ cmd, ...extra })
    });
  };

  const onTouch = (e) => {
    const { locationX, locationY } = e.nativeEvent;
    run('click', { x: locationX / (Dimensions.get('window').width * 0.95), y: locationY / 230 });
  };

  return (
    <View style={styles.c}>
      <Text style={styles.h}>TITAN MONSTER PRO</Text>
      <TouchableWithoutFeedback onPress={onTouch}>
        <View style={styles.f}><Image source={{ uri: screenUrl }} style={styles.i} resizeMode="stretch" /></View>
      </TouchableWithoutFeedback>
      <ScrollView style={styles.u}>
        <TextInput style={styles.in} placeholder="הקלד למחשב..." value={text} onChangeText={setText} textAlign="right" />
        <TouchableOpacity style={styles.b} onPress={() => { run('type', {text}); setText(""); }}><Text style={styles.bt}>שלח טקסט</Text></TouchableOpacity>
        <View style={styles.r}>
          <TouchableOpacity style={styles.bs} onPress={() => run('vol_up')}><Text style={styles.bt}>🔊 +</Text></TouchableOpacity>
          <TouchableOpacity style={styles.bs} onPress={() => run('vol_down')}><Text style={styles.bt}>🔉 -</Text></TouchableOpacity>
          <TouchableOpacity style={styles.bs} onPress={() => run('play_pause')}><Text style={styles.bt}>⏯️</Text></TouchableOpacity>
        </View>
        <TouchableOpacity style={[styles.b, {backgroundColor: '#3E2723'}]} onPress={() => run('shutdown')}><Text style={styles.bt}>🛑 כיבוי PC</Text></TouchableOpacity>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  c: { flex: 1, backgroundColor: '#1B1310', paddingTop: 50, alignItems: 'center' },
  h: { color: '#D2B48C', fontSize: 26, fontWeight: 'bold', marginBottom: 20 },
  f: { width: '95%', height: 230, borderRadius: 15, borderWidth: 3, borderColor: '#5D4037', overflow: 'hidden', backgroundColor: '#000' },
  i: { width: '100%', height: '100%' },
  u: { width: '100%', padding: 20 },
  in: { backgroundColor: '#EADDCA', borderRadius: 12, padding: 15, fontSize: 18, marginBottom: 10 },
  b: { backgroundColor: '#8B4513', padding: 18, borderRadius: 15, alignItems: 'center', marginBottom: 15, borderBottomWidth: 6, borderBottomColor: '#3E2723' },
  bs: { backgroundColor: '#6D4C41', width: '30%', padding: 15, borderRadius: 12, alignItems: 'center', borderBottomWidth: 5, borderBottomColor: '#3E2723' },
  r: { flexDirection: 'row-reverse', justifyContent: 'space-between', marginBottom: 15 },
  bt: { color: '#F5F5DC', fontWeight: 'bold', fontSize: 18 }
});
