import os
import sys
import time
import struct

os.environ['RF24_GPIO_CHIP'] = '0'
from RF24 import RF24, RF24_PA_MIN, RF24_250KBPS, RF24_CRC_16, RF24_PA_LOW, RF24_1MBPS

print("🛠️ Inicializando TX con Ack Payloads en BeagleBone...")

radio_tx = RF24(25, 0, 2000000)

if not radio_tx.begin():
    print("❌ Error al iniciar SPI0 en BBB")
    sys.exit(1)

PIPE_ADDRESS = b"1Node"

# --- CONFIGURACIÓN DE REGISTROS ---
radio_tx.setAutoAck(True)
radio_tx.enableDynamicPayloads()          # 👈 REQUISITO OBLIGATORIO PARA ACK PAYLOADS
radio_tx.enableAckPayload()               # Habilita recibir datos en el ACK
radio_tx.setRetries(15, 15)               # 15 reintentos con 1500us entre cada uno
radio_tx.setChannel(108)
radio_tx.setDataRate(RF24_250KBPS)
radio_tx.setPALevel(RF24_PA_MIN)
radio_tx.setCRCLength(RF24_CRC_16)
radio_tx.openWritingPipe(PIPE_ADDRESS)
radio_tx.stopListening()
radio_tx.printDetails()

print("✅ Transmisor listo y configurado.")
print("-" * 60)

contador = 0
try:
    while True:
        temp_simulada = 24.0 + (contador % 5)
        payload = struct.pack("if", contador, temp_simulada)
        
        # Enviar datos
        exito = radio_tx.write(payload)
        
        if exito:
            if radio_tx.isAckPayloadAvailable():
                ack_datos = radio_tx.read(4)
                codigo_rx = struct.unpack("i", ack_datos)[0]
                print(f"OUT -> Paquete #{contador} enviado | 🎉 ACK RECIBIDO de RPi5 (Respuesta: {codigo_rx})")
            else:
                print(f"OUT -> Paquete #{contador} enviado | ✅ ACK simple recibido (Sin payload)")
        else:
            print(f"⚠️ -> Paquete #{contador} FALLÓ (No llegó el ACK de la RPi5)")

        contador += 1
        time.sleep(0.1)  # Enviar cada 100 ms

except KeyboardInterrupt:
    print("\nTransmisión finalizada.")
