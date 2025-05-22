# Auto SSH Login CLI Interface

This Python script provides an automated SSH login interface that supports both username/password and SSH private key authentication. It captures specific prompt characters and executes corresponding commands automatically.

## Features

- Supports both password and SSH key-based authentication
- Automatically detects prompt characters ('>' and '#')
- Executes specific commands based on detected prompts:
  - Sends 'show version' when '>' is detected
  - Sends 'uname -a' when '#' is detected
- Interactive mode for manual command input
- Timeout handling for connections and commands
- Proper error handling and user feedback

## Requirements

- Python 3.6+
- Paramiko library

## Installation

1. Ensure you have Python 3.6 or higher installed
2. Install the required dependencies:

```bash
pip install paramiko
```

## Usage

```bash
python auto_ssh.py --host HOST [--port PORT] [--username USERNAME] 
                  [--password PASSWORD] [--key KEY_FILE]
                  [--timeout TIMEOUT]
```

### Arguments

- `--host`: Target host to connect to (required)
- `--port`: SSH port (default: 22)
- `--username`: SSH username (required)
- `--password`: SSH password (required if --key is not provided)
- `--key`: Path to SSH private key file (required if --password is not provided)
- `--timeout`: Connection timeout in seconds (default: 10)

### Examples

Connect using username and password:
```bash
python auto_ssh.py --host 192.168.1.1 --username admin --password secret
```

Connect using SSH key:
```bash
python auto_ssh.py --host 192.168.1.1 --username admin --key ~/.ssh/id_rsa
```

## How It Works

1. The script establishes an SSH connection to the specified host using the provided credentials
2. It opens an interactive shell channel
3. The script continuously reads output from the shell
4. When it detects a prompt character:
   - If '>' is detected, it automatically sends 'show version'
   - If '#' is detected, it automatically sends 'uname -a'
5. If no recognized prompt is detected, it allows manual command input
6. The session continues until the user types 'exit' or presses Ctrl+C

## Customization

You can modify the prompt detection and corresponding commands by editing the `prompt_actions` dictionary in the `AutoSSHClient` class:

```python
self.prompt_actions = {
    '>': 'show version',
    '#': 'uname -a',
    '$': 'ls -la'  # Example of adding a new prompt character
}
```

## Error Handling

The script includes comprehensive error handling for:
- Authentication failures
- Connection issues
- Timeout scenarios
- Key file errors
- General exceptions

## License

This script is provided as-is under the MIT License.

