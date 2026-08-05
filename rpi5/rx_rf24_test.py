import os
import sys
import time
import struct

# Set GPIO chip for Raspberry Pi 5 (rp1 chip)
os.environ['RF24_GPIO_CHIP'] = '0'
from RF24 import RF24, RF24_PA_MIN, RF24_250KBPS, RF24_CRC_16

print("🛠️ Initializing Receiver with Ack Payloads on Raspberry Pi 5...")

# Initialize radio with CE=GPIO25 (Pin 22) and CSN=SPI0_CE0 (Pin 24)
radio_rx = RF24(25, 0, 2000000)

if not radio_rx.begin():
    print("❌ Failed to initialize SPI0 on Raspberry Pi 5")
    sys.exit(1)

PIPE_ADDRESS = b"1Node"

# --- REGISTER CONFIGURATION ---
radio_rx.setAutoAck(True)
radio_rx.enableDynamicPayloads()          # Mandatory requirement for Ack Payloads
radio_rx.enableAckPayload()               # Enable responding with payload in ACK
radio_rx.setChannel(108)
radio_rx.setDataRate(RF24_250KBPS)
radio_rx.setPALevel(RF24_PA_MIN)
radio_rx.setCRCLength(RF24_CRC_16)
radio_rx.openReadingPipe(0, PIPE_ADDRESS)

# Pre-load the first ACK payload response for the initial incoming packet
status_code = 200
radio_rx.writeAckPayload(0, struct.pack("i", status_code))

radio_rx.startListening()
radio_rx.printDetails()

print("✅ Receiver ready. Listening on Channel 108...")
print("-" * 60)

try:
    while True:
        if radio_rx.available():
            # Get dynamic payload size
            len_bytes = radio_rx.getDynamicPayloadSize()
            if len_bytes > 0:
                data = radio_rx.read(len_bytes)
                rx_cnt, rx_temp = struct.unpack("if", data)
                print(f"IN <- Packet #{rx_cnt} received | Temp: {rx_temp:.1f}°C")

                # Pre-load response payload for the NEXT packet from transmitter
                status_code += 1
                radio_rx.writeAckPayload(0, struct.pack("i", status_code))

        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nReceiver stopped.")
