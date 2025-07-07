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
    sender = EmailSender('smtp.example.com', 25, use_ssl=False)  # Port 25 typically uses STARTTLS
    
    # Authenticate - replace with your actual email address and password
    username = 'your.email@example.com'
    password = 'your-password'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create a message
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='Port 25 Test Email',
        body='This is a test email sent through port 25 with STARTTLS.',
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def port25_no_tls_example():
    """Example of sending email through port 25 without TLS (plain)"""
    # Some servers might allow non-encrypted authentication on port 25
    # Note: This is less secure and not recommended for sensitive information
    
    # Create a custom EmailSender that skips TLS upgrade
    from email_sender import EmailSender as BaseEmailSender
    
    class PlainEmailSender(BaseEmailSender):
        def authenticate(self, username, password):
            """Override to skip TLS upgrade"""
            try:
                # Create plain SMTP connection
                self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                
                # Skip STARTTLS upgrade
                
                # Login to the server
                self.server.login(username, password)
                self.username = username
                self.is_authenticated = True
                print(f"Successfully authenticated as {username} (plain)")
                return True
                
            except Exception as e:
                print(f"Authentication failed: {str(e)}")
                self.is_authenticated = False
                return False
    
    # Use the custom sender
    sender = PlainEmailSender('smtp.example.com', 25, use_ssl=False)
    
    # Authenticate - replace with your actual email address and password
    username = 'your.email@example.com'
    password = 'your-password'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create and send message as usual
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='Plain Port 25 Test Email',
        body='This is a test email sent through port 25 without encryption.',
    )
    
    sender.send_email(message)
    sender.close()

def command_line_example():
    """Example of using the command line interface"""
    print("Command Line Usage Examples:")
    print("\n1. Basic email:")
    print("python email_sender.py --server smtp.gmail.com --port 465 --username your.email@gmail.com "
          "--to recipient@example.com --subject \"Test Email\" --body \"This is a test email.\"")
    
    print("\n2. Email with attachment:")
    print("python email_sender.py --server smtp.gmail.com --port 465 --username your.email@gmail.com "
          "--to recipient@example.com --subject \"Test Email with Attachment\" "
          "--body \"This is a test email with an attachment.\" --attach document.pdf")
    
    print("\n3. HTML email with multiple recipients and attachments:")
    print("python email_sender.py --server smtp.gmail.com --port 465 --username your.email@gmail.com "
          "--to \"recipient1@example.com, recipient2@example.com\" --cc \"cc@example.com\" "
          "--bcc \"bcc@example.com\" --subject \"HTML Email Test\" --body-file email_content.html "
          "--html --attach image1.jpg --attach document.pdf")
    
    print("\n4. Using TLS instead of SSL (e.g., for port 587):")
    print("python email_sender.py --server smtp.gmail.com --port 587 --use-tls --username your.email@gmail.com "
          "--to recipient@example.com --subject \"TLS Test\" --body \"This email was sent using TLS.\"")
          
    print("\n5. Using port 25 with STARTTLS:")
    print("python email_sender.py --server smtp.example.com --port 25 --use-tls --username your.email@example.com "
          "--to recipient@example.com --subject \"Port 25 Test\" --body \"This email was sent using port 25 with STARTTLS.\"")

if __name__ == "__main__":
    print("Email Sender Examples")
    print("=====================")
    print("Uncomment the example you want to run in the code.")
    
    # Uncomment the example you want to run:
    # gmail_example()
    # qq_mail_example()
    # multiple_attachments_example()
    # port25_example()  # Using port 25 with STARTTLS
    # port25_no_tls_example()  # Using port 25 without encryption (not recommended)
    command_line_example()
