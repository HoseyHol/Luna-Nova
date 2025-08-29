import numpy as np
import asyncio
from collections import deque

class LipSync:
    def __init__(self, tts_module, avatar_controller):
        self.tts = tts_module
        self.avatar = avatar_controller
        self.phoneme_map = {
            'a': 'aa', 'e': 'ee', 'i': 'ih', 'o': 'oh', 'u': 'ou',
            'b': 'aa', 'p': 'aa', 'm': 'aa', 'f': 'ee', 'v': 'ee',
            's': 'ih', 'z': 'ih', 'ʃ': 'ih', 'ʒ': 'ih',
            'd': 'oh', 't': 'oh', 'n': 'oh', 'l': 'oh',
            'r': 'ou', 'k': 'ou', 'g': 'ou', 'h': 'ou',
            'sil': 'neutral'
        }
        
        self.audio_buffer = deque()
        self.phoneme_queue = deque()
    
    async def synchronize(self, audio_data, text):
        """Sincroniza movimento labial com áudio"""
        # Extrair fonemas do texto
        phonemes = self.text_to_phonemes(text)
        
        # Calcular timing dos fonemas baseado no áudio
        audio_length = len(audio_data) / self.tts.sample_rate
        phoneme_count = len(phonemes)
        
        if phoneme_count > 0:
            phoneme_duration = audio_length / phoneme_count
        else:
            phoneme_duration = 0.1
        
        # Adicionar fonemas à fila com timing
        current_time = 0
        for phoneme in phonemes:
            self.phoneme_queue.append({
                'phoneme': phoneme,
                'start_time': current_time,
                'duration': phoneme_duration
            })
            current_time += phoneme_duration
        
        # Processar fila de fonemas
        await self.process_phoneme_queue()
    
    async def process_phoneme_queue(self):
        """Processa a fila de fonemas em tempo real"""
        start_time = asyncio.get_event_loop().time()
        
        while self.phoneme_queue:
            current_phoneme = self.phoneme_queue[0]
            elapsed_time = asyncio.get_event_loop().time() - start_time
            
            if elapsed_time >= current_phoneme['start_time']:
                # Aplicar fonema atual
                viseme = self.phoneme_map.get(current_phoneme['phoneme'], 'neutral')
                await self.avatar.set_viseme(viseme, 0.7)
                
                # Remover fonema processado
                self.phoneme_queue.popleft()
                
                # Agendar retorno ao neutro após duração do fonema
                asyncio.create_task(
                    self.reset_viseme_after_delay(
                        current_phoneme['duration'] * 0.8
                    )
                )
            
            await asyncio.sleep(0.01)  # Controle de taxa de atualização
    
    async def reset_viseme_after_delay(self, delay):
        """Retorna a boca ao estado neutro após um delay"""
        await asyncio.sleep(delay)
        await self.avatar.set_viseme('neutral', 0.3)
    
    def text_to_phonemes(self, text):
        """Converte texto para fonemas (simplificado)"""
        # Implementação básica - pode ser substituída por um sistema mais avançado
        phonemes = []
        for char in text.lower():
            if char in self.phoneme_map:
                phonemes.append(char)
            elif char == ' ':
                phonemes.append('sil')
        
        return phonemes