import asyncio
import numpy as np
from pyvrm import VRM

class AvatarController:
    def __init__(self):
        self.avatar = None
        self.current_expression = "neutral"
        
    async def load_avatar(self, vrm_path):
        """Carrega modelo VRM do avatar"""
        self.avatar = VRM.load(vrm_path)
        print("Avatar carregado")
    
    async def update_expression(self, text, vision_data):
        """Atualiza expressão facial baseada no contexto"""
        # Análise de sentimento simples do texto
        if any(word in text.lower() for word in ["feliz", "alegre", "obrigado"]):
            expression = "happy"
        elif any(word in text.lower() for word in ["triste", "desculpa", "problema"]):
            expression = "sad"
        elif any(word in text.lower() for word in ["surpresa", "incrível", "uau"]):
            expression = "surprised"
        else:
            expression = "neutral"
        
        # Aplicar expressão
        await self.set_expression(expression)
        
        # Atualizar pose baseada na visão
        if vision_data and vision_data.get('faces'):
            await self.adjust_posture(len(vision_data['faces']))
    
    async def set_expression(self, expression):
        """Aplica expressão facial ao avatar"""
        self.current_expression = expression
        # TODO: Implementar controle de blendshapes do avatar VRM
        print(f"Expressão alterada para: {expression}")
    
    async def adjust_posture(self, people_count):
        """Ajusta postura baseada no número de pessoas"""
        if people_count == 0:
            posture = "relaxed"
        elif people_count == 1:
            posture = "attentive"
        else:
            posture = "engaged"
        
        # TODO: Implementar ajuste de postura no avatar
        print(f"Postura ajustada para: {posture}")