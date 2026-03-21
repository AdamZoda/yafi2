import random
import re

class ResponseBuilder:
    """
    Class responsible for generating human-like responses without using external LLMs.
    It uses dynamic templates, parses Prolog output, and injects empathy based on user data.
    """
    
    # ------------------ TEMPLATES INITIATIONS ------------------
    INTRO_ENCOURAGING = [
        "Excellente question ! Voici ce que j'ai trouvé pour toi :",
        "Je vois, c'est un très bon choix de s'informer là-dessus. Regarde ça :",
        "C'est noté ! Voici les détails qui pourraient t'intéresser :",
        "Super ! Laisse-moi te donner les informations précises :"
    ]
    
    INTRO_NEUTRAL = [
        "Voici les informations demandées :",
        "D'après ma base de données, voici ce qu'il faut savoir :",
        "Voici les détails correspondants :"
    ]
    
    INTRO_EMPATHIC_LOW_GRADE = [
        "Pas de panique ! Une note moyenne ne ferme pas toutes les portes, bien au contraire. Voici des pistes solides :",
        "L'orientation ne se résume pas qu'à une note. Il y a d'excellentes opportunités pratiques pour toi :",
        "Ne te décourage pas. Le plus important est de trouver une filière qui te plaît. Regarde ces options :"
    ]
    
    INTRO_CONGRATS_HIGH_GRADE = [
        "Félicitations pour ces excellents résultats ! 🎉 Avec un tel dossier, de nombreuses portes te sont ouvertes :",
        "Bravo pour ton travail acharné ! 🌟 Voici les filières d'excellence que tu peux viser :",
        "C'est un profil impressionnant ! 🚀 Regarde ces options prestigieuses :"
    ]

    # ------------------ TEMPLATES CONCLUSIONS ------------------
    OUTRO_SUGGESTION = [
        "\n\n💡 *Veux-tu que je compare deux de ces écoles pour toi ?*",
        "\n\n💡 *As-tu une préférence de ville pour affiner ces résultats ?*",
        "\n\n💡 *Souhaites-tu connaître les bourses de mérite disponibles pour ces filières ?*",
        "\n\n💡 *N'hésite pas si tu as besoin de conseils sur la préparation des concours !*"
    ]

    @staticmethod
    def get_intro_for_grade(grade: float) -> str:
        """Returns an appropriate empathetic intro based on the grade."""
        if grade >= 16:
            return random.choice(ResponseBuilder.INTRO_CONGRATS_HIGH_GRADE)
        elif grade >= 13:
            return random.choice(ResponseBuilder.INTRO_ENCOURAGING)
        elif grade < 11:
            return random.choice(ResponseBuilder.INTRO_EMPATHIC_LOW_GRADE)
        else:
            return random.choice(ResponseBuilder.INTRO_NEUTRAL)
            
    @staticmethod
    def build_school_list(bot_intent: str, schools: list, location: str = None) -> str:
        """
        Formats a list of schools found by Prolog into a natural response.
        bot_intent usually describes why we searched (e.g., 'informatique', 'medecine')
        """
        intro = random.choice(ResponseBuilder.INTRO_ENCOURAGING)
        if location:
            intro = f"Si tu cherches à étudier à **{location.capitalize()}**, voici d'excellentes options pour toi :"
        
        response = f"{intro}\n\n🏫 **Établissements :**\n"
        for i, school in enumerate(schools[:10]): # Limit to 10 to avoid wall of text
            response += f"• {school}\n"
            
        if len(schools) > 10:
            response += f"\n*... et {len(schools) - 10} autres. Dis-moi si tu veux une ville précise !*"
            
        response += random.choice(ResponseBuilder.OUTRO_SUGGESTION)
        return response

    @staticmethod
    def build_strategy_response(grade: float, bac_type: str, prolog_raw_advice: str) -> str:
        """
        Takes raw strategy from Prolog and humanizes it based on the grade.
        """
        intro = ResponseBuilder.get_intro_for_grade(grade)
        
        # Clean up prolog text if needed (assuming clean_text was already run, but formatting can be heavy)
        advice_parts = prolog_raw_advice.split('👉')
        main_advice = advice_parts[0].replace('🌟', '').replace('📈', '').replace('🤔', '').replace('⚠️', '').strip()
        
        response = f"{intro}\n\n**Analyse de ton profil ({grade}/20 en {bac_type}) :**\n{main_advice}\n\n"
        
        if len(advice_parts) > 1:
            response += "🎯 **Mes recommandations prioritaires :**\n"
            for part in advice_parts[1:]:
                response += f"- {part.strip()}\n"
                
        response += "\n💡 *Veux-tu qu'on explore une de ces pistes en particulier ?*"
        return response

    @staticmethod
    def build_general_response(text: str) -> str:
        """
        Just wraps raw text in a slightly more conversational tone.
        """
        # If it's a simple one-liner, make it warm.
        if len(text.split('\n')) <= 2 and not text.startswith(('✅', '⚠️', '🏫')):
            intro = random.choice(["Bien sûr ! ", "Tout à fait. ", "Voici ce qu'il en est : "])
            return f"{intro}{text}"
        return text
