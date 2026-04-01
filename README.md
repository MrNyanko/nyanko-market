# Nyanko Market 🐾

A collection of custom Claude Code plugins developed by Chaoschan. 

## 📦 Available Plugins

### 1. `nyanko-ghostty-notify`
**Ghostty terminal notifications for Claude Code events (Tmux compatible)**

This plugin fuses rigorous TTY tracking with macOS native notification fallbacks (`osascript`). It is specifically optimized for **Ghostty** terminal users and fully supports **Tmux** environments.

**Supported Events:**
- 🛡️ Permission Prompts
- ⏳ Idle Prompts
- 🔑 Authentication Success
- 💬 Elicitation Dialogs (Asking a question)

---

## 🚀 Installation

1. **Add the marketplace** to Claude Code:
   ```bash
   # HTTPS
   claude plugin marketplace add https://github.com/Chaoschan/nyanko-market
   
   # SSH (if you have GitHub SSH keys configured)
   claude plugin marketplace add git@github.com:Chaoschan/nyanko-market.git
   ```

2. **Install the plugin**:
   ```bash
   claude plugin install nyanko-ghostty-notify
   ```

---

## ⚙️ Configuration & Requirements

### Tmux Users
If you are using **Tmux**, you must explicitly enable DCS passthrough in your `~/.tmux.conf` so that the OSC 777 desktop notification sequences can penetrate the Tmux session and reach Ghostty:

```tmux
# ~/.tmux.conf
set -g allow-passthrough on
```

*Don't forget to reload your Tmux configuration after adding the setting (`tmux source-file ~/.tmux.conf`).*

### macOS Fallback
The script includes a fallback to macOS native `osascript` notifications. If a valid TTY cannot be located, it will automatically route the notification through the macOS Notification Center to guarantee delivery.

## 📄 License
MIT License
