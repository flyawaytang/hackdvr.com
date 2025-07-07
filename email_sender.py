#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python 3 Email Sender with Authentication and Attachment Support
"""

import os
import smtplib
import argparse
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pathlib import Path
import getpass
import sys

class EmailSender:
    """
    A class to handle email sending with authentication and attachments
    """
    
    def __init__(self, smtp_server, smtp_port, use_ssl=True):
        """
        Initialize the EmailSender with SMTP server details
        
        Args:
            smtp_server (str): SMTP server address (e.g., smtp.gmail.com)
            smtp_port (int): SMTP server port (e.g., 465 for SSL, 587 for TLS)
            use_ssl (bool): Whether to use SSL connection (True) or TLS (False)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.use_ssl = use_ssl
        self.server = None
        self.is_authenticated = False
    
    def authenticate(self, username, password):
        """
        Authenticate with the SMTP server
        
        Args:
            username (str): Email username/address
            password (str): Email password or app password
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Create the appropriate server connection based on SSL/TLS
            if self.use_ssl:
                self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                self.server.starttls()  # Upgrade to secure connection
            
            # Login to the server
            self.server.login(username, password)
            self.username = username
            self.is_authenticated = True
            print(f"Successfully authenticated as {username}")
            return True
            
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            self.is_authenticated = False
            return False
    
    def create_message(self, to_addresses, subject, body, cc_addresses=None, 
                      bcc_addresses=None, attachments=None, html_body=False):
        """
        Create an email message with optional attachments
        
        Args:
            to_addresses (str or list): Recipient email address(es)
            subject (str): Email subject
            body (str): Email body content
            cc_addresses (str or list, optional): CC recipient(s)
            bcc_addresses (str or list, optional): BCC recipient(s)
            attachments (str or list, optional): Path(s) to attachment file(s)
            html_body (bool, optional): Whether the body is HTML (default: False)
            
        Returns:
            MIMEMultipart: The constructed email message
        """
        if not self.is_authenticated:
            raise ValueError("You must authenticate before creating a message")
        
        # Convert single addresses to lists for consistent handling
        if isinstance(to_addresses, str):
            to_addresses = [to_addresses]
        if isinstance(cc_addresses, str):
            cc_addresses = [cc_addresses]
        if isinstance(bcc_addresses, str):
            bcc_addresses = [bcc_addresses]
        if isinstance(attachments, str):
            attachments = [attachments]
            
        # Create message container
        message = MIMEMultipart()
        message['From'] = self.username
        message['To'] = ', '.join(to_addresses) if to_addresses else ''
        message['Subject'] = Header(subject, 'utf-8')
        
        # Add CC if provided
        if cc_addresses:
            message['Cc'] = ', '.join(cc_addresses)
            
        # Add body
        if html_body:
            message.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            
        # Add attachments if provided
        if attachments:
            for attachment_path in attachments:
                try:
                    # Check if file exists
                    if not os.path.isfile(attachment_path):
                        print(f"Warning: Attachment not found: {attachment_path}")
                        continue
                        
                    # Get filename from path
                    filename = os.path.basename(attachment_path)
                    
                    # Create attachment
                    attachment = MIMEBase('application', 'octet-stream')
                    
                    # Read file in binary mode
                    with open(attachment_path, 'rb') as file:
                        attachment.set_payload(file.read())
                    
                    # Encode in base64
                    encoders.encode_base64(attachment)
                    
                    # Add header
                    attachment.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{filename}"'
                    )
                    
                    # Add attachment to message
                    message.attach(attachment)
                    print(f"Attached: {filename}")
                    
                except Exception as e:
                    print(f"Failed to attach {attachment_path}: {str(e)}")
        
        return message
    
    def send_email(self, message, bcc_addresses=None):
        """
        Send the email message
        
        Args:
            message (MIMEMultipart): The email message to send
            bcc_addresses (list, optional): BCC recipients
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.is_authenticated or not self.server:
            raise ValueError("You must authenticate before sending an email")
        
        try:
            # Get all recipients
            recipients = []
            
            # Add To recipients
            if message['To']:
                recipients.extend(message['To'].split(', '))
                
            # Add Cc recipients
            if message.get('Cc'):
                recipients.extend(message['Cc'].split(', '))
                
            # Add Bcc recipients
            if bcc_addresses:
                if isinstance(bcc_addresses, str):
                    recipients.append(bcc_addresses)
                else:
                    recipients.extend(bcc_addresses)
            
            # Send the email
            self.server.sendmail(
                self.username,
                recipients,
                message.as_string()
            )
            
            print(f"Email sent successfully to {len(recipients)} recipient(s)")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def close(self):
        """Close the SMTP connection"""
        if self.server:
            self.server.quit()
            print("SMTP connection closed")


def main():
    """Command line interface for the email sender"""
    parser = argparse.ArgumentParser(description='Send emails with authentication and attachments')
    
    # Server settings
    parser.add_argument('--server', required=True, help='SMTP server address (e.g., smtp.gmail.com)')
    parser.add_argument('--port', type=int, required=True, help='SMTP server port (e.g., 465 for SSL, 587 for TLS)')
    parser.add_argument('--use-tls', action='store_true', help='Use TLS instead of SSL')
    
    # Authentication
    parser.add_argument('--username', help='Email username/address')
    
    # Email content
    parser.add_argument('--to', required=True, help='Recipient email address(es), comma-separated')
    parser.add_argument('--cc', help='CC recipient(s), comma-separated')
    parser.add_argument('--bcc', help='BCC recipient(s), comma-separated')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', help='Email body content')
    parser.add_argument('--body-file', help='File containing email body content')
    parser.add_argument('--html', action='store_true', help='Body is HTML content')
    
    # Attachments
    parser.add_argument('--attach', action='append', help='Path to attachment file (can be used multiple times)')
    
    args = parser.parse_args()
    
    # Get email body from file or argument
    body = ""
    if args.body_file:
        try:
            with open(args.body_file, 'r', encoding='utf-8') as f:
                body = f.read()
        except Exception as e:
            print(f"Error reading body file: {str(e)}")
            return 1
    elif args.body:
        body = args.body
    else:
        print("Email body must be provided either with --body or --body-file")
        return 1
    
    # Get username if not provided
    username = args.username
    if not username:
        username = input("Email username/address: ")
    
    # Get password securely
    password = getpass.getpass("Email password: ")
    
    # Parse recipient lists
    to_list = [addr.strip() for addr in args.to.split(',')]
    cc_list = [addr.strip() for addr in args.cc.split(',')] if args.cc else None
    bcc_list = [addr.strip() for addr in args.bcc.split(',')] if args.bcc else None
    
    # Create email sender
    sender = EmailSender(args.server, args.port, not args.use_tls)
    
    # Authenticate
    if not sender.authenticate(username, password):
        return 1
    
    # Create and send message
    try:
        message = sender.create_message(
            to_list, 
            args.subject, 
            body, 
            cc_list, 
            None,  # BCC is handled separately
            args.attach, 
            args.html
        )
        
        if not sender.send_email(message, bcc_list):
            return 1
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    finally:
        sender.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

