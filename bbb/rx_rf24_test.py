import os
import sys
import time
import struct

os.environ['RF24_GPIO_CHIP'] = '1'
from RF24 import RF24, RF24_PA_MIN, RF24_250KBPS, RF24_CRC_16

print("🛠️ Initializing Receiver with Ack Payloads on BeagleBone...")

# Initialize radio with CE=GPIO1_28 (Pin P9_12) and CSN on SPI1_CS0
radio_rx = RF24(28, 0, 2000000)

if not radio_rx.begin():
    print("❌ Failed to initialize SPI interface on BeagleBone Black")
    sys.exit(1)

PIPE_ADDRESS = b"1Node"

# --- REGISTER CONFIGURATION ---
radio_rx.enableDynamicPayloads()          # Mandatory requirement for Ack Payloads
radio_rx.enableAckPayload()               # Enable attaching custom payload data in ACK
radio_rx.setChannel(108)
radio_rx.setDataRate(RF24_250KBPS)
radio_rx.setPALevel(RF24_PA_MIN)
radio_rx.setCRCLength(RF24_CRC_16)
radio_rx.openReadingPipe(0, PIPE_ADDRESS)

# Pre-load the first ACK response payload for the very first incoming packet
status_code = 200
radio_rx.writeAckPayload(0, struct.pack("i", status_code))

radio_rx.startListening()
radio_rx.printDetails()

print("✅ Receiver ready. Listening on Channel 108...")
print("-" * 60)

try:
    while True:
        if radio_rx.available():
            # Get the size of the incoming dynamic payload
            len_bytes = radio_rx.getDynamicPayloadSize()
            if len_bytes > 0:
                raw_data = radio_rx.read(len_bytes)
                rx_cnt, rx_temp = struct.unpack("if", raw_data)
                print(f"IN <- Packet #{rx_cnt} received | Temp: {rx_temp:.1f}°C")

                # Pre-load response payload for the NEXT incoming packet from transmitter
                status_code += 1
                radio_rx.writeAckPayload(0, struct.pack("i", status_code))

        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nReceiver stopped.")
