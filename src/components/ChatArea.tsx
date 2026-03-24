import React, { useRef, useEffect } from 'react';
import type { Message } from '../types';
<<<<<<< HEAD
import { Loader2, Send, Mic, MicOff } from 'lucide-react';
=======
import { Loader2, Send, Mic, MicOff, Volume2, VolumeX } from 'lucide-react';
>>>>>>> 3257fc1 (final)
import { clsx } from 'clsx';
import Markdown from 'react-markdown';
import remarkBreaks from 'remark-breaks';
import { useTheme } from '../contexts/ThemeContext';
import { ExpertVerdictCard } from './ExpertVerdictCard';

interface ChatAreaProps {
    messages: Message[];
    isLoading: boolean;
<<<<<<< HEAD
=======
    keywords?: string;
>>>>>>> 3257fc1 (final)
    onSendMessage: (msg: string) => void;
    userName: string;
}

<<<<<<< HEAD
export const ChatArea: React.FC<ChatAreaProps> = ({ messages, isLoading, onSendMessage, userName }) => {
    const { theme } = useTheme();
    const [input, setInput] = React.useState('');
    const [isListening, setIsListening] = React.useState(false);
=======
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

>>>>>>> 3257fc1 (final)
    const scrollRef = useRef<HTMLDivElement>(null);

    const startListening = () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'fr-FR';
            recognition.interimResults = false;

<<<<<<< HEAD
            recognition.onstart = () => setIsListening(true);
            recognition.onend = () => setIsListening(false);
            recognition.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript;
                setInput(prev => prev + (prev ? ' ' : '') + transcript);
=======
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
>>>>>>> 3257fc1 (final)
            };
            recognition.onerror = () => setIsListening(false);

            recognition.start();
        } else {
            alert("Votre navigateur ne supporte pas la reconnaissance vocale.");
        }
    };

<<<<<<< HEAD
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, isLoading]);
=======
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

        // Limit length to avoid browser speech timeout, but keep it a decent chunk
        const utterance = new SpeechSynthesisUtterance(cleanText.substring(0, 1000));
        utterance.lang = 'fr-FR';
        
        // Slightly slower and deeper for a "Premium/Expert" feel
        utterance.rate = 0.92;
        utterance.pitch = 0.98;
        utterance.volume = 1.0;

        // Auto-listen loop: restart mic when speech finishes
        utterance.onend = () => {
            if (isAutoListen && !isMuted && !isLoading) {
                // Wait 500ms before re-opening mic for a natural pause
                setTimeout(() => {
                    startListening();
                }, 500);
            }
        };

        // Best voice selection
        const loadVoices = () => {
            const voices = window.speechSynthesis.getVoices();
            console.log("Available voices:", voices.length);
            
            // Priority: Natural > Google > High Quality > First French
            const bestVoice = voices.find(v => v.lang.startsWith('fr') && v.name.includes('Natural')) 
                           || voices.find(v => v.lang.startsWith('fr') && v.name.includes('Google'))
                           || voices.find(v => v.lang.startsWith('fr') && v.name.includes('High Quality'))
                           || voices.find(v => v.lang.startsWith('fr'));
            
            if (bestVoice) {
                utterance.voice = bestVoice;
                console.log("Selected voice:", bestVoice.name);
            }
        };

        window.speechSynthesis.cancel(); // Stop current speech
        
        // Voices are sometimes loaded asynchronously
        if (window.speechSynthesis.getVoices().length === 0) {
            window.speechSynthesis.onvoiceschanged = () => {
                loadVoices();
                if (!isMuted) window.speechSynthesis.speak(utterance);
            };
        } else {
            loadVoices();
            if (!isMuted) {
                // Add a tiny delay to allow the user to see the text start appearing
                setTimeout(() => {
                    window.speechSynthesis.speak(utterance);
                }, 300);
            }
        }
    };

    // Stop all speech
    const stopSpeech = () => {
        window.speechSynthesis.cancel();
        setIsAutoListen(false); // Stop the auto-loop when human interrupts
    };

    // Track the last message ID that was spoken to avoid repetitions
    const lastReadIdRef = useRef<string | null>(null);

    // Auto-read the last assistant message when it finishes loading
    useEffect(() => {
        if (!isLoading && messages.length > 0) {
            const lastMsg = messages[messages.length - 1];
            if (lastMsg.role === 'assistant' && lastMsg.id !== lastReadIdRef.current) {
                lastReadIdRef.current = lastMsg.id;
                if (!isMuted) {
                    speakMessage(lastMsg.content);
                    // Auto-listen will be triggered by utterance.onend (after TTS finishes)
                } else if (isAutoListen) {
                    // Sound is muted, but auto-listen is active: restart mic directly
                    setTimeout(() => {
                        startListening();
                    }, 500);
                }
            }
        }
    }, [isLoading, messages.length, isMuted]);

    useEffect(() => {
        if (scrollRef.current) {
            // Use a small timeout to ensure DOM has rendered markdown
            const timer = setTimeout(() => {
                scrollRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }, 100);
            return () => clearTimeout(timer);
        }
    }, [messages, isLoading, messages[messages.length - 1]?.content]);
