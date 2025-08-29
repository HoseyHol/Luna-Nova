import piper
import numpy as np
import asyncio
from pathlib import Path

class TextToSpeech:
    def __init__(self):
        self.model = None
        self.sample_rate = 22050
        
    async def load_model(self):
        """Carrega o modelo Piper TTS"""
        model_path = Path("models/tts/portuguese_model.onnx")
        if not model_path.exists():
            raise FileNotFoundError("Modelo Piper não encontrado")
        
        self.model = piper.PiperVoice.load(str(model_path))
        print("Modelo TTS carregado")
    
    async def synthesize(self, text):
        """Sintetiza fala a partir do texto"""
        if not self.model:
            raise RuntimeError("Modelo TTS não carregado")
        
        # Gerar áudio
        audio_data = self.model.synthesize(text)
        return np.frombuffer(audio_data, dtype=np.int16)