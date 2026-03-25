import React from 'react';
import { Lightbulb, ChevronRight, X } from 'lucide-react';
import { clsx } from 'clsx';
import { useTheme } from '../contexts/ThemeContext';

interface SuggestionsSidebarProps {
    isOpen: boolean;
    onToggle: () => void;
    onSendMessage: (msg: string) => void;
}

const SUGGESTIONS = [
    "Comparer EMSI et UIR (Salaires & Débouchés)",
    "Écoles d'ingénierie budget < 45000 DH",
    "Quel est le salaire moyen après l'EMSI ?",
    "Menu de la cantine à l'UIK aujourd'hui",
    "Calendrier des concours 2026 au Maroc",
    "Meilleure école d'info avec un Bac PC",
    "Différence entre ENSA et ENAM ?",
    "Bourses d'excellence à l'UM6P",
    "Frais de scolarité de l'ISCAE",
    "Est-ce que l'UIR a un internat ?",
    "Métiers d'avenir dans l'IA au Maroc",
    "Comment s'inscrire sur CursusSup ?",
    "Seuils médecine 2025 (Estimations)",
    "Filières possibles avec un Bac SM",
    "Calculer mon score pour l'ENSA",
    "Quiz : Quelle école me correspond ?",
    "Conseils pour réussir le concours ENCG",
    "Liste des écoles d'architecture privées",
    "Différence entre Licence Pro et Fondamentale",
    "Débouchés après un Bac Eco-Gestion",
    "Comment avoir la bourse Minhaty ?",
    "Écoles avec prépa intégrée à Casablanca",
    "Avantages du système LMD au Maroc",
    "Puis-je faire médecine avec 14 de moyenne ?",
    "Le diplôme de l'OFPPT est-il reconnu ?",
    "Meilleure méthode pour réviser le Bac",
    "Vaut-il mieux faire un BTS ou un DUT ?",
    "Frais d'inscription à l'Université Privée de Fès",
    "Comment devenir ingénieur en cybersécurité ?",
    "Les clubs étudiants à l'EMSI",
    "Prochaines dates d'inscription OFPPT"
];

export const SuggestionsSidebar: React.FC<SuggestionsSidebarProps> = ({ isOpen, onToggle, onSendMessage }) => {
    const { theme, isDarkMode } = useTheme();

    return (
        <>
            {/* Toggle Button (Visible when closed) */}
            {!isOpen && (
                <button
                    onClick={onToggle}
                    className={clsx(
                        "fixed right-4 top-24 px-4 py-3 rounded-xl shadow-lg transition-all z-20 flex items-center gap-2",
                        isDarkMode ? theme.bg_dark_soft : "bg-gradient-to-r from-amber-500 to-orange-500 text-white font-semibold",
                        isDarkMode ? theme.text_dark : "",
                        "hover:shadow-xl hover:scale-105 active:scale-95"
                    )}
                    title="Ouvrir les suggestions"
                >
                    <Lightbulb size={20} className={clsx("animate-pulse", !isDarkMode && "text-white")} />
                    <span className="hidden sm:inline">Suggestions</span>
                </button>
            )}

            {/* Sidebar */}
            <aside className={clsx(
                "fixed inset-y-0 right-0 z-30 w-80 bg-slate-50 dark:bg-black border-l border-slate-200 dark:border-slate-800 transform transition-transform duration-300 ease-in-out flex flex-col shadow-xl",
                isOpen ? "translate-x-0" : "translate-x-full",
                "md:relative md:transform-none md:shadow-none",
                !isOpen && "md:hidden"
            )}>
                <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-2 font-bold text-slate-700 dark:text-slate-200">
                        <Lightbulb size={20} className="text-amber-500" />
                        <span>Suggestions</span>
                    </div>
                    <button
                        onClick={onToggle}
                        className="p-1 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                    >
                        <X size={20} />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-2 custom-scrollbar">
                    {SUGGESTIONS.map((question, index) => (
                        <button
                            key={index}
                            onClick={() => onSendMessage(question)}
                            className={clsx(
                                "w-full text-left p-3 rounded-xl text-sm transition-all group flex items-start justify-between gap-2",
                                "bg-white dark:bg-zinc-900 border border-slate-200 dark:border-slate-700 hover:shadow-sm text-slate-600 dark:text-slate-300",
                                isDarkMode ? `hover:${theme.border_dark.replace('border-', 'border-opacity-100 border-')} hover:${theme.text_dark}` : `hover:${theme.border.replace('border-', 'border-opacity-100 border-')} hover:${theme.text}`
                            )}
                        >
                            <span className="leading-snug">{question}</span>
                            <ChevronRight size={16} className={clsx("opacity-0 group-hover:opacity-100 transition-opacity mt-0.5 shrink-0", isDarkMode ? theme.text_dark : theme.accent)} />
                        </button>
                    ))}
                </div>
            </aside>
        </>
    );
};
