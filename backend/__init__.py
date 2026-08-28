# -*- coding: utf-8 -*-
"""
Backend package for Meeting & Project Manager AI.
"""

from .database_manager import DatabaseManager
from .settings_manager import SettingsManager
from .parser_teams import TeamsTranscriptParser
from .mistral_client import MistralClient
from .export_manager import ExportManager

__all__ = [
    "DatabaseManager",
    "SettingsManager",
    "TeamsTranscriptParser",
    "MistralClient",
    "ExportManager",
]
