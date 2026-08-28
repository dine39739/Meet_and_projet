#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Réunions - Gestion des réunions, transcriptions et génération de comptes-rendus.
"""

import os
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QListWidget, QListWidgetItem, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QSplitter, QFileDialog,
    QMessageBox, QGroupBox, QFormLayout, QApplication
)
from PySide6.QtCore import Qt, QThread, Signal

from backend.mistral_client import MistralClient


class MistralWorker(QThread):
    finished = Signal(str, list)
    error = Signal(str)
    
    def __init__(self, mistral_client, transcript, ordre_du_jour=""):
        super().__init__()
        self.mistral_client = mistral_client
        self.transcript = transcript
        self.ordre_du_jour = ordre_du_jour
        
    def run(self):
        try:
            compte_rendu, taches = self.mistral_client.generate_compte_rendu(
                self.transcript, self.ordre_du_jour
            )
            self.finished.emit(compte_rendu, taches)
        except Exception as e:
            self.error.emit(str(e))


class ReunionsPage(QWidget):
    def __init__(self, db_manager, settings_manager):
        super().__init__()
        self.db_manager = db_manager
        self.settings_manager = settings_manager
        self.current_reunion_id = None
        self.worker = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_label = QLabel("📅 Gestion des Réunions")
        title_label.setObjectName("title_label")
        layout.addWidget(title_label)
        
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Partie gauche
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        new_btn = QPushButton("+ Nouvelle réunion")
        new_btn.setObjectName("primary_button")
        new_btn.clicked.connect(self._create_new_reunion)
        left_layout.addWidget(new_btn)
        
        self.reunions_list = QListWidget()
        self.reunions_list.itemClicked.connect(self._on_reunion_selected)
        left_layout.addWidget(self.reunions_list)
        
        splitter.addWidget(left_widget)
        
        # Partie droite
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        info_group = QGroupBox("Informations de la réunion")
        info_layout = QFormLayout(info_group)
        
        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText("JJ/MM/AAAA")
        info_layout.addRow("Date:", self.date_edit)
        
        self.titre_edit = QLineEdit()
        self.titre_edit.setPlaceholderText("Titre de la réunion")
        info_layout.addRow("Titre:", self.titre_edit)
        
        self.odj_edit = QTextEdit()
        self.odj_edit.setMaximumHeight(80)
        self.odj_edit.setPlaceholderText("Ordre du jour...")
        info_layout.addRow("Ordre du jour:", self.odj_edit)
        
        self.projet_combo = QComboBox()
        self.projet_combo.addItem("Aucun projet", None)
        info_layout.addRow("Projet associé:", self.projet_combo)
        
        right_layout.addWidget(info_group)
        
        buttons_layout = QHBoxLayout()
        self.import_btn = QPushButton("📂 Importer transcription")
        self.import_btn.setObjectName("secondary_button")
        self.import_btn.clicked.connect(self._import_transcript)
        buttons_layout.addWidget(self.import_btn)
        
        self.generate_btn = QPushButton("🤖 Générer CR avec IA")
        self.generate_btn.setObjectName("primary_button")
        self.generate_btn.clicked.connect(self._generate_compte_rendu)
        buttons_layout.addWidget(self.generate_btn)
        right_layout.addLayout(buttons_layout)
        
        transcript_group = QGroupBox("Transcription brute")
        transcript_layout = QVBoxLayout(transcript_group)
        self.transcript_edit = QTextEdit()
        self.transcript_edit.setPlaceholderText("La transcription apparaîtra ici...")
        self.transcript_edit.setReadOnly(True)
        transcript_layout.addWidget(self.transcript_edit)
        right_layout.addWidget(transcript_group)
        
        cr_group = QGroupBox("Compte-rendu généré")
        cr_layout = QVBoxLayout(cr_group)
        self.cr_edit = QTextEdit()
        self.cr_edit.setPlaceholderText("Le compte-rendu généré par l'IA apparaîtra ici...")
        cr_layout.addWidget(self.cr_edit)
        
        export_layout = QHBoxLayout()
        self.export_word_btn = QPushButton("📄 Export Word")
        self.export_word_btn.setObjectName("secondary_button")
        self.export_word_btn.clicked.connect(lambda: self._export_to("word"))
        export_layout.addWidget(self.export_word_btn)
        
        self.export_pdf_btn = QPushButton("📕 Export PDF")
        self.export_pdf_btn.setObjectName("secondary_button")
        self.export_pdf_btn.clicked.connect(lambda: self._export_to("pdf"))
        export_layout.addWidget(self.export_pdf_btn)
        
        export_layout.addStretch()
        
        self.save_btn = QPushButton("💾 Enregistrer")
        self.save_btn.setObjectName("primary_button")
        self.save_btn.clicked.connect(self._save_reunion)
        export_layout.addWidget(self.save_btn)
        
        self.delete_btn = QPushButton("🗑️ Supprimer")
        self.delete_btn.setObjectName("danger_button")
        self.delete_btn.clicked.connect(self._delete_reunion)
        export_layout.addWidget(self.delete_btn)
        
        cr_layout.addLayout(export_layout)
        right_layout.addWidget(cr_group)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        self.refresh_data()
        
    def refresh_data(self):
        self.reunions_list.clear()
        reunions = self.db_manager.get_all_reunions()
        for reunion in reunions:
            item_text = f"📅 {reunion['titre']} - {reunion['date']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, reunion['id'])
            self.reunions_list.addItem(item)
        
        self.projet_combo.clear()
        self.projet_combo.addItem("Aucun projet", None)
        projets = self.db_manager.get_all_projets()
        for projet in projets:
            self.projet_combo.addItem(projet['nom'], projet['id'])
        
        self.current_reunion_id = None
        self._clear_form()
        
    def _clear_form(self):
        self.date_edit.clear()
        self.titre_edit.clear()
        self.odj_edit.clear()
        self.projet_combo.setCurrentIndex(0)
        self.transcript_edit.clear()
        self.cr_edit.clear()
        self._toggle_form_enabled(False)
        
    def _toggle_form_enabled(self, enabled):
        self.date_edit.setEnabled(enabled)
        self.titre_edit.setEnabled(enabled)
        self.odj_edit.setEnabled(enabled)
        self.projet_combo.setEnabled(enabled)
        self.import_btn.setEnabled(enabled)
        self.generate_btn.setEnabled(enabled and bool(self.transcript_edit.toPlainText()))
        self.save_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
        self.export_word_btn.setEnabled(enabled and bool(self.cr_edit.toPlainText()))
        self.export_pdf_btn.setEnabled(enabled and bool(self.cr_edit.toPlainText()))
        
    def _create_new_reunion(self):
        self._clear_form()
        self.current_reunion_id = None
        self._toggle_form_enabled(True)
        self.date_edit.setText(datetime.now().strftime("%d/%m/%Y"))
        self.reunions_list.clearSelection()
        
    def _on_reunion_selected(self, item):
        reunion_id = item.data(Qt.UserRole)
        if not reunion_id:
            return
        reunion = self.db_manager.get_reunion_by_id(reunion_id)
        if not reunion:
            return
        self.current_reunion_id = reunion_id
        self.date_edit.setText(reunion['date'])
        self.titre_edit.setText(reunion['titre'])
        self.odj_edit.setText(reunion['ordre_du_jour'] or "")
        self.transcript_edit.setText(reunion['transcript_brut'] or "")
        self.cr_edit.setText(reunion['compte_rendu'] or "")
        if reunion.get('projet_id'):
            for i in range(self.projet_combo.count()):
                if self.projet_combo.itemData(i) == reunion['projet_id']:
                    self.projet_combo.setCurrentIndex(i)
                    break
        self._toggle_form_enabled(True)
        
    def _import_transcript(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importer une transcription", "",
            "Fichiers VTT/TXT (*.vtt *.txt);;Tous les fichiers (*)"
        )
        if not file_path:
            return
        try:
            from backend.parser_teams import TeamsTranscriptParser
            parser = TeamsTranscriptParser()
            transcript = parser.parse_file(file_path)
            self.transcript_edit.setText(transcript)
            participants = parser.extract_participants(transcript)
            if participants:
                QMessageBox.information(self, "Participants détectés", f"Participants extraits: {', '.join(participants)}")
            self.generate_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'import", f"Impossible de lire le fichier: {str(e)}")
            
    def _generate_compte_rendu(self):
        api_key = self.settings_manager.get_mistral_api_key()
        if not api_key:
            QMessageBox.warning(self, "Clé API manquante", "Veuillez configurer votre clé API Mistral dans les paramètres.")
            return
        transcript = self.transcript_edit.toPlainText()
        if not transcript:
            QMessageBox.warning(self, "Transcription vide", "Veuillez importer une transcription.")
            return
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("⏳ Génération en cours...")
        QApplication.processEvents()
        model = self.settings_manager.get_mistral_model()
        mistral_client = MistralClient(api_key, model)
        self.worker = MistralWorker(mistral_client, transcript, self.odj_edit.toPlainText())
        self.worker.finished.connect(self._on_generation_finished)
        self.worker.error.connect(self._on_generation_error)
        self.worker.start()
        
    def _on_generation_finished(self, compte_rendu, taches):
        self.cr_edit.setText(compte_rendu)
        if self.current_reunion_id and taches:
            for tache_data in taches:
                self.db_manager.add_tache(
                    reunion_id=self.current_reunion_id,
                    description=tache_data.get('tache', ''),
                    assigne_a=tache_data.get('responsable', ''),
                    deadline=tache_data.get('deadline', '')
                )
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🤖 Générer CR avec IA")
        self.export_word_btn.setEnabled(True)
        self.export_pdf_btn.setEnabled(True)
        
    def _on_generation_error(self, error_msg):
        QMessageBox.critical(self, "Erreur de génération", f"Impossible de générer le compte-rendu: {error_msg}")
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("🤖 Générer CR avec IA")
        
    def _save_reunion(self):
        titre = self.titre_edit.text().strip()
        if not titre:
            QMessageBox.warning(self, "Titre manquant", "Veuillez saisir un titre.")
            return
        if self.current_reunion_id:
            self.db_manager.update_reunion(
                self.current_reunion_id, date=self.date_edit.text(), titre=titre,
                ordre_du_jour=self.odj_edit.toPlainText(),
                transcript_brut=self.transcript_edit.toPlainText(),
                compte_rendu=self.cr_edit.toPlainText()
            )
            QMessageBox.information(self, "Succès", "Réunion mise à jour.")
        else:
            self.current_reunion_id = self.db_manager.add_reunion(
                date=self.date_edit.text(), titre=titre,
                ordre_du_jour=self.odj_edit.toPlainText(),
                transcript_brut=self.transcript_edit.toPlainText(),
                compte_rendu=self.cr_edit.toPlainText()
            )
            QMessageBox.information(self, "Succès", "Réunion créée.")
        self.refresh_data()
        for i in range(self.reunions_list.count()):
            item = self.reunions_list.item(i)
            if item.data(Qt.UserRole) == self.current_reunion_id:
                self.reunions_list.setCurrentItem(item)
                break
                
    def _delete_reunion(self):
        if not self.current_reunion_id:
            return
        reply = QMessageBox.question(self, "Confirmation", "Voulez-vous vraiment supprimer cette réunion ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db_manager.delete_reunion(self.current_reunion_id)
            self.refresh_data()
            QMessageBox.information(self, "Succès", "Réunion supprimée.")
            
    def _export_to(self, format_type):
        if not self.cr_edit.toPlainText():
            QMessageBox.warning(self, "Compte-rendu vide", "Aucun compte-rendu à exporter.")
            return
        from backend.export_manager import ExportManager
        titre = self.titre_edit.text() or "Reunion"
        date = self.date_edit.text() or datetime.now().strftime("%d/%m/%Y")
        compte_rendu = self.cr_edit.toPlainText()
        taches = []
        if self.current_reunion_id:
            taches = self.db_manager.get_all_taches(reunion_id=self.current_reunion_id)
        export_manager = ExportManager()
        default_filename = export_manager.generate_filename(titre, format_type)
        export_dir = self.settings_manager.get_export_directory()
        default_path = os.path.join(export_dir, default_filename)
        if format_type == "word":
            file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en Word", default_path, "Documents Word (*.docx)")
            if file_path:
                if export_manager.export_to_word(titre, date, compte_rendu, taches, file_path):
                    QMessageBox.information(self, "Succès", f"Export Word réussi: {file_path}")
                else:
                    QMessageBox.critical(self, "Erreur", "Échec de l'export Word.")
        elif format_type == "pdf":
            file_path, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", default_path, "Documents PDF (*.pdf)")
            if file_path:
                if export_manager.export_to_pdf(titre, date, compte_rendu, taches, file_path):
                    QMessageBox.information(self, "Succès", f"Export PDF réussi: {file_path}")
                else:
                    QMessageBox.critical(self, "Erreur", "Échec de l'export PDF.")
