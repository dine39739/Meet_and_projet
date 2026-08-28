#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire des paramètres de l'application.
Gère la clé API Mistral et autres configurations.
"""

import os
import json
from typing import Optional, Dict, Any


class SettingsManager:
    """Gestionnaire des paramètres de l'application."""
    
    DEFAULT_SETTINGS = {
        "mistral_api_key": "",
        "mistral_model": "mistral-large-latest",
        "export_directory": "",
        "language": "fr"
    }
    
    def __init__(self, config_dir: str):
        """
        Initialise le gestionnaire de paramètres.
        
        Args:
            config_dir: Répertoire où stocker le fichier de configuration.
        """
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "settings.json")
        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self.load_settings()
        
    def load_settings(self) -> None:
        """Charge les paramètres depuis le fichier de configuration."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    # Fusionner avec les paramètres par défaut
                    for key, value in loaded_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erreur lors du chargement des paramètres: {e}")
                
    def save_settings(self) -> bool:
        """Sauvegarde les paramètres dans le fichier de configuration."""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}")
            return False
            
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère la valeur d'un paramètre."""
        return self.settings.get(key, default)
        
    def set(self, key: str, value: Any) -> bool:
        """
        Définit la valeur d'un paramètre et sauvegarde.
        
        Returns:
            True si la sauvegarde a réussi, False sinon.
        """
        if key in self.settings:
            self.settings[key] = value
            return self.save_settings()
        return False
        
    def get_mistral_api_key(self) -> str:
        """Récupère la clé API Mistral."""
        return self.settings.get("mistral_api_key", "")
        
    def set_mistral_api_key(self, api_key: str) -> bool:
        """Définit la clé API Mistral."""
        return self.set("mistral_api_key", api_key)
        
    def get_mistral_model(self) -> str:
        """Récupère le modèle Mistral utilisé."""
        return self.settings.get("mistral_model", "mistral-large-latest")
        
    def set_mistral_model(self, model: str) -> bool:
        """Définit le modèle Mistral utilisé."""
        return self.set("mistral_model", model)
        
    def get_export_directory(self) -> str:
        """Récupère le répertoire d'export par défaut."""
        export_dir = self.settings.get("export_directory", "")
        if not export_dir:
            # Par défaut, utiliser le répertoire Documents
            if os.name == "nt":  # Windows
                export_dir = os.path.join(os.path.expanduser("~"), "Documents")
            else:
                export_dir = os.path.join(os.path.expanduser("~"), "Documents")
        return export_dir
        
    def set_export_directory(self, directory: str) -> bool:
        """Définit le répertoire d'export par défaut."""
        return self.set("export_directory", directory)
        
    def get_language(self) -> str:
        """Récupère la langue de l'interface."""
        return self.settings.get("language", "fr")
        
    def set_language(self, language: str) -> bool:
        """Définit la langue de l'interface."""
        return self.set("language", language)
