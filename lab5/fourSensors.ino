Adafruit_GPS GPS;
PulseOximeter pox;

int sound_val = 0;

void setup() { 
	// put your setup code here, to run once:
    //temperature
    pinMode(A1, INPUT);

    // vitals
    pinMode(2, INPUT);
    pinMode(3, OUTPUT);

    // sound
    pinMode(7, INPUT);
    pinMode(13, OUTPUT);

    Serial.begin(9600);
}

void loop() { 
	// put your main code here, to run repeatedly:
    float temp = analogRead(A1) / 1023.0 * 5.0 * 100.0;
    Serial.println("temperature: " + to_string(temp));
    delay(1000);

    // sound
    sound_val = digitalRead(7);
    if (sound_val == HIGH) {
        digitalWrite(13, HIGH);
    } else {
        Serial.println(sound_val);
        digitalWrite(13, LOW);
    }
    delay(100);
    
    if (Serial.available() > 0) {
        // GPS
        string gpsResult = GPS.read();
        Serial.println(gpsResult);

        // vitals
        if (pox.begin()) {
            string spO2_res = pox.getSpO2();
            string hb_res = pox.getHeartRate();
            Serial.println("Oxygen percentage: " + spO2_res + "; Heart rate: " + hb_res);
        }
        digitalWrite(3, HIGH);
    } else {
      Serial.write("No data");
      digitalWrite(3, LOW);
    }
    delay(1000);
}
