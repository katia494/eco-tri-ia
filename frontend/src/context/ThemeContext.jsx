import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
    const [darkMode, setDarkMode] = useState(
        () => localStorage.getItem('theme') === 'dark'
    );

    /* Applique / retire la classe "dark" sur <html> à chaque changement */
    useEffect(() => {
        if (darkMode) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }, [darkMode]);

    const toggleDark = () => setDarkMode(d => !d);

    return (
        <ThemeContext.Provider value={{ darkMode, toggleDark }}>
            {children}
        </ThemeContext.Provider>
    );
}

/* Hook court pour consommer le contexte */
export function useTheme() {
    return useContext(ThemeContext);
}
