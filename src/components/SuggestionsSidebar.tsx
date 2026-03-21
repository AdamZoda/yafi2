import React from 'react';
import { Lightbulb, ChevronRight, X } from 'lucide-react';
import { clsx } from 'clsx';

interface SuggestionsSidebarProps {
    isOpen: boolean;
    onToggle: () => void;
    onSendMessage: (msg: string) => void;
}

const SUGGESTIONS = [
    "J'ai une moyenne de 12, que faire ?",
    "Quels sont les débouchés pour un Bac SVT ?",
    "C'est quoi l'ENCG ?",
    "Comment s'inscrire à la Fac ?",
    "Y a-t-il une ENSA à Tanger ?",
    "Quel était le seuil de médecine 2023 ?",
    "Différence entre FST et Fac ?",
    "Comment avoir une bourse Minhaty ?",
    "Quels sont les frais de l'UIR ?",
    "Est-ce que je peux faire ingénieur avec un Bac Eco ?",
    "Où étudier l'architecture au Maroc ?",
    "Conseils pour gérer le stress du Bac",
    "Les meilleures écoles d'informatique ?",
    "C'est quoi le système LMD ?",
    "Date du concours ENSA ?",
    "Avantages d'étudier en anglais ?",
    "Vaut-il mieux faire un BTS ou un DUT ?",
    "Liste des écoles à Marrakech",
    "Comment devenir pilote de ligne ?",
    "Moyenne demandée pour CPGE ?",
    "Les débouchés de la filière SM ?",
    "C'est quoi l'OFPPT ?",
    "Prix des écoles de commerce privées",
    "Comment préparer le concours de médecine ?",
    "Est-ce que les stages sont obligatoires ?",
    "Quelles sont les villes avec moins de concurrence ?",
    "Date résultats Bac 2026 ?",
    "Inscription CursusSup, c'est quand ?",
    "Différence Public vs Privé ?",
    "Métiers d'avenir au Maroc ?"
];

export const SuggestionsSidebar: React.FC<SuggestionsSidebarProps> = ({ isOpen, onToggle, onSendMessage }) => {
    return (
        <>
            {/* Toggle Button (Visible when closed) */}
            {!isOpen && (
                <button
                    onClick={onToggle}
                    className={clsx(
                        "fixed right-4 top-24 px-4 py-3 rounded-xl shadow-lg transition-all z-20 flex items-center gap-2",
                        "bg-gradient-to-r from-amber-500 to-orange-500 text-white font-semibold",
                        "hover:shadow-xl hover:scale-105 active:scale-95"
                    )}
                    title="Ouvrir les suggestions"
                >
                    <Lightbulb size={20} className="animate-pulse" />
                    <span className="hidden sm:inline">Suggestions</span>
                </button>
            )}

            {/* Sidebar */}
            <aside className={clsx(
                "fixed inset-y-0 right-0 z-30 w-80 bg-slate-50 border-l border-slate-200 transform transition-transform duration-300 ease-in-out flex flex-col shadow-xl",
                isOpen ? "translate-x-0" : "translate-x-full",
                "md:relative md:transform-none md:shadow-none", // On desktop we might want it collapsible too, let's keep it collapsible for now based on isOpen
                !isOpen && "md:hidden" // Fully hide on desktop if closed
            )}>
                <div className="p-4 border-b border-slate-200 flex items-center justify-between">
                    <div className="flex items-center gap-2 font-bold text-slate-700">
                        <Lightbulb size={20} className="text-amber-500" />
                        <span>Suggestions</span>
                    </div>
                    <button
                        onClick={onToggle}
                        className="p-1 hover:bg-slate-200 rounded-full text-slate-400 hover:text-slate-600 transition-colors"
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
                                "bg-white border border-slate-200 hover:border-emerald-300 hover:shadow-sm hover:text-emerald-800 text-slate-600",
                            )}
                        >
                            <span className="leading-snug">{question}</span>
                            <ChevronRight size={16} className="opacity-0 group-hover:opacity-100 transition-opacity text-emerald-500 mt-0.5 shrink-0" />
                        </button>
                    ))}
                </div>
            </aside>
        </>
    );
};
