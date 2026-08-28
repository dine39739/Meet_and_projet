#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meeting & Project Manager AI
Point d'entrée principal de l'application.
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from backend.database_manager import DatabaseManager
from backend.settings_manager import SettingsManager
from gui.main_window import MainWindow


def main():
    """Fonction principale de l'application."""
    
    # Configuration du chemin de la base de données
    if sys.platform == "win32":
        app_data_path = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "MeetingManager"
        )
    else:
        app_data_path = os.path.join(
            os.path.expanduser("~"),
            ".local",
            "share",
            "MeetingManager"
        )
    
    os.makedirs(app_data_path, exist_ok=True)
    db_path = os.path.join(app_data_path, "meeting_manager_data.db")
    
    # Initialisation de la base de données
    db_manager = DatabaseManager(db_path)
    db_manager.create_tables()
    
    # Initialisation des paramètres
    settings_manager = SettingsManager(app_data_path)
    
    # Création de l'application Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Meeting & Project Manager AI")
    app.setOrganizationName("MeetingManager")
    
    # Configuration de la police par défaut
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Style global
    from gui.styles import get_global_stylesheet
    app.setStyleSheet(get_global_stylesheet())
    
    # Création et affichage de la fenêtre principale
    window = MainWindow(db_manager, settings_manager)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
