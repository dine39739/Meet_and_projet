#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Projets - Gestion des projets et suivi des tâches.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QListWidget, QListWidgetItem, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QSplitter, QMessageBox, 
    QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QDialogButtonBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from datetime import datetime


class ProjetDialog(QDialog):
    def __init__(self, parent=None, projet_data=None):
        super().__init__(parent)
        self.projet_data = projet_data
        self.setWindowTitle("Nouveau projet" if not projet_data else "Modifier le projet")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        self.nom_edit = QLineEdit()
        if projet_data:
            self.nom_edit.setText(projet_data.get("nom", ""))
        form_layout.addRow("Nom:", self.nom_edit)
        
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate().addMonths(1))
        if projet_data and projet_data.get("deadline"):
            try:
                date = datetime.strptime(projet_data["deadline"], "%d/%m/%Y")
                self.deadline_edit.setDate(QDate(date.year, date.month, date.day))
            except:
                pass
        form_layout.addRow("Deadline:", self.deadline_edit)
        
        self.statut_combo = QComboBox()
        self.statut_combo.addItems(["En cours", "Terminé", "En pause", "Annulé"])
        if projet_data:
            index = self.statut_combo.findText(projet_data.get("statut", "En cours"))
            if index >= 0:
                self.statut_combo.setCurrentIndex(index)
        form_layout.addRow("Statut:", self.statut_combo)
        
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        if projet_data:
            self.description_edit.setText(projet_data.get("description", ""))
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def get_data(self):
        return {
            "nom": self.nom_edit.text().strip(),
            "deadline": self.deadline_edit.date().toString("dd/MM/yyyy"),
            "statut": self.statut_combo.currentText(),
            "description": self.description_edit.toPlainText().strip()
        }


