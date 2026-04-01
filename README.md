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

1. **Clone this repository** to your local machine (e.g., `~/Projects/nyanko-market`):
   ```bash
   git clone https://github.com/Chaoschan/nyanko-market.git ~/Projects/nyanko-market
   ```

2. **Register the local marketplace** in Claude Code:
   ```bash
   claude plugin marketplace add ~/Projects/nyanko-market
   ```

3. **Install the plugin**:
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
