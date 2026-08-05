import os
import sys
import time
import struct

os.environ['RF24_GPIO_CHIP'] = '1'
from RF24 import RF24, RF24_PA_MIN, RF24_250KBPS, RF24_CRC_16

print("🛠️ Initializing Transmitter with Ack Payloads on BeagleBone...")

# Initialize radio with CE=GPIO1_28 (Pin P9_12) and CSN on SPI1_CS0
radio_tx = RF24(28, 0, 2000000)

if not radio_tx.begin():
    print("❌ Failed to initialize SPI interface on BeagleBone Black")
    sys.exit(1)

PIPE_ADDRESS = b"1Node"

# --- REGISTER CONFIGURATION ---
radio_tx.setAutoAck(True)
radio_tx.enableDynamicPayloads()          # Mandatory requirement for Ack Payloads
radio_tx.enableAckPayload()               # Enable receiving custom payload data in ACK
radio_tx.setRetries(15, 15)               # 15 retries with 1500us delay between attempts
radio_tx.setChannel(108)
radio_tx.setDataRate(RF24_250KBPS)
radio_tx.setPALevel(RF24_PA_MIN)
radio_tx.setCRCLength(RF24_CRC_16)
radio_tx.openWritingPipe(PIPE_ADDRESS)
radio_tx.stopListening()
radio_tx.printDetails()

print("✅ Transmitter ready and configured.")
print("-" * 60)

counter = 0
try:
    while True:
        simulated_temp = 24.0 + (counter % 5)
        payload = struct.pack("if", counter, simulated_temp)
        
        # Send payload to receiver
        success = radio_tx.write(payload)
        
        if success:
            if radio_tx.isAckPayloadAvailable():
                ack_data = radio_tx.read(4)
                rx_code = struct.unpack("i", ack_data)[0]
                print(f"OUT -> Packet #{counter} sent | 🎉 ACK RECEIVED (Response payload: {rx_code})")
            else:
                print(f"OUT -> Packet #{counter} sent | ✅ Standard ACK received (No payload)")
        else:
            print(f"⚠️ -> Packet #{counter} FAILED (No ACK received from peer)")

        counter += 1
        time.sleep(0.1)  # Send packet every 100 ms

except KeyboardInterrupt:
    print("\nTransmitter stopped.")
