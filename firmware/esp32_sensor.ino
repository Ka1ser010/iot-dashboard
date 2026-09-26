

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

const char* WIFI_SSID     = "WIFI_HERE";
const char* WIFI_PASSWORD = "PASSWORD_HERE";
const char* SERVER_URL = "http://192.168.1.100:8000/readings/";

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const unsigned long INTERVAL_MS = 10000;
unsigned long lastSend = 0;

void connectWiFi() {
  Serial.print("Conectando ao WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado! IP do ESP32: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  connectWiFi();
}

void sendReading(float temperature, float humidity) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi caiu, tentando reconectar...");
    connectWiFi();
    return;
  }

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"temperature\": " + String(temperature, 1) +
                    ", \"humidity\": " + String(humidity, 1) + "}";

  int responseCode = http.POST(payload);

  if (responseCode > 0) {
    Serial.printf("Enviado! Código de resposta: %d\n", responseCode);
  } else {
    Serial.printf("Erro ao enviar: %s\n", http.errorToString(responseCode).c_str());
  }

  http.end();
}

void loop() {
  if (millis() - lastSend >= INTERVAL_MS) {
    lastSend = millis();

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Falha ao ler o sensor DHT22 (confira a fiação).");
      return;
    }

    Serial.printf("Temp: %.1f C | Umidade: %.1f%%\n", temperature, humidity);
    sendReading(temperature, humidity);
  }
}
