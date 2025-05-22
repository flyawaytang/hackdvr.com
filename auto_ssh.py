#!/usr/bin/env python3
"""
Auto SSH Login CLI Interface

This script provides an automated SSH login interface that supports both
username/password and SSH private key authentication. It captures specific
prompt characters and executes corresponding commands.

Usage:
    python auto_ssh.py --host HOST [--port PORT] [--username USERNAME] 
                      [--password PASSWORD] [--key KEY_FILE]
                      [--timeout TIMEOUT]

Example:
    python auto_ssh.py --host 192.168.1.1 --username admin --password secret
    python auto_ssh.py --host 192.168.1.1 --username admin --key ~/.ssh/id_rsa
"""

import argparse
import os
import sys
import time
import socket
import paramiko
import re


class AutoSSHClient:
    def __init__(self, host, port=22, username=None, password=None, key_file=None, timeout=10):
        """
        Initialize the SSH client with connection parameters.
        
        Args:
            host (str): Target host to connect to
            port (int): SSH port (default: 22)
            username (str): SSH username
            password (str): SSH password (optional if key_file is provided)
            key_file (str): Path to SSH private key file (optional if password is provided)
            timeout (int): Connection timeout in seconds (default: 10)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file
        self.timeout = timeout
        self.client = None
        self.channel = None
        self.buffer_size = 1024
        self.prompt_actions = {
            '>': 'show version',
            '#': 'uname -a'
        }
        # Pagination prompts and the key to send to continue
        self.pagination_prompts = {
            '--More--': ' ',  # Space to continue
            'More': ' ',      # Space to continue
            '(y/n)': 'y',     # Yes to continue
            '(Y/n)': 'y',     # Yes to continue
            '(y/N)': 'y',     # Yes to continue
            '(Y/N)': 'y',     # Yes to continue
            'Press any key to continue': '\n',  # Enter to continue
            'Press Enter to continue': '\n',    # Enter to continue
            'q to quit': ' ',  # Space to continue, q would quit
            'Q to quit': ' ',  # Space to continue, Q would quit
        }
    
    def connect(self):
        """Establish SSH connection using either password or key-based authentication."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            connect_kwargs = {
                'hostname': self.host,
                'port': self.port,
                'username': self.username,
                'timeout': self.timeout,
            }
            
            # Use key file if provided
            if self.key_file:
                if os.path.exists(self.key_file):
                    try:
                        key = paramiko.RSAKey.from_private_key_file(self.key_file)
                        connect_kwargs['pkey'] = key
                    except paramiko.ssh_exception.PasswordRequiredException:
                        # If key is password protected, prompt for password
                        passphrase = input(f"Enter passphrase for key '{self.key_file}': ")
                        key = paramiko.RSAKey.from_private_key_file(self.key_file, password=passphrase)
                        connect_kwargs['pkey'] = key
                else:
                    print(f"Error: Key file '{self.key_file}' not found.")
                    return False
            # Use password if provided
            elif self.password:
                connect_kwargs['password'] = self.password
            else:
                print("Error: Either password or key file must be provided.")
                return False
            
            print(f"Connecting to {self.host}:{self.port}...")
            self.client.connect(**connect_kwargs)
            
            # Open an interactive shell channel
            self.channel = self.client.invoke_shell()
            self.channel.settimeout(self.timeout)
            
            print(f"Successfully connected to {self.host}")
            return True
            
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as e:
            print(f"SSH error: {str(e)}")
        except socket.error as e:
            print(f"Connection error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        return False
    
    def check_for_pagination(self, output):
        """
        Check if the output contains pagination prompts.
        
        Args:
            output (str): The output text to check
            
        Returns:
            tuple: (is_paginated, key_to_send) where is_paginated is a boolean
                  indicating if pagination was detected and key_to_send is the
                  key to send to continue (or None)
        """
        for prompt, key in self.pagination_prompts.items():
            if prompt in output:
                return True, key
        return False, None
    
    def read_until_prompt(self, timeout=30, handle_pagination=True):
        """
        Read from the channel until a prompt character is detected or timeout.
        
        Args:
            timeout (int): Maximum time to wait for a prompt
            handle_pagination (bool): Whether to automatically handle pagination
            
        Returns:
            tuple: (output, prompt_char) where output is the text received and
                  prompt_char is the detected prompt character (or None)
        """
        start_time = time.time()
        output = ""
        prompt_char = None
        
        while (time.time() - start_time) < timeout:
            if self.channel.recv_ready():
                chunk = self.channel.recv(self.buffer_size).decode('utf-8', errors='ignore')
                output += chunk
                
                # Check for pagination prompts
                if handle_pagination:
                    is_paginated, key_to_send = self.check_for_pagination(output)
                    if is_paginated:
                        print(f"Pagination detected, sending '{key_to_send}' to continue...")
                        self.channel.send(key_to_send)
                        # Small delay to allow the device to process the pagination key
                        time.sleep(0.5)
                        continue
                
                # Check for command prompts
                for char in self.prompt_actions.keys():
                    if output.strip().endswith(char):
                        prompt_char = char
                        return output, prompt_char
            
            # Small delay to prevent CPU hogging
            time.sleep(0.1)
        
        return output, prompt_char
    
    def send_command(self, command, timeout=30, handle_pagination=True):
        """
        Send a command to the SSH channel and read the output.
        
        Args:
            command (str): Command to send
            timeout (int): Maximum time to wait for output
            handle_pagination (bool): Whether to automatically handle pagination
            
        Returns:
            str: The command output
        """
        if not self.channel:
            print("Error: Not connected. Please connect first.")
            return ""
        
        # Send the command
        self.channel.send(command + '\n')
        print(f"Sent command: {command}")
        
        # Read the output
        output, _ = self.read_until_prompt(timeout=timeout, handle_pagination=handle_pagination)
        return output
    
    def interact(self):
        """
        Main interaction loop that reads output and responds based on prompts.
        """
        if not self.channel:
            print("Error: Not connected. Please connect first.")
            return
        
        try:
            # Initial read to capture login banner and initial prompt
            output, prompt = self.read_until_prompt()
            print(output)
            
            # Continue interaction until user interrupts
            while True:
                if prompt in self.prompt_actions:
                    command = self.prompt_actions[prompt]
                    output = self.send_command(command)
                    print(output)
                    
                    # Get the next prompt
                    _, prompt = self.read_until_prompt(timeout=5, handle_pagination=False)
                else:
                    # If no recognized prompt is found, wait for user input
                    user_input = input("Command (or 'exit' to quit): ")
                    
                    if user_input.lower() in ('exit', 'quit'):
                        break
                    
                    output = self.send_command(user_input)
                    print(output)
                    
                    # Get the next prompt
                    _, prompt = self.read_until_prompt(timeout=5, handle_pagination=False)
        
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
        except Exception as e:
            print(f"Error during interaction: {str(e)}")
        finally:
            self.disconnect()
    
    def disconnect(self):
        """Close the SSH connection."""
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
        print(f"Disconnected from {self.host}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Auto SSH Login CLI Interface')
    parser.add_argument('--host', required=True, help='Target host to connect to')
    parser.add_argument('--port', type=int, default=22, help='SSH port (default: 22)')
    parser.add_argument('--username', required=True, help='SSH username')
    parser.add_argument('--password', help='SSH password (optional if key is provided)')
    parser.add_argument('--key', help='Path to SSH private key file (optional if password is provided)')
    parser.add_argument('--timeout', type=int, default=10, help='Connection timeout in seconds (default: 10)')
    parser.add_argument('--no-pagination', action='store_true', help='Disable automatic pagination handling')
    
    args = parser.parse_args()
    
    # Validate that either password or key is provided
    if not args.password and not args.key:
        parser.error("Either --password or --key must be provided")
    
    return args


def main():
    """Main function to run the auto SSH client."""
    args = parse_arguments()
    
    ssh_client = AutoSSHClient(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        key_file=args.key,
        timeout=args.timeout
    )
    
    if ssh_client.connect():
        ssh_client.interact()


if __name__ == "__main__":
    main()
