#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Dashboard - Vue d'ensemble des statistiques et activités.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QGridLayout, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt


class DashboardPage(QWidget):
    """Page de tableau de bord avec les statistiques."""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre
        title_label = QLabel("🏬 Tableau de bord")
        title_label.setObjectName("title_label")
        layout.addWidget(title_label)
        
        # Scroll area pour le contenu
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll_area)
        
        # Widget contenu
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)
        
        # Cartes de statistiques
        self.stats_cards_layout = QGridLayout()
        self.stats_cards_layout.setSpacing(15)
        content_layout.addLayout(self.stats_cards_layout)
        
        # Section dernières réunions
        content_layout.addWidget(QLabel("<h3>📅 Dernières réunions</h3>"))
        self.last_reunions_frame = QFrame()
        self.last_reunions_frame.setObjectName("card")
        last_reunions_layout = QVBoxLayout(self.last_reunions_frame)
        content_layout.addWidget(self.last_reunions_frame)
        
        # Section projets actifs
        content_layout.addWidget(QLabel("<h3>📁 Projets actifs</h3>"))
        self.active_projets_frame = QFrame()
        self.active_projets_frame.setObjectName("card")
        active_projets_layout = QVBoxLayout(self.active_projets_frame)
        content_layout.addWidget(self.active_projets_frame)
        
        content_layout.addStretch()
        
        # Charger les données initiales
        self.refresh_data()
        
    def refresh_data(self):
        """Rafraîchit les données du dashboard."""
        # Nettoyer les cartes existantes
        while self.stats_cards_layout.count():
            item = self.stats_cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Récupérer les statistiques
        stats = self.db_manager.get_stats()
        
        # Créer les cartes de statistiques
        cards_config = [
            ("📁", "Total Projets", str(stats.get("total_projets", 0)), "card_blue"),
            ("📅", "Total Réunions", str(stats.get("total_reunions", 0)), "card_green"),
            ("✅", "Tâches Totales", str(stats.get("total_taches", 0)), "card_orange"),
        ]
        
        for i, (icon, title, value, card_style) in enumerate(cards_config):
            card = self._create_stat_card(icon, title, value, card_style)
            row = i // 3
            col = i % 3
            self.stats_cards_layout.addWidget(card, row, col)
            
        # Rafraîchir les dernières réunions
        self._refresh_last_reunions()
        
        # Rafraîchir les projets actifs
        self._refresh_active_projets()
        
    def _create_stat_card(self, icon: str, title: str, value: str, card_style: str) -> QFrame:
        """Crée une carte de statistique."""
        card = QFrame()
        card.setObjectName(card_style)
        card.setFixedHeight(120)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        
        # Icône et valeur
        value_label = QLabel(f"{icon} {value}")
        value_label.setObjectName("stats_number")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        # Titre
        title_label = QLabel(title)
        title_label.setObjectName("subtitle_label")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        return card
        
    def _refresh_last_reunions(self):
        """Rafraîchit la liste des dernières réunions."""
        layout = self.last_reunions_frame.layout()
        
        # Nettoyer
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        reunions = self.db_manager.get_all_reunions()[:5]  # 5 dernières
        
        if not reunions:
            label = QLabel("Aucune réunion enregistrée")
            label.setStyleSheet("color: #94A3B8; padding: 20px;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        else:
            for reunion in reunions:
                reunion_label = QLabel(
                    f"📅 <b>{reunion['titre']}</b> - {reunion['date']}"
                )
                reunion_label.setStyleSheet("padding: 8px;")
                layout.addWidget(reunion_label)
                
    def _refresh_active_projets(self):
        """Rafraîchit la liste des projets actifs."""
        layout = self.active_projets_frame.layout()
        
        # Nettoyer
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        projets = self.db_manager.get_all_projets()[:5]  # 5 premiers
        
        if not projets:
            label = QLabel("Aucun projet enregistré")
            label.setStyleSheet("color: #94A3B8; padding: 20px;")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        else:
            for projet in projets:
                statut_color = {
                    "En cours": "#3B82F6",
                    "Terminé": "#10B981",
                    "En pause": "#F59E0B",
                    "Annulé": "#EF4444"
                }.get(projet["statut"], "#64748B")
                
                projet_label = QLabel(
                    f"📁 <b>{projet['nom']}</b> - "
                    f"<span style='color: {statut_color};'>{projet['statut']}</span>"
                )
                projet_label.setStyleSheet("padding: 8px;")
                layout.addWidget(projet_label)
