# Real-Time Speech Translation

A real-time speech-to-speech translation system that listens to English speech, translates it to Spanish, and speaks the translation back using text-to-speech.

## Features

- 🎤 **Real-time speech recognition** using RealtimeSTT
- 🌐 **Offline translation** using Argos Translate (English → Spanish)
- 🔊 **Text-to-speech output** using Piper TTS
- 🧹 **Clean console output** with suppressed verbose logging
- 🔄 **Continuous listening** mode

## Demo

```
🎤 Listening...
📝 Hello, how are you doing today?
🌐 Hola, ¿cómo estás hoy?
🔊 Speaking...
------------------------------------------------------------
```

## Prerequisites

- Python 3.8 or higher
- Microphone for audio input
- **Headphones recommended** to prevent audio feedback loops

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/BeyonderLimit/Offline-ASR-Translation.git
cd realtime-speech-translation
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Piper TTS

```bash
pip install piper-tts
```

### 4. Download Piper voice model

Download a Spanish voice model from the [Piper releases page](https://github.com/rhasspy/piper/blob/master/VOICES.md):

```bash
# Example: Download Spanish model
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/es_ES-sharvard-medium.onnx
```

### 5. Set up environment variables (optional)

```bash
# Set custom model path
export PIPER_MODEL_PATH="/path/to/es_ES-sharvard-medium.onnx"

# Set custom piper binary location (if not in PATH)
export PIPER_BINARY="/path/to/piper"
```

## Usage

### Basic Usage

```bash
python realtime_translation.py
```

The application will:
1. Start listening for English speech
2. Transcribe your speech in real-time
3. Translate to Spanish
4. Speak the translation
5. Continue listening for more input

### Stopping the Application

Press `Ctrl+C` to stop the application.

## Configuration

### Change Translation Languages

Edit the language codes in `realtime_translation.py`:

```python
from_code = "en"  # Source language
to_code = "es"    # Target language
```

Available language pairs depend on installed Argos Translate packages.

### Install Additional Language Packages

```python
import argostranslate.package

# Update package index
argostranslate.package.update_package_index()

# List available packages
available_packages = argostranslate.package.get_available_packages()
for pkg in available_packages:
    print(f"{pkg.from_code} -> {pkg.to_code}")
```

## Project Structure

```
realtime-speech-translation/
├── realtime_translation.py    # Main application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── LICENSE                   # License file
├── .gitignore               # Git ignore rules
└── models/                  # Voice models directory (optional)
    └── es_ES-sharvard-medium.onnx
```

## Troubleshooting

### Audio Feedback Loop

**Problem:** The system picks up its own Spanish output and translates it again.

**Solution:** 
- ✅ **Use headphones** (best solution)
- The application attempts to mute the microphone during playback
- Adjust your microphone sensitivity/positioning

### Piper Model Not Found

**Problem:** `⚠️ Piper not found` or model errors

**Solution:**
```bash
# Ensure piper is installed
pip install piper-tts

# Set model path explicitly
export PIPER_MODEL_PATH="/full/path/to/model.onnx"
```

### No Audio Playback

**Problem:** Translation works but no audio output

**Solution:**
- **Linux:** Install audio player: `sudo apt-get install alsa-utils`
- **macOS:** afplay should be available by default
- **Windows:** PowerShell audio should work by default

### Verbose Logging Still Appears

**Problem:** Still seeing INFO messages from argostranslate

**Solution:** The `SuppressOutput` context manager should handle this. If issues persist, check that all imports happen after logging configuration.

## Dependencies

- `RealtimeSTT` - Real-time speech-to-text
- `argostranslate` - Offline translation
- `piper-tts` - Text-to-speech synthesis
- `stanza` - NLP library (used by argostranslate)

See `requirements.txt` for complete list.

## Performance Notes

- First translation may be slower (model loading)
- Translation speed: ~1-2 seconds for typical sentences
- Works completely offline after initial setup
- CPU usage depends on model size (medium models recommended)

## Known Limitations

- Currently configured for English → Spanish only
- Requires manual model downloads
- System microphone muting may not work on all platforms
- Best results with clear speech and minimal background noise

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) - Real-time speech recognition
- [Argos Translate](https://github.com/argosopentech/argos-translate) - Offline translation
- [Piper](https://github.com/rhasspy/piper) - Fast, local text-to-speech

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/BeyonderLimit/Offline-ASR-Translation)/issues)
3. Open a new issue with details about your system and the problem

## Roadmap

- [ ] Support for more language pairs
- [ ] GUI interface
- [ ] Voice activity detection improvements
- [ ] Automatic model downloads
- [ ] Multi-threaded audio processing
- [ ] Configuration file support
- [ ] Docker containerization

---

**Note:** Remember to use headphones to prevent audio feedback! 🎧
