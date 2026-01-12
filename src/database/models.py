"""
Database models for Smart Video Editor Pro
Stores learned editing patterns and profiles
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class EditingProfile(Base):
    """Stores editing profile information"""
    __tablename__ = 'editing_profiles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    scene_patterns = relationship("ScenePattern", back_populates="profile", cascade="all, delete-orphan")
    audio_patterns = relationship("AudioPattern", back_populates="profile", cascade="all, delete-orphan")


class ScenePattern(Base):
    """Stores learned scene change patterns"""
    __tablename__ = 'scene_patterns'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('editing_profiles.id'), nullable=False)
    
    # Scene characteristics
    avg_scene_duration = Column(Float)  # Average duration of scenes in seconds
    min_scene_duration = Column(Float)  # Minimum scene duration
    max_scene_duration = Column(Float)  # Maximum scene duration
    scene_change_threshold = Column(Float)  # Threshold for detecting scene changes
    
    profile = relationship("EditingProfile", back_populates="scene_patterns")


class AudioPattern(Base):
    """Stores learned audio/voice patterns"""
    __tablename__ = 'audio_patterns'
    
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('editing_profiles.id'), nullable=False)
    
    # Audio characteristics
    silence_threshold = Column(Float)  # dB threshold for silence
    min_silence_duration = Column(Float)  # Minimum silence duration to remove (seconds)
    speech_padding_before = Column(Float)  # Padding before speech (seconds)
    speech_padding_after = Column(Float)  # Padding after speech (seconds)
    
    profile = relationship("EditingProfile", back_populates="audio_patterns")


class Database:
    """Database manager class"""
    
    def __init__(self, db_path='data/video_editor.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def create_profile(self, name, description=''):
        """Create a new editing profile"""
        session = self.get_session()
        try:
            profile = EditingProfile(name=name, description=description)
            session.add(profile)
            session.commit()
            profile_id = profile.id
            session.refresh(profile)
            return profile
        finally:
            session.close()
    
    def get_profile(self, profile_name):
        """Get a profile by name"""
        session = self.get_session()
        try:
            return session.query(EditingProfile).filter_by(name=profile_name).first()
        finally:
            session.close()
    
    def get_all_profiles(self):
        """Get all profiles"""
        session = self.get_session()
        try:
            return session.query(EditingProfile).all()
        finally:
            session.close()
    
    def delete_profile(self, profile_name):
        """Delete a profile"""
        session = self.get_session()
        try:
            profile = session.query(EditingProfile).filter_by(name=profile_name).first()
            if profile:
                session.delete(profile)
                session.commit()
                return True
            return False
        finally:
            session.close()
