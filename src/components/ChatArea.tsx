import React, { useRef, useEffect } from 'react';
import type { Message } from '../types';
import { Loader2, Send, Mic, MicOff, Volume2, VolumeX } from 'lucide-react';
import { clsx } from 'clsx';
import Markdown from 'react-markdown';
import remarkBreaks from 'remark-breaks';
import { useTheme } from '../contexts/ThemeContext';
import { ExpertVerdictCard } from './ExpertVerdictCard';

interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
    keywords?: string;
    onSendMessage: (msg: string) => void;
    userName: string;
}

export const ChatArea: React.FC<ChatAreaProps> = ({ messages, isLoading, keywords, onSendMessage, userName }) => {
    const { theme, isDarkMode } = useTheme();
    const [input, setInput] = React.useState('');
    const [isListening, setIsListening] = React.useState(false);
    const [isMuted, setIsMuted] = React.useState(false);
    const [isAutoListen, setIsAutoListen] = React.useState(false);

    // Looping status logic
    const [statusIndex, setStatusIndex] = React.useState(0);
    const statuses = [
        `🔍 RECHERCHE EN COURS : "${keywords || 'votre question'}"...`,
        "🧠 ANALYSE DES DONNÉES ET DU CONTEXTE...",
        "✍️ GÉNÉRATION DE LA RÉPONSE EN COURS..."
    ];

    React.useEffect(() => {
        if (!isLoading) {
            setStatusIndex(0);
            return;
        }
        const interval = setInterval(() => {
            setStatusIndex(prev => (prev + 1) % statuses.length);
        }, 4000); // 4 seconds per state
        return () => clearInterval(interval);
    }, [isLoading, statuses.length]);

    const scrollRef = useRef<HTMLDivElement>(null);

    const startListening = () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'fr-FR';
            recognition.interimResults = false;

            let finalTranscript = '';

            recognition.onstart = () => setIsListening(true);
            recognition.onend = () => {
                setIsListening(false);
                if (finalTranscript.trim()) {
                    setIsAutoListen(true); // User spoke, activate auto-loop
                    onSendMessage(finalTranscript.trim());
                    setInput('');
                }
            };
            recognition.onresult = (event: any) => {
                finalTranscript = event.results[0][0].transcript;
                setInput(finalTranscript);
            };
            recognition.onerror = () => setIsListening(false);

            recognition.start();
        } else {
            alert("Votre navigateur ne supporte pas la reconnaissance vocale.");
        }
    };

    // --- TTS Logic: Speak the response ---
    const speakMessage = (text: string) => {
        if (!window.speechSynthesis || !text) return;

        // Clean markdown and HTML for speech
        const cleanText = text
            .replace(/<[^>]*>?/gm, '')         // Remove HTML tags
            .replace(/[\*#_\[\]\(\)>-]/g, ' ') // Replace markdown with space for pauses
            .replace(/📍|🎓|💰|🏠|🎭|🍽️|📚|ℹ️|💡|🏛️|📈/g, '') // Remove emojis visually read by TTS
            .replace(/\n\n/g, '. ')             // Double newline = long pause
            .replace(/\n/g, ', ')               // Single newline = short pause
            .replace(/\s+/g, ' ')               // Collapse whitespace
            .trim();

        if (cleanText.length < 2) return;       // Don't read empty/junk text

        const utterance = new SpeechSynthesisUtterance(cleanText.substring(0, 1000));
        utterance.lang = 'fr-FR';
        utterance.rate = 0.92;
        utterance.pitch = 0.98;
        utterance.volume = 1.0;

        utterance.onend = () => {
            if (isAutoListen && !isMuted && !isLoading) {
                setTimeout(() => {
                    startListening();
                }, 500);
            }
        };

        const loadVoices = () => {
            const voices = window.speechSynthesis.getVoices();
            const bestVoice = voices.find(v => v.lang.startsWith('fr') && v.name.includes('Natural')) 
                           || voices.find(v => v.lang.startsWith('fr') && v.name.includes('Google'))
                           || voices.find(v => v.lang.startsWith('fr') && v.name.includes('High Quality'))
                           || voices.find(v => v.lang.startsWith('fr'));
            
            if (bestVoice) {
                utterance.voice = bestVoice;
            }
        };

        window.speechSynthesis.cancel();
        if (window.speechSynthesis.getVoices().length === 0) {
            window.speechSynthesis.onvoiceschanged = () => {
                loadVoices();
                if (!isMuted) window.speechSynthesis.speak(utterance);
            };
        } else {
            loadVoices();
            if (!isMuted) {
                setTimeout(() => {
                    window.speechSynthesis.speak(utterance);
                }, 300);
            }
        }
    };

    const stopSpeech = () => {
        window.speechSynthesis.cancel();
        setIsAutoListen(false);
    };

    const lastReadIdRef = useRef<string | null>(null);

    useEffect(() => {
        if (!isLoading && messages.length > 0) {
            const lastMsg = messages[messages.length - 1];
            if (lastMsg.role === 'assistant' && lastMsg.id !== lastReadIdRef.current) {
                lastReadIdRef.current = lastMsg.id;
                if (!isMuted) {
                    speakMessage(lastMsg.content);
                } else if (isAutoListen) {
                    setTimeout(() => {
                        startListening();
                    }, 500);
                }
            }
        }
    }, [isLoading, messages.length, isMuted]);

    useEffect(() => {
        if (scrollRef.current) {
            const timer = setTimeout(() => {
                scrollRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }, 100);
            return () => clearTimeout(timer);
        }
    }, [messages, isLoading, messages[messages.length - 1]?.content]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;
        setIsAutoListen(false);
        onSendMessage(input);
        setInput('');
    };

    const [currentQuestionIndex, setCurrentQuestionIndex] = React.useState(0);
    const [fade, setFade] = React.useState(true);

    const fullQuestionPool = [
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

    useEffect(() => {
        const interval = setInterval(() => {
            setFade(false);
            setTimeout(() => {
                setCurrentQuestionIndex((prev) => (prev + 4) % fullQuestionPool.length);
                setFade(true);
            }, 300);
        }, 7000);
        return () => clearInterval(interval);
    }, [fullQuestionPool.length]);

    const currentSuggestions = fullQuestionPool.slice(currentQuestionIndex, currentQuestionIndex + 4);
    if (currentSuggestions.length < 4) {
        currentSuggestions.push(...fullQuestionPool.slice(0, 4 - currentSuggestions.length));
    }

    return (
        <main className={clsx("flex-1 flex flex-col relative overflow-hidden transition-colors duration-300", isDarkMode ? theme.bg_dark : theme.bg_soft)}>
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
                {messages.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-center opacity-0 animate-fade-in" style={{ opacity: 1 }}>
                        <div className="w-24 h-24 mb-6 animate-bounce-slow">
                            <img src="/yafi.png" alt="YAFI Logo" className="w-full h-full object-contain drop-shadow-lg" />
                        </div>
                        <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-2">Bonjour, {userName} !</h2>
                        <p className="text-slate-500 dark:text-slate-400 max-w-md mb-8">Je suis votre assistant académique YAFI. Posez-moi une question ou choisissez une suggestion ci-dessous.</p>

                        <div
                            className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl transition-opacity duration-300"
                            style={{ opacity: fade ? 1 : 0 }}
                        >
                            {currentSuggestions.map((s, i) => (
                                <button
                                    key={`${s}-${i}`}
                                    onClick={() => onSendMessage(s)}
                                    className={clsx(
                                        "p-4 bg-white dark:bg-zinc-900 border rounded-2xl text-slate-600 dark:text-slate-300 text-sm hover:shadow-md transition-all text-left",
                                        isDarkMode ? theme.border_dark : theme.border,
                                        isDarkMode ? `hover:${theme.border_dark.replace('border-', 'border-opacity-100 border-')}` : `hover:${theme.border.replace('border-', 'border-opacity-100 border-')}`
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
                                msg.role === 'user' ? "bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300" : clsx("text-white shadow-md", theme.primary)
                            )}>
                                {msg.role === 'user' ? "U" : "IA"}
                            </div>

                            <div className={clsx(
                                "p-4 sm:p-5 rounded-2xl shadow-sm leading-relaxed text-sm sm:text-base transition-colors duration-200",
                                msg.role === 'user'
                                    ? "bg-white dark:bg-zinc-900 text-slate-800 dark:text-slate-200 rounded-tr-none border border-slate-100 dark:border-slate-700"
                                    : clsx("text-slate-800 dark:text-slate-200 rounded-tl-none border bg-gradient-to-br", isDarkMode ? theme.bg_dark_soft : "bg-white " + theme.bg_soft, isDarkMode ? theme.border_dark : theme.border)
                            )}>
                                <Markdown
                                    remarkPlugins={[remarkBreaks]}
                                    components={{
                                        ul: ({ ...props }) => <ul {...props} className="list-disc pl-4 mb-2" />,
                                        ol: ({ ...props }) => <ol {...props} className="list-decimal pl-4 mb-2" />,
                                        p: ({ ...props }) => <p {...props} className="mb-2 last:mb-0" />,
                                        strong: ({ ...props }) => <strong {...props} className={clsx("font-bold", isDarkMode ? theme.text_dark : theme.text)} />,
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

                {isLoading && (
                    <div className="flex gap-4 max-w-3xl mx-auto animate-fade-in">
                        <div className={clsx("w-8 h-8 rounded-full text-white flex items-center justify-center shrink-0", theme.primary)}>
                            IA
                        </div>
                        <div className={clsx("bg-white dark:bg-zinc-900 px-4 py-3 rounded-2xl rounded-tl-none border shadow-sm flex items-center gap-2 transition-colors", isDarkMode ? theme.border_dark : theme.border)}>
                            <Loader2 size={16} className={clsx("animate-spin", isDarkMode ? theme.text_dark : theme.accent)} />
                            <span className="text-slate-400 text-sm font-medium">
                                {statuses[statusIndex]}
                            </span>
                        </div>
                    </div>
                )}
                <div ref={scrollRef} className="h-20" />
            </div>

            <div className={clsx("p-4 sm:p-6 border-t transition-colors duration-300", isDarkMode ? `bg-black ${theme.border_dark}` : `bg-white ${theme.border}`)}>
                <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative flex items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Posez votre question (max 50 car.)..."
                        maxLength={50}
                        className={clsx(
                            "w-full pl-6 pr-32 py-4 bg-slate-50 dark:bg-zinc-900 border border-slate-200 dark:border-slate-700 rounded-full focus:outline-none focus:ring-2 transition-all text-slate-700 dark:text-slate-200 shadow-inner",
                            `focus:ring-${theme.primary.split('-')[1]}-500/50`,
                            isDarkMode ? `focus:border-${theme.primary.split('-')[1]}-400` : `focus:border-${theme.primary.split('-')[1]}-500`
                        )}
                        style={{ '--tw-ring-color': theme.primary.replace('bg-', 'var(--tw-colors-') } as React.CSSProperties}
                        disabled={isLoading}
                    />

                    {input.length > 35 && (
                        <span className="absolute right-24 text-[10px] font-mono text-slate-400 select-none">
                            {input.length}/50
                        </span>
                    )}

                    <button
                        type="button"
                        onClick={() => {
                            if (!isMuted) stopSpeech();
                            setIsMuted(!isMuted);
                        }}
                        className={clsx(
                            "absolute right-24 p-2 rounded-full transition-all",
                            isMuted ? "text-red-400 hover:bg-red-50" : "text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
                        )}
                        title={isMuted ? "Activer le son" : "Couper le son"}
                    >
                        {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
                    </button>

                    <button
                        type="button"
                        onClick={startListening}
                        className={clsx(
                            "absolute right-14 p-2 rounded-full transition-all",
                            isListening ? "bg-red-100 dark:bg-red-900/30 text-red-500 animate-pulse" : clsx("text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700", `hover:${isDarkMode ? theme.text_dark : theme.accent}`)
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
                            `hover:${theme.primary.replace('600', '700').replace('500', '600')}`
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
