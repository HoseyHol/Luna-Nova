import google.generativeai as genai
import asyncio
from config import settings

class GeminiBrain:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.model = None
        
    async def initialize(self):
        """Inicializa o modelo Gemini"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        print("Modelo Gemini inicializado")
    
    async def process_input(self, text_input, vision_data=None):
        """Processa entrada com contexto e visão"""
        # Obter contexto da memória
        context = self.memory.get_context()
        
        # Construir prompt com contexto
        prompt = self.build_prompt(text_input, context, vision_data)
        
        # Gerar resposta
        response = await self.model.generate_content_async(prompt)
        return response.text
    
    def build_prompt(self, text_input, context, vision_data):
        """Constrói o prompt para o Gemini com contexto"""
        prompt = "Você é um companion virtual amigável e útil.\n\n"
        
        # Adicionar contexto de memória
        if context:
            prompt += "Contexto recente:\n"
            for interaction in context:
                prompt += f"Usuário: {interaction['input']}\n"
                prompt += f"Você: {interaction['response']}\n\n"
        
        # Adicionar informações visuais
        if vision_data and vision_data.get('faces'):
            prompt += "Informações visuais:\n"
            for face in vision_data['faces']:
                prompt += f"- {face['name']} está visível\n"
        
        prompt += f"\nUsuário: {text_input}\nCompanion:"
        return prompt