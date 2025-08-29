import asyncio
import time
from pyvrm import VRM
import numpy as np

class AvatarController:
    def __init__(self):
        self.avatar = None
        self.current_emotion = "neutral"
        self.emotion_intensity = 0.5
        self.current_gesture = "idle"
        self.gesture_intensity = 0.5
        self.gesture_end_time = 0
        
        # Estados de blend shapes para expressões faciais
        self.blend_shapes = {
            "neutral": 0.0,
            "happy": 0.0,
            "sad": 0.0,
            "angry": 0.0,
            "surprised": 0.0,
            "aa": 0.0,    # Para sincronia labial
            "ih": 0.0,
            "ou": 0.0,
            "ee": 0.0,
            "oh": 0.0
        }
        
        # Parâmetros de animação
        self.animation_parameters = {
            "head_rotation": [0, 0, 0],  # pitch, yaw, roll
            "body_posture": "neutral",   # neutral, attentive, relaxed
            "eye_blink": 0.0,
            "breathing": 0.0
        }
    
    async def load_avatar(self, vrm_path):
        """Carrega modelo VRM do avatar"""
        self.avatar = VRM.load(vrm_path)
        print("Avatar carregado")
    
    async def set_emotion(self, emotion_blend_shape, intensity):
        """Define a expressão emocional do avatar"""
        self.current_emotion = emotion_blend_shape
        self.emotion_intensity = intensity
        
        # Resetar todas as expressões
        for shape in self.blend_shapes:
            self.blend_shapes[shape] = 0.0
        
        # Aplicar a expressão emocional principal
        if emotion_blend_shape in self.blend_shapes:
            self.blend_shapes[emotion_blend_shape] = intensity
        
        # Aplicar expressões secundárias baseadas na emoção principal
        if emotion_blend_shape == "happy":
            self.blend_shapes["aa"] = min(intensity * 0.7, 0.7)
        elif emotion_blend_shape == "surprised":
            self.blend_shapes["ou"] = min(intensity * 0.8, 0.8)
        
        # Atualizar o avatar
        await self._apply_blend_shapes()
    
    async def set_gesture(self, gesture_name, blend_shape, intensity, duration):
        """Executa um gesto no avatar"""
        self.current_gesture = gesture_name
        self.gesture_intensity = intensity
        self.gesture_end_time = time.time() + duration
        
        # Aplicar blend shape do gesto
        if blend_shape in self.blend_shapes:
            self.blend_shapes[blend_shape] = intensity
            await self._apply_blend_shapes()
    
    async def update_idle_animations(self):
        """Atualiza animações idle (piscar de olhos, respiração)"""
        current_time = time.time()
        
        # Piscar os olhos periodicamente
        if int(current_time * 2) % 4 == 0:
            self.blend_shapes["eye_blink"] = 0.8
        else:
            self.blend_shapes["eye_blink"] = 0.0
        
        # Simular respiração
        self.animation_parameters["breathing"] = (np.sin(current_time) + 1) * 0.1
        
        # Verificar se o gesto terminou
        if self.current_gesture != "idle" and current_time > self.gesture_end_time:
            self.current_gesture = "idle"
            # Manter apenas a expressão emocional atual
            await self.set_emotion(self.current_emotion, self.emotion_intensity)
        
        await self._apply_blend_shapes()
    
    async def _apply_blend_shapes(self):
        """Aplica os blend shapes ao avatar (implementação específica do motor 3D)"""
        # Esta é uma implementação genérica - precisa ser adaptada para a biblioteca específica
        if self.avatar:
            for shape_name, value in self.blend_shapes.items():
                # Aqui você aplicaria o blend shape ao modelo VRM
                # Exemplo: self.avatar.set_blend_shape_value(shape_name, value)
                pass
        
        # Aplicar parâmetros de animação
        self._apply_animation_parameters()
    
    def _apply_animation_parameters(self):
        """Aplica parâmetros de animação ao avatar"""
        # Implementação específica para o motor 3D
        pass
    
    async def update_from_vision(self, vision_data):
        """Atualiza o avatar com base nos dados de visão"""
        if vision_data and vision_data.get('faces'):
            # Ajustar direção do olhar baseado na posição do rosto
            primary_face = vision_data['faces'][0]
            face_location = primary_face['location']
            
            # Calcular desvio do centro (simplificado)
            center_x = 320  # Metade da largura assumida de 640px
            face_center_x = (face_location[3] + face_location[1]) / 2
            
            # Ajustar rotação da cabeça baseado na posição do rosto
            deviation = (face_center_x - center_x) / center_x
            self.animation_parameters["head_rotation"][1] = deviation * 0.5
            
            await self._apply_animation_parameters()

async def set_viseme(self, viseme, intensity):
    """Define o viseme atual para sincronia labial"""
    if viseme in self.blend_shapes:
        # Reduzir intensidade de outros visemes
        for v in ['aa', 'ih', 'ou', 'ee', 'oh']:
            if v != viseme:
                self.blend_shapes[v] = max(0, self.blend_shapes[v] - 0.3)
        
        # Aplicar o viseme atual
        self.blend_shapes[viseme] = intensity
        
        await self._apply_blend_shapes()