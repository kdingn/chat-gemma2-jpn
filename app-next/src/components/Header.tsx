import "@/styles/global.css";
import DiamondIcon from "@mui/icons-material/Diamond";
import GitHubIcon from "@mui/icons-material/GitHub";
import Link from "next/link";
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
        <div className="px-2">
          <ThemeSwitch />
        </div>
        <Link
          href="https://github.com/kdingn/chat-gemma2-jpn"
          className="padding-left-10"
        >
          <GitHubIcon />
        </Link>
      </div>
    </div>
  );
}

export default Header;
