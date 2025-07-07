#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example usage of the EmailSender class
"""

from email_sender import EmailSender

def gmail_example():
    """Example of sending email through Gmail"""
    # For Gmail, you'll need to use an App Password if 2FA is enabled
    # Create one at: https://myaccount.google.com/apppasswords
    
    # Create the sender with Gmail's SMTP settings
    sender = EmailSender('smtp.gmail.com', 465)  # Gmail uses port 465 for SSL
    
    # Authenticate - replace with your actual Gmail address and password/app password
    username = 'your.email@gmail.com'
    password = 'your-app-password'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create a message with an attachment
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='Test Email with Attachment',
        body='This is a test email sent from Python with an attachment.',
        cc_addresses=['cc-recipient@example.com'],
        attachments=['./document.pdf'],  # Replace with actual file path
        html_body=False
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def qq_mail_example():
    """Example of sending email through QQ Mail"""
    # For QQ Mail, you'll need to generate an authorization code
    # Enable SMTP in QQ Mail settings and get the code
    
    # Create the sender with QQ Mail's SMTP settings
    sender = EmailSender('smtp.qq.com', 465)  # QQ Mail uses port 465 for SSL
    
    # Authenticate - replace with your actual QQ Mail address and authorization code
    username = 'your-qq-number@qq.com'
    password = 'your-authorization-code'  # Not your QQ password!
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create a message with HTML content
    html_body = """
    <html>
      <body>
        <h1>HTML Email Test</h1>
        <p>This is a <b>test email</b> with <span style="color: blue;">HTML formatting</span>.</p>
        <p>Here's a list:</p>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
          <li>Item 3</li>
        </ul>
      </body>
    </html>
    """
    
    message = sender.create_message(
        to_addresses=['recipient@example.com'],
        subject='HTML Email Test',
        body=html_body,
        html_body=True  # Specify that we're using HTML content
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
    sender.close()

def multiple_attachments_example():
    """Example of sending email with multiple attachments"""
    # Create the sender (using 163 Mail as an example)
    sender = EmailSender('smtp.163.com', 465)
    
    # Authenticate - replace with your actual 163 Mail address and password
    username = 'your-username@163.com'
    password = 'your-password-or-authorization-code'
    
    if not sender.authenticate(username, password):
        print("Authentication failed. Exiting.")
        return
    
    # Create a message with multiple attachments
    message = sender.create_message(
        to_addresses=['recipient1@example.com', 'recipient2@example.com'],
        subject='Multiple Attachments Test',
        body='This email contains multiple attachments.',
        attachments=[
            './document1.pdf',  # Replace with actual file paths
            './image.jpg',
            './spreadsheet.xlsx'
        ]
    )
    
    # Send the email
    sender.send_email(message)
    
    # Close the connection
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

if __name__ == "__main__":
    print("Email Sender Examples")
    print("=====================")
    print("Uncomment the example you want to run in the code.")
    
    # Uncomment the example you want to run:
    # gmail_example()
    # qq_mail_example()
    # multiple_attachments_example()
    command_line_example()

