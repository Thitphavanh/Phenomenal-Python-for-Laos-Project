#!/bin/bash
# Script to install qrcode in virtual environment

echo "Installing qrcode and pillow in virtual environment..."

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: Virtual environment is not activated!"
    echo "Please activate your virtual environment first:"
    echo "   source venv/bin/activate"
    exit 1
fi

echo "✅ Virtual environment detected: $VIRTUAL_ENV"
echo ""

# Install qrcode with pillow support
echo "Installing packages..."
pip install qrcode[pil]

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import qrcode; print('✅ qrcode imported successfully')" && \
python -c "from PIL import Image; print('✅ Pillow imported successfully')"

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now run your Django server:"
echo "   python manage.py runserver"
