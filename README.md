# Meeting & Project Manager AI

Application de bureau complète pour la gestion de réunions et de projets, intégrant l'IA Mistral pour la génération automatique de comptes-rendus.

## 🚀 Fonctionnalités

- **Gestion des réunions** : Import de transcriptions Teams (.vtt, .txt), génération de CR avec IA
- **Gestion des projets** : Suivi des projets et des tâches associées
- **Tableau de bord** : Vue d'ensemble des statistiques
- **Exports** : Word (.docx) et PDF des comptes-rendus
- **Interface moderne** : Design professionnel avec PySide6/Qt

## 📋 Prérequis

- Python 3.9 ou supérieur
- Clé API Mistral (obtenir sur https://console.mistral.ai)

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone <repository-url>
cd meeting-manager
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
python main.py
```

## 📁 Structure du projet

```
meeting-manager/
├── main.py                 # Point d'entrée
├── requirements.txt        # Dépendances Python
├── README.md              # Ce fichier
├── meeting_manager.spec   # Configuration PyInstaller
├── setup.iss              # Script Inno Setup
├── backend/
│   ├── __init__.py
│   ├── database_manager.py    # Gestion SQLite
│   ├── settings_manager.py    # Paramètres utilisateur
│   ├── parser_teams.py        # Parser transcriptions Teams
│   ├── mistral_client.py      # Client API Mistral
│   └── export_manager.py      # Exports Word/PDF
└── gui/
    ├── __init__.py
    ├── main_window.py         # Fenêtre principale
    ├── styles.py              # Feuille de style QSS
    └── pages/
        ├── __init__.py
        ├── dashboard_page.py  # Page tableau de bord
        ├── reunions_page.py   # Page réunions
        ├── projets_page.py    # Page projets
        └── settings_page.py   # Page paramètres
```

## ⚙️ Configuration

1. Lancez l'application
2. Allez dans l'onglet **Paramètres**
3. Entrez votre clé API Mistral
4. Sélectionnez le modèle souhaité (mistral-large-latest recommandé)
5. Cliquez sur "Tester la connexion"

## 📝 Utilisation

### Créer une réunion

1. Onglet **Réunions** → "+ Nouvelle réunion"
2. Remplissez les informations (date, titre, ordre du jour)
3. Importez la transcription Teams (.vtt ou .txt)
4. Cliquez sur "🤖 Générer CR avec IA"
5. Exportez en Word ou PDF si besoin

### Gérer un projet

1. Onglet **Projets** → "+ Nouveau projet"
2. Ajoutez des tâches au projet
3. Suivez l'avancement

## 🔧 Compilation (Windows)

### Avec PyInstaller

```bash
pyinstaller meeting_manager.spec
```

### Créateur d'installateur

Après compilation, utilisez Inno Setup avec `setup.iss` pour créer un installateur Windows.

## 📄 Licence

MIT License

## 👥 Auteur

Développé avec ❤️ pour la productivité professionnelle.
