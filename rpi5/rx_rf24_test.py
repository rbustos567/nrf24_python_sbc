import os
import sys
import time
import struct

os.environ['RF24_GPIO_CHIP'] = '0'
from RF24 import RF24, RF24_PA_MIN, RF24_250KBPS, RF24_CRC_16

print("🛠️ Inicializando RX con Ack Payloads en RPi 5...")

radio_rx = RF24(25, 0, 2000000)

if not radio_rx.begin():
    print("❌ Error al iniciar SPI0 en RPi 5")
    sys.exit(1)

PIPE_ADDRESS = b"1Node"

# --- CONFIGURACIÓN DE REGISTROS ---
radio_rx.setAutoAck(True)
radio_rx.enableDynamicPayloads()          # 👈 REQUISITO OBLIGATORIO PARA ACK PAYLOADS
radio_rx.enableAckPayload()               # Habilita responder con datos en el ACK
radio_rx.setChannel(108)
radio_rx.setDataRate(RF24_250KBPS)
radio_rx.setPALevel(RF24_PA_MIN)
radio_rx.setCRCLength(RF24_CRC_16)
radio_rx.openReadingPipe(0, PIPE_ADDRESS)

# Precargamos la primera respuesta ACK para el primer paquete que reciba
codigo_estado = 200
radio_rx.writeAckPayload(0, struct.pack("i", codigo_estado))

radio_rx.startListening()
radio_rx.printDetails()

print("✅ Receptor listo. Escuchando en canal 108...")
print("-" * 60)
try:
    while True:
        if radio_rx.available():
            # Obtener el tamaño del payload dinámico
            len_bytes = radio_rx.getDynamicPayloadSize()
            if len_bytes > 0:
                datos = radio_rx.read(len_bytes)
                rx_cnt, rx_temp = struct.unpack("if", datos)
                print(f"IN <- Paquete #{rx_cnt} recibido | Temp: {rx_temp:.1f}°C")
                
                # Cargamos la respuesta para el SIGUIENTE paquete que mande la BBB
                codigo_estado += 1
                radio_rx.writeAckPayload(0, struct.pack("i", codigo_estado))

        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nRecepción finalizada.")
