#!/usr/bin/env bash
# ==============================================================================
# Automatic Installation Script for pyRF24
# Compatible with Raspberry Pi OS, Debian 11/12/13, and BeagleBone Black
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status

echo "📦 Updating repositories and installing build dependencies..."
sudo apt update
sudo apt install -y git build-essential cmake python3-dev python3-setuptools python3-spidev

TEMP_DIR=$(mktemp -d)
echo "📁 Created temporary directory at $TEMP_DIR"

echo "📥 Cloning official RF24 repository..."
git clone https://github.com/nRF24/RF24.git "$TEMP_DIR/RF24"
cd "$TEMP_DIR/RF24"

echo "⚙️ Compiling native C++ library (Driver: SPIDEV)..."
./configure --driver=SPIDEV
make
sudo make install

echo "🐍 Compiling Python bindings (pyRF24)..."
cd pyRF24
python3 setup.py build

echo "💾 Installing Python wrapper into system..."
# Check for Python 3.11+ to handle PEP 668 externally managed environments
if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
    echo "ℹ️ Python 3.11+ detected. Applying --break-system-packages..."
    sudo python3 setup.py install --break-system-packages
else
    sudo python3 setup.py install
fi

# Cleanup
cd ~
rm -rf "$TEMP_DIR"

echo "----------------------------------------------------"
echo "🧪 Verifying installation..."
if python3 -c "import RF24, spidev" 2>/dev/null; then
    echo "✅ Installation completed successfully! RF24 and spidev are ready."
else
    echo "❌ An error occurred during final verification."
    exit 1
fi
