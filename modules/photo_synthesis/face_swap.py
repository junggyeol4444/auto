"""
Face swapping functionality
"""
from PIL import Image
import cv2
import numpy as np
from typing import Optional


class FaceSwapper:
    """Face swapping between images"""
    
    def __init__(self):
        self.face_recognition_available = False
        self.insightface_available = False
        
        # Try to import face_recognition
        try:
            import face_recognition
            self.face_recognition = face_recognition
            self.face_recognition_available = True
        except ImportError:
            print("Warning: face_recognition not available. Face swap will use basic method.")
        
        # Try to import InsightFace
        try:
            import insightface
            self.insightface = insightface
            self.insightface_available = True
        except ImportError:
            print("Note: InsightFace not available. Using basic face swap.")
    
    def swap_faces(self, source_image: Image.Image, target_image: Image.Image) -> Optional[Image.Image]:
        """
        Swap face from source to target image
        
        Args:
            source_image: PIL Image with source face
            target_image: PIL Image with target face
        
        Returns:
            PIL Image with swapped face or None if failed
        """
        if self.face_recognition_available:
            return self._swap_with_face_recognition(source_image, target_image)
        else:
            return self._swap_basic(source_image, target_image)
    
    def _swap_with_face_recognition(self, source_image: Image.Image, 
                                   target_image: Image.Image) -> Optional[Image.Image]:
        """Swap faces using face_recognition library"""
        # Convert to RGB numpy arrays
        source_rgb = np.array(source_image.convert('RGB'))
        target_rgb = np.array(target_image.convert('RGB'))
        
        # Detect face landmarks
        source_landmarks = self.face_recognition.face_landmarks(source_rgb)
        target_landmarks = self.face_recognition.face_landmarks(target_rgb)
        
        if not source_landmarks or not target_landmarks:
            print("Could not detect faces in one or both images")
            return None
        
        source_face = source_landmarks[0]
        target_face = target_landmarks[0]
        
        # Get face bounding boxes
        source_box = self._get_face_box(source_face)
        target_box = self._get_face_box(target_face)
        
        # Extract source face
        source_face_img = source_rgb[source_box[1]:source_box[3], 
                                     source_box[0]:source_box[2]]
        
        # Resize source face to target size
        target_width = target_box[2] - target_box[0]
        target_height = target_box[3] - target_box[1]
        
        source_face_resized = cv2.resize(source_face_img, (target_width, target_height))
        
        # Blend faces
        result = target_rgb.copy()
        
        # Create mask for blending
        mask = np.ones((target_height, target_width, 3), dtype=np.float32)
        center = ((target_box[0] + target_box[2]) // 2, 
                 (target_box[1] + target_box[3]) // 2)
        
        # Seamless clone
        try:
            result = cv2.seamlessClone(source_face_resized, result, 
                                      (mask * 255).astype(np.uint8),
                                      center, cv2.NORMAL_CLONE)
        except:
            # Fallback to simple paste
            result[target_box[1]:target_box[3], target_box[0]:target_box[2]] = source_face_resized
        
        return Image.fromarray(result)
    
    def _swap_basic(self, source_image: Image.Image, target_image: Image.Image) -> Optional[Image.Image]:
        """Basic face swap using OpenCV Haar Cascade"""
        # Load face detector
        try:
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        except:
            print("Could not load face detector")
            return None
        
        # Convert to OpenCV format
        source_cv = cv2.cvtColor(np.array(source_image.convert('RGB')), cv2.COLOR_RGB2BGR)
        target_cv = cv2.cvtColor(np.array(target_image.convert('RGB')), cv2.COLOR_RGB2BGR)
        
        # Detect faces
        source_gray = cv2.cvtColor(source_cv, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target_cv, cv2.COLOR_BGR2GRAY)
        
        source_faces = face_cascade.detectMultiScale(source_gray, 1.3, 5)
        target_faces = face_cascade.detectMultiScale(target_gray, 1.3, 5)
        
        if len(source_faces) == 0 or len(target_faces) == 0:
            print("Could not detect faces")
            return None
        
        # Use first face from each
        sx, sy, sw, sh = source_faces[0]
        tx, ty, tw, th = target_faces[0]
        
        # Extract and resize source face
        source_face = source_cv[sy:sy+sh, sx:sx+sw]
        source_face_resized = cv2.resize(source_face, (tw, th))
        
        # Create result
        result = target_cv.copy()
        
        # Simple blend with feathering
        mask = np.ones((th, tw), dtype=np.float32)
        
        # Create feathered edges
        feather = 10
        for i in range(feather):
            alpha = i / feather
            mask[i, :] *= alpha
            mask[th-1-i, :] *= alpha
            mask[:, i] *= alpha
            mask[:, tw-1-i] *= alpha
        
        # Blend
        for c in range(3):
            result[ty:ty+th, tx:tx+tw, c] = (
                source_face_resized[:, :, c] * mask + 
                result[ty:ty+th, tx:tx+tw, c] * (1 - mask)
            ).astype(np.uint8)
        
        # Convert back to PIL
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return Image.fromarray(result_rgb)
    
    def _get_face_box(self, landmarks: dict) -> tuple:
        """Get bounding box from face landmarks"""
        all_x = []
        all_y = []
        
        for feature in landmarks.values():
            for point in feature:
                all_x.append(point[0])
                all_y.append(point[1])
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        # Add padding
        padding = 20
        return (max(0, min_x - padding), max(0, min_y - padding),
                max_x + padding, max_y + padding)
