#!/usr/bin/env bash

# Fail fast, fail early, fail loud.
set -euo pipefail

workspace_dir="$PWD"

echo "==> Upgrading packages"
sudo apt-get update
sudo apt-get upgrade --yes

echo "==> Installing ripgrep"
sudo apt-get install --yes ripgrep

echo "==> Installing Starship"
sudo apt-get install starship --yes
grep -qxF 'eval "$(starship init bash)"' "$HOME/.bashrc" || echo 'eval "$(starship init bash)"' >> "$HOME/.bashrc"
grep -qxF 'eval "$(starship init zsh)"' "$HOME/.zshrc" || echo 'eval "$(starship init zsh)"' >> "$HOME/.zshrc"
mkdir -p "$HOME/.config"
if [ ! -f "$HOME/.config/starship.toml" ]; then
    cp "$workspace_dir/.devcontainer/starship.toml" "$HOME/.config/starship.toml"
fi

echo "==> Installing Codex and Claude Code"
npm config set allow-scripts=@anthropic-ai/claude-code --location=user
npm install -g @openai/codex @anthropic-ai/claude-code

echo "==> Installing uv"
command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "==> Initializing the Lightning submodule"
if [ ! -e "$workspace_dir/lightning/.git" ]; then
    git -C "$workspace_dir" submodule sync -- lightning
    git -C "$workspace_dir" submodule update --init lightning
fi

echo "==> Fetching Lightning's git submodules"
git -C "$workspace_dir/lightning" submodule sync --recursive
git -C "$workspace_dir/lightning" submodule update --init --recursive

echo "==> Installing Python 3.12"
# Pre-commit's docformatter hook also needs a plain `python3.12` on PATH
# (see the language_version pin in lightning/.pre-commit-config.yaml).
uv python install 3.12

echo "==> Setting up Lightning's Python and venv"
cd "$workspace_dir/lightning"
uv venv --allow-existing --python 3.12
source .venv/bin/activate
make setup

echo "==> Installing scratch's Python dependencies"
cd "$workspace_dir/scratch"
uv sync --python 3.12
