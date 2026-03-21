import React, { useRef, useEffect } from 'react';
import type { Message } from '../types';
import { Loader2, Send, Mic, MicOff } from 'lucide-react';
import { clsx } from 'clsx';
import Markdown from 'react-markdown';
import remarkBreaks from 'remark-breaks';
import { useTheme } from '../contexts/ThemeContext';
import { ExpertVerdictCard } from './ExpertVerdictCard';

interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
    onSendMessage: (msg: string) => void;
    userName: string;
}

export const ChatArea: React.FC<ChatAreaProps> = ({ messages, isLoading, onSendMessage, userName }) => {
    const { theme } = useTheme();
    const [input, setInput] = React.useState('');
    const [isListening, setIsListening] = React.useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    const startListening = () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'fr-FR';
            recognition.interimResults = false;

            recognition.onstart = () => setIsListening(true);
            recognition.onend = () => setIsListening(false);
            recognition.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript;
                setInput(prev => prev + (prev ? ' ' : '') + transcript);
            };
            recognition.onerror = () => setIsListening(false);

            recognition.start();
        } else {
            alert("Votre navigateur ne supporte pas la reconnaissance vocale.");
        }
    };

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, isLoading]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;
        onSendMessage(input);
        setInput('');
    };

    // Rotating suggestions logic
    const [currentQuestionIndex, setCurrentQuestionIndex] = React.useState(0);
    const [fade, setFade] = React.useState(true);

    const fullQuestionPool = [
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

    useEffect(() => {
        const interval = setInterval(() => {
            setFade(false); // Start interacting fade out
            setTimeout(() => {
                setCurrentQuestionIndex((prev) => (prev + 4) % fullQuestionPool.length);
                setFade(true); // Fade in new questions
            }, 300); // 300ms fade transition
        }, 7000); // Change every 7 seconds

        return () => clearInterval(interval);
    }, []);

    const currentSuggestions = fullQuestionPool.slice(currentQuestionIndex, currentQuestionIndex + 4);
    // Handle wrap-around for the slice if we are near the end of the array
    if (currentSuggestions.length < 4) {
        currentSuggestions.push(...fullQuestionPool.slice(0, 4 - currentSuggestions.length));
    }

    return (
        <main className={clsx("flex-1 flex flex-col relative overflow-hidden", theme.bg_soft)}>
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
                {messages.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-center opacity-0 animate-fade-in" style={{ opacity: 1 }}>
                        <div className="w-24 h-24 mb-6 animate-bounce-slow">
                            <img src="/yafi.png" alt="YAFI Logo" className="w-full h-full object-contain drop-shadow-lg" />
                        </div>
                        <h2 className="text-2xl font-bold text-slate-800 mb-2">Bonjour, {userName} !</h2>
                        <p className="text-slate-500 max-w-md mb-8">Je suis votre assistant académique YAFI. Posez-moi une question ou choisissez une suggestion ci-dessous.</p>

                        <div
                            className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl transition-opacity duration-300"
                            style={{ opacity: fade ? 1 : 0 }}
                        >
                            {currentSuggestions.map((s, i) => (
                                <button
                                    key={`${s}-${i}`}
                                    onClick={() => onSendMessage(s)}
                                    className={clsx(
                                        "p-4 bg-white border rounded-2xl text-slate-600 text-sm hover:shadow-md transition-all text-left",
                                        theme.border,
                                        `hover:${theme.border.replace('border-', 'border-opacity-100 border-')}`
                                    )}
                                >
                                    {s}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={clsx(
                                "flex gap-4 max-w-3xl mx-auto animate-fade-in",
                                msg.role === 'user' ? "flex-row-reverse" : "flex-row"
                            )}
                        >
                            <div className={clsx(
                                "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                                msg.role === 'user' ? "bg-slate-200 text-slate-600" : clsx("text-white", theme.primary)
                            )}>
                                {msg.role === 'user' ? "U" : "IA"}
                            </div>

                            <div className={clsx(
                                "p-4 sm:p-5 rounded-2xl shadow-sm leading-relaxed text-sm sm:text-base",
                                msg.role === 'user'
                                    ? "bg-white text-slate-800 rounded-tr-none border border-slate-100"
                                    : clsx("bg-white text-slate-800 rounded-tl-none border bg-gradient-to-br", theme.border, theme.bg_soft)
                            )}>
                                <Markdown
                                    remarkPlugins={[remarkBreaks]}
                                    components={{
                                        ul: ({ node, ...props }) => <ul {...props} className="list-disc pl-4 mb-2" />,
                                        ol: ({ node, ...props }) => <ol {...props} className="list-decimal pl-4 mb-2" />,
                                        p: ({ node, ...props }) => <p {...props} className="mb-2 last:mb-0" />,
                                        strong: ({ node, ...props }) => <strong {...props} className={clsx("font-bold", theme.text)} />,
                                        br: () => <br />,
                                    }}
                                >
                                    {msg.content}
                                </Markdown>

                                {msg.metadata?.score != null && (
                                    <ExpertVerdictCard 
                                        score={msg.metadata.score} 
                                        ecole={msg.metadata.ecole} 
                                    />
                                )}

                                {msg.role === 'assistant' && msg.metadata?.response_time_ms != null && (
                                    <div className="mt-2 pt-2 border-t border-slate-100 flex items-center gap-1.5 text-xs text-slate-400">
                                        <span>⏱️</span>
                                        <span>
                                            {msg.metadata.response_time_ms >= 1000
                                                ? `${(msg.metadata.response_time_ms / 1000).toFixed(1)}s`
                                                : `${msg.metadata.response_time_ms}ms`
                                            }
                                        </span>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                )}

                {/* Helper for loading state */}
                {isLoading && (
                    <div className="flex gap-4 max-w-3xl mx-auto animate-fade-in">
                        <div className={clsx("w-8 h-8 rounded-full text-white flex items-center justify-center shrink-0", theme.primary)}>
                            IA
                        </div>
                        <div className={clsx("bg-white px-4 py-3 rounded-2xl rounded-tl-none border shadow-sm flex items-center gap-2", theme.border)}>
                            <Loader2 size={16} className={clsx("animate-spin", theme.accent)} />
                            <span className="text-slate-400 text-sm">L'IA est en train de réfléchir...</span>
                        </div>
                    </div>
                )}
                <div ref={scrollRef} />
            </div>

            {/* Input Area */}
            <div className={clsx("p-4 sm:p-6 bg-white border-t", theme.border)}>
                <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative flex items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Posez votre question à propos du YAFI..."
                        className={clsx(
                            "w-full pl-6 pr-24 py-4 bg-slate-50 border border-slate-200 rounded-full focus:outline-none focus:ring-2 transition-all text-slate-700 shadow-inner",
                            `focus:ring-${theme.primary.split('-')[1]}-500/50`,
                            `focus:border-${theme.primary.split('-')[1]}-500`
                        )}
                        style={{ '--tw-ring-color': theme.primary.replace('bg-', 'var(--tw-colors-') } as React.CSSProperties}
                        disabled={isLoading}
                    />

                    <button
                        type="button"
                        onClick={startListening}
                        className={clsx(
                            "absolute right-14 p-2 rounded-full transition-all",
                            isListening ? "bg-red-100 text-red-500 animate-pulse" : clsx("text-slate-400 hover:bg-slate-100", `hover:${theme.accent}`)
                        )}
                        title="Dicter vocalement"
                    >
                        {isListening ? <MicOff size={20} /> : <Mic size={20} />}
                    </button>

                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className={clsx(
                            "absolute right-2 p-2 text-white rounded-full disabled:opacity-50 transition-all shadow-md",
                            theme.primary,
                            `hover:${theme.primary.replace('600', '700').replace('500', '600')}` // Basic hover darkening
                        )}
                    >
                        <Send size={20} className={isLoading ? "opacity-0" : "ml-0.5"} />
                        {isLoading && <span className="absolute inset-0 flex items-center justify-center"><Loader2 size={20} className="animate-spin" /></span>}
                    </button>
                </form>
                <p className="text-center text-xs text-slate-400 mt-2">
                    IA générative peut faire des erreurs. Vérifiez les informations importantes.
                </p>
            </div>
        </main>
    );
};
