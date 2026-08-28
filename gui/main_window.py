#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale de l'application Meeting & Project Manager AI.
Contient la sidebar de navigation et le stacked widget des pages.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
    QVBoxLayout, QPushButton, QLabel, QFrame, QSpacerItem,
    QSizePolicy
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application."""
    
    def __init__(self, db_manager, settings_manager):
        super().__init__()
        
        self.db_manager = db_manager
        self.settings_manager = settings_manager
        
        # Configuration de la fenêtre
        self.setWindowTitle("Meeting & Project Manager AI")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Création de la sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Création du stacked widget pour les pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("content_stack")
        main_layout.addWidget(self.stacked_widget)
        
        # Création des pages
        self._create_pages()
        
    def _create_sidebar(self) -> QFrame:
        """Crée la barre latérale de navigation."""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo / Titre de l'application
        title_frame = QFrame()
        title_frame.setFixedHeight(80)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("📊 Meeting Manager")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        layout.addWidget(title_frame)
        layout.addSpacing(20)
        
        # Boutons de navigation
        self.nav_buttons = {}
        
        buttons_config = [
            ("dashboard", "🏬 Tableau de bord", 0),
            ("reunions", "📅 Réunions", 1),
            ("projets", "📁 Projets", 2),
            ("settings", "⚙️ Paramètres", 3),
        ]
        
        for btn_id, text, index in buttons_config:
            btn = QPushButton(text)
            btn.setObjectName("nav_button")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=index: self._on_nav_clicked(idx))
            btn.setFixedHeight(50)
            
            self.nav_buttons[btn_id] = btn
            layout.addWidget(btn)
            
        # Espacer pour pousser vers le bas
        layout.addStretch()
        
        # Pied de sidebar
        footer_frame = QFrame()
        footer_frame.setFixedHeight(60)
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setAlignment(Qt.AlignCenter)
        
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #64748B; font-size: 9pt;")
        version_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(version_label)
        
        layout.addWidget(footer_frame)
        
        return sidebar
        
    def _create_pages(self):
        """Crée et ajoute toutes les pages au stacked widget."""
        from gui.pages.dashboard_page import DashboardPage
        from gui.pages.reunions_page import ReunionsPage
        from gui.pages.projets_page import ProjetsPage
        from gui.pages.settings_page import SettingsPage
        
        # Page Dashboard
        self.dashboard_page = DashboardPage(self.db_manager)
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Page Réunions
        self.reunions_page = ReunionsPage(self.db_manager, self.settings_manager)
        self.stacked_widget.addWidget(self.reunions_page)
        
        # Page Projets
        self.projets_page = ProjetsPage(self.db_manager)
        self.stacked_widget.addWidget(self.projets_page)
        
        # Page Paramètres
        self.settings_page = SettingsPage(self.settings_manager)
        self.stacked_widget.addWidget(self.settings_page)
        
    def _on_nav_clicked(self, index: int):
        """Gère le clic sur un bouton de navigation."""
        # Mettre à jour le stacked widget
        self.stacked_widget.setCurrentIndex(index)
        
        # Mettre à jour l'état des boutons
        button_ids = list(self.nav_buttons.keys())
        for btn_id, btn in self.nav_buttons.items():
            btn.setChecked(button_ids.index(btn_id) == index)
            
        # Rafraîchir la page si nécessaire
        if index == 0:  # Dashboard
            self.dashboard_page.refresh_data()
        elif index == 1:  # Réunions
            self.reunions_page.refresh_data()
        elif index == 2:  # Projets
            self.projets_page.refresh_data()
