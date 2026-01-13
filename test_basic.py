"""
Basic unit tests for Smart Video Editor Pro
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import unittest
from database.models import Database, EditingProfile


class TestDatabase(unittest.TestCase):
    """Test database functionality"""
    
    def setUp(self):
        """Set up test database"""
        self.db = Database('data/test_video_editor.db')
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists('data/test_video_editor.db'):
            os.remove('data/test_video_editor.db')
    
    def test_create_profile(self):
        """Test creating a profile"""
        profile = self.db.create_profile('Test Profile', 'Test description')
        self.assertIsNotNone(profile)
        self.assertEqual(profile.name, 'Test Profile')
        self.assertEqual(profile.description, 'Test description')
    
    def test_get_profile(self):
        """Test retrieving a profile"""
        self.db.create_profile('Test Profile 2', 'Another test')
        profile = self.db.get_profile('Test Profile 2')
        self.assertIsNotNone(profile)
        self.assertEqual(profile.name, 'Test Profile 2')
    
    def test_get_all_profiles(self):
        """Test getting all profiles"""
        self.db.create_profile('Profile 1')
        self.db.create_profile('Profile 2')
        profiles = self.db.get_all_profiles()
        self.assertEqual(len(profiles), 2)
    
    def test_delete_profile(self):
        """Test deleting a profile"""
        self.db.create_profile('To Delete')
        result = self.db.delete_profile('To Delete')
        self.assertTrue(result)
        profile = self.db.get_profile('To Delete')
        self.assertIsNone(profile)


class TestSceneDetector(unittest.TestCase):
    """Test scene detection functionality"""
    
    def test_calculate_scene_statistics(self):
        """Test scene statistics calculation"""
        from core.scene_detector import SceneDetector
        
        detector = SceneDetector()
        scenes = [(0.0, 2.5), (2.5, 5.0), (5.0, 8.5)]
        stats = detector.calculate_scene_statistics(scenes)
        
        self.assertEqual(stats['total_scenes'], 3)
        self.assertAlmostEqual(stats['avg_duration'], 2.833, places=2)
        self.assertEqual(stats['min_duration'], 2.5)
        self.assertEqual(stats['max_duration'], 3.5)


class TestAudioAnalyzer(unittest.TestCase):
    """Test audio analysis functionality"""
    
    def test_calculate_audio_statistics(self):
        """Test audio statistics calculation"""
        from core.audio_analyzer import AudioAnalyzer
        
        analyzer = AudioAnalyzer()
        voice_segments = [(0.5, 2.5), (3.0, 5.5), (6.0, 9.0)]
        total_duration = 10.0
        stats = analyzer.calculate_audio_statistics(voice_segments, total_duration)
        
        self.assertEqual(stats['total_voice_segments'], 3)
        self.assertEqual(stats['total_voice_time'], 7.5)
        self.assertEqual(stats['total_silence_time'], 2.5)
        self.assertEqual(stats['voice_percentage'], 75.0)


if __name__ == '__main__':
    # Run tests
    unittest.main()
