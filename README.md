# nRF24L01+ Python Examples for Linux SBCs (Raspberry Pi 3/5 & BeagleBone Black)

This repository provides clean Python examples for sending and receiving data using the **nRF24L01+** 2.4 GHz RF transceiver module across different Single Board Computers (SBCs) via the official **`RF24` Python wrapper (`pyRF24`)**.

Note: As of now, I have been able to make work the nRF24L01+ modules as either only Transmitter or Receiver, but never the same one as both. Therefore, identify which is which, and you can only run one direction communication between two SBCs. Also, I was able to transmit messages between rpi and BBB.

---

## ⚙️ Prerequisites & System Configuration

Before running the scripts, you must ensure that the SPI hardware interface is enabled on your board and that the required Python library is installed.

---

### 1. Enabling & Verifying SPI Hardware Interface

#### 🍓 Raspberry Pi (3B+ / 5)

```text
How to Enable SPI:

1. Open the Raspberry Pi configuration tool:
   ```bash
   sudo raspi-config

2. Navigate to Interface Options -> SPI.
3. Select Yes when asked if you want the SPI interface to be enabled.
4. Reboot your board to apply the changes:
sudo reboot now

How to Verify:
Run the following command to check if the SPI device nodes are created:

ls -l /dev/spidev*

Expected Output:

crw-rw---- 1 root spi 153, 0 Aug  4 21:00 /dev/spidev0.0
crw-rw---- 1 root spi 153, 1 Aug  4 21:00 /dev/spidev0.1

```

#### 🦴 BeagleBone Black

```text
How to Enable SPI1:

On recent Debian distributions (11/12/13), SPI1 can be enabled via Device Tree Overlays in /boot/uEnv.txt.

1. Open /boot/uEnv.txt in a text editor:
sudo nano /boot/uEnv.txt

2. Locate the line starting with uboot_overlay_addr or enable_uboot_overlays=1 and ensure SPI1 is enabled:
uboot_overlay_addr4=/lib/firmware/BB-SPI1-00A0.dtbo
(Alternatively, if using uboot_overlay_pru, add uboot_overlay_addr4=/lib/firmware/BB-SPIDEV1-00A0.dtbo)

3. Save the file and reboot the BeagleBone Black:
sudo reboot

How to Verify:
Verify that the spidev1 nodes appear in /dev:

ls -l /dev/spidev1.*

Expected Output:

crw-rw---- 1 root spi 153, 0 Aug  4 21:00 /dev/spidev1.0
crw-rw---- 1 root spi 153, 1 Aug  4 21:00 /dev/spidev1.1
```

### Installing the RF24 Python Library

```text
An installation script install_rf24_python_lib.sh is provided in the repository to automate building the C++ RF24 core library with SPIDEV support and compiling its Python wrapper (pyRF24).

1. Make the script executable:
chmod +x install_rf24_python_lib.sh

2. Run the installation script:
./install_rf24_python_lib.sh

3. Verify that Python can import the RF24 module without errors:
python3 -c "import RF24; print('✅ pyRF24 installed successfully!')"
```

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
<img width="2064" height="1185" alt="raspberry-pi-5-gpio-pinout-diagram" src="https://github.com/user-attachments/assets/d86e6ee5-1cff-456e-99ff-df1ba5a1b983" />

## 🦴 2. BeagleBone Black (`/dev/spidev1.0` - Header P9)

| nRF24L01+ | BBB Physical Pin (Header P9) | Function / Signal |
| :--- | :--- | :--- |
| **VCC** | **P9_05** or **P9_06** | **VDD_5V (5V Power)** |
| **GND** | **P9_01** or **P9_02** | **DGND (Ground)** |
| **CE** | **P9_12** | **GPIO_60** |
| **CSN** | **P9_17** | **SPI0_CS0** |
| **SCK** | **P9_22** | **SPI0_SCLK** |
| **MOSI** | **P9_18** | **SPI0_D1** |
| **MISO** | **P9_21** | **SPI0_D0** |

---
<img width="1194" height="901" alt="beaglebone-black-pinout" src="https://github.com/user-attachments/assets/2fd2aacb-a9e1-4415-9091-475de16d660a" />

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
