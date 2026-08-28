#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser pour les transcriptions Microsoft Teams.
Nettoie les fichiers .vtt et .txt extraits de Teams.
"""

import re
from typing import List, Tuple


class TeamsTranscriptParser:
    """Parser pour nettoyer et formater les transcriptions Teams."""
    
    def __init__(self):
        """Initialise le parser."""
        pass
        
    def parse_file(self, file_path: str) -> str:
        """
        Parse un fichier de transcription Teams.
        
        Args:
            file_path: Chemin vers le fichier .vtt ou .txt.
            
        Returns:
            La transcription nettoyée et formatée.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            if file_path.endswith(".vtt"):
                return self.parse_vtt(content)
            else:
                return self.parse_txt(content)
        except IOError as e:
            raise Exception(f"Erreur lors de la lecture du fichier: {e}")
            
    def parse_vtt(self, content: str) -> str:
        """
        Parse un fichier WebVTT (.vtt).
        
        - Ignore les métadonnées WEBVTT
        - Ignore les timestamps
        - Extrait le locuteur et le texte
        
        Args:
            content: Contenu brut du fichier VTT.
            
        Returns:
            La transcription formatée.
        """
        lines = content.split("\n")
        formatted_lines = []
        current_speaker = None
        current_text = []
        
        # Pattern pour détecter le header WEBVTT
        is_webvtt_header = False
        
        # Pattern pour les timestamps (00:00:00.000 --> 00:00:00.000)
        timestamp_pattern = re.compile(r"\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[.,]\d{3}")
        
        # Pattern pour le locuteur format <v Nom>
        speaker_v_pattern = re.compile(r"<v\s+([^>]+)>")
        
        # Pattern pour le locuteur format "Nom 00:00:00"
        speaker_time_pattern = re.compile(r"^([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s\.\-']*)\s+\d{2}:\d{2}:\d{2}")
        
        for line in lines:
            line = line.strip()
            
            # Ignorer le header WEBVTT
            if line.startswith("WEBVTT"):
                is_webvtt_header = True
                continue
                
            # Ignorer les lignes vides au début
            if is_webvtt_header and not line:
                continue
                
            # Ignorer les timestamps
            if timestamp_pattern.match(line):
                continue
                
            # Ignorer les numéros de bloc VTT
            if re.match(r"^\d+$", line):
                continue
                
            # Détecter le locuteur avec <v Nom>
            speaker_match = speaker_v_pattern.search(line)
            if speaker_match:
                # Sauvegarder le texte précédent s'il existe
                if current_speaker and current_text:
                    formatted_lines.append(f"**{current_speaker}:** {' '.join(current_text)}")
                    current_text = []
                    
                current_speaker = speaker_match.group(1).strip()
                # Extraire le texte après la balise <v>
                text_after_tag = speaker_v_pattern.sub("", line).strip()
                if text_after_tag:
                    current_text.append(text_after_tag)
                continue
                
            # Détecter le locuteur avec format "Nom 00:00:00"
            speaker_time_match = speaker_time_pattern.match(line)
            if speaker_time_match:
                # Sauvegarder le texte précédent s'il existe
                if current_speaker and current_text:
                    formatted_lines.append(f"**{current_speaker}:** {' '.join(current_text)}")
                    current_text = []
                    
                current_speaker = speaker_time_match.group(1).strip()
                # Extraire le texte après le timestamp
                text_after_time = speaker_time_pattern.sub("", line).strip()
                if text_after_time:
                    current_text.append(text_after_time)
                continue
                
            # Ligne de texte normale
            if line and not line.startswith("<"):
                if current_speaker:
                    current_text.append(line)
                elif line:
                    # Texte sans locuteur identifié
                    formatted_lines.append(line)
                    
        # Ajouter le dernier bloc
        if current_speaker and current_text:
            formatted_lines.append(f"**{current_speaker}:** {' '.join(current_text)}")
            
        return "\n".join(formatted_lines)
        
    def parse_txt(self, content: str) -> str:
        """
        Parse un fichier texte (.txt).
        
        Tente d'identifier les locuteurs et formate le texte.
        
        Args:
            content: Contenu brut du fichier TXT.
            
        Returns:
            La transcription formatée.
        """
        lines = content.split("\n")
        formatted_lines = []
        current_speaker = None
        current_text = []
        
        # Pattern pour détecter "Nom :" ou "Nom:"
        speaker_pattern = re.compile(r"^([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s\.\-']*)\s*:")
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
                
            # Détecter un nouveau locuteur
            speaker_match = speaker_pattern.match(line)
            if speaker_match:
                # Sauvegarder le texte précédent s'il existe
                if current_speaker and current_text:
                    formatted_lines.append(f"**{current_speaker}:** {' '.join(current_text)}")
                    current_text = []
                    
                current_speaker = speaker_match.group(1).strip()
                # Extraire le texte après le ":"
                text_after_colon = speaker_pattern.sub("", line).strip()
                if text_after_colon:
                    current_text.append(text_after_colon)
            else:
                # Ligne de texte normale
                if current_speaker:
                    current_text.append(line)
                else:
                    # Texte sans locuteur identifié
                    formatted_lines.append(line)
                    
        # Ajouter le dernier bloc
        if current_speaker and current_text:
            formatted_lines.append(f"**{current_speaker}:** {' '.join(current_text)}")
            
        return "\n".join(formatted_lines)
        
    def extract_participants(self, transcript: str) -> List[str]:
        """
        Extrait la liste des participants depuis une transcription.
        
        Args:
            transcript: La transcription formatée.
            
        Returns:
            Liste des noms des participants.
        """
        participants = set()
        
        # Pattern pour extraire les noms après **
        pattern = re.compile(r"\*\*([^:]+):\*\*")
        matches = pattern.findall(transcript)
        
        for match in matches:
            name = match.strip()
            if name:
                participants.add(name)
                
        return sorted(list(participants))
