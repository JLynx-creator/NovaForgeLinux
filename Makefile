# ============================================================
# NovaForge Linux — Build System
# ============================================================
# Usage:
#   make iso          Build the ISO image
#   make clean        Clean build artifacts
#   make purge        Deep clean (removes cache too)
#   make validate     Validate the built ISO
#   make test-qemu    Boot ISO in QEMU for testing
#   make setup        Install build dependencies
#   make version      Show current version
# ============================================================

SHELL := /bin/bash
.PHONY: iso clean purge validate test-qemu setup version help

# Configuration
VERSION := $(shell cat VERSION 2>/dev/null || echo "0.0.0")
ISO_NAME := novaforge-linux-$(VERSION)-amd64
BUILD_DIR := build
OUTPUT_DIR := output
LOG_FILE := build.log

# Colors for terminal output
CYAN := \033[0;36m
PURPLE := \033[0;35m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color
BOLD := \033[1m

# ============================================================
# Default target
# ============================================================
help:
	@echo -e "$(CYAN)$(BOLD)"
	@echo "  ╔══════════════════════════════════════════════╗"
	@echo "  ║         🔥 NovaForge Linux Builder 🔥        ║"
	@echo "  ║              Forge Your Universe             ║"
	@echo "  ╚══════════════════════════════════════════════╝"
	@echo -e "$(NC)"
	@echo -e "  $(BOLD)Available targets:$(NC)"
	@echo -e "    $(GREEN)make setup$(NC)       Install build dependencies"
	@echo -e "    $(GREEN)make iso$(NC)         Build the ISO image"
	@echo -e "    $(GREEN)make clean$(NC)       Clean build artifacts"
	@echo -e "    $(GREEN)make purge$(NC)       Deep clean (removes cache)"
	@echo -e "    $(GREEN)make validate$(NC)    Validate built ISO"
	@echo -e "    $(GREEN)make test-qemu$(NC)   Boot ISO in QEMU"
	@echo -e "    $(GREEN)make version$(NC)     Show current version"
	@echo ""
	@echo -e "  $(BOLD)Current version:$(NC) $(CYAN)$(VERSION)$(NC)"
	@echo ""

# ============================================================
# Install build dependencies
# ============================================================
setup:
	@echo -e "$(CYAN)[NovaForge]$(NC) Installing build dependencies..."
	@sudo bash $(BUILD_DIR)/scripts/setup-build-env.sh
	@echo -e "$(GREEN)[NovaForge]$(NC) Build environment ready!"

# ============================================================
# Build ISO
# ============================================================
iso: $(OUTPUT_DIR)
	@echo -e "$(CYAN)$(BOLD)"
	@echo "  ╔══════════════════════════════════════════════╗"
	@echo "  ║       Building NovaForge Linux $(VERSION)        ║"
	@echo "  ╚══════════════════════════════════════════════╝"
	@echo -e "$(NC)"
	@echo -e "$(YELLOW)[NovaForge]$(NC) Starting ISO build process..."
	@sudo bash $(BUILD_DIR)/scripts/build-iso.sh $(VERSION)
	@if [ -f $(OUTPUT_DIR)/$(ISO_NAME).iso ]; then \
		echo -e "$(GREEN)[NovaForge]$(NC) ISO built successfully!"; \
		echo -e "$(GREEN)[NovaForge]$(NC) Output: $(OUTPUT_DIR)/$(ISO_NAME).iso"; \
		ls -lh $(OUTPUT_DIR)/$(ISO_NAME).iso; \
	else \
		echo -e "$(RED)[NovaForge]$(NC) Build failed! Check $(LOG_FILE) for details."; \
		exit 1; \
	fi

$(OUTPUT_DIR):
	@mkdir -p $(OUTPUT_DIR)

# ============================================================
# Validate ISO
# ============================================================
validate:
	@echo -e "$(CYAN)[NovaForge]$(NC) Validating ISO..."
	@bash $(BUILD_DIR)/scripts/validate-iso.sh $(OUTPUT_DIR)/$(ISO_NAME).iso
	@echo -e "$(GREEN)[NovaForge]$(NC) Validation complete!"

# ============================================================
# Test in QEMU
# ============================================================
test-qemu:
	@echo -e "$(CYAN)[NovaForge]$(NC) Launching QEMU with NovaForge ISO..."
	@if [ ! -f $(OUTPUT_DIR)/$(ISO_NAME).iso ]; then \
		echo -e "$(RED)[NovaForge]$(NC) ISO not found! Run 'make iso' first."; \
		exit 1; \
	fi
	@qemu-system-x86_64 \
		-cdrom $(OUTPUT_DIR)/$(ISO_NAME).iso \
		-m 4096 \
		-smp 2 \
		-boot d \
		-enable-kvm \
		-vga virtio \
		-display gtk

# ============================================================
# Clean build artifacts
# ============================================================
clean:
	@echo -e "$(YELLOW)[NovaForge]$(NC) Cleaning build artifacts..."
	@cd $(BUILD_DIR) && sudo lb clean 2>/dev/null || true
	@rm -f $(LOG_FILE)
	@echo -e "$(GREEN)[NovaForge]$(NC) Clean complete."

# ============================================================
# Deep clean (removes cache too)
# ============================================================
purge:
	@echo -e "$(YELLOW)[NovaForge]$(NC) Deep cleaning (including cache)..."
	@cd $(BUILD_DIR) && sudo lb clean --purge 2>/dev/null || true
	@rm -rf $(OUTPUT_DIR)/*.iso
	@rm -f $(LOG_FILE)
	@echo -e "$(GREEN)[NovaForge]$(NC) Purge complete."

# ============================================================
# Show version
# ============================================================
version:
	@echo -e "$(CYAN)NovaForge Linux$(NC) v$(VERSION)"
