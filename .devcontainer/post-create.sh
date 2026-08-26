#!/usr/bin/env bash

# Fail fast, fail early, fail loud.
set -euo pipefail

workspace_dir="${containerWorkspaceFolder:-/workspaces/lightning}"

echo "==> Upgrading packages"
sudo apt-get update
sudo apt-get upgrade --yes

echo "==> Installing ripgrep"
sudo apt-get install --yes ripgrep

echo "==> Installing Starship"
sudo apt-get install starship --yes
grep -qxF 'eval "$(starship init bash)"' "$HOME/.bashrc" || echo 'eval "$(starship init bash)"' >> "$HOME/.bashrc"
grep -qxF 'eval "$(starship init zsh)"' "$HOME/.zshrc" || echo 'eval "$(starship init zsh)"' >> "$HOME/.zshrc"

echo "==> Installing Codex and Claude Code"
npm config set allow-scripts=@anthropic-ai/claude-code --location=user
npm install -g @openai/codex @anthropic-ai/claude-code

echo "==> Installing uv"
command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "==> Cloning pytorch-lightning"
if [ ! -d "$workspace_dir/lightning" ]; then
    git clone https://github.com/pupeno/pytorch-lightning.git "$workspace_dir/lightning"
fi

echo "==> Setting up Lightning's Python and venv"
cd "$workspace_dir/lightning"
uv venv --allow-existing --python 3.11
source .venv/bin/activate
make setup

echo "==> Installing scratch's Python dependencies"
cd "$workspace_dir/scratch"
uv sync --python 3.11
