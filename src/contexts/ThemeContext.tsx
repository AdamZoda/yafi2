import React, { createContext, useContext, useState, useEffect } from 'react';
import { themes, type ThemeColor } from '../lib/themes';

interface ThemeContextType {
    currentTheme: ThemeColor;
    theme: typeof themes['emerald'];
    setTheme: (theme: ThemeColor) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [currentTheme, setCurrentTheme] = useState<ThemeColor>('emerald');

    useEffect(() => {
        const savedTheme = localStorage.getItem('est_safi_theme') as ThemeColor;
        if (savedTheme && themes[savedTheme]) {
            setCurrentTheme(savedTheme);
        }
    }, []);

    const handleSetTheme = (theme: ThemeColor) => {
        setCurrentTheme(theme);
        localStorage.setItem('est_safi_theme', theme);
    };

    return (
        <ThemeContext.Provider value={{
            currentTheme,
            theme: themes[currentTheme],
            setTheme: handleSetTheme
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
