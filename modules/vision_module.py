import cv2
import face_recognition
import numpy as np
import asyncio
from PIL import Image

class VisionProcessor:
    def __init__(self):
        self.cap = None
        self.known_faces = []
        self.face_encodings = []
        self.face_names = []
        
    async def load_models(self):
        """Carrega modelos de visão computacional"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Não foi possível abrir a câmera")
        
        # Carregar rostos conhecidos
        await self.load_known_faces()
        print("Modelos de visão carregados")
    
    async def load_known_faces(self):
        """Carrega rostos conhecidos do diretório"""
        faces_dir = Path("data/faces")
        if faces_dir.exists():
            for face_file in faces_dir.glob("*.jpg"):
                image = face_recognition.load_image_file(face_file)
                encoding = face_recognition.face_encodings(image)[0]
                self.face_encodings.append(encoding)
                self.face_names.append(face_file.stem)
    
    async def process_frame(self):
        """Processa um frame da câmera"""
        ret, frame = self.cap.read()
        if not ret:
            return {"faces": [], "objects": []}
        
        # Detectar rostos
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        face_data = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(self.face_encodings, face_encoding)
            name = "Desconhecido"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = self.face_names[first_match_index]
            
            face_data.append({
                "name": name,
                "location": face_location,
                "encoding": face_encoding
            })
        
        # Detectar objetos (simplificado - pode ser expandido com YOLO/etc)
        object_data = self.detect_objects(frame)
        
        return {
            "faces": face_data,
            "objects": object_data,
            "raw_frame": frame
        }
    
    def detect_objects(self, frame):
        """Detecta objetos no frame (implementação simplificada)"""
        # TODO: Implementar detecção de objetos com modelo pré-treinado
        return []