#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feuille de style QSS globale pour Meeting & Project Manager AI.
Design moderne avec couleurs professionnelles.
"""


def get_global_stylesheet() -> str:
    """
    Retourne la feuille de style QSS complète pour l'application.
    
    Returns:
        La feuille de style sous forme de chaîne.
    """
    return """
/* ============================================
   STYLE GLOBAL - Meeting & Project Manager AI
   ============================================ */

/* Widget principal */
QWidget {
    background-color: #F5F7FA;
    color: #1E293B;
    font-family: "Segoe UI", "Roboto", sans-serif;
    font-size: 10pt;
}

/* ============================================
   SIDEBAR (Barre latérale)
   ============================================ */
QFrame#sidebar {
    background-color: #1E293B;
    border-right: 1px solid #334155;
    min-width: 250px;
    max-width: 250px;
}

/* Boutons de navigation */
QPushButton#nav_button {
    background-color: transparent;
    border: none;
    border-left: 4px solid transparent;
    padding: 12px 16px;
    text-align: left;
    color: #94A3B8;
    font-size: 10pt;
    font-weight: 500;
    border-radius: 0px;
}

QPushButton#nav_button:hover {
    background-color: #334155;
    color: #E2E8F0;
}

QPushButton#nav_button:checked {
    background-color: #334155;
    color: #FFFFFF;
    border-left: 4px solid #3B82F6;
}

/* Icônes dans les boutons */
QPushButton#nav_button::indicator {
    width: 0px;
    height: 0px;
}

/* ============================================
   BOUTONS PRIMAIRES
   ============================================ */
QPushButton#primary_button {
    background-color: #3B82F6;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 10pt;
}

QPushButton#primary_button:hover {
    background-color: #2563EB;
}

QPushButton#primary_button:pressed {
    background-color: #1D4ED8;
}

QPushButton#primary_button:disabled {
    background-color: #94A3B8;
    color: #CBD5E1;
}

/* ============================================
   BOUTONS SECONDAIRES
   ============================================ */
QPushButton#secondary_button {
    background-color: #FFFFFF;
    color: #1E293B;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 10pt;
}

QPushButton#secondary_button:hover {
    background-color: #F1F5F9;
    border-color: #94A3B8;
}

QPushButton#secondary_button:pressed {
    background-color: #E2E8F0;
}

/* ============================================
   BOUTONS DANGER
   ============================================ */
QPushButton#danger_button {
    background-color: #EF4444;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 10pt;
}

QPushButton#danger_button:hover {
    background-color: #DC2626;
}

QPushButton#danger_button:pressed {
    background-color: #B91C1C;
}

/* ============================================
   CARTES (Cards)
   ============================================ */
QFrame#card {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
}

QFrame#card:hover {
    border-color: #CBD5E1;
}

/* Cartes avec bordure gauche colorée */
QFrame#card_blue {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #3B82F6;
}

QFrame#card_green {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #10B981;
}

QFrame#card_orange {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #F59E0B;
}

QFrame#card_red {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #EF4444;
}

/* ============================================
   LABELS ET TITRES
   ============================================ */
QLabel#title_label {
    font-size: 18pt;
    font-weight: 700;
    color: #1E293B;
}

QLabel#subtitle_label {
    font-size: 12pt;
    font-weight: 600;
    color: #64748B;
}

QLabel#normal_label {
    font-size: 10pt;
    color: #334155;
}

QLabel#stats_number {
    font-size: 24pt;
    font-weight: 700;
    color: #3B82F6;
}

/* ============================================
   CHAMPS DE SAISIE (QLineEdit)
   ============================================ */
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 8px 12px;
    color: #1E293B;
    selection-background-color: #3B82F6;
    selection-color: #FFFFFF;
}

QLineEdit:focus {
    border-color: #3B82F6;
}

QLineEdit:disabled {
    background-color: #F1F5F9;
    color: #94A3B8;
}

/* ============================================
   ZONES DE TEXTE (QTextEdit, QPlainTextEdit)
   ============================================ */
QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 8px;
    color: #1E293B;
    selection-background-color: #3B82F6;
    selection-color: #FFFFFF;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #3B82F6;
}

QTextEdit:disabled, QPlainTextEdit:disabled {
    background-color: #F1F5F9;
    color: #94A3B8;
}

/* ============================================
   COMBOBOX
   ============================================ */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 8px 12px;
    color: #1E293B;
}

QComboBox:focus {
    border-color: #3B82F6;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #CBD5E1;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #64748B;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    selection-background-color: #3B82F6;
    selection-color: #FFFFFF;
}

QComboBox QAbstractItemView::item {
    padding: 8px 12px;
}

/* ============================================
   LISTES (QListWidget)
   ============================================ */
QListWidget {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    outline: none;
}

QListWidget::item {
    padding: 10px 12px;
    border-bottom: 1px solid #F1F5F9;
}

QListWidget::item:selected {
    background-color: #EFF6FF;
    color: #1E293B;
    border-left: 3px solid #3B82F6;
}

QListWidget::item:hover {
    background-color: #F8FAFC;
}

/* ============================================
   TABLEAUX (QTableWidget)
   ============================================ */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    gridline-color: #E2E8F0;
    outline: none;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #EFF6FF;
    color: #1E293B;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #64748B;
    font-weight: 600;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #E2E8F0;
}

/* ============================================
   SPLITTER
   ============================================ */
QSplitter::handle {
    background-color: #E2E8F0;
    width: 4px;
}

QSplitter::handle:hover {
    background-color: #3B82F6;
}

/* ============================================
   SCROLLBARS
   ============================================ */
QScrollBar:vertical {
    background-color: #F8FAFC;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #CBD5E1;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #F8FAFC;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #CBD5E1;
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ============================================
   GROUPBOX
   ============================================ */
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: 600;
    color: #1E293B;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 8px;
    color: #64748B;
}

/* ============================================
   CHECKBOX ET RADIO
   ============================================ */
QCheckBox, QRadioButton {
    color: #334155;
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #CBD5E1;
    background-color: #FFFFFF;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #3B82F6;
    border-color: #3B82F6;
}

QCheckBox::indicator:hover, QRadioButton::indicator:hover {
    border-color: #3B82F6;
}

/* ============================================
   PROGRESS BAR
   ============================================ */
QProgressBar {
    background-color: #E2E8F0;
    border-radius: 6px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #3B82F6;
    border-radius: 6px;
}

/* ============================================
   TAB WIDGET
   ============================================ */
QTabWidget::pane {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
}

QTabBar::tab {
    background-color: #F8FAFC;
    color: #64748B;
    padding: 10px 20px;
    border: 1px solid transparent;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #3B82F6;
    border-color: #E2E8F0;
    border-bottom: 2px solid #FFFFFF;
}

QTabBar::tab:hover:!selected {
    background-color: #FFFFFF;
    color: #1E293B;
}

/* ============================================
   TOOL TIP
   ============================================ */
QToolTip {
    background-color: #1E293B;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 9pt;
}

/* ============================================
   STACKED WIDGET
   ============================================ */
QStackedWidget {
    background-color: #F5F7FA;
}

/* ============================================
   SPINBOX
   ============================================ */
QSpinBox, QDoubleSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px 10px;
    color: #1E293B;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #3B82F6;
}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    width: 16px;
    border: none;
    background-color: transparent;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #F1F5F9;
}
"""
