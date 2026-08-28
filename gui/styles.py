"""
Feuille de style QSS moderne pour Meeting & Project Manager AI
Design inspiré du Material Design 3 et des interfaces modernes
"""

STYLESHEET = """
/* ========================================
   VARIABLES GLOBALES & RESET
   ======================================== */
QMainWindow, QWidget {
    background-color: #F8FAFC;
    font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
    font-size: 14px;
    color: #334155;
}

/* ========================================
   SCROLLBARS MODERNES
   ======================================== */
QScrollBar:vertical {
    background-color: #F1F5F9;
    width: 10px;
    border-radius: 5px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #CBD5E1;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #F1F5F9;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #CBD5E1;
    min-width: 30px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #94A3B8;
}

/* ========================================
   SIDEBAR DE NAVIGATION
   ======================================== */
QFrame#sidebar {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0F172A, stop:1 #1E293B);
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
    padding: 20px 10px;
}

QPushButton#nav_button {
    background-color: transparent;
    border: none;
    border-left: 4px solid transparent;
    border-radius: 12px;
    padding: 15px 20px;
    text-align: left;
    font-size: 15px;
    font-weight: 500;
    color: #94A3B8;
    margin: 5px 10px;
    transition: all 0.3s ease;
}

QPushButton#nav_button:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #F8FAFC;
}

QPushButton#nav_button:checked {
    background-color: rgba(59, 130, 246, 0.15);
    border-left: 4px solid #3B82F6;
    color: #3B82F6;
    font-weight: 600;
}

QLabel#app_title {
    color: #F8FAFC;
    font-size: 20px;
    font-weight: 700;
    padding: 20px 20px 30px 20px;
    letter-spacing: 0.5px;
}

QLabel#app_subtitle {
    color: #64748B;
    font-size: 12px;
    padding: 0px 20px 20px 20px;
}

/* ========================================
   CARTES & CONTENUS
   ======================================== */
QFrame#content_area {
    background-color: #F8FAFC;
    border-radius: 0px;
}

QFrame#card {
    background-color: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
}

QFrame#stat_card {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #FFFFFF, stop:1 #F8FAFC);
    border-radius: 16px;
    border: 1px solid #E2E8F0;
}

QLabel#stat_title {
    color: #64748B;
    font-size: 13px;
    font-weight: 500;
}

QLabel#stat_value {
    color: #0F172A;
    font-size: 32px;
    font-weight: 700;
}

QLabel#card_title {
    color: #0F172A;
    font-size: 18px;
    font-weight: 600;
    padding: 10px;
}

/* ========================================
   BOUTONS
   ======================================== */
QPushButton#primary_button {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3B82F6, stop:1 #2563EB);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    min-width: 120px;
}

QPushButton#primary_button:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2563EB, stop:1 #1D4ED8);
}

QPushButton#primary_button:pressed {
    background-color: #1D4ED8;
}

QPushButton#secondary_button {
    background-color: #FFFFFF;
    color: #3B82F6;
    border: 2px solid #3B82F6;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#secondary_button:hover {
    background-color: #EFF6FF;
}

QPushButton#danger_button {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #EF4444, stop:1 #DC2626);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#danger_button:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #DC2626, stop:1 #B91C1C);
}

QPushButton#icon_button {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 8px;
    color: #64748B;
}

QPushButton#icon_button:hover {
    background-color: #F1F5F9;
    color: #3B82F6;
}

/* ========================================
   CHAMPS DE SAISIE
   ======================================== */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QDateEdit, QSpinBox {
    background-color: #FFFFFF;
    border: 2px solid #E2E8F0;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 14px;
    color: #334155;
    selection-background-color: #3B82F6;
    selection-color: white;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, 
QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
    border: 2px solid #3B82F6;
    outline: none;
}

QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover,
QComboBox:hover, QDateEdit:hover, QSpinBox:hover {
    border: 2px solid #CBD5E1;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #64748B;
    margin-right: 10px;
}

/* ========================================
   TABLEAUX & LISTES
   ======================================== */
QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    gridline-color: #F1F5F9;
    selection-background-color: #EFF6FF;
    selection-color: #334155;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #F1F5F9;
}

QTableWidget::item:selected {
    background-color: #DBEAFE;
    color: #1E40AF;
    border-radius: 6px;
}

QTableWidget::item:hover {
    background-color: #F8FAFC;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #64748B;
    font-weight: 600;
    font-size: 13px;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #E2E8F0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QListWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    outline: none;
}

QListWidget::item {
    padding: 12px 16px;
    border-bottom: 1px solid #F1F5F9;
    border-radius: 8px;
    margin: 2px 8px;
}

QListWidget::item:selected {
    background-color: #EFF6FF;
    color: #3B82F6;
    border-left: 4px solid #3B82F6;
}

QListWidget::item:hover {
    background-color: #F8FAFC;
}

/* ========================================
   ONGLETS & SPLITTERS
   ======================================== */
QTabWidget::pane {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    background-color: #FFFFFF;
    top: -1px;
}

QTabBar::tab {
    background-color: #F1F5F9;
    color: #64748B;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #3B82F6;
    border-bottom: 2px solid #3B82F6;
}

QTabBar::tab:hover:!selected {
    background-color: #E2E8F0;
}

QSplitter::handle {
    background-color: #E2E8F0;
    border-radius: 2px;
}

QSplitter::handle:horizontal {
    width: 4px;
}

QSplitter::handle:vertical {
    height: 4px;
}

QSplitter::handle:hover {
    background-color: #3B82F6;
}

/* ========================================
   CHECKBOXES & RADIOS
   ======================================== */
QCheckBox, QRadioButton {
    color: #334155;
    spacing: 8px;
    font-size: 14px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid #CBD5E1;
    background-color: #FFFFFF;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #3B82F6;
    border: 2px solid #3B82F6;
}

QRadioButton::indicator {
    border-radius: 10px;
}

/* ========================================
   LABELS & TITRES
   ======================================== */
QLabel {
    color: #334155;
}

QLabel#section_title {
    font-size: 24px;
    font-weight: 700;
    color: #0F172A;
    padding: 10px 0px;
}

QLabel#status_active {
    color: #10B981;
    font-weight: 600;
    background-color: #D1FAE5;
    padding: 4px 12px;
    border-radius: 20px;
}

QLabel#status_pending {
    color: #F59E0B;
    font-weight: 600;
    background-color: #FEF3C7;
    padding: 4px 12px;
    border-radius: 20px;
}

QLabel#status_completed {
    color: #3B82F6;
    font-weight: 600;
    background-color: #DBEAFE;
    padding: 4px 12px;
    border-radius: 20px;
}

/* ========================================
   PROGRESS BARS
   ======================================== */
QProgressBar {
    background-color: #E2E8F0;
    border-radius: 10px;
    height: 12px;
    text-align: center;
    border: none;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3B82F6, stop:1 #8B5CF6);
    border-radius: 10px;
}

/* ========================================
   GROUP BOX
   ======================================== */
QGroupBox {
    font-weight: 600;
    color: #0F172A;
    border: 2px solid #E2E8F0;
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 20px;
    background-color: #FFFFFF;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 20px;
    padding: 0px 10px;
    color: #3B82F6;
}

/* ========================================
   DIALOGS & MESSAGE BOXES
   ======================================== */
QMessageBox {
    background-color: #FFFFFF;
    border-radius: 16px;
}

QMessageBox QLabel {
    color: #334155;
    font-size: 14px;
}

QMessageBox QPushButton {
    min-width: 80px;
    padding: 8px 16px;
    border-radius: 8px;
}

QDialog {
    background-color: #F8FAFC;
    border-radius: 16px;
}

/* ========================================
   TOOLTIPS
   ======================================== */
QToolTip {
    background-color: #1E293B;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
}

/* ========================================
   ANIMATIONS & EFFETS
   ======================================== */
QWidget {
    /* Active les transitions CSS quand supportées */
}

/* Effet de focus global */
QWidget:focus {
    outline: none;
}
"""
