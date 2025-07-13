# Makefile for Terminal Chat Bluetooth

.PHONY: help install install-macos install-linux install-windows install-termux test run clean

# Default target
help:
	@echo "Terminal Chat Bluetooth - Available targets:"
	@echo ""
	@echo "  install          - Auto-detect platform and install"
	@echo "  install-macos    - Install on macOS"
	@echo "  install-linux    - Install on Linux"
	@echo "  install-windows  - Install on Windows (use install.bat instead)"
	@echo "  install-termux   - Install on Termux (Android)"
	@echo "  test             - Run test suite"
	@echo "  test-scan        - Test Bluetooth scanning"
	@echo "  run              - Run the application"
	@echo "  run-bluetooth    - Force run Bluetooth version"
	@echo "  run-tcp          - Force run TCP fallback version"
	@echo "  clean            - Clean up temporary files"
	@echo "  permissions      - Setup permissions (Linux/macOS)"
	@echo ""

# Auto-detect platform and install
install:
	@echo "Detecting platform..."
	@if [ "$(shell uname)" = "Darwin" ]; then \
		make install-macos; \
	elif [ "$(shell uname)" = "Linux" ]; then \
		if [ -n "$(shell which pkg 2>/dev/null)" ]; then \
			make install-termux; \
		else \
			make install-linux; \
		fi; \
	else \
		echo "Unsupported platform. Use install.bat for Windows."; \
	fi

# macOS installation
install-macos:
	@echo "Installing for macOS..."
	@chmod +x install.sh
	@./install.sh

# Linux installation
install-linux:
	@echo "Installing for Linux..."
	@chmod +x install.sh
	@./install.sh

# Termux installation
install-termux:
	@echo "Installing for Termux..."
	@chmod +x install_termux.sh
	@./install_termux.sh

# Run tests
test:
	@echo "Running test suite..."
	@python3 test.py

# Test Bluetooth scanning
test-scan:
	@echo "Testing Bluetooth scanning..."
	@python3 test.py --scan

# Run application
run:
	@echo "Starting Terminal Chat Bluetooth..."
	@python3 launcher.py

# Force run Bluetooth version
run-bluetooth:
	@echo "Starting Bluetooth chat (forced)..."
	@python3 bluetooth_chat.py

# Force run TCP version
run-tcp:
	@echo "Starting TCP chat (fallback)..."
	@python3 tcp_chat_fallback.py

# Setup permissions (Linux/macOS)
permissions:
	@echo "Setting up permissions..."
	@if [ "$(shell uname)" = "Linux" ]; then \
		echo "Adding user to bluetooth group..."; \
		sudo usermod -a -G bluetooth $$USER; \
		echo "Enabling Bluetooth service..."; \
		sudo systemctl enable bluetooth; \
		sudo systemctl start bluetooth; \
		echo "Please log out and log back in for group changes to take effect."; \
	elif [ "$(shell uname)" = "Darwin" ]; then \
		echo "Please manually grant Bluetooth permissions:"; \
		echo "System Preferences > Security & Privacy > Privacy > Bluetooth"; \
		echo "Add Terminal.app to the list"; \
	fi

# Clean up
clean:
	@echo "Cleaning up temporary files..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.log" -delete
	@echo "Cleanup complete."

# Quick setup (install + test + run)
setup: install test
	@echo ""
	@echo "Setup complete! Run 'make run' to start chatting."

# Development helpers
dev-install:
	@echo "Installing development dependencies..."
	@pip3 install --user pylint flake8 black

lint:
	@echo "Running linter..."
	@python3 -m flake8 --max-line-length=88 --ignore=E203,W503 *.py || true

format:
	@echo "Formatting code..."
	@python3 -m black *.py || echo "black not available, skipping format"

# Create distribution package
dist:
	@echo "Creating distribution package..."
	@mkdir -p dist
	@tar -czf dist/terminal-chat-bluetooth.tar.gz \
		*.py *.txt *.md *.json *.sh *.bat Makefile
	@echo "Package created: dist/terminal-chat-bluetooth.tar.gz"

# Show system info
info:
	@echo "System Information:"
	@echo "Platform: $(shell uname -s)"
	@echo "Architecture: $(shell uname -m)"
	@echo "Python version: $(shell python3 --version 2>/dev/null || echo 'Not found')"
	@echo "Pip version: $(shell pip3 --version 2>/dev/null || echo 'Not found')"
	@echo ""
	@echo "Bluetooth status:"
	@if command -v bluetoothctl >/dev/null 2>&1; then \
		echo "bluetoothctl available"; \
		bluetoothctl show 2>/dev/null | head -3 || echo "Bluetooth service not running"; \
	else \
		echo "bluetoothctl not available"; \
	fi
