import asyncio
import time
from modules.stt_module import SpeechToText
from modules.tts_module import TextToSpeech
from modules.vision_module import VisionProcessor
from modules.memory_module import MemorySystem
from modules.gemini_module import GeminiBrain
from modules.avatar_module import AvatarController
from modules.lipsync_module import LipSync

class VirtualCompanion:
    def __init__(self):
        self.is_running = False
        self.modules = {}
        
    async def initialize(self):
        """Inicializa todos os módulos"""
        print("Inicializando companion virtual...")
        
        # Inicializar módulos
        self.modules['memory'] = MemorySystem()
        self.modules['vision'] = VisionProcessor()
        self.modules['stt'] = SpeechToText()
        self.modules['tts'] = TextToSpeech()
        self.modules['gemini'] = GeminiBrain(self.modules['memory'])
        self.modules['avatar'] = AvatarController()
        self.modules['lipsync'] = LipSync(self.modules['tts'])
        
        # Carregar modelos
        await asyncio.gather(
            self.modules['stt'].load_model(),
            self.modules['tts'].load_model(),
            self.modules['vision'].load_models(),
            self.modules['memory'].load()
        )
        
        print("Companion inicializado com sucesso!")
    
    async def run(self):
        """Loop principal do companion"""
        self.is_running = True
        
        while self.is_running:
            # Processar visão
            vision_data = await self.modules['vision'].process_frame()
            
            # Escutar com STT
            text_input = await self.modules['stt'].listen()
            
            if text_input:
                # Processar com Gemini
                response = await self.modules['gemini'].process_input(
                    text_input, 
                    vision_data
                )
                
                # Atualizar memória
                self.modules['memory'].add_interaction(text_input, response)
                
                # Gerar áudio com TTS
                audio_data = await self.modules['tts'].synthesize(response)
                
                # Sincronizar lábios e controlar avatar
                await self.modules['lipsync'].synchronize(audio_data, response)
                await self.modules['avatar'].update_expression(response, vision_data)
            
            await asyncio.sleep(0.1)  # Evitar uso excessivo da CPU

async def main():
    companion = VirtualCompanion()
    await companion.initialize()
    await companion.run()

if __name__ == "__main__":
    asyncio.run(main())