# Dashboard IoT — Sensor ESP32 (temperatura e umidade)

Pipeline completo: ESP32 com sensor DHT22 → backend FastAPI → dashboard
web com gráfico em tempo real.

## Estrutura

```
firmware/
└── esp32_sensor.ino   # código real, para gravar no ESP32 (Arduino IDE)
backend/
├── app/
│   ├── main.py          # API que recebe e serve as leituras
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── requirements.txt
└── simulate_esp32.py    # "ESP32 virtual" — testa tudo sem hardware
dashboard/
└── index.html            # abre direto no navegador, sem servidor extra
```

## Como testar AGORA, sem hardware nenhum

```bash
# 1. Instalar dependências do backend
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Subir o backend
uvicorn app.main:app --reload
```

Com o backend rodando, abra **dois** terminais adicionais:

**Terminal 2** — abra `dashboard/index.html` direto no navegador (duplo clique no arquivo).

**Terminal 3** — dispare o ESP32 virtual para simular leituras chegando:
```bash
cd backend
python simulate_esp32.py
```

Volte pro navegador: o gráfico deve começar a se popular sozinho, a cada
poucos segundos, com temperatura e umidade "fake" mas realistas.

## Como usar com o ESP32 de verdade

1. Abra `firmware/esp32_sensor.ino` no Arduino IDE.
2. Instale as bibliotecas indicadas no topo do arquivo.
3. Troque `WIFI_SSID`, `WIFI_PASSWORD` e `SERVER_URL` pelos seus dados
   (o `SERVER_URL` deve apontar pro IP do computador rodando o backend
   na sua rede local — **não** use `127.0.0.1` aqui, isso aponta pro
   próprio ESP32).
4. Monte o circuito: DHT22 → VCC (3.3V), GND (GND), DATA (GPIO 4).
5. Grave o firmware e abra o Monitor Serial (115200 baud) para
   acompanhar as leituras sendo enviadas.
6. O dashboard vai mostrar dados reais no lugar dos simulados —
   nenhuma linha de código do backend ou do dashboard precisa mudar.

## Roadmap (próximos passos)

- [x] Fase 1 — ESP32 lendo sensor + enviando via HTTP + dashboard básico
- [ ] Fase 2 — Trocar HTTP por MQTT (mais próximo do padrão industrial)
- [ ] Fase 3 — Alerta automático quando passar de um limite configurável
- [ ] Fase 4 — Persistir em PostgreSQL (reaproveitando o Projeto 2)
