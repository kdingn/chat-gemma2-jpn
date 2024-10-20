import "@/styles/global.css";
import DiamondIcon from "@mui/icons-material/Diamond";
import { ThemeSwitch } from "./ThemeSwitch";

function Header() {
  const title = "Chat Gemma2 JPN";
  return (
    <div className="header">
      <div className="header-title-container">
        <DiamondIcon className="header-icon" />
        <span className="header-title">{title}</span>
      </div>
      <div className="header-theme-icon">
        <ThemeSwitch />
      </div>
    </div>
  );
}

export default Header;
