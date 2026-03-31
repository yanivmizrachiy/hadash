import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Image, TextInput, ScrollView, Dimensions } from 'react-native';

const PC_INFO_URL = "https://raw.githubusercontent.com/yanivmizrachiy/hadash/main/pc_info.json";

export default function App() {
  const [pcIp, setPcIp] = useState("10.100.102.10"); // ה-IP שקיבלנו מהמחשב שלך
  const [screenUrl, setScreenUrl] = useState(null);
  const [textToSend, setTextToSend] = useState("");

  useEffect(() => {
    // רענון מסך כל חצי שנייה למהירות מקסימלית
    const interval = setInterval(() => {
      setScreenUrl(`http://${pcIp}:5000/screen?t=${Date.now()}`);
    }, 500);
    return () => clearInterval(interval);
  }, [pcIp]);

  const runCmd = (cmd, extra = {}) => {
    fetch(`http://${pcIp}:5000/action`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ cmd, ...extra })
    });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>TITAN MONSTER V5.3</Text>
      
      {/* תצוגת מסך המחשב בשידור חי */}
      <View style={styles.screenContainer}>
        {screenUrl && <Image source={{ uri: screenUrl }} style={styles.liveImage} resizeMode="contain" />}
      </View>

      <ScrollView contentContainerStyle={styles.controls}>
        <TextInput 
          style={styles.input} 
          placeholder="הקלד טקסט למחשב..." 
          placeholderTextColor="#A1887F"
          onChangeText={setTextToSend}
          onSubmitEditing={() => runCmd('type', {text: textToSend})}
        />

        <View style={styles.row}>
          <TouchableOpacity style={[styles.btn3d, {backgroundColor: '#5D4037'}]} onPress={() => runCmd('type', {text: textToSend})}>
            <Text style={styles.btnText}>שלח טקסט</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={[styles.btn3d, {backgroundColor: '#3E2723'}]} onPress={() => runCmd('shutdown')}>
            <Text style={styles.btnText}>כיבוי מחשב</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.status}>סטטוס: מחובר למחשב סלון ✅</Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1B1310', paddingTop: 50 },
  header: { color: '#D2B48C', fontSize: 26, fontWeight: 'bold', textAlign: 'center', marginBottom: 20 },
  screenContainer: { 
    width: '95%', height: 230, alignSelf: 'center', backgroundColor: '#000', 
    borderRadius: 20, borderWidth: 4, borderColor: '#5D4037', overflow: 'hidden', elevation: 20 
  },
  liveImage: { width: '100%', height: '100%' },
  controls: { padding: 20, alignItems: 'center' },
  input: { 
    width: '100%', height: 60, backgroundColor: '#EADDCA', borderRadius: 15, 
    paddingHorizontal: 20, textAlign: 'right', fontSize: 18, marginBottom: 20, borderWidth: 2, borderColor: '#8D6E63' 
  },
  row: { flexDirection: 'row-reverse', justifyContent: 'space-between', width: '100%' },
  btn3d: { 
    width: '48%', height: 80, borderRadius: 15, justifyContent: 'center', alignItems: 'center',
    borderBottomWidth: 6, borderBottomColor: '#2D1A12', elevation: 8, shadowColor: '#000'
  },
  btnText: { color: '#F5F5DC', fontSize: 18, fontWeight: 'bold' },
  status: { color: '#8D6E63', marginTop: 30, fontSize: 14 }
});
