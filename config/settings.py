import os
from pathlib import Path

# Configurações da API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "sua_chave_aqui")

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# Configurações de Áudio
SAMPLE_RATE = 22050
CHUNK_SIZE = 1024

# Configurações de Visão
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Configurações do Avatar
VRM_PATH = BASE_DIR / "assets" / "avatar.vrm"