# nRF24L01+ Python Examples for Linux SBCs (Raspberry Pi 3/5 & BeagleBone Black)

This repository provides clean Python examples for sending and receiving data using the **nRF24L01+** 2.4 GHz RF transceiver module across different Single Board Computers (SBCs) via the official **`RF24` Python wrapper (`pyRF24`)**.

Note: I have noticed that some nRF24L01+ work as either only Transmitter or Receiver. Therefore, identify which is which, and you can only run one direction communication between two SBCs. Also, I was able to transmit messages between rpi and BBB.

---

## 📁 Repository Structure

```bash
nrf24_python_sbc/
├── README.md
├── install_rf24_python_lib.sh
├── rpi5/
│   ├── tx_rf24_test.py
│   └── rx_rf24_test.py
└── bbb/
    ├── tx_rf24_test.py
    └── rx_rf24_test.py
```

## 🔌 Hardware Wiring (Pinout Guides)
Important: It is strongly recommended to use the nRF24L01+ Adapter Module (with an on-board AMS1117 3.3V regulator and decoupling capacitors) to ensure power stability. Connect VCC of the adapter module to 5V.
```bash
nRF24L01+ Power Adapter Pinout
             ┌───────────────┐
       GND  ─┤ [1]       [2] ├─ VCC (5V Input)
        CE  ─┤ [3]       [4] ├─ CSN
       SCK  ─┤ [5]       [6] ├─ MOSI
      MISO  ─┤ [7]       [8] ├─ IRQ (Unused)
             └───────────────┘
```

## 🍓 1. Raspberry Pi 3 & Raspberry Pi 5 (`/dev/spidev0.0`)

| nRF24L01+ | RPi Physical Pin (40-pin Header) | Function / Signal |
| :--- | :--- | :--- |
| **VCC** | **Pin 2** or **Pin 4** | **5V Power** |
| **GND** | **Pin 6** | **Ground** |
| **CE** | **Pin 22** | **GPIO 25** |
| **CSN** | **Pin 24** | **GPIO 8 (SPI0_CE0)** |
| **SCK** | **Pin 23** | **GPIO 11 (SPI0_SCLK)** |
| **MOSI** | **Pin 19** | **GPIO 10 (SPI0_MOSI)** |
| **MISO** | **Pin 21** | **GPIO 9 (SPI0_MISO)** |

---

## 🦴 2. BeagleBone Black (`/dev/spidev1.0` - Header P9)

| nRF24L01+ | BBB Physical Pin (Header P9) | Function / Signal |
| :--- | :--- | :--- |
| **VCC** | **P9_07** or **P9_08** | **SYS_5V (5V Power)** |
| **GND** | **P9_01** or **P9_02** | **DGND (Ground)** |
| **CE** | **P9_12** | **GPIO1_28** |
| **CSN** | **P9_28** | **SPI1_CS0** |
| **SCK** | **P9_31** | **SPI1_SCLK** |
| **MOSI** | **P9_30** | **SPI1_D1 (MOSI)** |
| **MISO** | **P9_29** | **SPI1_D0 (MISO)** |

## 🚀 Execution

# Raspberry Pi 3 / 5:
```bash
# Terminal 1 - SBC with nRF24L01+ Receiver
sudo python3 rx_rf24_test.py

# Terminal 2 - SBC with nRF24L01+ Transmitter
sudo python3 tx_rf24_test.py
```

# BeagleBone Black:
```bash
# Terminal 1 - SBC with nRF24L01+ Receiver
sudo python3 rx_rf24_test.py

# Terminal 2 - SBC with nRF24L01+ Transmitter
sudo python3 tx_rf24_test.py
```

## 🛠️ Troubleshooting
If you experience lost packets or connection timeouts:

1. Ensure the RF24 Python module is properly imported: python3 -c "import RF24".
2. Verify that SPI is enabled in raspi-config (Raspberry Pi) or via Device Tree Overlays in /boot/uEnv.txt (BeagleBone Black).
