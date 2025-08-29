import speech_recognition as sr
import numpy as np
import asyncio

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        
    async def load_model(self):
        """Carrega o modelo de STT local"""
        # Ajustar para ruído ambiente
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Modelo STT carregado")
    
    async def listen(self):
        """Escuta e transcreve áudio"""
        try:
            with self.microphone as source:
                print("Ouvindo...")
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
            # Usar recognizer offline (precisa de modelo treinado)
            text = self.recognizer.recognize_vosk(audio)
            print(f"Texto reconhecido: {text}")
            return text
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Erro no STT: {e}")
            return None