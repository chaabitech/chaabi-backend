import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64

def send_mail(to, subject, text, list_of_attachments):
    gmail_user = "crofarmsender@gmail.com"
    gmail_pwd = "crofarm@1234"
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    if list_of_attachments:
        for obj in list_of_attachments:
            file_name = obj.get("name", "error.csv")
            out_content = obj['value']
            part = MIMEBase('application', "octet-stream")
            part.set_payload(out_content)
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename='+file_name)
            msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()

# def send_html_mail(to, subject, html, list_of_attachments):
#     gmail_user = "crofarmsender@gmail.com"
#     gmail_pwd = "crofarm@1234"
#     msg = MIMEMultipart()
#     msg['From'] = gmail_user
#     msg['To'] = to
#     msg['Subject'] = subject
#     msg.attach(MIMEText(html, 'html'))
#     if list_of_attachments:
#         for obj in list_of_attachments:
#             file_name = obj.get("name", "error.csv")
#             out_content = obj['value']
#             part = MIMEBase('application', "octet-stream")
#             part.set_payload(out_content)
#             Encoders.encode_base64(part)
#             part.add_header('Content-Disposition', 'attachment; filename='+file_name)
#             msg.attach(part)
#     mailServer = smtplib.SMTP("smtp.gmail.com", 587)
#     mailServer.ehlo()
#     mailServer.starttls()
#     mailServer.ehlo()
#     mailServer.login(gmail_user, gmail_pwd)
#     mailServer.sendmail(gmail_user, to, msg.as_string())
#     mailServer.close()

import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Replace sender@example.com with your "From" address. 
# This address must be verified.
def send_html_mail(to, subject, html, list_of_attachments):
    SENDER = 'crofarmsender@gmail.com'  
    SENDERNAME = 'Crofarm'

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT  = to

    # Replace smtp_username with your Amazon SES SMTP user name.
    USERNAME_SMTP = "AKIA2EL6SZIG3V5FH2PW"

    # Replace smtp_password with your Amazon SES SMTP password.
    PASSWORD_SMTP = "BFkk26VSJwFKAvF5qRvfPEJh95FKgCidoCKCF6UYxI/t"

    # (Optional) the name of a configuration set to use for this message.
    # If you comment out this line, you also need to remove or comment out
    # the "X-SES-CONFIGURATION-SET:" header below.
    #CONFIGURATION_SET = "ConfigSet"

    # If you're using Amazon SES in an AWS Region other than US West (Oregon), 
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP  
    # endpoint in the appropriate region.
    HOST = "email-smtp.ap-south-1.amazonaws.com"
    PORT = 587

    # The subject line of the email.
    SUBJECT = 'Amazon SES Test (Python smtplib)'

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test\r\n"
                 "This email was sent through the Amazon SES SMTP "
                 "Interface using the Python smtplib package."
                )

    # The HTML body of the email.
    BODY_HTML = html

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    # Comment or delete the next line if you are not using a configuration set
    #msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(BODY_HTML, 'html')


    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)

    if list_of_attachments:
        for obj in list_of_attachments:
            file_name = obj.get("name", "error.csv")
            out_content = obj['value']
            part = MIMEBase('application', "octet-stream")
            part.set_payload(out_content)
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename='+file_name)
            msg.attach(part)

    # Try to send the message.
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
        print ("mail sent!")
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
   