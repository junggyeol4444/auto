"""Webnovel module initialization"""
from .generator import WebNovelGenerator
from .character import CharacterGenerator
from .plot import PlotGenerator
from .dialogue import DialogueGenerator

__all__ = ['WebNovelGenerator', 'CharacterGenerator', 'PlotGenerator', 'DialogueGenerator']
