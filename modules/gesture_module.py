import asyncio
import random
import re
from typing import Dict, List

class GestureController:
    def __init__(self, avatar_controller):
        self.avatar = avatar_controller
        self.current_gesture = "idle"
        self.gesture_intensity = 0.5
        
        # Mapeamento de palavras-chave para gestos
        self.gesture_mapping = {
            "saudação": ["olá", "oi", "e aí", "bom dia", "boa tarde", "boa noite"],
            "despedida": ["tchau", "até mais", "até logo", "adeus"],
            "concordância": ["sim", "claro", "certamente", "concordo", "exato"],
            "discordância": ["não", "discordo", "não acho", "errado"],
            "pensativo": ["pensar", "considerar", "ponderar", "refletir"],
            "explicação": ["explicar", "mostrar", "demonstrar", "ensinar"],
            "entusiasmo": ["incrível", "maravilhoso", "fantástico", "surpreendente"]
        }
        
        # Gestos disponíveis e seus parâmetros
        self.available_gestures = {
            "wave": {"duration": 2.0, "blend_shape": "joy", "intensity": 0.7},
            "nod": {"duration": 1.5, "blend_shape": "affirm", "intensity": 0.8},
            "shake": {"duration": 1.5, "blend_shape": "negation", "intensity": 0.8},
            "think": {"duration": 3.0, "blend_shape": "thinking", "intensity": 0.6},
            "explain": {"duration": 2.5, "blend_shape": "aa", "intensity": 0.7},
            "excite": {"duration": 2.0, "blend_shape": "happy", "intensity": 0.9},
            "idle": {"duration": 0, "blend_shape": "neutral", "intensity": 0.5}
        }
    
    async def analyze_text_for_gestures(self, text: str) -> str:
        """Analisa o texto para determinar gestos apropriados"""
        text_lower = text.lower()
        
        # Verificar correspondências com palavras-chave
        matched_gestures = []
        for gesture, keywords in self.gesture_mapping.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    matched_gestures.append(gesture)
                    break
        
        # Escolher o gesto mais apropriado com base no contexto
        if matched_gestures:
            # Priorizar alguns gestos sobre outros
            if "saudação" in matched_gestures:
                return "wave"
            elif "despedida" in matched_gestures:
                return "wave"
            elif "entusiasmo" in matched_gestures:
                return "excite"
            elif "pensativo" in matched_gestures:
                return "think"
            elif "explicação" in matched_gestures:
                return "explain"
            elif "concordância" in matched_gestures:
                return "nod"
            elif "discordância" in matched_gestures:
                return "shake"
        
        # Gestos aleatórios durante conversas longas
        if len(text.split()) > 8:
            random_gestures = ["nod", "explain", "think"]
            return random.choice(random_gestures)
        
        return "idle"
    
    async def execute_gesture(self, gesture_name: str, intensity: float = 0.5):
        """Executa um gesto específico"""
        if gesture_name not in self.available_gestures:
            gesture_name = "idle"
        
        gesture_config = self.available_gestures[gesture_name]
        self.current_gesture = gesture_name
        self.gesture_intensity = intensity
        
        # Aplicar o gesto no avatar
        await self.avatar.set_gesture(
            gesture_name, 
            gesture_config["blend_shape"],
            intensity * gesture_config["intensity"],
            gesture_config["duration"]
        )
        
        print(f"Executando gesto: {gesture_name} com intensidade: {intensity}")