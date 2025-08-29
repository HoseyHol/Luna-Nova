import json
import numpy as np
from datetime import datetime
from pathlib import Path

class MemorySystem:
    def __init__(self):
        self.short_term_memory = []
        self.long_term_memory = []
        self.memory_file = Path("data/memory/memory.json")
        
    async def load(self):
        """Carrega memória de longo prazo do arquivo"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                self.long_term_memory = json.load(f)
        print("Memória carregada")
    
    async def save(self):
        """Salva memória de longo prazo no arquivo"""
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump(self.long_term_memory, f, indent=2)
    
    def add_interaction(self, input_text, response):
        """Adiciona uma interação à memória"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "response": response
        }
        
        # Adicionar à memória de curto prazo
        self.short_term_memory.append(interaction)
        
        # Se importante, adicionar à memória de longo prazo
        if self.is_important(interaction):
            self.long_term_memory.append(interaction)
            asyncio.create_task(self.save())
        
        # Manter tamanho limitado da memória de curto prazo
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)
    
    def is_important(self, interaction):
        """Determina se uma interação é importante o suficiente para memória longa"""
        # Implementar lógica para determinar importância
        keywords = ["nome", "lembrar", "importante", "gosto", "não gosto"]
        return any(keyword in interaction["input"].lower() for keyword in keywords)
    
    def get_context(self, limit=5):
        """Retorna contexto recente para o modelo"""
        return self.short_term_memory[-limit:] if self.short_term_memory else []