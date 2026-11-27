# Nyanko Market 🐾

A collection of custom plugins developed by Chaoschan.

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

### 3. `video-to-talk`

把技术视频做成能在组会上按自己的节奏讲解的中文演示。给一个本地视频或可播放的链接，先取一段做样片，再按原片时间码核对全片分镜。原生 HTML 离线播放，保留鼠标，画面上没有按钮。单击、空格或右方向键播一段，默认 0.5 秒后停住。可按需另交中文讲稿、Obsidian 笔记或 Notion 配图长文。[查看技能说明](video-to-talk/skills/video-to-talk/SKILL.md)

在 Codex 或 Claude Code 里可以这样提需求：

> 用 video-to-talk 处理这段本地录屏。先把两个工具对比的那一分钟做成样片，每个停点给我一句中文讲稿。

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

   # 技术视频改编为组会分享
   claude plugin install video-to-talk@nyanko-market
   ```

在 Codex 中安装 `video-to-talk`：

```bash
codex plugin marketplace add https://github.com/MrNyanko/nyanko-market
codex plugin add video-to-talk@nyanko-market
```

若已添加市场，先用 `claude plugin marketplace update nyanko-market` 或 `codex plugin marketplace upgrade nyanko-market` 刷新，再执行相应的插件安装命令。

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
