#!/bin/bash

# I See U Toolkit - Automated Installation Script
# Author: kishwordulal1234
# Description: Complete installation script for all I See U Toolkit versions
# Usage: curl -fsSL https://raw.githubusercontent.com/kishwordulal1234/i-see-u/main/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    echo -e "${PURPLE}"
    echo "  ██╗    ███████╗███████╗███████╗    ██╗   ██╗"
    echo "  ██║    ██╔════╝██╔════╝██╔════╝    ██║   ██║"
    echo "  ██║    ███████╗█████╗  █████╗      ██║   ██║"
    echo "  ██║    ╚════██║██╔══╝  ██╔══╝      ██║   ██║"
    echo "  ██║    ███████║███████╗███████╗    ╚██████╔╝"
    echo "  ╚═╝    ╚══════╝╚══════╝╚══════╝     ╚═════╝ "
    echo ""
    echo -e "${WHITE}     Advanced Payload Generation & APK Injection Toolkit${NC}"
    echo -e "${CYAN}     https://github.com/kishwordulal1234/i-see-u${NC}"
    echo ""
}

# Logging function
log() {
    local level=$1
    shift
    case $level in
        INFO)  echo -e "${GREEN}[INFO]${NC} $*" ;;
        WARN)  echo -e "${YELLOW}[WARN]${NC} $*" ;;
        ERROR) echo -e "${RED}[ERROR]${NC} $*" ;;
        DEBUG) echo -e "${BLUE}[DEBUG]${NC} $*" ;;
    esac
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log ERROR "This script should not be run as root for security reasons!"
        log INFO "Please run as a regular user. Sudo will be used when needed."
        exit 1
    fi
}

# Detect OS
detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
    else
        log ERROR "Cannot detect OS. This script supports Ubuntu, Debian, Kali, Fedora, CentOS."
        exit 1
    fi
    
    log INFO "Detected OS: $OS $VERSION"
}

# Check system architecture
check_architecture() {
    ARCH=$(uname -m)
    case $ARCH in
        x86_64|amd64) log INFO "Architecture: $ARCH (64-bit) ✓" ;;
        i386|i686)    log WARN "Architecture: $ARCH (32-bit) - Limited support" ;;
        armv7l|arm64) log INFO "Architecture: $ARCH (ARM) - Experimental support" ;;
        *) log ERROR "Unsupported architecture: $ARCH"; exit 1 ;;
    esac
}

# Check Python version
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        log INFO "Python $PYTHON_VERSION found"
        
        # Check if Python version is >= 3.7
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
            log INFO "Python version check: ✓"
        else
            log ERROR "Python 3.7+ required. Current: $PYTHON_VERSION"
            exit 1
        fi
    else
        log ERROR "Python3 not found. Installing..."
        install_python
    fi
}

# Install Python based on OS
install_python() {
    case $OS in
        ubuntu|debian|kali)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-dev python3-venv python3-tk
            ;;
        fedora|centos|rhel)
            sudo dnf install -y python3 python3-pip python3-devel python3-tkinter
            ;;
        *) log ERROR "Unsupported OS for automatic Python installation"; exit 1 ;;
    esac
}

# Install system dependencies
install_dependencies() {
    log INFO "Installing system dependencies..."
    
    case $OS in
        ubuntu|debian)
            log INFO "Installing dependencies for Ubuntu/Debian..."
            sudo apt update
            sudo apt install -y \
                git curl wget unzip \
                build-essential \
                openjdk-11-jdk openjdk-11-jre-headless \
                python3 python3-pip python3-dev python3-venv python3-tk \
                apktool zipalign \
                postgresql postgresql-contrib \
                nmap \
                ruby ruby-dev \
                libpq-dev \
                libssl-dev \
                libffi-dev \
                libbz2-dev \
                libreadline-dev \
                libsqlite3-dev \
                libncurses5-dev \
                libncursesw5-dev \
                xz-utils \
                tk-dev
            ;;
            
        kali)
            log INFO "Installing dependencies for Kali Linux..."
            sudo apt update
            sudo apt install -y \
                git curl wget unzip \
                build-essential \
                openjdk-11-jdk \
                python3 python3-pip python3-dev python3-venv python3-tk \
                apktool zipalign \
                metasploit-framework \
                postgresql \
                nmap \
                ruby ruby-dev \
                libpq-dev \
                libssl-dev \
                libffi-dev
            ;;
            
        fedora)
            log INFO "Installing dependencies for Fedora..."
            sudo dnf update -y
            sudo dnf install -y \
                git curl wget unzip \
                gcc gcc-c++ make \
                java-11-openjdk java-11-openjdk-devel \
                python3 python3-pip python3-devel python3-tkinter \
                postgresql postgresql-server \
                nmap \
                ruby ruby-devel \
                openssl-devel \
                libffi-devel \
                bzip2-devel \
                readline-devel \
                sqlite-devel \
                ncurses-devel
            ;;
            
        centos|rhel)
            log INFO "Installing dependencies for CentOS/RHEL..."
            sudo yum update -y
            sudo yum install -y epel-release
            sudo yum install -y \
                git curl wget unzip \
                gcc gcc-c++ make \
                java-11-openjdk java-11-openjdk-devel \
                python3 python3-pip python3-devel python3-tkinter \
                postgresql postgresql-server \
                nmap \
                ruby ruby-devel \
                openssl-devel \
                libffi-devel
            ;;
            
        *) log ERROR "Unsupported OS: $OS"; exit 1 ;;
    esac
    
    log INFO "System dependencies installed ✓"
}

