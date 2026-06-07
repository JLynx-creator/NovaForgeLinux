# ============================================================
# NovaForge Linux — Custom Zsh Configuration
# ============================================================
# Preconfigured with Starship prompt, auto-suggestions,
# and syntax highlighting for developers and AI engineers.
# ============================================================

# ── Environment & History Settings ────────────────────────
export HISTFILE=~/.zsh_history
export HISTSIZE=10000
export SAVEHIST=10000
setopt APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_REDUCE_BLANKS

# Keybindings - Standard Home/End keys
bindkey '\e[1~' beginning-of-line
bindkey '\e[4~' end-of-line
bindkey '\e[H'   beginning-of-line
bindkey '\e[F'   end-of-line
bindkey '^[[H'  beginning-of-line
bindkey '^[[F'  end-of-line

# ── Plugins Integration ───────────────────────────────────

# 1. Zsh Auto-Suggestions
if [ -f /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
    source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
    # Change suggestion color to dark gray/purple
    ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=60'
fi

# 2. Zsh Syntax Highlighting
if [ -f /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
    source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

# 3. Autojump Integration
if [ -f /usr/share/autojump/autojump.sh ]; then
    source /usr/share/autojump/autojump.sh
fi

# ── Custom Terminal Aliases ───────────────────────────────
alias ls='ls --color=auto'
alias ll='ls -lh --color=auto'
alias la='ls -lha --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gd='git diff'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline -n 10'

# NovaForge shortcuts
alias cc='novaforge-control-center'
alias chat='novaforge-chat'
alias ai='novaforge-chat'
alias openwebui='novaforge-openwebui'

# ── Starship Prompt Initialization ───────────────────────
if command -v starship &>/dev/null; then
    eval "$(starship init zsh)"
fi
