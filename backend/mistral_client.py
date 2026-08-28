#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client pour l'API Mistral AI.
Génère des comptes-rendus et extrait des tâches depuis les transcriptions.
"""

import re
import json
from typing import Tuple, Optional, List, Dict, Any
from mistralai import Mistral


class MistralClient:
    """Client pour interagir avec l'API Mistral AI."""
    
    SYSTEM_PROMPT = """Tu es un assistant de direction expert spécialisé dans la rédaction de comptes-rendus de réunions professionnelles.

Ta mission est d'analyser la transcription d'une réunion et de produire :
1. Un compte-rendu structuré et professionnel
2. Une liste de tâches actionnables extraites de la discussion

Règles importantes :
- Le compte-rendu doit être clair, concis et professionnel
- Utilise des émojis pertinents pour structurer le contenu :
  - 📌 pour les points clés et décisions
  - ⚠️ pour les alertes et points de vigilance
  - 💡 pour les idées et suggestions
  - ✅ pour les actions validées
- Les tâches doivent être spécifiques, assignées à une personne et avoir une échéance si mentionnée
- Reste factuel et objectif"""

    USER_PROMPT_TEMPLATE = """Voici la transcription d'une réunion :

{transcript}

Ordre du jour (si disponible) : {ordre_du_jour}

Tu dois répondre STRICTEMENT avec le format suivant, en incluant les deux balises :

[COMPTERENDU]
Rédige ici le compte-rendu structuré avec des sections claires. Utilise les émojis 📌, ⚠️, 💡, ✅ pour organiser le contenu.
[/COMPTERENDU]

[JSON_TACHES]
[
  {{
    "responsable": "Nom de la personne",
    "tache": "Description précise de la tâche",
    "deadline": "Date limite ou 'À définir'"
  }}
]
[/JSON_TACHES]

Assure-toi que le JSON soit valide et parseable."""

    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        """
        Initialise le client Mistral.
        
        Args:
            api_key: Clé API Mistral.
            model: Nom du modèle à utiliser.
        """
        self.api_key = api_key
        self.model = model
        self.client = Mistral(api_key=api_key) if api_key else None
        
    def generate_compte_rendu(self, transcript: str, ordre_du_jour: str = "") -> Tuple[str, List[Dict[str, str]]]:
        """
        Génère un compte-rendu et extrait les tâches depuis une transcription.
        
        Args:
            transcript: La transcription de la réunion.
            ordre_du_jour: L'ordre du jour de la réunion (optionnel).
            
        Returns:
            Un tuple contenant :
            - Le compte-rendu formaté (str)
            - La liste des tâches (list de dict)
            
        Raises:
            Exception: Si l'appel API échoue.
        """
        if not self.client:
            raise Exception("Clé API Mistral non configurée")
            
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            transcript=transcript,
            ordre_du_jour=ordre_du_jour if ordre_du_jour else "Non spécifié"
        )
        
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            response_content = response.choices[0].message.content
            
            # Extraire le compte-rendu et les tâches
            compte_rendu = self._extract_compte_rendu(response_content)
            taches = self._extract_taches(response_content)
            
            return compte_rendu, taches
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'appel à Mistral AI: {str(e)}")
            
    def _extract_compte_rendu(self, response: str) -> str:
        """
        Extrait le compte-rendu depuis la réponse de l'API.
        
        Args:
            response: La réponse brute de l'API.
            
        Returns:
            Le compte-rendu extrait.
        """
        pattern = r"\[COMPTERENDU\](.*?)\[/COMPTERENDU\]"
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        else:
            # Si le format n'est pas respecté, retourner la réponse brute
            return response.strip()
            
    def _extract_taches(self, response: str) -> List[Dict[str, str]]:
        """
        Extrait la liste des tâches depuis la réponse de l'API.
        
        Args:
            response: La réponse brute de l'API.
            
        Returns:
            La liste des tâches sous forme de dictionnaires.
        """
        pattern = r"\[JSON_TACHES\](.*?)\[/JSON_TACHES\]"
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        
        if match:
            json_str = match.group(1).strip()
            try:
                taches = json.loads(json_str)
                # Valider le format
                if isinstance(taches, list):
                    validated_taches = []
                    for tache in taches:
                        if isinstance(tache, dict):
                            validated_taches.append({
                                "responsable": tache.get("responsable", "Non assigné"),
                                "tache": tache.get("tache", ""),
                                "deadline": tache.get("deadline", "À définir")
                            })
                    return validated_taches
            except json.JSONDecodeError as e:
                print(f"Erreur lors du parsing JSON: {e}")
                
        return []
        
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API Mistral.
        
        Returns:
            True si la connexion réussit, False sinon.
        """
        if not self.client:
            return False
            
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Réponds simplement 'OK' si tu me reçois."}
                ],
                max_tokens=10
            )
            return True
        except Exception:
            return False
