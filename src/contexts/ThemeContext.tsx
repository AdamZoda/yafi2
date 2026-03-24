import React, { createContext, useContext, useState, useEffect } from 'react';
import { themes, type ThemeColor } from '../lib/themes';

interface ThemeContextType {
    currentTheme: ThemeColor;
    theme: typeof themes['emerald'];
<<<<<<< HEAD
    setTheme: (theme: ThemeColor) => void;
=======
    isDarkMode: boolean;
    setTheme: (theme: ThemeColor) => void;
    toggleDarkMode: () => void;
>>>>>>> 3257fc1 (final)
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [currentTheme, setCurrentTheme] = useState<ThemeColor>('emerald');
<<<<<<< HEAD
=======
    const [isDarkMode, setIsDarkMode] = useState(false);
>>>>>>> 3257fc1 (final)

    useEffect(() => {
        const savedTheme = localStorage.getItem('est_safi_theme') as ThemeColor;
        if (savedTheme && themes[savedTheme]) {
            setCurrentTheme(savedTheme);
        }
<<<<<<< HEAD
=======

        const savedDarkMode = localStorage.getItem('yafi_dark_mode') === 'true';
        setIsDarkMode(savedDarkMode);
        if (savedDarkMode) {
            document.documentElement.classList.add('dark');
        }
>>>>>>> 3257fc1 (final)
    }, []);

    const handleSetTheme = (theme: ThemeColor) => {
        setCurrentTheme(theme);
        localStorage.setItem('est_safi_theme', theme);
    };

<<<<<<< HEAD
=======
    const toggleDarkMode = () => {
        setIsDarkMode(prev => {
            const newValue = !prev;
            localStorage.setItem('yafi_dark_mode', String(newValue));
            if (newValue) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
            return newValue;
        });
    };

>>>>>>> 3257fc1 (final)
    return (
        <ThemeContext.Provider value={{
            currentTheme,
            theme: themes[currentTheme],
<<<<<<< HEAD
            setTheme: handleSetTheme
=======
            isDarkMode,
            setTheme: handleSetTheme,
            toggleDarkMode
>>>>>>> 3257fc1 (final)
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
