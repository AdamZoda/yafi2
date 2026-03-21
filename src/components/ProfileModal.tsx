import React, { useState } from 'react';
import { X, User, Mail, LogOut, Check, Palette, Loader2 } from 'lucide-react';
import type { Profile } from '../types';
import { useTheme } from '../contexts/ThemeContext';
import { themes, type ThemeColor } from '../lib/themes';
import { supabase } from '../lib/supabase';
import { clsx } from 'clsx';

interface ProfileModalProps {
    isOpen: boolean;
    onClose: () => void;
    profile: Profile;
    onUpdateProfile: (updatedProfile: Profile) => void;
    onLogout: () => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({
    isOpen,
    onClose,
    profile,
    onUpdateProfile,
    onLogout
}) => {
    const { currentTheme, setTheme, theme } = useTheme();
    const [name, setName] = useState(profile.name);
    const [email, setEmail] = useState(profile.email);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

    if (!isOpen) return null;

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setMessage(null);

        try {
            // Update in Supabase
            const { error } = await supabase
                .from('users')
                .update({ full_name: name, email: email })
                .eq('id', profile.id);

            if (error) throw error;

            // Update local state
            const updatedProfile = { ...profile, name, email };
            onUpdateProfile(updatedProfile);

            setMessage({ type: 'success', text: 'Profil mis à jour avec succès !' });

            // Close after brief delay
            setTimeout(() => {
                onClose();
                setMessage(null);
            }, 1500);

        } catch (err: any) {
            console.error(err);
            setMessage({ type: 'error', text: 'Erreur lors de la mise à jour.' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            className="fixed inset-0 z-[999] flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-sm animate-fade-in"
            onClick={onClose}
        >
            <div
                className="bg-white rounded-[2rem] shadow-2xl w-full max-w-md relative flex flex-col max-h-[90vh] animate-scale-in"
                onClick={(e) => e.stopPropagation()}
            >

                {/* Header - Fixed at top */}
                <div
                    className={clsx(
                        "p-6 flex items-center justify-between text-white shadow-md shrink-0 rounded-t-[2rem]",
                        "bg-gradient-to-br",
                        theme.gradient,
                        !theme.gradient && theme.primary
                    )}
                    style={{ backgroundColor: !theme.gradient ? '#059669' : undefined }}
                >
                    <h2 className="text-xl font-bold flex items-center gap-2">
                        <User size={24} />
                        Modifier mon profil
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-2 bg-white/20 hover:bg-white/30 rounded-full transition-colors backdrop-blur-sm shadow-sm"
                        aria-label="Fermer"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Scrollable Content */}
                <div className="p-6 space-y-6 overflow-y-auto custom-scrollbar">
                    {/* Theme Selector */}
                    <div>
                        <h3 className="text-sm font-bold text-slate-700 mb-3 flex items-center gap-2">
                            <Palette size={16} className={theme.accent} />
                            Thème
                        </h3>
                        <div className="flex gap-3 justify-center flex-wrap">
                            {(Object.keys(themes) as ThemeColor[]).map((colorKey) => (
                                <button
                                    key={colorKey}
                                    onClick={() => setTheme(colorKey)}
                                    className={clsx(
                                        "w-10 h-10 rounded-full flex items-center justify-center transition-all border-2",
                                        themes[colorKey].primary,
                                        currentTheme === colorKey
                                            ? "ring-2 ring-offset-2 ring-slate-400 scale-110 border-white"
                                            : "border-transparent opacity-70 hover:opacity-100 hover:scale-105"
                                    )}
                                    title={themes[colorKey].name}
                                >
                                    {currentTheme === colorKey && <Check size={16} className="text-white" />}
                                </button>
                            ))}
                        </div>
                    </div>

                    <hr className="border-slate-100" />

                    {/* Edit Form */}
                    <form onSubmit={handleSave} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">Nom Complet</label>
                            <div className="relative">
                                <User className="absolute left-3 top-3.5 text-slate-400" size={18} />
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 outline-none transition-all"
                                    style={{ '--tw-ring-color': theme.primary.replace('bg-', 'var(--tw-colors-') } as React.CSSProperties}
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-3.5 text-slate-400" size={18} />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 outline-none transition-all bg-slate-50 text-slate-500 cursor-not-allowed"
                                    disabled
                                    title="Modification d'email désactivée pour le moment"
                                />
                            </div>
                        </div>

                        {message && (
                            <div className={clsx(
                                "p-3 rounded-lg text-sm flex items-center gap-2",
                                message.type === 'success' ? "bg-emerald-50 text-emerald-600" : "bg-red-50 text-red-600"
                            )}>
                                {message.type === 'success' ? <Check size={16} /> : <Loader2 size={16} />}
                                {message.text}
                            </div>
                        )}

                        <div className="pt-2">
                            <button
                                type="submit"
                                disabled={loading}
                                className={clsx(
                                    "w-full py-3 rounded-xl font-bold text-white shadow-lg transition-all active:scale-95 flex items-center justify-center gap-2",
                                    theme.primary,
                                    theme.shadow
                                )}
                            >
                                {loading ? <Loader2 className="animate-spin" /> : "Enregistrer les modifications"}
                            </button>
                        </div>
                    </form>

                    <button
                        onClick={onLogout}
                        className="w-full py-3 rounded-xl font-medium text-slate-500 hover:bg-slate-50 hover:text-red-500 transition-colors flex items-center justify-center gap-2"
                    >
                        <LogOut size={18} />
                        Se déconnecter
                    </button>

                    <button
                        onClick={onClose}
                        className="w-full py-2 text-sm text-slate-400 hover:text-slate-600 transition-colors"
                    >
                        Fermer
                    </button>
                </div>
            </div>
        </div>
    );
};
