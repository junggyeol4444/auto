"""Proofreading module initialization"""
from .grammar_check import GrammarChecker
from .style_check import StyleChecker
from .consistency import ConsistencyChecker

__all__ = ['GrammarChecker', 'StyleChecker', 'ConsistencyChecker']
