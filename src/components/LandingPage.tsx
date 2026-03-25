import React from 'react';
import { ArrowRight, BookOpen, MessageSquare, ShieldCheck, Brain, Sparkles, Zap } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { clsx } from 'clsx';

interface LandingPageProps {
    onStart: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onStart }) => {
    const { theme, isDarkMode } = useTheme();

    return (
        <div className={clsx("min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden", isDarkMode ? "bg-black" : "bg-slate-50")}>

            {/* Animated Background Gradient Orbs */}
            <div className={clsx("absolute top-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full blur-[120px] opacity-30 animate-pulse", isDarkMode ? "bg-emerald-700" : "bg-emerald-300")} />
            <div className={clsx("absolute bottom-[-10%] right-[-5%] w-[600px] h-[600px] rounded-full blur-[120px] opacity-20 animate-pulse", isDarkMode ? "bg-blue-700" : "bg-blue-300")} style={{ animationDelay: '2s' }} />
            <div className={clsx("absolute top-[40%] right-[20%] w-[300px] h-[300px] rounded-full blur-[100px] opacity-15 animate-pulse", isDarkMode ? "bg-purple-700" : "bg-purple-200")} style={{ animationDelay: '4s' }} />

            {/* Main Card */}
            <div className={clsx(
                "max-w-5xl w-full rounded-[2.5rem] shadow-2xl overflow-hidden flex flex-col lg:flex-row transition-all duration-500 relative z-10",
                isDarkMode ? "bg-zinc-900/90 border border-zinc-800/80 shadow-black/40" : "bg-white/90 backdrop-blur-xl border border-white/60"
            )}>

                {/* Left Side: Brand Hero */}
                <div className={clsx("lg:w-[45%] p-10 md:p-14 text-white flex flex-col justify-between relative overflow-hidden bg-gradient-to-br", theme.gradient)}>
                    
                    {/* Logo */}
                    <div className="relative z-10">
                        <img src="/yafi.png" alt="YAFI Logo" className="w-20 h-20 object-contain mb-8 drop-shadow-2xl" />
                        <h1 className="text-4xl md:text-5xl font-extrabold mb-4 leading-tight tracking-tight">
                            YAFI
                            <span className="block text-white/70 text-2xl md:text-3xl font-semibold mt-1">Your Academic Future Intelligence</span>
                        </h1>
                        <p className="text-white/80 text-base md:text-lg leading-relaxed max-w-sm">
                            Chatbot intelligent d'orientation académique pour les bacheliers marocains, combinant un système expert Prolog et un LLM local (Ollama).
                        </p>
                    </div>

                    {/* Feature pills */}
                    <div className="relative z-10 mt-10 space-y-3">
                        {[
                            { icon: <Brain size={16} />, label: "Système Expert Pyswip (Prolog)" },
                            { icon: <MessageSquare size={16} />, label: "Conversation Vocale (TTS + STT)" },
                            { icon: <ShieldCheck size={16} />, label: "Garde-fou Anti-Hallucination" },
                        ].map((item, i) => (
                            <div key={i} className="flex items-center gap-3 text-sm font-medium text-white/90">
                                <div className="w-8 h-8 rounded-lg bg-white/15 backdrop-blur-sm flex items-center justify-center border border-white/10">
                                    {item.icon}
                                </div>
                                <span>{item.label}</span>
                            </div>
                        ))}
                    </div>

                    {/* Abstract decorative circles */}
                    <div className="absolute -bottom-20 -right-20 w-56 h-56 rounded-full border-[3px] border-white/5" />
                    <div className="absolute -top-10 -right-10 w-28 h-28 rounded-full border-[3px] border-white/5" />
                    <div className="absolute bottom-10 left-[-40px] w-20 h-20 rounded-full bg-white/5" />
                </div>

                {/* Right Side: Info & CTA */}
                <div className="lg:w-[55%] p-10 md:p-14 flex flex-col justify-center">

                    {/* Badge */}
                    <div className={clsx("inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider mb-6 w-fit",
                        isDarkMode ? "bg-emerald-900/30 text-emerald-400 border border-emerald-800/50" : "bg-emerald-50 text-emerald-700 border border-emerald-100"
                    )}>
                        <Sparkles size={14} />
                        Projet de Fin d'Études — EST Safi
                    </div>

                    <h2 className={clsx("text-3xl font-bold mb-4", isDarkMode ? "text-white" : "text-slate-900")}>
                        L'IA au service de l'orientation scolaire
                    </h2>
                    <p className={clsx("mb-8 leading-relaxed text-base", isDarkMode ? "text-zinc-400" : "text-slate-600")}>
                        YAFI interroge une base de connaissances Prolog contenant les écoles, filières, frais, localisations et seuils d'admission du système éducatif marocain. Lorsque Prolog n'a pas la réponse, le LLM local Ollama prend le relais avec un prompt cadré pour éviter toute hallucination.
                    </p>

                    {/* Feature cards grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-8">
                        {[
                            { icon: <BookOpen size={20} />, title: "200+", desc: "Faits Prolog" },
                            { icon: <Zap size={20} />, title: "Ollama", desc: "LLM 100% Local" },
                            { icon: <Brain size={20} />, title: "SSE", desc: "Streaming Temps Réel" },
                        ].map((card, i) => (
                            <div key={i} className={clsx(
                                "p-4 rounded-2xl border text-center transition-all hover:scale-105",
                                isDarkMode ? "bg-zinc-800/50 border-zinc-700/50 hover:border-zinc-600" : "bg-slate-50 border-slate-100 hover:border-slate-200 hover:shadow-sm"
                            )}>
                                <div className={clsx("mx-auto w-10 h-10 rounded-xl flex items-center justify-center mb-2", isDarkMode ? "bg-zinc-700/50 text-emerald-400" : "bg-emerald-50 text-emerald-600")}>
                                    {card.icon}
                                </div>
                                <p className={clsx("font-bold text-lg", isDarkMode ? "text-white" : "text-slate-800")}>{card.title}</p>
                                <p className={clsx("text-xs", isDarkMode ? "text-zinc-500" : "text-slate-400")}>{card.desc}</p>
                            </div>
                        ))}
                    </div>

                    {/* CTA Button */}
                    <button
                        onClick={onStart}
                        className={clsx(
                            "group w-full py-4 rounded-2xl font-bold text-lg transition-all shadow-lg flex items-center justify-center gap-3",
                            "bg-gradient-to-r text-white hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]",
                            theme.gradient
                        )}
                    >
                        Accéder à la plateforme
                        <ArrowRight size={22} className="group-hover:translate-x-1.5 transition-transform" />
                    </button>
                </div>

            </div>

            {/* Footer */}
            <p className={clsx("mt-8 text-sm font-medium", isDarkMode ? "text-zinc-700" : "text-slate-400")}>
                © 2025 EST Safi — Projet PFE · YAFI v2.1
            </p>
        </div>
    );
};