>>>>>>> 3257fc1 (final)

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;
<<<<<<< HEAD
=======
        setIsAutoListen(false); // Disable auto-loop if user switched to typing
>>>>>>> 3257fc1 (final)
        onSendMessage(input);
        setInput('');
    };

    // Rotating suggestions logic
    const [currentQuestionIndex, setCurrentQuestionIndex] = React.useState(0);
    const [fade, setFade] = React.useState(true);

    const fullQuestionPool = [
<<<<<<< HEAD
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
=======
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
>>>>>>> 3257fc1 (final)
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
<<<<<<< HEAD
        <main className={clsx("flex-1 flex flex-col relative overflow-hidden", theme.bg_soft)}>
=======
        <main className={clsx("flex-1 flex flex-col relative overflow-hidden transition-colors duration-300", isDarkMode ? theme.bg_dark : theme.bg_soft)}>
>>>>>>> 3257fc1 (final)
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
                {messages.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-center opacity-0 animate-fade-in" style={{ opacity: 1 }}>
                        <div className="w-24 h-24 mb-6 animate-bounce-slow">
                            <img src="/yafi.png" alt="YAFI Logo" className="w-full h-full object-contain drop-shadow-lg" />
                        </div>
<<<<<<< HEAD
                        <h2 className="text-2xl font-bold text-slate-800 mb-2">Bonjour, {userName} !</h2>
                        <p className="text-slate-500 max-w-md mb-8">Je suis votre assistant académique YAFI. Posez-moi une question ou choisissez une suggestion ci-dessous.</p>
=======
                        <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-2">Bonjour, {userName} !</h2>
                        <p className="text-slate-500 dark:text-slate-400 max-w-md mb-8">Je suis votre assistant académique YAFI. Posez-moi une question ou choisissez une suggestion ci-dessous.</p>
>>>>>>> 3257fc1 (final)

                        <div
                            className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl transition-opacity duration-300"
                            style={{ opacity: fade ? 1 : 0 }}
                        >
                            {currentSuggestions.map((s, i) => (
                                <button
                                    key={`${s}-${i}`}
                                    onClick={() => onSendMessage(s)}
                                    className={clsx(
<<<<<<< HEAD
                                        "p-4 bg-white border rounded-2xl text-slate-600 text-sm hover:shadow-md transition-all text-left",
                                        theme.border,
                                        `hover:${theme.border.replace('border-', 'border-opacity-100 border-')}`
=======
                                        "p-4 bg-white dark:bg-zinc-900 border rounded-2xl text-slate-600 dark:text-slate-300 text-sm hover:shadow-md transition-all text-left",
                                        isDarkMode ? theme.border_dark : theme.border,
                                        isDarkMode ? `hover:${theme.border_dark.replace('border-', 'border-opacity-100 border-')}` : `hover:${theme.border.replace('border-', 'border-opacity-100 border-')}`
>>>>>>> 3257fc1 (final)
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
<<<<<<< HEAD
                                msg.role === 'user' ? "bg-slate-200 text-slate-600" : clsx("text-white", theme.primary)
=======
                                msg.role === 'user' ? "bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-300" : clsx("text-white shadow-md", theme.primary)
>>>>>>> 3257fc1 (final)
                            )}>
                                {msg.role === 'user' ? "U" : "IA"}
                            </div>

                            <div className={clsx(
<<<<<<< HEAD
                                "p-4 sm:p-5 rounded-2xl shadow-sm leading-relaxed text-sm sm:text-base",
                                msg.role === 'user'
                                    ? "bg-white text-slate-800 rounded-tr-none border border-slate-100"
                                    : clsx("bg-white text-slate-800 rounded-tl-none border bg-gradient-to-br", theme.border, theme.bg_soft)
=======
                                "p-4 sm:p-5 rounded-2xl shadow-sm leading-relaxed text-sm sm:text-base transition-colors duration-200",
                                msg.role === 'user'
                                    ? "bg-white dark:bg-zinc-900 text-slate-800 dark:text-slate-200 rounded-tr-none border border-slate-100 dark:border-slate-700"
                                    : clsx("text-slate-800 dark:text-slate-200 rounded-tl-none border bg-gradient-to-br", isDarkMode ? theme.bg_dark_soft : "bg-white " + theme.bg_soft, isDarkMode ? theme.border_dark : theme.border)
>>>>>>> 3257fc1 (final)
                            )}>
                                <Markdown
                                    remarkPlugins={[remarkBreaks]}
                                    components={{
                                        ul: ({ node, ...props }) => <ul {...props} className="list-disc pl-4 mb-2" />,
                                        ol: ({ node, ...props }) => <ol {...props} className="list-decimal pl-4 mb-2" />,
                                        p: ({ node, ...props }) => <p {...props} className="mb-2 last:mb-0" />,
<<<<<<< HEAD
                                        strong: ({ node, ...props }) => <strong {...props} className={clsx("font-bold", theme.text)} />,
=======
                                        strong: ({ node, ...props }) => <strong {...props} className={clsx("font-bold", isDarkMode ? theme.text_dark : theme.text)} />,
>>>>>>> 3257fc1 (final)
                                        br: () => <br />,
                                    }}
                                >
                                    {msg.content}
                                </Markdown>

                                {msg.metadata?.score != null && (
<<<<<<< HEAD
                                    <ExpertVerdictCard 
                                        score={msg.metadata.score} 
                                        ecole={msg.metadata.ecole} 
=======
                                    <ExpertVerdictCard
                                        score={msg.metadata.score}
                                        ecole={msg.metadata.ecole}
>>>>>>> 3257fc1 (final)
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
<<<<<<< HEAD
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
=======
                        <div className={clsx("bg-white dark:bg-zinc-900 px-4 py-3 rounded-2xl rounded-tl-none border shadow-sm flex items-center gap-2 transition-colors", isDarkMode ? theme.border_dark : theme.border)}>
                            <Loader2 size={16} className={clsx("animate-spin", isDarkMode ? theme.text_dark : theme.accent)} />
                            <span className="text-slate-400 text-sm font-medium">
                                {statuses[statusIndex]}
                            </span>
                        </div>
                    </div>
                )}
                <div ref={scrollRef} className="h-20" /> {/* Extra space to ensure last message is fully visible */}
            </div>

            {/* Input Area */}
            <div className={clsx("p-4 sm:p-6 border-t transition-colors duration-300", isDarkMode ? `bg-black ${theme.border_dark}` : `bg-white ${theme.border}`)}>
>>>>>>> 3257fc1 (final)
                <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative flex items-center">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
<<<<<<< HEAD
                        placeholder="Posez votre question à propos du YAFI..."
                        className={clsx(
                            "w-full pl-6 pr-24 py-4 bg-slate-50 border border-slate-200 rounded-full focus:outline-none focus:ring-2 transition-all text-slate-700 shadow-inner",
                            `focus:ring-${theme.primary.split('-')[1]}-500/50`,
                            `focus:border-${theme.primary.split('-')[1]}-500`
=======
                        placeholder="Posez votre question (max 50 car.)..."
                        maxLength={50}
                        className={clsx(
                            "w-full pl-6 pr-32 py-4 bg-slate-50 dark:bg-zinc-900 border border-slate-200 dark:border-slate-700 rounded-full focus:outline-none focus:ring-2 transition-all text-slate-700 dark:text-slate-200 shadow-inner",
                            `focus:ring-${theme.primary.split('-')[1]}-500/50`,
                            isDarkMode ? `focus:border-${theme.primary.split('-')[1]}-400` : `focus:border-${theme.primary.split('-')[1]}-500`
>>>>>>> 3257fc1 (final)
                        )}
                        style={{ '--tw-ring-color': theme.primary.replace('bg-', 'var(--tw-colors-') } as React.CSSProperties}
                        disabled={isLoading}
                    />

<<<<<<< HEAD
=======
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
                            isMuted ? "text-red-400 hover:bg-red-50" : "text-slate-400 hover:bg-slate-100"
                        )}
                        title={isMuted ? "Activer le son" : "Couper le son"}
                    >
                        {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
                    </button>

>>>>>>> 3257fc1 (final)
                    <button
                        type="button"
                        onClick={startListening}
                        className={clsx(
                            "absolute right-14 p-2 rounded-full transition-all",
<<<<<<< HEAD
                            isListening ? "bg-red-100 text-red-500 animate-pulse" : clsx("text-slate-400 hover:bg-slate-100", `hover:${theme.accent}`)
=======
                            isListening ? "bg-red-100 dark:bg-red-900/30 text-red-500 animate-pulse" : clsx("text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700", `hover:${isDarkMode ? theme.text_dark : theme.accent}`)
>>>>>>> 3257fc1 (final)
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
