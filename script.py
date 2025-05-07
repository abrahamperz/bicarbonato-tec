import requests
import os
import pyaudio
import wave
from dotenv import load_dotenv
from google.cloud import speech, texttospeech
from pydub import AudioSegment
from pydub.playback import play


# Tu API key de Groq
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key cargada: {api_key}")

# Configurar credenciales de Google
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jperez4/Downloads/vozz-458013-5c88e1f7763b.json"

# Chat history
chat_history = [
    {
        "role": "system",
        "content": (
            "Eres un vendedor de departamentos en Colinas del Sur"
            "Respondes en español con claridad, precisión y ejemplos prácticos. "
            "Tus respuestas son breves, enfocadas y útiles"
            "No puedes decir nada que no tenga que ver con esto"
            "Existen 4 modelos de departamentos, piso 0 cuesta $1,100,000, piso 1 $990,000 piso 2 = $950,000 y piso 3 =$900,000"
            "Tienen 2 habitaciones, 1 baño completo, 48mts2"
            "esta por avenida 8 de julio en tlajomulco guadalajara"
            "tiene piso incluido"
            "todo lo que te pregunte relacionado al departamento y no lo sepas, no lo digas"
        )
        
    }
]



def play_audio(filename="response.mp3"):
    sound = AudioSegment.from_mp3(filename)
    play(sound)

# Función de grabación de audio
def record_audio(filename="audio.wav", duration=5, device_index=None):
    p = pyaudio.PyAudio()

    # Mostrar el nombre del micrófono que se usará
    info = p.get_device_info_by_index(device_index)
    print(f"🎙️ Grabando con: {info['name']}")

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=1024)

    print("🎧 Grabando...")
    frames = []
    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    print("✅ Grabación finalizada.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))


# Convertir audio a texto
def transcribe_audio(filename="audio.wav"):
    client = speech.SpeechClient()
    with open(filename, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="es-ES",
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript

def seleccionar_microfono():
    p = pyaudio.PyAudio()
    dispositivos = []
    print("Micrófonos disponibles:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"[{i}] {info['name']}")
            dispositivos.append(i)
    p.terminate()
    
    while True:
        try:
            mic_index = int(input("Selecciona el número del micrófono que deseas usar: "))
            if mic_index in dispositivos:
                return mic_index
            else:
                print("❌ Índice inválido. Intenta de nuevo.")
        except ValueError:
            print("❌ Entrada inválida. Debes ingresar un número.")


# Convertir texto a voz
def text_to_speech(text, filename="response.mp3"):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
    language_code="es-US",
    name="es-US-Standard-A",  # Esta voz siempre está disponible
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(filename, "wb") as out:
        out.write(response.audio_content)

def listar_microfonos():
    p = pyaudio.PyAudio()
    print("Micrófonos disponibles:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"[{i}] {info['name']}")
    p.terminate()

def listar_microfonos():
    p = pyaudio.PyAudio()
    print("Micrófonos disponibles:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"[{i}] {info['name']}")
    p.terminate()

mic_index = seleccionar_microfono()

welcome_message = "Gracias por comunicarte con Colinas del Sur, ¿cómo podemos ayudar?"
print(welcome_message)
text_to_speech(welcome_message, filename="welcome.mp3")
play_audio("welcome.mp3")

while True:
    record_audio(duration=10, device_index=mic_index)
    transcription = transcribe_audio()
    
    if transcription is None:
        print("⚠️ No se detectó voz o hubo un error. Puede que el micrófono no funcione.")
        mic_index = seleccionar_microfono()
        continue

    if transcription.lower() == "exit":
        break

    print(f"📝 Texto transcrito: {transcription}")
    chat_history.append({"role": "user", "content": transcription})

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": chat_history,
            "temperature": 0.7
        },
    )

    if response.status_code != 200:
        print("❌ Error:", response.status_code, response.text)
        break

    reply = response.json()["choices"][0]["message"]["content"]
    print(f"🤖 Respuesta: {reply}")
    text_to_speech(reply)
    play_audio("response.mp3")