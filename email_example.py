#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example usage of the EmailSender class
"""

from email_sender import EmailSender

def gmail_example():
    """Example of sending email through Gmail"""
    # Create the sender with SSL
    sender = EmailSender('smtp.gmail.com', 465)
    
    # Authenticate - replace with your actual Gmail address and app password
    # For Gmail with 2FA, you need to use an app password
    username = 'your.email@gmail.com'
    password = 'your-app-password'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create a message
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='Test Email from Python',
        body='This is a test email sent from Python using the EmailSender class.',
        cc_addresses=['cc@example.com'],
        bcc_addresses=['bcc@example.com'],
        attachments=['./document.pdf'],
        is_html=False
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def qq_mail_example():
    """Example of sending email through QQ Mail"""
    # Create the sender with SSL
    sender = EmailSender('smtp.qq.com', 465)
    
    # Authenticate - replace with your actual QQ email and authorization code
    # You need to enable SMTP in QQ Mail settings and get an authorization code
    username = 'your-qq-number@qq.com'
    password = 'your-authorization-code'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create HTML content
    html_body = """
    <html>
    <head></head>
    <body>
        <h1>HTML Email Test</h1>
        <p>This is an <b>HTML</b> email sent from Python using the EmailSender class.</p>
        <p>It supports:</p>
        <ul>
            <li>Formatted text</li>
            <li>Links: <a href="https://www.example.com">Example</a></li>
            <li>And more...</li>
        </ul>
    </body>
    </html>
    """
    
    # Create a message with HTML content
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='HTML Email Test',
        body=html_body,
        is_html=True
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def multiple_attachments_example():
    """Example of sending email with multiple attachments"""
    # Create the sender with SSL
    sender = EmailSender('smtp.gmail.com', 465)
    
    # Authenticate
    username = 'your.email@gmail.com'
    password = 'your-app-password'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create a message with multiple attachments
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='Multiple Attachments Test',
        body='This email contains multiple attachments.',
        attachments=[
            './document1.pdf',
            './image.jpg',
            './spreadsheet.xlsx'
        ]
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def port25_example():
    """Example of sending email through port 25 with STARTTLS"""
    # Create the sender with port 25 and TLS
    sender = EmailSender('smtp.example.com', 25, use_ssl=False)
    
    # Authenticate
    username = 'your.email@example.com'
    password = 'your-password'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create a message
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='Port 25 Test with STARTTLS',
        body='This is a test email sent through port 25 with STARTTLS encryption.',
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def port25_no_auth_example():
    """Example of sending email through port 25 without authentication"""
    # Create the sender with port 25 and TLS
    sender = EmailSender('smtp.example.com', 25, use_ssl=False)
    
    # Connect without authentication
    if not sender.connect(require_auth=False):
        print("Connection failed. Exiting.")
        return
    
    # Create a message
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='Port 25 Test without Authentication',
        body='This is a test email sent through port 25 without authentication.',
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def command_line_examples():
    """Examples of command line usage"""
    print("Example 1: Send email with Gmail")
    print("python email_sender.py --server smtp.gmail.com --port 465 --username your.email@gmail.com "
          "--to recipient@example.com --subject 'Test Email' --body 'This is a test email.'")
    
    print("\nExample 2: Send email with HTML content")
    print("python email_sender.py --server smtp.gmail.com --port 465 --username your.email@gmail.com "
          "--to recipient@example.com --subject 'HTML Test' --body '<h1>Hello</h1><p>This is HTML.</p>' --html")
    
    print("\nExample 3: Send email with attachment")
    print("python email_sender.py --server smtp.gmail.com --port 465 --username your.email@gmail.com "
          "--to recipient@example.com --subject 'Attachment Test' --body 'See attachment.' "
          "--attach ./document.pdf --attach ./image.jpg")
    
    print("\nExample 4: Send email using port 25 with STARTTLS")
    print("python email_sender.py --server smtp.example.com --port 25 --use-tls "
          "--username your.email@example.com --to recipient@example.com "
          "--subject 'Port 25 Test' --body 'This is a test email via port 25.'")
    
    print("\nExample 5: Send email using port 25 without authentication")
    print("python email_sender.py --server smtp.example.com --port 25 --use-tls --no-auth "
          "--to recipient@example.com --subject 'No Auth Test' "
          "--body 'This is a test email without authentication.'")

if __name__ == "__main__":
    # Uncomment the example you want to run
    # gmail_example()
    # qq_mail_example()
    # multiple_attachments_example()
    # port25_example()
    # port25_no_auth_example()
    command_line_examples()