# Install Metasploit Framework
install_metasploit() {
    if command -v msfconsole &> /dev/null; then
        log INFO "Metasploit Framework already installed ✓"
        return
    fi
    
    log INFO "Installing Metasploit Framework..."
    
    if [[ $OS == "kali" ]]; then
        log INFO "Metasploit should be pre-installed on Kali"
        sudo apt install -y metasploit-framework
    else
        # Install Metasploit using the official installer
        log INFO "Downloading Metasploit installer..."
        curl -fsSL https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > /tmp/msfinstall
        chmod 755 /tmp/msfinstall
        
        log INFO "Running Metasploit installer (this may take a while)..."
        sudo /tmp/msfinstall
    fi
    
    # Initialize Metasploit database
    log INFO "Initializing Metasploit database..."
    sudo msfdb init
    
    log INFO "Metasploit Framework installed ✓"
}

# Install Android tools
install_android_tools() {
    log INFO "Installing Android development tools..."
    
    # Check if apktool is already installed
    if command -v apktool &> /dev/null; then
        log INFO "apktool already installed ✓"
    else
        case $OS in
            ubuntu|debian|kali)
                sudo apt install -y apktool zipalign
                ;;
            fedora|centos|rhel)
                # Manual installation for Fedora/CentOS
                log INFO "Installing apktool manually..."
                APKTOOL_VERSION="2.7.0"
                wget -q "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool" -O /tmp/apktool
                wget -q "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_${APKTOOL_VERSION}.jar" -O /tmp/apktool.jar
                sudo cp /tmp/apktool.jar /usr/local/bin/
                sudo cp /tmp/apktool /usr/local/bin/
                sudo chmod +x /usr/local/bin/apktool
                sudo ln -sf /usr/local/bin/apktool /usr/bin/apktool 2>/dev/null || true
                ;;
        esac
    fi
    
    # Verify Java tools are available
    if command -v keytool &> /dev/null && command -v jarsigner &> /dev/null; then
        log INFO "Java signing tools available ✓"
    else
        log ERROR "Java development tools not properly installed"
        exit 1
    fi
    
    log INFO "Android tools installed ✓"
}

# Clone repository
clone_repository() {
    local repo_dir="$HOME/i-see-u"
    
    if [[ -d "$repo_dir" ]]; then
        log WARN "Repository directory already exists"
        read -p "Do you want to update it? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log INFO "Updating repository..."
            cd "$repo_dir"
            git pull origin main
        else
            log INFO "Using existing repository"
        fi
    else
        log INFO "Cloning I See U Toolkit repository..."
        git clone https://github.com/kishwordulal1234/i-see-u.git "$repo_dir"
    fi
    
    cd "$repo_dir"
    chmod +x *.py
    
    export ISEEU_HOME="$repo_dir"
    log INFO "Repository cloned to: $repo_dir"
}

# Install Python dependencies
install_python_dependencies() {
    log INFO "Installing Python dependencies..."
    
    if [[ -f requirements.txt ]]; then
        # Create virtual environment
        log INFO "Creating Python virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        
        # Upgrade pip
        pip install --upgrade pip setuptools wheel
        
        # Install requirements
        pip install -r requirements.txt
        
        log INFO "Python dependencies installed ✓"
    else
        log WARN "requirements.txt not found, installing common dependencies..."
        pip3 install --user colorama requests psutil tkinter
    fi
}

