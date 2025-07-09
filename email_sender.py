#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Email Sender - A simple tool for sending emails with attachments

This module provides a class for sending emails with attachments using SMTP.
It supports both SSL and TLS encryption, as well as port 25 for standard SMTP.
"""

import argparse
import getpass
import os
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

# Import compression utilities if available
try:
    from compression_utils import create_archive
    COMPRESSION_AVAILABLE = True
except ImportError:
    COMPRESSION_AVAILABLE = False

class EmailSender:
    """A class for sending emails with attachments using SMTP"""

    def __init__(self, smtp_server, smtp_port, use_ssl=True):
        """
        Initialize the EmailSender with server details

        Args:
            smtp_server (str): SMTP server address
            smtp_port (int): SMTP server port
            use_ssl (bool, optional): Whether to use SSL encryption. Defaults to True.
                If False and port is 25 or 587, will attempt to use STARTTLS.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.use_ssl = use_ssl
        self.server = None
        self.username = None
        self.is_authenticated = False
        
    def connect(self, require_auth=True):
        """
        Connect to the SMTP server without authentication
        
        Args:
            require_auth (bool): Whether authentication is required
            
        Returns:
            bool: True if connection was successful, False otherwise
        """
        try:
            # Create the appropriate server connection
            if self.use_ssl:
                self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                # For non-SSL connections (like port 25 or 587)
                self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                
                # Try to use STARTTLS if available (for security)
                if self.smtp_port in [25, 587]:
                    try:
                        self.server.starttls()
                        print("STARTTLS encryption enabled")
                    except smtplib.SMTPNotSupportedError:
                        print("Warning: STARTTLS not supported by server. Connection is not encrypted.")
                    except Exception as e:
                        print(f"Warning: Failed to enable STARTTLS: {str(e)}")
            
            # If authentication is not required, mark as authenticated
            if not require_auth:
                self.is_authenticated = True
                print("Connected to SMTP server without authentication")
                return True
                
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False

    def authenticate(self, username, password):
        """
        Authenticate with the SMTP server

        Args:
            username (str): Email address or username
            password (str): Password or app password

        Returns:
            bool: True if authentication was successful, False otherwise
        """
        try:
            # Connect to the server first
            if not self.server and not self.connect():
                return False
            
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
                      bcc_addresses=None, attachments=None, is_html=False,
                      compress_attachments=None):
        """
        Create an email message with optional attachments
        
        Args:
            to_addresses (str or list): Recipient email address(es)
            subject (str): Email subject
            body (str): Email body content
            cc_addresses (str or list, optional): CC recipient(s)
            bcc_addresses (str or list, optional): BCC recipient(s)
            attachments (str or list, optional): Path(s) to attachment file(s)
            is_html (bool, optional): Whether body is HTML content
            compress_attachments (dict, optional): Options for compressing attachments
                Format: {
                    'archive_type': 'zip'|'tar'|'tar.gz'|'tar.bz2',
                    'archive_name': 'filename.zip',  # Optional, default is 'attachments.{ext}'
                    'compression_level': 6,  # Optional, for zip only (0-9)
                }
            
        Returns:
            MIMEMultipart: The created email message object
        """
        if not self.is_authenticated:
            raise ValueError("You must authenticate before creating a message")
        
        # Convert single addresses to lists
        if isinstance(to_addresses, str):
            to_addresses = [to_addresses]
        if cc_addresses and isinstance(cc_addresses, str):
            cc_addresses = [cc_addresses]
        if bcc_addresses and isinstance(bcc_addresses, str):
            bcc_addresses = [bcc_addresses]
        if attachments and isinstance(attachments, str):
            attachments = [attachments]
        
        # Create message container
        message = MIMEMultipart()
        
        # Set From header - handle case when username is None (no-auth mode)
        if self.username:
            message['From'] = formataddr((str(Header(self.username, 'utf-8')), self.username))
        else:
            # Use a generic sender name when username is not available
            message['From'] = formataddr((str(Header('Email Sender', 'utf-8')), 'noreply@localhost'))
            
        message['To'] = ', '.join(to_addresses)
        message['Subject'] = Header(subject, 'utf-8')
        
        # Add CC if provided
        if cc_addresses:
            message['Cc'] = ', '.join(cc_addresses)
            
        # Add body
        if is_html:
            message.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            message.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Handle attachments
        if attachments:
            # Check if compression is requested and available
            if compress_attachments and COMPRESSION_AVAILABLE:
                try:
                    # Set default archive name if not provided
                    archive_name = compress_attachments.get('archive_name')
                    if not archive_name:
                        ext = compress_attachments['archive_type']
                        archive_name = f"attachments.{ext}"
                    
                    # Create temporary archive
                    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
                    os.makedirs(temp_dir, exist_ok=True)
                    archive_path = os.path.join(temp_dir, archive_name)
                    
                    # Create the archive
                    archive_path = create_archive(
                        attachments,
                        archive_path,
                        compress_attachments.get('archive_type', 'zip'),
                        compress_attachments.get('compression_level', 6)
                    )
                    
                    # Add the archive as a single attachment
                    self._add_attachment_to_message(message, archive_path)
                    print(f"Added compressed archive: {archive_name}")
                    
                except Exception as e:
                    print(f"Error compressing attachments: {str(e)}")
                    print("Falling back to individual attachments")
                    for attachment_path in attachments:
                        self._add_attachment_to_message(message, attachment_path)
            else:
                # Add attachments individually
                for attachment_path in attachments:
                    self._add_attachment_to_message(message, attachment_path)
        
        return message
    
    def _add_attachment_to_message(self, message, attachment_path):
        """
        Add a single attachment to the message
        
        Args:
            message (MIMEMultipart): The email message
            attachment_path (str): Path to the attachment file
        """
        try:
            # Check if file exists
            if not os.path.isfile(attachment_path):
                print(f"Warning: Attachment file not found: {attachment_path}")
                return
            
            # Get filename from path
            filename = os.path.basename(attachment_path)
            
            # Open file in binary mode
            with open(attachment_path, 'rb') as attachment_file:
                # Create MIME attachment part
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
            
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)
            
            # Add header as key/value pair to attachment part
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"',
            )
            
            # Add attachment to message
            message.attach(part)
            print(f"Added attachment: {filename}")
            
        except Exception as e:
            print(f"Error adding attachment {attachment_path}: {str(e)}")
    
    def send_email(self, message, bcc_addresses=None):
        """
        Send the email message
        
        Args:
            message (MIMEMultipart): The email message to send
            bcc_addresses (list, optional): BCC recipient(s)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not self.is_authenticated:
            print("Error: You must authenticate before sending an email")
            return False
        
        try:
            # Get all recipients
            recipients = []
            
            # Add To recipients
            if 'To' in message:
                recipients.extend(message['To'].split(', '))
            
            # Add CC recipients
            if 'Cc' in message:
                recipients.extend(message['Cc'].split(', '))
            
            # Add BCC recipients
            if bcc_addresses:
                if isinstance(bcc_addresses, str):
                    bcc_addresses = [bcc_addresses]
                recipients.extend(bcc_addresses)
            
            # Get sender address
            from_addr = message['From']
            if '<' in from_addr:
                # Extract email from "Name <email>" format
                from_addr = from_addr.split('<')[1].split('>')[0]
            
            # Send the email
            self.server.sendmail(
                from_addr,
                recipients,
                message.as_string()
            )
            
            print(f"Email sent to: {', '.join(recipients)}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def close(self):
        """Close the SMTP connection"""
        if self.server:
            self.server.quit()
            print("SMTP connection closed")


def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='Send emails with attachments')
    parser.add_argument('--server', required=True, help='SMTP server address')
    parser.add_argument('--port', required=True, type=int, help='SMTP server port')
    parser.add_argument('--use-tls', action='store_true', help='Use TLS instead of SSL (for ports 25, 587)')
    parser.add_argument('--no-auth', action='store_true', help='Skip authentication (for servers that don\'t require it)')
    parser.add_argument('--username', help='Email username/address')
    parser.add_argument('--to', required=True, help='Recipient email address(es), comma separated')
    parser.add_argument('--cc', help='CC recipient(s), comma separated')
    parser.add_argument('--bcc', help='BCC recipient(s), comma separated')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', help='Email body text')
    parser.add_argument('--body-file', help='File containing email body')
    parser.add_argument('--html', action='store_true', help='Treat body as HTML')
    parser.add_argument('--attach', action='append', help='File to attach (can be used multiple times)')
    parser.add_argument('--compress', choices=['zip', 'tar', 'tar.gz', 'tar.bz2'], 
                        help='Compress attachments into a single archive')
    
    args = parser.parse_args()
    
    # Validate body arguments
    if not args.body and not args.body_file:
        parser.error("Either --body or --body-file must be provided")
    
    if args.body and args.body_file:
        parser.error("Cannot use both --body and --body-file")
    
    # Create the sender
    sender = EmailSender(args.server, args.port, not args.use_tls)
    
    # Handle authentication
    if args.no_auth:
        # Skip authentication
        if not sender.connect(require_auth=False):
            print("Failed to connect to SMTP server")
            sys.exit(1)
    else:
        # Get username if not provided
        username = args.username
        if not username:
            username = input("Email address: ")
        
        # Get password securely
        password = getpass.getpass("Password: ")
        
        # Authenticate
        if not sender.authenticate(username, password):
            sys.exit(1)
    
    # Get body content
    body = args.body
    if args.body_file:
        try:
            with open(args.body_file, 'r', encoding='utf-8') as f:
                body = f.read()
        except Exception as e:
            print(f"Error reading body file: {str(e)}")
            sys.exit(1)
    
    # Parse recipients
    to_list = [addr.strip() for addr in args.to.split(',') if addr.strip()]
    cc_list = []
    if args.cc:
        cc_list = [addr.strip() for addr in args.cc.split(',') if addr.strip()]
    bcc_list = []
    if args.bcc:
        bcc_list = [addr.strip() for addr in args.bcc.split(',') if addr.strip()]
    
    # Handle compression options
    compress_attachments = None
    if args.compress and args.attach:
        if not COMPRESSION_AVAILABLE:
            print("Warning: Compression requested but compression_utils module not available.")
            print("Attachments will be sent individually without compression.")
        else:
            compress_attachments = {
                'archive_type': args.compress,
                'archive_name': f"attachments.{args.compress}"
            }
    
    # Create message
    message = sender.create_message(
        to_addresses=to_list,
        cc_addresses=cc_list,
        bcc_addresses=bcc_list,
        subject=args.subject,
        body=body,
        is_html=args.html,
        attachments=args.attach,
        compress_attachments=compress_attachments
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()
    
    print("Email sent successfully!")

if __name__ == "__main__":
    main()

