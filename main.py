import asyncio
import time
from modules.stt_module import SpeechToText
from modules.tts_module import TextToSpeech
from modules.vision_module import VisionProcessor
from modules.memory_module import MemorySystem
from modules.gemini_module import GeminiBrain
from modules.avatar_module import AvatarController
from modules.lipsync_module import LipSync
from modules.gesture_module import GestureController
from modules.emotion_module import EmotionEngine

class VirtualCompanion:
    def __init__(self):
        self.is_running = False
        self.modules = {}
        
    async def initialize(self):
        """Inicializa todos os módulos"""
        print("Inicializando companion virtual...")
        
        # Inicializar módulos básicos
        self.modules['memory'] = MemorySystem()
        self.modules['vision'] = VisionProcessor()
        self.modules['stt'] = SpeechToText()
        self.modules['tts'] = TextToSpeech()
        self.modules['gemini'] = GeminiBrain(self.modules['memory'])
        self.modules['avatar'] = AvatarController()
        self.modules['lipsync'] = LipSync(self.modules['tts'])
        
        # Inicializar novos módulos
        self.modules['gesture'] = GestureController(self.modules['avatar'])
        self.modules['emotion'] = EmotionEngine(
            self.modules['memory'], 
            self.modules['avatar']
        )
        
        # Carregar modelos
        await asyncio.gather(
            self.modules['stt'].load_model(),
            self.modules['tts'].load_model(),
            self.modules['vision'].load_models(),
            self.modules['memory'].load(),
            self.modules['avatar'].load_avatar("assets/avatar.vrm")
        )
        
        print("Companion inicializado com sucesso!")
    
    async def run(self):
        """Loop principal do companion"""
        self.is_running = True
        last_update_time = time.time()
        
        while self.is_running:
            current_time = time.time()
            
            # Processar visão a cada 0.5 segundos
            if current_time - last_update_time > 0.5:
                vision_data = await self.modules['vision'].process_frame()
                await self.modules['avatar'].update_from_vision(vision_data)
                last_update_time = current_time
            
            # Atualizar animações idle
            await self.modules['avatar'].update_idle_animations()
            
            # Escutar com STT
            text_input = await self.modules['stt'].listen()
            
            if text_input:
                # Atualizar emoção com base na fala do usuário
                await self.modules['emotion'].update_emotion(text_input, False)
                
                # Processar com Gemini
                response = await self.modules['gemini'].process_input(
                    text_input, 
                    vision_data
                )
                
                # Atualizar memória
                self.modules['memory'].add_interaction(text_input, response)
                
                # Atualizar emoção com base na resposta do companion
                await self.modules['emotion'].update_emotion(response, True)
                
                # Analisar e executar gestos
                gesture = await self.modules['gesture'].analyze_text_for_gestures(response)
                await self.modules['gesture'].execute_gesture(gesture, 
                    self.modules['emotion'].emotion_intensity)
                
                # Gerar áudio com TTS
                audio_data = await self.modules['tts'].synthesize(response)
                
                # Sincronizar lábios
                await self.modules['lipsync'].synchronize(audio_data, response)
            
            await asyncio.sleep(0.05)  # Loop mais responsivo

async def main():
    companion = VirtualCompanion()
    await companion.initialize()
    await companion.run()

if __name__ == "__main__":
    asyncio.run(main())