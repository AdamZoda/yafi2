import React, { useEffect, useState } from 'react';
import { MessageSquarePlus, MessageSquare, History, UserCog, Ghost, X, LifeBuoy } from 'lucide-react';
import type { Session, Profile } from '../types';
import { supabase } from '../lib/supabase';
import { useTheme } from '../contexts/ThemeContext';
import { clsx } from 'clsx';
import { Link } from 'react-router-dom';

interface SidebarProps {
    currentSessionId: string | null;
    onSelectSession: (id: string) => void;
    onNewChat: () => void;
    profile: Profile;
    refreshKey?: number;
    isOpen: boolean;
    onClose: () => void;
    extractedProfile?: any;
}

export const Sidebar: React.FC<SidebarProps> = ({
    currentSessionId,
    onSelectSession,
    onNewChat,
    profile,
    refreshKey = 0,
    isOpen,
    onClose,
    extractedProfile
}) => {
    const { theme, isDarkMode } = useTheme();
    const [sessions, setSessions] = useState<Session[]>([]);

    useEffect(() => {
        fetchSessions();
    }, [currentSessionId, refreshKey]);

    const fetchSessions = async () => {
        if (!supabase) return;
        const { data, error } = await supabase
            .from('sessions')
            .select('*')
            .eq('user_id', profile.id)
            .order('created_at', { ascending: false })
            .limit(20);

        if (error) console.error("Error fetching sessions:", error);
        if (data) setSessions(data);
    };

    return (
        <>
            {/* Overlay for mobile */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-20 md:hidden animate-fade-in"
                    onClick={onClose}
                />
            )}

            <aside className={clsx(
                "fixed md:static inset-y-0 left-0 z-30 w-72 md:w-64 bg-slate-50 dark:bg-black border-r border-slate-200 dark:border-slate-800 h-full md:h-[calc(100vh-4rem)] flex flex-col transition-all duration-300 ease-in-out md:translate-x-0",
                isOpen ? "translate-x-0" : "-translate-x-full"
            )}>
                <div className="p-4 flex items-center gap-3">
                    <button
                        onClick={() => { onNewChat(); onClose(); }}
                        className={clsx(
                            "flex-1 flex items-center justify-center gap-2 text-white py-3 rounded-2xl font-semibold shadow-lg transition-all active:scale-95",
                            theme.primary,
                            theme.shadow
                        )}
                    >
                        <MessageSquarePlus size={20} />
                        Nouveau Chat
                    </button>

                    <button
                        onClick={onClose}
                        className="p-3 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-xl text-slate-500 dark:text-slate-400 md:hidden"
                        title="Fermer"
                    >
                        <X size={20} />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1 custom-scrollbar">
                    <div className="px-3 py-2 text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                        <History size={12} />
                        Historique
                    </div>

                    {sessions.length === 0 ? (
                        <div className="text-center py-10 text-slate-400 dark:text-slate-600">
                            <Ghost className="mx-auto mb-2 opacity-50" size={32} />
                            <p className="text-sm">Aucune conversation</p>
                        </div>
                    ) : (
                        sessions.map((session) => (
                            <button
                                key={session.id}
                                onClick={() => { onSelectSession(session.id); onClose(); }}
                                className={clsx(
                                    "w-full text-left px-4 py-3 rounded-xl text-sm transition-all flex items-start gap-3",
                                    currentSessionId === session.id
                                        ? clsx("shadow-sm border font-medium", isDarkMode ? "bg-slate-800" : "bg-white", isDarkMode ? theme.border_dark : theme.border, isDarkMode ? theme.text_dark : theme.text)
                                        : "text-slate-600 dark:text-slate-400 hover:bg-slate-100/50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-slate-200"
                                )}
                            >
                                <MessageSquare size={16} className={currentSessionId === session.id ? clsx("mt-0.5", theme.accent) : "text-slate-400 mt-0.5"} />
                                <span className="truncate">{session.title || "Nouvelle conversation"}</span>
                            </button>
                        ))
                    )}
                </div>

                {/* --- ÉTAPE 5 : PROFIL ÉTUDIANT (DASHBOARD) --- */}
                {extractedProfile && (
                    <div className="mx-4 mb-4 p-4 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-sm animate-fade-in">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></div>
                            Profil Étudiant Détecté
                        </div>
                        <div className="space-y-3">
                            {extractedProfile.bac && (
                                <div className="flex justify-between items-center text-xs">
                                    <span className="text-slate-500 dark:text-slate-400">Série Bac</span>
                                    <span className="font-bold text-slate-700 dark:text-slate-300 bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded-md">{extractedProfile.bac}</span>
                                </div>
                            )}
                            {extractedProfile.moyenne && (
                                <div className="flex justify-between items-center text-xs">
                                    <span className="text-slate-500 dark:text-slate-400">Moyenne</span>
                                    <span className="font-bold text-slate-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-900/30 text-blue-700 px-2 py-0.5 rounded-md">{extractedProfile.moyenne}/20</span>
                                </div>
                            )}
                            {extractedProfile.ville && (
                                <div className="flex justify-between items-center text-xs">
                                    <span className="text-slate-500 dark:text-slate-400">Ville</span>
                                    <span className="font-bold text-slate-700 dark:text-slate-300 capitalize">{extractedProfile.ville}</span>
                                </div>
                            )}
                            {extractedProfile.budget && (
                                <div className="flex justify-between items-center text-xs">
                                    <span className="text-slate-500 dark:text-slate-400">Budget Max</span>
                                    <span className="font-bold text-emerald-600 dark:text-emerald-400">{extractedProfile.budget} DH</span>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {profile.role === 'admin' && (
                    <div className={clsx("p-4 border-t border-slate-200 dark:border-slate-700 transition-colors", isDarkMode ? theme.bg_dark_soft : theme.bg_soft)}>
                        <Link to="/admin" className={clsx("flex items-center gap-3 px-4 py-3 font-bold bg-white dark:bg-zinc-900 border rounded-xl hover:shadow-md transition-all text-sm", isDarkMode ? theme.text_dark : theme.text, isDarkMode ? theme.border_dark : theme.border)}>
                            <UserCog size={18} />
                            Panel Admin
                        </Link>
                    </div>
                )}

                {profile.is_premium && (
                    <div className="p-4 border-t border-slate-100 dark:border-slate-800 bg-emerald-50/30 dark:bg-emerald-900/10 transition-colors">
                        <Link to="/support" onClick={onClose} className="flex items-center gap-3 px-4 py-3 font-bold bg-white dark:bg-zinc-900 border border-emerald-100 dark:border-emerald-800/50 rounded-xl hover:shadow-md transition-all text-sm text-emerald-800 dark:text-emerald-400">
                            <LifeBuoy size={18} className="text-emerald-500 dark:text-emerald-400" />
                            Support Premium
                        </Link>
                    </div>
                )}
            </aside>
        </>
    );
};
