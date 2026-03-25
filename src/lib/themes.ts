export type ThemeColor = 'emerald' | 'blue' | 'purple' | 'orange' | 'rose';

export const themes: Record<ThemeColor, {
    name: string;
    primary: string;
    secondary: string;
    accent: string;
    gradient: string;
    shadow: string;
    border: string;
    text: string;
    bg_soft: string;
    // Dark Mode
    bg_dark: string;
    bg_dark_soft: string;
    border_dark: string;
    text_dark: string;
}> = {
    emerald: {
        name: 'Émeraude',
        primary: 'bg-emerald-600',
        secondary: 'bg-emerald-50',
        accent: 'text-emerald-600',
        gradient: 'from-emerald-500 to-teal-600',
        shadow: 'shadow-emerald-200',
        border: 'border-emerald-200',
        text: 'text-emerald-800',
        bg_soft: 'bg-emerald-50/50',
        // Dark Mode
        bg_dark: 'bg-black',
        bg_dark_soft: 'bg-zinc-900/80',
        border_dark: 'border-zinc-800',
        text_dark: 'text-emerald-400'
    },
    blue: {
        name: 'Océan',
        primary: 'bg-blue-600',
        secondary: 'bg-blue-50',
        accent: 'text-blue-600',
        gradient: 'from-blue-500 to-indigo-600',
        shadow: 'shadow-blue-200',
        border: 'border-blue-200',
        text: 'text-blue-800',
        bg_soft: 'bg-blue-50/50',
        // Dark Mode
        bg_dark: 'bg-black',
        bg_dark_soft: 'bg-zinc-900/80',
        border_dark: 'border-zinc-800',
        text_dark: 'text-blue-400'
    },
    purple: {
        name: 'Améthyste',
        primary: 'bg-purple-600',
        secondary: 'bg-purple-50',
        accent: 'text-purple-600',
        gradient: 'from-purple-500 to-pink-600',
        shadow: 'shadow-purple-200',
        border: 'border-purple-200',
        text: 'text-purple-800',
        bg_soft: 'bg-purple-50/50',
        // Dark Mode
        bg_dark: 'bg-black',
        bg_dark_soft: 'bg-zinc-900/80',
        border_dark: 'border-zinc-800',
        text_dark: 'text-purple-400'
    },
    orange: {
        name: 'Sunset',
        primary: 'bg-orange-500',
        secondary: 'bg-orange-50',
        accent: 'text-orange-600',
        gradient: 'from-orange-500 to-red-500',
        shadow: 'shadow-orange-200',
        border: 'border-orange-200',
        text: 'text-orange-800',
        bg_soft: 'bg-orange-50/50',
        // Dark Mode
        bg_dark: 'bg-black',
        bg_dark_soft: 'bg-zinc-900/80',
        border_dark: 'border-zinc-800',
        text_dark: 'text-orange-400'
    },
    rose: {
        name: 'Rose',
        primary: 'bg-rose-500',
        secondary: 'bg-rose-50',
        accent: 'text-rose-600',
        gradient: 'from-rose-500 to-pink-500',
        shadow: 'shadow-rose-200',
        border: 'border-rose-200',
        text: 'text-rose-800',
        bg_soft: 'bg-rose-50/50',
        // Dark Mode
        bg_dark: 'bg-black',
        bg_dark_soft: 'bg-zinc-900/80',
        border_dark: 'border-zinc-800',
        text_dark: 'text-rose-400'
    }
};
