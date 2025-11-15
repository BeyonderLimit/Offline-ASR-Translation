import logging
import sys
import subprocess
import os
import tempfile
import platform
import argostranslate.package
import argostranslate.translate
from RealtimeSTT import AudioToTextRecorder

# More aggressive logging suppression - must be done before importing
logging.basicConfig(level=logging.ERROR)
for logger_name in ['argostranslate', 'argostranslate.utils', 'stanza', 'RealtimeSTT']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.ERROR)
    logger.propagate = False

# Suppress all argostranslate INFO output
class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open('/dev/null', 'w') if sys.platform != 'win32' else open('nul', 'w')
        sys.stderr = open('/dev/null', 'w') if sys.platform != 'win32' else open('nul', 'w')
        return self
    
    def __exit__(self, *args):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

from_code = "en"
to_code = "es"

# Download and install Argos Translate package
print("Setting up translation package...")
with SuppressOutput():
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
print("Translation package ready!\n")

def speak_with_piper(text, language="es"):
    """
    Speak text using Piper TTS
    
    Prerequisites:
    1. Install piper: pip install piper-tts
       OR download binary from: https://github.com/rhasspy/piper/releases
    2. Download voice model from: https://github.com/rhasspy/piper/releases
       Example: es_ES-sharvard-medium.onnx
    
    Configuration:
    - Set PIPER_MODEL_PATH environment variable or update model_path below
    - Ensure piper is in your PATH or provide full path to binary
    """
    
    # Configuration - adjust these paths for your setup
    model_path = os.environ.get('PIPER_MODEL_PATH', 'es_ES-sharvard-medium.onnx')
    piper_command = os.environ.get('PIPER_BINARY', 'piper')
    
    try:
        # Create temporary file for audio output
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            output_file = tmp_file.name
        
        # Generate audio with Piper
        process = subprocess.Popen(
            [piper_command, '--model', model_path, '--output_file', output_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=text.encode('utf-8'))
        
        if process.returncode != 0:
            print(f"⚠️  Piper error: {stderr.decode()}")
            return
        
        # Play the audio file
        play_audio(output_file)
        
        # Clean up temporary file
        try:
            os.remove(output_file)
        except:
            pass
            
    except FileNotFoundError:
        print("⚠️  Piper not found. Install with: pip install piper-tts")
        print("   Or set PIPER_BINARY environment variable to piper path")
    except Exception as e:
        print(f"⚠️  TTS error: {e}")

def mute_microphone(mute=True):
    """
    Mute/unmute system microphone
    """
    try:
        if sys.platform == 'darwin':  # macOS
            volume = '0' if mute else '50'
            subprocess.run(['osascript', '-e', 
                          f'set volume input volume {volume}'],
                         check=False, stderr=subprocess.DEVNULL)
        elif sys.platform == 'linux':  # Linux
            state = 'mute' if mute else 'unmute'
            # Try amixer first
            subprocess.run(['amixer', 'set', 'Capture', state],
                         check=False, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        elif sys.platform == 'win32':  # Windows
            state = '0' if mute else '50'
            subprocess.run(['nircmd.exe', 'setsysvolume', state, 'microphone'],
                         check=False, stderr=subprocess.DEVNULL)
    except:
        pass  # Silently fail if muting not supported

def play_audio(audio_file):
    """
    Play audio file using platform-appropriate command (blocking - waits for completion)
    """
    try:
        # Mute microphone before playback
        mute_microphone(True)
        
        if sys.platform == 'darwin':  # macOS
            # afplay is already synchronous/blocking
            subprocess.run(['afplay', audio_file], check=True)
        elif sys.platform == 'linux':  # Linux
            # Try common audio players in order of preference
            for player in ['aplay', 'paplay', 'mpg123']:
                try:
                    # These players are blocking by default
                    subprocess.run([player, audio_file], check=True, 
                                 stderr=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL)
                    break
                except FileNotFoundError:
                    continue
            else:
                # If no player found, try ffplay with auto-exit
                try:
                    subprocess.run(['ffplay', '-nodisp', '-autoexit', audio_file], 
                                 check=True,
                                 stderr=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL)
                except FileNotFoundError:
                    print("⚠️  No audio player found. Install aplay, paplay, or ffplay")
        elif sys.platform == 'win32':  # Windows
            # PlaySync() is already synchronous/blocking
            subprocess.run([
                'powershell', '-c',
                f"(New-Object Media.SoundPlayer '{audio_file}').PlaySync()"
            ], check=True)
        
        # Unmute microphone after playback
        time.sleep(0.5)  # Small delay before unmuting
        mute_microphone(False)
        
    except Exception as e:
        mute_microphone(False)  # Ensure mic gets unmuted on error
        print(f"⚠️  Audio playback error: {e}")

import time

recorder = None

def process_text(text):
    global recorder
    
    print(f"📝 {text}")
    
    # Translate with suppressed output
    with SuppressOutput():
        translated = argostranslate.translate.translate(text, from_code, to_code)
    
    print(f"🌐 {translated}")
    print(f"🔊 Speaking...")
    
    # Stop the recorder completely during playback
    if recorder:
        recorder.stop()
    
    # Speak the translation (this blocks until audio finishes)
    speak_with_piper(translated, to_code)
    
    # Add extra buffer time to ensure audio device is released
    time.sleep(1.0)
    
    print("-" * 60)

if __name__ == '__main__':
    print("🎤 Ready! Start speaking (Ctrl+C to stop)...\n")
    print("💡 Tip: Use headphones to prevent audio feedback\n")
    print("=" * 60)
    
    try:
        while True:
            # Create new recorder for each session
            print("🎤 Listening...")
            recorder = AudioToTextRecorder()
            
            # Record and process one utterance (blocks until speech detected)
            recorder.text(process_text)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("⏹️  Stopping...")
    finally:
        if recorder:
            recorder.stop()
        print("✅ Done.")