class ProjetsPage(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.current_projet_id = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        title_label = QLabel("📁 Gestion des Projets")
        title_label.setObjectName("title_label")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        new_btn = QPushButton("+ Nouveau projet")
        new_btn.setObjectName("primary_button")
        new_btn.clicked.connect(self._create_new_projet)
        header_layout.addWidget(new_btn)
        layout.addLayout(header_layout)
        
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.projets_list = QListWidget()
        self.projets_list.itemClicked.connect(self._on_projet_selected)
        left_layout.addWidget(self.projets_list)
        splitter.addWidget(left_widget)
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        self.info_group = QGroupBox("Informations du projet")
        info_layout = QFormLayout(self.info_group)
        self.nom_label = QLabel("")
        self.nom_label.setObjectName("subtitle_label")
        info_layout.addRow("Nom:", self.nom_label)
        self.deadline_label = QLabel("")
        info_layout.addRow("Deadline:", self.deadline_label)
        self.statut_label = QLabel("")
        info_layout.addRow("Statut:", self.statut_label)
        self.description_label = QLabel("")
        self.description_label.setWordWrap(True)
        info_layout.addRow("Description:", self.description_label)
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        self.edit_btn = QPushButton("✏️ Modifier")
        self.edit_btn.setObjectName("secondary_button")
        self.edit_btn.clicked.connect(self._edit_projet)
        action_layout.addWidget(self.edit_btn)
        self.delete_btn = QPushButton("🗑️ Supprimer")
        self.delete_btn.setObjectName("danger_button")
        self.delete_btn.clicked.connect(self._delete_projet)
        action_layout.addWidget(self.delete_btn)
        info_layout.addRow("", action_layout)
        right_layout.addWidget(self.info_group)
        
        taches_group = QGroupBox("Tâches associées")
        taches_layout = QVBoxLayout(taches_group)
        self.taches_table = QTableWidget()
        self.taches_table.setColumnCount(4)
        self.taches_table.setHorizontalHeaderLabels(["Tâche", "Responsable", "Échéance", "Statut"])
        self.taches_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.taches_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.taches_table.setAlternatingRowColors(True)
        taches_layout.addWidget(self.taches_table)
        
        taches_btn_layout = QHBoxLayout()
        add_tache_btn = QPushButton("+ Ajouter tâche")
        add_tache_btn.setObjectName("secondary_button")
        add_tache_btn.clicked.connect(self._add_tache)
        taches_btn_layout.addWidget(add_tache_btn)
        taches_btn_layout.addStretch()
        complete_tache_btn = QPushButton("✅ Marquer comme faite")
        complete_tache_btn.setObjectName("primary_button")
        complete_tache_btn.clicked.connect(self._complete_tache)
        taches_btn_layout.addWidget(complete_tache_btn)
        delete_tache_btn = QPushButton("🗑️ Supprimer tâche")
        delete_tache_btn.setObjectName("danger_button")
        delete_tache_btn.clicked.connect(self._delete_tache)
        taches_btn_layout.addWidget(delete_tache_btn)
        taches_layout.addLayout(taches_btn_layout)
        right_layout.addWidget(taches_group)
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        self._toggle_details_enabled(False)
        self.refresh_data()
        
    def refresh_data(self):
        self.projets_list.clear()
        projets = self.db_manager.get_all_projets()
        for projet in projets:
            statut_color = {"En cours": "#3B82F6", "Terminé": "#10B981", "En pause": "#F59E0B", "Annulé": "#EF4444"}.get(projet["statut"], "#64748B")
            item_text = f"📁 {projet['nom']} - <span style='color: {statut_color};'>{projet['statut']}</span>"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, projet["id"])
            self.projets_list.addItem(item)
        self.current_projet_id = None
        self._clear_details()
        
    def _clear_details(self):
        self.nom_label.setText("")
        self.deadline_label.setText("")
        self.statut_label.setText("")
        self.description_label.setText("")
        self.taches_table.setRowCount(0)
        self._toggle_details_enabled(False)
        
    def _toggle_details_enabled(self, enabled):
        self.edit_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
        
    def _on_projet_selected(self, item):
        projet_id = item.data(Qt.UserRole)
        if not projet_id:
            return
        projet = self.db_manager.get_projet_by_id(projet_id)
        if not projet:
            return
        self.current_projet_id = projet_id
        self.nom_label.setText(projet["nom"])
        self.deadline_label.setText(projet["deadline"] or "Non définie")
        self.statut_label.setText(projet["statut"])
        self.description_label.setText(projet["description"] or "Aucune description")
        self._load_taches(projet_id)
        self._toggle_details_enabled(True)
        
    def _load_taches(self, projet_id):
        taches = self.db_manager.get_all_taches(projet_id=projet_id)
        self.taches_table.setRowCount(len(taches))
        for i, tache in enumerate(taches):
            self.taches_table.setItem(i, 0, QTableWidgetItem(tache["description"]))
            self.taches_table.setItem(i, 1, QTableWidgetItem(tache["assigne_a"] or "Non assigné"))
            self.taches_table.setItem(i, 2, QTableWidgetItem(tache["deadline"] or "À définir"))
            statut_item = QTableWidgetItem(tache["statut"])
            if tache["statut"] == "Faite":
                statut_item.setBackground(Qt.green)
            elif tache["statut"] == "En cours":
                statut_item.setBackground(Qt.yellow)
            self.taches_table.setItem(i, 3, statut_item)
            
    def _create_new_projet(self):
        dialog = ProjetDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["nom"]:
                QMessageBox.warning(self, "Erreur", "Le nom du projet est obligatoire.")
                return
            self.db_manager.add_projet(**data)
            self.refresh_data()
            QMessageBox.information(self, "Succès", "Projet créé.")
            
    def _edit_projet(self):
        if not self.current_projet_id:
            return
        projet = self.db_manager.get_projet_by_id(self.current_projet_id)
        if not projet:
            return
        dialog = ProjetDialog(self, projet)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            self.db_manager.update_projet(self.current_projet_id, **data)
            self.refresh_data()
            for i in range(self.projets_list.count()):
                item = self.projets_list.item(i)
                if item.data(Qt.UserRole) == self.current_projet_id:
                    self.projets_list.setCurrentItem(item)
                    break
            QMessageBox.information(self, "Succès", "Projet mis à jour.")
            
    def _delete_projet(self):
        if not self.current_projet_id:
            return
        reply = QMessageBox.question(self, "Confirmation", "Voulez-vous vraiment supprimer ce projet ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db_manager.delete_projet(self.current_projet_id)
            self.refresh_data()
            QMessageBox.information(self, "Succès", "Projet supprimé.")
            
    def _add_tache(self):
        if not self.current_projet_id:
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouvelle tâche")
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        desc_edit = QTextEdit()
        desc_edit.setMaximumHeight(80)
        form.addRow("Description:", desc_edit)
        assigne_edit = QLineEdit()
        form.addRow("Assigné à:", assigne_edit)
        deadline_edit = QDateEdit()
        deadline_edit.setCalendarPopup(True)
        deadline_edit.setDate(QDate.currentDate().addDays(7))
        form.addRow("Échéance:", deadline_edit)
        layout.addLayout(form)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec() == QDialog.Accepted:
            desc = desc_edit.toPlainText().strip()
            if not desc:
                QMessageBox.warning(self, "Erreur", "La description est obligatoire.")
                return
            self.db_manager.add_tache(reunion_id=None, projet_id=self.current_projet_id, description=desc, assigne_a=assigne_edit.text().strip(), deadline=deadline_edit.date().toString("dd/MM/yyyy"), statut="À faire")
            self._load_taches(self.current_projet_id)
            QMessageBox.information(self, "Succès", "Tâche ajoutée.")
            
    def _complete_tache(self):
        row = self.taches_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attention", "Sélectionnez une tâche.")
            return
        taches = self.db_manager.get_all_taches(projet_id=self.current_projet_id)
        if row < len(taches):
            tache_id = taches[row]["id"]
            self.db_manager.update_tache(tache_id, statut="Faite")
            self._load_taches(self.current_projet_id)
            
    def _delete_tache(self):
        row = self.taches_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attention", "Sélectionnez une tâche.")
            return
        taches = self.db_manager.get_all_taches(projet_id=self.current_projet_id)
        if row < len(taches):
            tache_id = taches[row]["id"]
            self.db_manager.delete_tache(tache_id)
            self._load_taches(self.current_projet_id)
