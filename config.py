"""
Advanced configuration for PDF extraction system.
Allows fine-tuning of extraction parameters.
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for PDF extraction system."""

    # Performance settings
    MAX_PAGES_FOR_FONT_ANALYSIS = int(os.getenv('MAX_PAGES_FOR_FONT_ANALYSIS', '10'))
    FONT_SIZE_PRECISION = float(os.getenv('FONT_SIZE_PRECISION', '0.1'))
    MIN_HEADING_FREQUENCY = float(os.getenv('MIN_HEADING_FREQUENCY', '0.001'))

    # Text processing settings
    MIN_TEXT_LENGTH = int(os.getenv('MIN_TEXT_LENGTH', '3'))
    MAX_HEADING_LEVELS = int(os.getenv('MAX_HEADING_LEVELS', '6'))
    COMBINE_CONSECUTIVE_TEXT = bool(os.getenv('COMBINE_CONSECUTIVE_TEXT', 'True').lower() == 'true')

    # Language support settings
    MULTILINGUAL_SUPPORT = bool(os.getenv('MULTILINGUAL_SUPPORT', 'True').lower() == 'true')
    DEFAULT_ENCODING = os.getenv('DEFAULT_ENCODING', 'utf-8')

    # Memory optimization
    PROCESS_PAGES_IN_CHUNKS = bool(os.getenv('PROCESS_PAGES_IN_CHUNKS', 'False').lower() == 'true')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '10'))

    # Debug settings
    DEBUG_MODE = bool(os.getenv('DEBUG_MODE', 'False').lower() == 'true')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return {
            'max_pages_for_font_analysis': cls.MAX_PAGES_FOR_FONT_ANALYSIS,
            'font_size_precision': cls.FONT_SIZE_PRECISION,
            'min_heading_frequency': cls.MIN_HEADING_FREQUENCY,
            'min_text_length': cls.MIN_TEXT_LENGTH,
            'max_heading_levels': cls.MAX_HEADING_LEVELS,
            'combine_consecutive_text': cls.COMBINE_CONSECUTIVE_TEXT,
            'multilingual_support': cls.MULTILINGUAL_SUPPORT,
            'default_encoding': cls.DEFAULT_ENCODING,
            'process_pages_in_chunks': cls.PROCESS_PAGES_IN_CHUNKS,
            'chunk_size': cls.CHUNK_SIZE,
            'debug_mode': cls.DEBUG_MODE,
            'log_level': cls.LOG_LEVEL
        }