# Create desktop shortcuts
create_shortcuts() {
    local desktop_dir="$HOME/Desktop"
    local applications_dir="$HOME/.local/share/applications"
    
    if [[ ! -d "$desktop_dir" ]]; then
        return
    fi
    
    log INFO "Creating desktop shortcuts..."
    
    # CLI version shortcut
    cat > "$desktop_dir/ISeeu-CLI.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=I See U Toolkit (CLI)
Comment=Advanced Payload Generation Tool - CLI Version
Exec=gnome-terminal -- bash -c "cd '$ISEEU_HOME' && python3 iseeu_toolkit.py; exec bash"
Icon=terminal
Terminal=false
Categories=Security;Network;
EOF
    
    # Modern GUI shortcut
    if [[ -f "$ISEEU_HOME/iseeu-morden-gui.py" ]]; then
        cat > "$desktop_dir/ISeeu-Modern-GUI.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=I See U Toolkit (Modern GUI)
Comment=Advanced Payload Generation Tool - Modern Interface
Exec=python3 '$ISEEU_HOME/iseeu-morden-gui.py'
Icon=applications-security
Terminal=false
Categories=Security;Network;
EOF
    fi
    
    # XP Style GUI shortcut
    if [[ -f "$ISEEU_HOME/iseeu-xp-version.py" ]]; then
        cat > "$desktop_dir/ISeeu-XP-GUI.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=I See U Toolkit (XP Style)
Comment=Advanced Payload Generation Tool - XP Style Interface
Exec=python3 '$ISEEU_HOME/iseeu-xp-version.py'
Icon=applications-security
Terminal=false
Categories=Security;Network;
EOF
    fi
    
    # Make shortcuts executable
    chmod +x "$desktop_dir"/*.desktop
    
    # Copy to applications directory
    mkdir -p "$applications_dir"
    cp "$desktop_dir"/ISeeu-*.desktop "$applications_dir/" 2>/dev/null || true
    
    log INFO "Desktop shortcuts created ✓"
}

# Setup environment variables
setup_environment() {
    local bashrc="$HOME/.bashrc"
    local profile="$HOME/.profile"
    
    log INFO "Setting up environment variables..."
    
    # Add ISEEU_HOME to bashrc if not already present
    if ! grep -q "ISEEU_HOME" "$bashrc" 2>/dev/null; then
        echo "" >> "$bashrc"
        echo "# I See U Toolkit Environment" >> "$bashrc"
        echo "export ISEEU_HOME=\"$ISEEU_HOME\"" >> "$bashrc"
        echo "export PATH=\"\$PATH:\$ISEEU_HOME\"" >> "$bashrc"
        echo "alias iseeu='cd \$ISEEU_HOME && python3 iseeu_toolkit.py'" >> "$bashrc"
        echo "alias iseeu-modern='cd \$ISEEU_HOME && python3 iseeu-morden-gui.py'" >> "$bashrc"
        echo "alias iseeu-xp='cd \$ISEEU_HOME && python3 iseeu-xp-version.py'" >> "$bashrc"
    fi
    
    # Set Java environment if needed
    if [[ -z "$JAVA_HOME" ]]; then
        JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::")
        echo "export JAVA_HOME=\"$JAVA_HOME\"" >> "$bashrc"
    fi
    
    log INFO "Environment variables configured ✓"
}

# Post-installation configuration
post_install_config() {
    log INFO "Running post-installation configuration..."
    
    # Create config directory
    mkdir -p "$ISEEU_HOME/configs"
    mkdir -p "$ISEEU_HOME/payloads"
    mkdir -p "$ISEEU_HOME/logs"
    
    # Create default configuration
    cat > "$ISEEU_HOME/configs/default.json" << EOF
{
    "lhost": "127.0.0.1",
    "lport": 4444,
    "encoder": "x86/shikata_ga_nai",
    "iterations": 3,
    "format": "exe",
    "platform": "windows",
    "android_target": 11,
    "stealth_mode": false,
    "auto_listener": true,
    "output_dir": "$ISEEU_HOME/payloads",
    "log_level": "INFO"
}
EOF
    
    # Create Kali-optimized config
    cat > "$ISEEU_HOME/configs/kali.json" << EOF
{
    "lhost": "eth0",
    "lport": 4444,
    "encoder": "x64/xor_dynamic",
    "iterations": 5,
    "format": "elf",
    "platform": "linux",
    "android_target": 10,
    "stealth_mode": true,
    "auto_listener": true,
    "output_dir": "$ISEEU_HOME/payloads",
    "log_level": "DEBUG"
}
EOF
    
    # Set proper permissions
    chmod 755 "$ISEEU_HOME"/*.py
    chmod 644 "$ISEEU_HOME"/configs/*.json
    
    log INFO "Post-installation configuration complete ✓"
}

# System verification
verify_installation() {
    log INFO "Verifying installation..."
    
    local errors=0
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log ERROR "Python3 not found"
        ((errors++))
    fi
    
    # Check Java
    if ! command -v java &> /dev/null || ! command -v javac &> /dev/null; then
        log ERROR "Java development kit not properly installed"
        ((errors++))
    fi
    
    # Check Metasploit
    if ! command -v msfconsole &> /dev/null; then
        log ERROR "Metasploit Framework not found"
        ((errors++))
    fi
    
    # Check Android tools
    if ! command -v apktool &> /dev/null; then
        log ERROR "apktool not found"
        ((errors++))
    fi
    
    # Check repository files
    local required_files=("iseeu_toolkit.py")
    for file in "${required_files[@]}"; do
        if [[ ! -f "$ISEEU_HOME/$file" ]]; then
            log ERROR "Required file not found: $file"
            ((errors++))
        fi
    done
    
    if [[ $errors -eq 0 ]]; then
        log INFO "Installation verification passed ✓"
        return 0
    else
        log ERROR "Installation verification failed with $errors errors"
        return 1
    fi
}

# Quick system test
run_quick_test() {
    log INFO "Running quick system test..."
    
    cd "$ISEEU_HOME"
    
    # Test Python imports
    if python3 -c "import sys, os, json, subprocess, threading, time" 2>/dev/null; then
        log INFO "Python imports: ✓"
    else
        log ERROR "Python imports: ✗"
        return 1
    fi
    
    # Test Java
    if java -version &>/dev/null && javac -version &>/dev/null; then
        log INFO "Java tools: ✓"
    else
        log ERROR "Java tools: ✗"
        return 1
    fi
    
    # Test Metasploit database
    if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw msf; then
        log INFO "Metasploit database: ✓"
    else
        log WARN "Metasploit database: ⚠ (may need initialization)"
    fi
    
    # Test apktool
    if apktool --version &>/dev/null; then
        log INFO "APKTool: ✓"
    else
        log ERROR "APKTool: ✗"
        return 1
    fi
    
    log INFO "Quick system test completed ✓"
    return 0
}

# Interactive installation menu
installation_menu() {
    log INFO "Choose installation type:"
    echo ""
    echo -e "${GREEN}1)${NC} Full Installation (Recommended) - All components"
    echo -e "${GREEN}2)${NC} Minimal Installation - Core components only"
    echo -e "${GREEN}3)${NC} Developer Installation - Includes development tools"
    echo -e "${GREEN}4)${NC} Custom Installation - Choose components"
    echo -e "${GREEN}5)${NC} Repair/Update Installation"
    echo ""
    read -p "Enter your choice [1-5]: " choice
    
    case $choice in
        1) full_installation ;;
        2) minimal_installation ;;
        3) developer_installation ;;
        4) custom_installation ;;
        5) repair_installation ;;
        *) log ERROR "Invalid choice"; exit 1 ;;
    esac
}

# Full installation
full_installation() {
    log INFO "Starting full installation..."
    install_dependencies
    install_metasploit
    install_android_tools
    clone_repository
    install_python_dependencies
    create_shortcuts
    setup_environment
    post_install_config
    verify_installation
    run_quick_test
    show_completion_message
}

# Minimal installation
minimal_installation() {
    log INFO "Starting minimal installation..."
    install_python
    
    # Install only essential dependencies
    case $OS in
        ubuntu|debian|kali)
            sudo apt install -y git python3-pip openjdk-11-jdk apktool
            ;;
        fedora|centos|rhel)
            sudo dnf install -y git python3-pip java-11-openjdk
            ;;
    esac
    
    clone_repository
    install_python_dependencies
    setup_environment
    post_install_config
    log INFO "Minimal installation completed"
}

# Developer installation
developer_installation() {
    log INFO "Starting developer installation..."
    full_installation
    
    # Additional developer tools
    log INFO "Installing development dependencies..."
    pip3 install --user pytest black flake8 mypy sphinx
    
    # Setup pre-commit hooks
    if command -v pre-commit &> /dev/null; then
        cd "$ISEEU_HOME"
        pre-commit install
    fi
    
    log INFO "Developer installation completed"
}

# Custom installation
custom_installation() {
    log INFO "Custom installation options:"
    
    read -p "Install Metasploit Framework? [Y/n]: " install_msf
    read -p "Install Android tools? [Y/n]: " install_android
    read -p "Create desktop shortcuts? [Y/n]: " create_desktop
    read -p "Install GUI dependencies? [Y/n]: " install_gui
    
    install_dependencies
    
    if [[ ! $install_msf =~ ^[Nn]$ ]]; then
        install_metasploit
    fi
    
    if [[ ! $install_android =~ ^[Nn]$ ]]; then
        install_android_tools
    fi
    
    clone_repository
    install_python_dependencies
    
    if [[ ! $install_gui =~ ^[Nn]$ ]]; then
        case $OS in
            ubuntu|debian|kali)
                sudo apt install -y python3-tk
                ;;
            fedora|centos|rhel)
                sudo dnf install -y python3-tkinter
                ;;
        esac
    fi
    
    if [[ ! $create_desktop =~ ^[Nn]$ ]]; then
        create_shortcuts
    fi
    
    setup_environment
    post_install_config
    verify_installation
    log INFO "Custom installation completed"
}

# Repair/update installation
repair_installation() {
    log INFO "Repairing/updating installation..."
    
    if [[ -d "$HOME/i-see-u" ]]; then
        cd "$HOME/i-see-u"
        git pull origin main
        pip3 install --upgrade -r requirements.txt
        chmod +x *.py
        post_install_config
        verify_installation
        log INFO "Installation repaired/updated ✓"
    else
        log ERROR "I See U installation not found. Run full installation instead."
        exit 1
    fi
}

# Show completion message
show_completion_message() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    INSTALLATION COMPLETE!                   ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${WHITE}📍 Installation Directory:${NC} $ISEEU_HOME"
    echo ""
    echo -e "${WHITE}🚀 Quick Start Commands:${NC}"
    echo -e "   ${CYAN}iseeu${NC}        - Launch CLI version"
    echo -e "   ${CYAN}iseeu-modern${NC}  - Launch modern GUI"
    echo -e "   ${CYAN}iseeu-xp${NC}      - Launch XP-style GUI"
    echo ""
    echo -e "${WHITE}📚 Usage Examples:${NC}"
    echo -e "   ${YELLOW}cd \$ISEEU_HOME && python3 iseeu_toolkit.py${NC}"
    echo -e "   ${YELLOW}python3 iseeu-morden-gui.py${NC}"
    echo ""
    echo -e "${WHITE}⚠️  Important Notes:${NC}"
    echo -e "   • Restart your terminal or run: ${CYAN}source ~/.bashrc${NC}"
    echo -e "   • For Metasploit issues, run: ${CYAN}sudo msfdb init${NC}"
    echo -e "   • Check logs in: ${CYAN}\$ISEEU_HOME/logs/${NC}"
    echo ""
    echo -e "${RED}⚖️  Legal Reminder:${NC} Use only for authorized testing!"
    echo ""
}

# Cleanup on error
cleanup() {
    log ERROR "Installation failed or interrupted"
    log INFO "Cleaning up temporary files..."
    rm -f /tmp/msfinstall /tmp/apktool /tmp/apktool.jar
    exit 1
}

# Main installation function
main() {
    # Set trap for cleanup
    trap cleanup ERR INT TERM
    
    print_banner
    
    # Check if we should run automated installation
    if [[ "$1" == "--auto" ]] || [[ "$1" == "--full" ]]; then
        log INFO "Running automated full installation..."
        check_root
        detect_os
        check_architecture
        check_python
        full_installation
        exit 0
    fi
    
    # Interactive installation
    check_root
    detect_os
    check_architecture
    check_python
    
    echo -e "${WHITE}Welcome to I See U Toolkit Installer!${NC}"
    echo ""
    echo -e "${YELLOW}This installer will set up:${NC}"
    echo "• Python dependencies and virtual environment"
    echo "• Metasploit Framework (if not present)"
    echo "• Android development tools (apktool, zipalign)"
    echo "• Java Development Kit"
    echo "• Desktop shortcuts and environment setup"
    echo ""
    
    read -p "Continue with installation? [Y/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        log INFO "Installation cancelled by user"
        exit 0
    fi
    
    installation_menu
}

# Run main function
main "$@"
