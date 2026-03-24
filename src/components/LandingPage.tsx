import React from 'react';
<<<<<<< HEAD
import { ArrowRight, BookOpen, MessageSquare, ShieldCheck, GraduationCap } from 'lucide-react';
=======
import { ArrowRight, BookOpen, MessageSquare, ShieldCheck, Brain, Sparkles, Zap } from 'lucide-react';
>>>>>>> 3257fc1 (final)
import { useTheme } from '../contexts/ThemeContext';
import { clsx } from 'clsx';

interface LandingPageProps {
    onStart: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onStart }) => {
<<<<<<< HEAD
    const { theme } = useTheme();

    return (
        <div className={clsx("min-h-screen bg-gradient-to-br flex flex-col items-center justify-center p-6 relative overflow-hidden", theme.gradient.replace('from-', 'from-slate-50 to-').split(' ')[1])}>
            {/* Background elements */}
            <div className="absolute inset-0 bg-slate-50 -z-20" />
            <div className={clsx("absolute inset-0 opacity-10 bg-gradient-to-br", theme.gradient)} />

            {/* Background Decor */}
            <div className={clsx("absolute top-20 left-20 w-64 h-64 rounded-full blur-3xl animate-pulse opacity-20", theme.primary)} />
            <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-200/20 rounded-full blur-3xl animate-pulse delay-1000" />

            <div className="max-w-4xl w-full bg-white/80 backdrop-blur-xl rounded-[2.5rem] shadow-2xl overflow-hidden border border-white/50 flex flex-col md:flex-row">

                {/* Left Side: Visual & Brand */}
                <div className={clsx("md:w-1/2 p-12 text-white flex flex-col justify-between relative overflow-hidden", theme.primary)}>
                    <div className="relative z-10">
                        <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mb-8 backdrop-blur-sm border border-white/20">
                            <GraduationCap size={40} className="text-white" />
                        </div>
                        <h1 className="text-4xl font-bold mb-4 leading-tight">YAFI Chatbot <br /><span className="text-white/80">EST Safi</span></h1>
                        <p className="text-white/80 text-lg leading-relaxed">
                            Une plateforme intelligente d'assistance éducative propulsée par l'Intelligence Artificielle.
                        </p>
                    </div>

                    <div className="relative z-10 mt-12 space-y-4">
                        <div className="flex items-center gap-4 text-sm font-medium text-white/90">
                            <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center"><BookOpen size={16} /></div>
                            <span>Base Documentaire RAG</span>
                        </div>
                        <div className="flex items-center gap-4 text-sm font-medium text-white/90">
                            <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center"><MessageSquare size={16} /></div>
                            <span>Assistance 24/7</span>
                        </div>
                        <div className="flex items-center gap-4 text-sm font-medium text-white/90">
                            <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center"><ShieldCheck size={16} /></div>
                            <span>Securité & Confidentialité</span>
                        </div>
                    </div>

                    {/* Abstract Pattern */}
                    <div className="absolute -bottom-24 -right-24 w-64 h-64 rounded-full border-4 border-white/5" />
                    <div className="absolute -top-12 -right-12 w-32 h-32 rounded-full border-4 border-white/5" />
                </div>

                {/* Right Side: Context & Action */}
                <div className="md:w-1/2 p-12 flex flex-col justify-center">
                    <h2 className="text-2xl font-bold text-slate-800 mb-6">À propos du projet</h2>
                    <p className="text-slate-600 mb-6 leading-relaxed">
                        Ce projet de fin d'études vise à faciliter l'accès à l'information pour les étudiants et l'administration.
                        Grâce à une IA avancée, posez vos questions sur les cours, les emplois du temps ou les procédures administratives et obtenez des réponses instantanées basées sur des documents officiels.
                    </p>

                    <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100 mb-8">
                        <h3 className="font-semibold text-slate-900 mb-2">Fonctionnalités Clés</h3>
                        <ul className="space-y-2 text-sm text-slate-500">
                            <li>• Recherche documentaire intelligente</li>
                            <li>• Mémoire contextuelle des conversations</li>
                            <li>• Interface administrative dédiée</li>
                        </ul>
                    </div>

                    <button
                        onClick={onStart}
                        className={clsx(
                            "group w-full py-4 text-white rounded-xl font-bold transition-all shadow-lg flex items-center justify-center gap-2 bg-slate-900 hover:opacity-90",
                            `hover:${theme.shadow}`
                        )}
                    >
                        Accéder à la plateforme
                        <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
=======
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
>>>>>>> 3257fc1 (final)
                    </button>
                </div>

            </div>

<<<<<<< HEAD
            <p className="mt-8 text-slate-400 text-sm font-medium">© 2024 EST Safi - Projet YAFI</p>
=======
            {/* Footer */}
            <p className={clsx("mt-8 text-sm font-medium", isDarkMode ? "text-zinc-700" : "text-slate-400")}>
                © 2025 EST Safi — Projet PFE · YAFI v2.1
            </p>
>>>>>>> 3257fc1 (final)
        </div>
    );
};
