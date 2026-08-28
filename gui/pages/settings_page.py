#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Paramètres - Configuration de l'application.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QLineEdit, QPushButton, QMessageBox, QGroupBox, QFormLayout,
    QFileDialog, QComboBox
)
from PySide6.QtCore import Qt


class SettingsPage(QWidget):
    """Page de configuration des paramètres."""
    
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre
        title_label = QLabel("⚙️ Paramètres")
        title_label.setObjectName("title_label")
        layout.addWidget(title_label)
        
        # Groupe API Mistral
        api_group = QGroupBox("Configuration API Mistral")
        api_layout = QFormLayout(api_group)
        
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("Entrez votre clé API Mistral")
        self.api_key_edit.setText(self.settings_manager.get_mistral_api_key())
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        api_layout.addRow("Clé API:", self.api_key_edit)
        
        self.show_api_btn = QPushButton("👁️ Afficher")
        self.show_api_btn.setObjectName("secondary_button")
        self.show_api_btn.setFixedWidth(100)
        self.show_api_btn.clicked.connect(self._toggle_api_key_visibility)
        api_layout.addRow("", self.show_api_btn)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "mistral-large-latest",
            "mistral-medium-latest",
            "mistral-small-latest",
            "open-mistral-7b",
            "open-mixtral-8x7b"
        ])
        current_model = self.settings_manager.get_mistral_model()
        index = self.model_combo.findText(current_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        api_layout.addRow("Modèle:", self.model_combo)
        
        self.test_api_btn = QPushButton("🧪 Tester la connexion")
        self.test_api_btn.setObjectName("secondary_button")
        self.test_api_btn.clicked.connect(self._test_api_connection)
        api_layout.addRow("", self.test_api_btn)
        
        layout.addWidget(api_group)
        
        # Groupe Export
        export_group = QGroupBox("Configuration des exports")
        export_layout = QFormLayout(export_group)
        
        self.export_dir_edit = QLineEdit()
        self.export_dir_edit.setText(self.settings_manager.get_export_directory())
        self.export_dir_edit.setReadOnly(True)
        export_layout.addRow("Répertoire d'export:", self.export_dir_edit)
        
        browse_btn = QPushButton("📂 Parcourir")
        browse_btn.setObjectName("secondary_button")
        browse_btn.clicked.connect(self._browse_export_directory)
        export_layout.addRow("", browse_btn)
        
        layout.addWidget(export_group)
        
        # Groupe Langue
        lang_group = QGroupBox("Langue")
        lang_layout = QFormLayout(lang_group)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            ("Français", "fr"),
            ("English", "en")
        ])
        current_lang = self.settings_manager.get_language()
        for i in range(self.lang_combo.count()):
            if self.lang_combo.itemData(i) == current_lang:
                self.lang_combo.setCurrentIndex(i)
                break
        lang_layout.addRow("Langue:", self.lang_combo)
        
        layout.addWidget(lang_group)
        
        # Boutons d'action
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("secondary_button")
        cancel_btn.clicked.connect(self._load_settings)
        action_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setObjectName("primary_button")
        save_btn.clicked.connect(self._save_settings)
        action_layout.addWidget(save_btn)
        
        layout.addLayout(action_layout)
        
        layout.addStretch()
        
    def _toggle_api_key_visibility(self):
        """Affiche/masque la clé API."""
        if self.api_key_edit.echoMode() == QLineEdit.Password:
            self.api_key_edit.setEchoMode(QLineEdit.Normal)
            self.show_api_btn.setText("🙈 Masquer")
        else:
            self.api_key_edit.setEchoMode(QLineEdit.Password)
            self.show_api_btn.setText("👁️ Afficher")
            
    def _browse_export_directory(self):
        """Parcourt le répertoire d'export."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le répertoire d'export",
            self.export_dir_edit.text()
        )
        
        if directory:
            self.export_dir_edit.setText(directory)
            
    def _test_api_connection(self):
        """Teste la connexion à l'API Mistral."""
        api_key = self.api_key_edit.text().strip()
        
        if not api_key:
            QMessageBox.warning(
                self,
                "Clé manquante",
                "Veuillez saisir une clé API."
            )
            return
            
        from backend.mistral_client import MistralClient
        
        client = MistralClient(api_key, self.model_combo.currentText())
        
        QMessageBox.information(
            self,
            "Test en cours",
            "Test de la connexion à l'API Mistral..."
        )
        
        if client.test_connection():
            QMessageBox.information(
                self,
                "Succès",
                "Connexion à l'API Mistral réussie !"
            )
        else:
            QMessageBox.critical(
                self,
                "Échec",
                "Impossible de se connecter à l'API Mistral.\n"
                "Vérifiez votre clé API et votre connexion internet."
            )
            
    def _save_settings(self):
        """Enregistre les paramètres."""
        # Clé API
        api_key = self.api_key_edit.text().strip()
        if api_key:
            self.settings_manager.set_mistral_api_key(api_key)
            
        # Modèle
        self.settings_manager.set_mistral_model(self.model_combo.currentText())
        
        # Répertoire d'export
        export_dir = self.export_dir_edit.text().strip()
        if export_dir:
            self.settings_manager.set_export_directory(export_dir)
            
        # Langue
        lang = self.lang_combo.currentData()
        self.settings_manager.set_language(lang)
        
        QMessageBox.information(
            self,
            "Succès",
            "Paramètres enregistrés avec succès."
        )
        
    def _load_settings(self):
        """Recharge les paramètres depuis le gestionnaire."""
        self.api_key_edit.setText(self.settings_manager.get_mistral_api_key())
        self.model_combo.setCurrentText(self.settings_manager.get_mistral_model())
        self.export_dir_edit.setText(self.settings_manager.get_export_directory())
        
        current_lang = self.settings_manager.get_language()
        for i in range(self.lang_combo.count()):
            if self.lang_combo.itemData(i) == current_lang:
                self.lang_combo.setCurrentIndex(i)
                break
