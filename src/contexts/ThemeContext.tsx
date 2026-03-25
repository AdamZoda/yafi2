import React, { createContext, useContext, useState, useEffect } from 'react';
import { themes, type ThemeColor } from '../lib/themes';

interface ThemeContextType {
    currentTheme: ThemeColor;
    theme: typeof themes['emerald'];
    isDarkMode: boolean;
    setTheme: (theme: ThemeColor) => void;
    toggleDarkMode: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [currentTheme, setCurrentTheme] = useState<ThemeColor>('emerald');
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
        const savedTheme = localStorage.getItem('est_safi_theme') as ThemeColor;
        if (savedTheme && themes[savedTheme]) {
            setCurrentTheme(savedTheme);
        }

        const savedDarkMode = localStorage.getItem('yafi_dark_mode') === 'true';
        document.documentElement.classList.toggle('dark', savedDarkMode);
        setIsDarkMode(savedDarkMode);
    }, []);

    const handleSetTheme = (theme: ThemeColor) => {
        setCurrentTheme(theme);
        localStorage.setItem('est_safi_theme', theme);
    };

    const toggleDarkMode = () => {
        setIsDarkMode(prev => {
            const newValue = !prev;
            localStorage.setItem('yafi_dark_mode', String(newValue));
            document.documentElement.classList.toggle('dark', newValue);
            return newValue;
        });
    };

    return (
        <ThemeContext.Provider value={{
            currentTheme,
            theme: themes[currentTheme],
            isDarkMode,
            setTheme: handleSetTheme,
            toggleDarkMode
        }}>
            {children}
        </ThemeContext.Provider>
    );
};

export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};
