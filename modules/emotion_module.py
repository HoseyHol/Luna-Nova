import asyncio
import re
from datetime import datetime
from typing import Dict, List, Tuple

class EmotionEngine:
    def __init__(self, memory_system, avatar_controller):
        self.memory = memory_system
        self.avatar = avatar_controller
        self.current_emotion = "neutral"
        self.emotion_intensity = 0.5
        self.emotion_history = []
        
        # Mapeamento de emoções para blend shapes
        self.emotion_blend_shapes = {
            "happy": ["happy", "joy"],
            "sad": ["sad", "sorrow"],
            "angry": ["angry", "rage"],
            "surprised": ["surprised", "astonished"],
            "confused": ["confused", "puzzled"],
            "excited": ["excited", "enthusiastic"],
            "neutral": ["neutral"]
        }
        
        # Palavras-chave e seus pesos emocionais
        self.emotional_keywords = {
            "happy": ["feliz", "alegre", "gostar", "adorar", "incrível", "maravilhoso", "perfeito"],
            "sad": ["triste", "chateado", "decepcionado", "desanimado", "perder", "fracassar"],
            "angry": ["raiva", "bravo", "furioso", "irritado", "ódio", "injusto"],
            "surprised": ["surpresa", "incrível", "inesperado", "uau", "impressionante"],
            "confused": ["confuso", "dúvida", "perguntar", "não sei", "não entender"],
            "excited": ["animado", "empolgado", "entusiasmado", "esperançoso", "ansioso"]
        }
        
        # Fatores contextuais que influenciam emoções
        self.context_factors = {
            "time_of_day": {
                "morning": {"happy": 0.1, "energy": 0.2},
                "afternoon": {"neutral": 0.1},
                "evening": {"tired": 0.1, "relaxed": 0.1},
                "night": {"tired": 0.2, "calm": 0.1}
            },
            "interaction_history": {
                "positive": {"happy": 0.2, "friendly": 0.1},
                "negative": {"cautious": 0.1, "reserved": 0.1},
                "neutral": {"neutral": 0.1}
            }
        }
    
    def get_time_of_day_factor(self) -> Dict[str, float]:
        """Retorna fatores emocionais baseados na hora do dia"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return self.context_factors["time_of_day"]["morning"]
        elif 12 <= hour < 17:
            return self.context_factors["time_of_day"]["afternoon"]
        elif 17 <= hour < 22:
            return self.context_factors["time_of_day"]["evening"]
        else:
            return self.context_factors["time_of_day"]["night"]
    
    def get_interaction_history_factor(self) -> Dict[str, float]:
        """Retorna fatores emocionais baseados no histórico de interações"""
        recent_interactions = self.memory.get_recent_interactions(5)
        
        if not recent_interactions:
            return self.context_factors["interaction_history"]["neutral"]
        
        # Analisar sentimento das interações recentes
        positive_count = 0
        negative_count = 0
        
        for interaction in recent_interactions:
            emotion = self.analyze_text_emotion(interaction["input"])
            if emotion in ["happy", "excited"]:
                positive_count += 1
            elif emotion in ["sad", "angry"]:
                negative_count += 1
        
        if positive_count > negative_count:
            return self.context_factors["interaction_history"]["positive"]
        elif negative_count > positive_count:
            return self.context_factors["interaction_history"]["negative"]
        else:
            return self.context_factors["interaction_history"]["neutral"]
    
    def analyze_text_emotion(self, text: str) -> Tuple[str, float]:
        """Analisa o texto para determinar a emoção predominante"""
        text_lower = text.lower()
        emotion_scores = {emotion: 0 for emotion in self.emotional_keywords}
        
        # Contar palavras-chave emocionais
        for emotion, keywords in self.emotional_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    emotion_scores[emotion] += 1
        
        # Adicionar fatores contextuais
        time_factor = self.get_time_of_day_factor()
        history_factor = self.get_interaction_history_factor()
        
        for emotion, score in time_factor.items():
            if emotion in emotion_scores:
                emotion_scores[emotion] += score
        
        for emotion, score in history_factor.items():
            if emotion in emotion_scores:
                emotion_scores[emotion] += score
        
        # Determinar emoção predominante
        if not any(emotion_scores.values()):
            return "neutral", 0.5
        
        predominant_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[predominant_emotion]
        total_score = sum(emotion_scores.values())
        
        intensity = min(max_score / total_score * 2, 1.0) if total_score > 0 else 0.5
        
        return predominant_emotion, intensity
    
    async def update_emotion(self, text: str, is_companion_speech: bool = False):
        """Atualiza o estado emocional com base no texto"""
        emotion, intensity = self.analyze_text_emotion(text)
        
        # Suavizar transições emocionais
        if self.current_emotion != emotion:
            intensity = max(0.3, intensity)  # Garantir intensidade mínima para transições
        
        self.current_emotion = emotion
        self.emotion_intensity = intensity
        
        # Registrar no histórico
        self.emotion_history.append({
            "timestamp": datetime.now(),
            "emotion": emotion,
            "intensity": intensity,
            "source": "companion" if is_companion_speech else "user"
        })
        
        # Manter histórico limitado
        if len(self.emotion_history) > 100:
            self.emotion_history.pop(0)
        
        # Aplicar emoção ao avatar
        blend_shape = self.emotion_blend_shapes.get(emotion, ["neutral"])[0]
        await self.avatar.set_emotion(blend_shape, intensity)
        
        print(f"Emoção atualizada: {emotion} com intensidade: {intensity}")