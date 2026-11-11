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

### 2. `affirmative-first-writing`
**直接、具体的多语言写作规范**

用于解释问题、撰写文章与润色文字，优先写清事实、机制、原因和证据。按语境减少防御性否定、虚构反方、空洞转折与反复免责声明，同时保留有事实意义的纠错、批判和不确定性。涉及复杂链路、拓扑、时序或前后变化时，按需配图辅助解释，Markdown中的结构图优先使用Mermaid。

规则集中在一个 [`SKILL.md`](affirmative-first-writing/skills/affirmative-first-writing/SKILL.md) 中，包含识别要点、配图原则、改写示例与交稿前检查。Claude 可按任务自动选用，也可在会话中显式调用：

```text
/affirmative-first-writing:affirmative-first-writing 请按这份规范润色下面的文字：……
```

---

## 🚀 Installation

1. **Add the marketplace** to Claude Code:
   ```bash
   # HTTPS
   claude plugin marketplace add https://github.com/MrNyanko/nyanko-market
   
   # SSH (if you have GitHub SSH keys configured)
   claude plugin marketplace add git@github.com:MrNyanko/nyanko-market.git
   ```

2. **Install the plugin you need**:
   ```bash
   claude plugin install nyanko-ghostty-notify

   # 自然语言写作规范
   claude plugin install affirmative-first-writing@nyanko-market
   ```

---

## ⚙️ Ghostty Notification Requirements

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
