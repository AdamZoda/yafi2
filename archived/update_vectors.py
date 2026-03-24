import json
import os

def update_knowledge_base():
    filepath = 'yafi_knowledge_context.json'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    new_qa = [
        {
            "q": "C'est quoi l'ISCAE et quels sont les frais ?",
            "full_answer": "L'ISCAE (Institut Supérieur de Commerce et d'Administration des Entreprises) est un établissement public d'excellence situé à Casablanca et Rabat. Étant public, les frais de scolarité sont quasi gratuits (environ 500 DH/an pour l'inscription). L'accès y est extrêmement sélectif via un concours national nécessitant généralement d'avoir fait les classes préparatoires (CPGE) ou d'avoir d'excellents résultats en licence.",
            "category": "Écoles"
        },
        {
            "q": "Quelle est la différence entre ENAM et ENSAM ?",
            "full_answer": "Il ne faut pas confondre l'ENAM et l'ENSAM !\n\n- **ENAM** (École Nationale d'Agriculture de Meknès) : Forme des ingénieurs agronomes. C'est une école spécialisée dans l'agriculture, le développement rural et l'agroalimentaire.\n- **ENSAM** (École Nationale Supérieure d'Arts et Métiers) : Présente à Meknès, Casablanca et Rabat. Forme des ingénieurs d'État dans les domaines de la mécanique, l'industrie et l'électromécanique.\n\nLes deux sont publiques et très sélectives.",
            "category": "Écoles"
        },
        {
            "q": "Parle-moi de l'UIK (Université Internationale d'Agadir) : prix et campus",
            "full_answer": "L'Université Internationale d'Agadir (UIK - Universiapolis) est un campus privé intégré.\n\n- **Frais de scolarité** : Environ 65 000 à 75 000 DH/an selon les filières (Ingénierie, Management, Tourisme).\n- **Vie de campus** : Le campus est très dynamique et dispose d'une cantine universitaire, de terrains de sport, et de plusieurs clubs étudiants.\n- **Internat** : Oui, l'UIK propose des résidences étudiantes directement sur le campus.",
            "category": "Écoles"
        },
        {
            "q": "Quelles sont les informations sur l'ESTS (EST Safi) ?",
            "full_answer": "L'ESTS (École Supérieure de Technologie de Safi) est un établissement public rattaché à l'Université Cadi Ayyad.\n\n- **Filières principales** : Génie Informatique (GI), Techniques de Management (TM), Maintenance Industrielle, et Mécatronique.\n- **Admission** : La sélection se fait sur dossier (Notes du Bac). Le seuil d'admission tourne souvent autour de 14.20/20 pour les filières techniques, mais cela varie chaque année.\n- **Débouchés** : Permet une excellente insertion technique (DUT en 2 ans) ou la poursuite d'études en Licence Professionnelle ou en École d'Ingénieurs (ENSA, FST).",
            "category": "Écoles"
        },
        {
            "q": "Quels sont les détails sur l'Université Privée de Fès (UPF) ?",
            "full_answer": "L'Université Privée de Fès (UPF) propose des formations en Ingénierie, Architecture, et Management.\n\n- **Frais de scolarité** : Varient entre 50 000 DH et 70 000 DH par an selon la faculté (l'Architecture étant souvent la plus chère).\n- **Campus** : Infrastructure moderne, disposant de laboratoires équipés et de partenariats internationaux pour les échanges étudiants.",
            "category": "Écoles"
        },
        {
            "q": "Est-ce que l'UIR et l'UM6P ont des internats ou offrent des bourses ?",
            "full_answer": "Oui, ces deux grandes universités marocaines brillent par leurs infrastructures et leurs aides financières :\n\n- **UIR (Rabat)** : Dispose de 6 résidences modernes sur le campus, de nombreux clubs (Aéro, Débat) et de bourses allant jusqu'à 100% pour les excellents dossiers scolaires.\n- **UM6P (Benguerir)** : L'Université Mohammed VI Polytechnique offre des conditions d'études exceptionnelles (chambres individuelles, installations sportives olympiques) et délivre de généreuses bourses (Bourse Excellence OCP) pour les étudiants brillants issus de milieux modestes.",
            "category": "Boursses"
        }
    ]
    
    # Append the new data
    data['qa_database'].extend(new_qa)
    data['total_questions'] = len(data['qa_database'])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Added {len(new_qa)} new vectors. Total QA entries: {data['total_questions']}")

if __name__ == '__main__':
    update_knowledge_base()
