#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de base de données SQLite pour Meeting & Project Manager AI.
Crée et gère les tables: projets, reunions, taches.
"""

import sqlite3
import os
from typing import Optional, List, Dict, Any


class DatabaseManager:
    """Gestionnaire de la base de données SQLite."""
    
    def __init__(self, db_path: str):
        """
        Initialise le gestionnaire de base de données.
        
        Args:
            db_path: Chemin complet vers le fichier de base de données.
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        
    def connect(self) -> None:
        """Établit la connexion à la base de données."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            
    def create_tables(self) -> None:
        """Crée les tables nécessaires si elles n'existent pas déjà."""
        self.connect()
        
        try:
            # Table projets
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS projets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    deadline TEXT,
                    statut TEXT DEFAULT 'En cours',
                    description TEXT
                )
            """)
            
            # Table reunions
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reunions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    titre TEXT NOT NULL,
                    ordre_du_jour TEXT,
                    transcript_brut TEXT,
                    compte_rendu TEXT,
                    participants TEXT
                )
            """)
            
            # Table taches avec Foreign Keys
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS taches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reunion_id INTEGER,
                    projet_id INTEGER,
                    description TEXT NOT NULL,
                    assigne_a TEXT,
                    deadline TEXT,
                    statut TEXT DEFAULT 'À faire',
                    FOREIGN KEY (reunion_id) REFERENCES reunions(id) ON DELETE CASCADE,
                    FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE SET NULL
                )
            """)
            
            self.conn.commit()
        finally:
            self.disconnect()
            
    def add_projet(self, nom: str, deadline: str = "", statut: str = "En cours", 
                   description: str = "") -> int:
        """
        Ajoute un nouveau projet.
        
        Returns:
            L'ID du projet créé.
        """
        self.connect()
        try:
            self.cursor.execute(
                "INSERT INTO projets (nom, deadline, statut, description) VALUES (?, ?, ?, ?)",
                (nom, deadline, statut, description)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        finally:
            self.disconnect()
            
    def get_all_projets(self) -> List[Dict[str, Any]]:
        """Récupère tous les projets."""
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM projets ORDER BY id DESC")
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            self.disconnect()
            
    def update_projet(self, projet_id: int, nom: str = None, deadline: str = None,
                      statut: str = None, description: str = None) -> bool:
        """Met à jour un projet."""
        self.connect()
        try:
            updates = []
            values = []
            
            if nom is not None:
                updates.append("nom = ?")
                values.append(nom)
            if deadline is not None:
                updates.append("deadline = ?")
                values.append(deadline)
            if statut is not None:
                updates.append("statut = ?")
                values.append(statut)
            if description is not None:
                updates.append("description = ?")
                values.append(description)
                
            if not updates:
                return False
                
            values.append(projet_id)
            query = f"UPDATE projets SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        finally:
            self.disconnect()
            
    def delete_projet(self, projet_id: int) -> bool:
        """Supprime un projet."""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM projets WHERE id = ?", (projet_id,))
            self.conn.commit()
            return True
        finally:
            self.disconnect()
            
    def add_reunion(self, date: str, titre: str, ordre_du_jour: str = "",
                    transcript_brut: str = "", compte_rendu: str = "",
                    participants: str = "") -> int:
        """
        Ajoute une nouvelle réunion.
        
        Returns:
            L'ID de la réunion créée.
        """
        self.connect()
        try:
            self.cursor.execute(
                """INSERT INTO reunions (date, titre, ordre_du_jour, transcript_brut, 
                   compte_rendu, participants) VALUES (?, ?, ?, ?, ?, ?)""",
                (date, titre, ordre_du_jour, transcript_brut, compte_rendu, participants)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        finally:
            self.disconnect()
            
    def get_all_reunions(self) -> List[Dict[str, Any]]:
        """Récupère toutes les réunions."""
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM reunions ORDER BY date DESC, id DESC")
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            self.disconnect()
            
    def get_reunion_by_id(self, reunion_id: int) -> Optional[Dict[str, Any]]:
        """Récupère une réunion par son ID."""
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM reunions WHERE id = ?", (reunion_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        finally:
            self.disconnect()
            
    def update_reunion(self, reunion_id: int, **kwargs) -> bool:
        """Met à jour une réunion."""
        self.connect()
        try:
            updates = []
            values = []
            
            for key, value in kwargs.items():
                if key in ["date", "titre", "ordre_du_jour", "transcript_brut", 
                          "compte_rendu", "participants"]:
                    updates.append(f"{key} = ?")
                    values.append(value)
                    
            if not updates:
                return False
                
            values.append(reunion_id)
            query = f"UPDATE reunions SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        finally:
            self.disconnect()
            
    def delete_reunion(self, reunion_id: int) -> bool:
        """Supprime une réunion et ses tâches associées."""
        self.connect()
        try:
            # Supprimer d'abord les tâches associées
            self.cursor.execute("DELETE FROM taches WHERE reunion_id = ?", (reunion_id,))
            # Puis la réunion
            self.cursor.execute("DELETE FROM reunions WHERE id = ?", (reunion_id,))
            self.conn.commit()
            return True
        finally:
            self.disconnect()
            
    def add_tache(self, reunion_id: int, projet_id: int = None, description: str = "",
                  assigne_a: str = "", deadline: str = "", statut: str = "À faire") -> int:
        """
        Ajoute une nouvelle tâche.
        
        Returns:
            L'ID de la tâche créée.
        """
        self.connect()
        try:
            self.cursor.execute(
                """INSERT INTO taches (reunion_id, projet_id, description, assigne_a, 
                   deadline, statut) VALUES (?, ?, ?, ?, ?, ?)""",
                (reunion_id, projet_id, description, assigne_a, deadline, statut)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        finally:
            self.disconnect()
            
    def get_all_taches(self, reunion_id: int = None, projet_id: int = None) -> List[Dict[str, Any]]:
        """Récupère toutes les tâches, optionnellement filtrées."""
        self.connect()
        try:
            query = "SELECT * FROM taches WHERE 1=1"
            params = []
            
            if reunion_id is not None:
                query += " AND reunion_id = ?"
                params.append(reunion_id)
            if projet_id is not None:
                query += " AND projet_id = ?"
                params.append(projet_id)
                
            query += " ORDER BY deadline ASC, id DESC"
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            self.disconnect()
            
    def update_tache(self, tache_id: int, **kwargs) -> bool:
        """Met à jour une tâche."""
        self.connect()
        try:
            updates = []
            values = []
            
            for key, value in kwargs.items():
                if key in ["reunion_id", "projet_id", "description", "assigne_a", 
                          "deadline", "statut"]:
                    updates.append(f"{key} = ?")
                    values.append(value)
                    
            if not updates:
                return False
                
            values.append(tache_id)
            query = f"UPDATE taches SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        finally:
            self.disconnect()
            
    def delete_tache(self, tache_id: int) -> bool:
        """Supprime une tâche."""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM taches WHERE id = ?", (tache_id,))
            self.conn.commit()
            return True
        finally:
            self.disconnect()
            
    def get_stats(self) -> Dict[str, Any]:
        """Récupère des statistiques générales."""
        self.connect()
        try:
            stats = {}
            
            # Nombre total de projets
            self.cursor.execute("SELECT COUNT(*) FROM projets")
            stats["total_projets"] = self.cursor.fetchone()[0]
            
            # Nombre total de réunions
            self.cursor.execute("SELECT COUNT(*) FROM reunions")
            stats["total_reunions"] = self.cursor.fetchone()[0]
            
            # Nombre total de tâches
            self.cursor.execute("SELECT COUNT(*) FROM taches")
            stats["total_taches"] = self.cursor.fetchone()[0]
            
            # Tâches par statut
            self.cursor.execute("SELECT statut, COUNT(*) FROM taches GROUP BY statut")
            stats["taches_par_statut"] = {row["statut"]: row[1] for row in self.cursor.fetchall()}
            
            return stats
        finally:
            self.disconnect()
