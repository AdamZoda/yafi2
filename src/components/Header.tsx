import React from 'react';
import { Bot, UserCircle, Menu } from 'lucide-react';
import type { Profile } from '../types';
import { useTheme } from '../contexts/ThemeContext';
import { clsx } from 'clsx';

interface HeaderProps {
    profile: Profile | null;
    onOpenProfile: () => void;
    onUpgrade?: () => void;
    onToggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({ profile, onOpenProfile, onUpgrade, onToggleSidebar }) => {
    const { theme } = useTheme();

    return (
        <header className={clsx("h-16 flex items-center justify-between px-4 sm:px-6 sticky top-0 z-10 shadow-sm backdrop-blur-md border-b", theme.border, "bg-white/80")}>
            <div className="flex items-center gap-2 sm:gap-3">
                <button
                    onClick={onToggleSidebar}
                    className="p-2 hover:bg-slate-100 rounded-xl transition-colors md:hidden text-slate-600"
                    title="Menu"
                >
                    <Menu size={24} />
                </button>
                <img src="/yafi.png" alt="YAFI Logo" className={clsx("w-10 h-10 rounded-xl shadow-lg object-cover", theme.shadow)} />
                <div>
                    <h1 className="font-bold text-slate-800 text-lg leading-tight">YAFI Chatbot</h1>
                    <p className={clsx("text-xs font-medium", theme.accent)}>EST Safi Edition</p>
                </div>
            </div>

            <div className="flex items-center gap-4">
                <button className={clsx("hidden md:flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold transition-colors", theme.secondary, theme.accent)}>
                    <Bot size={18} />
                    <span>Assistant Actif</span>
                </button>

                {profile && (
                    <div className="flex items-center gap-3 pl-4 border-l border-slate-200">
                        {profile.is_premium ? (
                            <div className="hidden sm:flex items-center gap-1 px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-bold border border-amber-200 shadow-sm">
                                <span className="text-sm">👑</span> PLUS
                            </div>
                        ) : (
                            <button
                                onClick={onUpgrade}
                                className="hidden sm:flex items-center gap-1 px-3 py-1.5 bg-gradient-to-r from-amber-400 to-orange-500 text-white rounded-lg text-xs font-bold hover:shadow-lg hover:scale-105 transition-all shadow-md animate-pulse-slow"
                            >
                                <span className="text-sm">⭐</span> UPGRADE
                            </button>
                        )}
                        <div className="text-right hidden sm:block">
                            <p className="text-sm font-bold text-slate-700">{profile.name}</p>
                            <p className="text-xs text-slate-500 uppercase">{profile.role}</p>
                        </div>
                        <button
                            onClick={onOpenProfile}
                            className="p-1 hover:bg-slate-100 rounded-full transition-colors relative group"
                            title="Modifier Profil"
                        >
                            <UserCircle size={32} className="text-slate-400 group-hover:text-slate-600" />
                            <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-green-500 border-2 border-white rounded-full"></span>
                        </button>
                    </div>
                )}
            </div>
        </header>
    );
};
