import { ReactNode, createContext, useContext, useEffect, useState } from 'react';
import { Appearance, ColorSchemeName } from 'react-native';

interface ThemeContextValue {
  colorScheme: ColorSchemeName;
  setScheme: (scheme: ColorSchemeName) => void;
}

const ThemeContext = createContext<ThemeContextValue>({ colorScheme: 'dark', setScheme: () => {} });

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [colorScheme, setColorScheme] = useState<ColorSchemeName>('dark');

  useEffect(() => {
    const scheme = Appearance.getColorScheme();
    setColorScheme(scheme ?? 'dark');
  }, []);

  return (
    <ThemeContext.Provider value={{ colorScheme, setScheme: setColorScheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeScheme = () => useContext(ThemeContext);
