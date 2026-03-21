import React from 'react';
import { ArrowRight, BookOpen, MessageSquare, ShieldCheck, GraduationCap } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { clsx } from 'clsx';

interface LandingPageProps {
    onStart: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onStart }) => {
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
                    </button>
                </div>

            </div>

            <p className="mt-8 text-slate-400 text-sm font-medium">© 2024 EST Safi - Projet YAFI</p>
        </div>
    );
};
