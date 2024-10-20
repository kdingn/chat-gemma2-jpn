"use client";

import { useTheme } from "@/hooks/useTheme";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";

export const ThemeSwitch = () => {
  const { theme, switchTheme } = useTheme();

  return (
    <div>
      {theme === "light" ? (
        <LightModeIcon onClick={switchTheme} />
      ) : (
        <DarkModeIcon onClick={switchTheme} />
      )}
    </div>
  );
};
