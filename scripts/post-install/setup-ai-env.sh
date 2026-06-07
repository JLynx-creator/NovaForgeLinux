#!/bin/bash
# ============================================================
# NovaForge Linux — AI Development Environment Setup
# ============================================================
set -e

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${CYAN}=== NovaForge AI Environment Installer ===${NC}"
echo "This script configures a Python virtual environment with popular AI/ML libraries."

# 1. Install prerequisites
echo -e "${CYAN}[AI Setup]${NC} Installing system packages..."
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    git-lfs \
    build-essential \
    libffi-dev \
    libssl-dev

# Initialize Git LFS
git lfs install || true

# 2. Create python virtual environment
AI_VENV_DIR="$HOME/novaforge-ai-env"
if [ -d "$AI_VENV_DIR" ]; then
    echo -e "${YELLOW}[AI Setup]${NC} Virtual environment already exists at $AI_VENV_DIR. Upgrading packages..."
else
    echo -e "${CYAN}[AI Setup]${NC} Creating virtual environment at $AI_VENV_DIR..."
    python3 -m venv "$AI_VENV_DIR"
fi

# Activate venv
source "$AI_VENV_DIR/bin/activate"

# 3. Upgrade pip, setuptools, wheel
echo -e "${CYAN}[AI Setup]${NC} Upgrading Python package tools..."
pip install --upgrade pip setuptools wheel

# 4. Install ML frameworks
echo -e "${CYAN}[AI Setup]${NC} Installing PyTorch and related vision/audio libraries (CPU by default, CUDA script handles GPU)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo -e "${CYAN}[AI Setup]${NC} Installing TensorFlow (CPU)..."
pip install tensorflow-cpu

echo -e "${CYAN}[AI Setup]${NC} Installing HuggingFace ecosystem (transformers, datasets, accelerate, huggingface_hub)..."
pip install transformers datasets accelerate huggingface_hub

echo -e "${CYAN}[AI Setup]${NC} Installing Jupyter and core scientific libraries (numpy, pandas, matplotlib, scikit-learn)..."
pip install jupyterlab ipywidgets numpy pandas matplotlib seaborn scikit-learn scipy

# Register virtual environment as a Jupyter kernel
python3 -m ipykernel install --user --name=novaforge-ai --display-name="Python 3 (NovaForge AI)"

echo ""
echo -e "${GREEN}=== NovaForge: AI Development Environment Configured! ===${NC}"
echo -e "To activate the environment in your terminal, run:"
echo -e "  ${YELLOW}source $AI_VENV_DIR/bin/activate${NC}"
echo -e "To launch Jupyter Lab, run:"
echo -e "  ${YELLOW}jupyter lab${NC}"
echo ""
