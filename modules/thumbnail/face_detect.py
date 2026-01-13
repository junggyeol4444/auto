"""
Face detection and cropping for thumbnails
"""
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional, List


class FaceDetector:
    """Detect and crop faces in images"""
    
    def __init__(self):
        # Try to load Haar Cascade classifier
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            self.use_haar = True
        except:
            self.use_haar = False
    
    def detect_faces(self, image: Image.Image) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in image
        
        Args:
            image: PIL Image object
        
        Returns:
            List of face bounding boxes (x, y, width, height)
        """
        if not self.use_haar:
            return []
        
        # Convert to grayscale
        img_array = np.array(image.convert('RGB'))
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return [tuple(face) for face in faces]
    
    def crop_face(self, image: Image.Image, padding: float = 0.3) -> Optional[Image.Image]:
        """
        Crop image to focus on detected face with padding
        
        Args:
            image: PIL Image object
            padding: Padding around face as ratio of face size
        
        Returns:
            Cropped PIL Image or None if no face detected
        """
        faces = self.detect_faces(image)
        
        if not faces:
            return None
        
        # Use largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        
        # Add padding
        pad_w = int(w * padding)
        pad_h = int(h * padding)
        
        x1 = max(0, x - pad_w)
        y1 = max(0, y - pad_h)
        x2 = min(image.width, x + w + pad_w)
        y2 = min(image.height, y + h + pad_h)
        
        return image.crop((x1, y1, x2, y2))
    
    def crop_multiple_faces(self, image: Image.Image, padding: float = 0.2) -> Optional[Image.Image]:
        """
        Crop image to include all detected faces
        
        Args:
            image: PIL Image object
            padding: Padding around faces as ratio
        
        Returns:
            Cropped PIL Image or None if no faces detected
        """
        faces = self.detect_faces(image)
        
        if not faces:
            return None
        
        # Find bounding box that includes all faces
        min_x = min(f[0] for f in faces)
        min_y = min(f[1] for f in faces)
        max_x = max(f[0] + f[2] for f in faces)
        max_y = max(f[1] + f[3] for f in faces)
        
        # Add padding
        width = max_x - min_x
        height = max_y - min_y
        pad_w = int(width * padding)
        pad_h = int(height * padding)
        
        x1 = max(0, min_x - pad_w)
        y1 = max(0, min_y - pad_h)
        x2 = min(image.width, max_x + pad_w)
        y2 = min(image.height, max_y + pad_h)
        
        return image.crop((x1, y1, x2, y2))
    
    def get_face_center(self, image: Image.Image) -> Optional[Tuple[int, int]]:
        """
        Get center point of largest detected face
        
        Args:
            image: PIL Image object
        
        Returns:
            (x, y) tuple of face center or None
        """
        faces = self.detect_faces(image)
        
        if not faces:
            return None
        
        # Use largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        
        center_x = x + w // 2
        center_y = y + h // 2
        
        return (center_x, center_y)
    
    def smart_crop_for_thumbnail(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """
        Smart crop image for thumbnail, focusing on faces if detected
        
        Args:
            image: PIL Image object
            target_size: (width, height) tuple for output
        
        Returns:
            Cropped and resized PIL Image
        """
        target_width, target_height = target_size
        target_aspect = target_width / target_height
        
        # Try to detect face
        face_center = self.get_face_center(image)
        
        img_width, img_height = image.size
        img_aspect = img_width / img_height
        
        if img_aspect > target_aspect:
            # Image is wider than target
            new_height = img_height
            new_width = int(img_height * target_aspect)
            
            if face_center:
                # Center crop on face
                center_x = face_center[0]
                x1 = max(0, center_x - new_width // 2)
                x1 = min(x1, img_width - new_width)
                y1 = 0
            else:
                # Center crop
                x1 = (img_width - new_width) // 2
                y1 = 0
            
            cropped = image.crop((x1, y1, x1 + new_width, y1 + new_height))
        else:
            # Image is taller than target
            new_width = img_width
            new_height = int(img_width / target_aspect)
            
            if face_center:
                # Center crop on face
                center_y = face_center[1]
                y1 = max(0, center_y - new_height // 2)
                y1 = min(y1, img_height - new_height)
                x1 = 0
            else:
                # Center crop
                x1 = 0
                y1 = (img_height - new_height) // 2
            
            cropped = image.crop((x1, y1, x1 + new_width, y1 + new_height))
        
        # Resize to target
        return cropped.resize(target_size, Image.Resampling.LANCZOS)
