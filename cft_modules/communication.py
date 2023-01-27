
import smtplib
import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders


def send_email(subject, body, sender, recipients, password, output_pdf = None, output_xlsx = None, output_txt = None):
    # msg is an MIMEMultipart object that can include both txt and attachments
    msg = MIMEMultipart()
    # msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    # msg['Bcc'] = sender
    msg.attach(MIMEText(body, "plain"))

#     below could possibly attach all three files only if they are provided in this func
    ############## Encoding binary data PDF into ASCII characters thru base64 and attach ot the msg obj #########################
    # Open PDF file in binary mode
    if output_pdf is not None:   
        
        output_pdf_name = output_pdf.split('/')[-1]
        output_pdf_name
        with open(output_pdf, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part_pdf = MIMEBase("application", "octet-stream")
            part_pdf.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part_pdf)
        # Add header as key/value pair to attachment part
        part_pdf.add_header(
            "Content-Disposition",
            f"attachment; filename= {output_pdf_name}",
        )
        # Add attachment to message and convert message to string
        msg.attach(part_pdf)
    #########################################end of PDF attach ################################################################
    ############## Encoding binary data EXCEL into ASCII characters thru base64 and attach ot the msg obj #########################
    # Open PDF file in binary mode
    if output_xlsx is not None:
        with open(output_xlsx, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part_xlsx = MIMEBase("application", "octet-stream")
            part_xlsx.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part_xlsx)
        # Add header as key/value pair to attachment part
        part_xlsx.add_header(
            "Content-Disposition",
            f"attachment; filename= {output_xlsx}",
        )
        # Add attachment to message and convert message to string
        msg.attach(part_xlsx)
    #########################################end of XLSX attach ################################################################
    ############## Encoding binary data TXT/LOG  into ASCII characters thru base64 and attach ot the msg obj #########################
    # Open PDF file in binary mode
    
    if output_txt is not None:
        
        output_txt_name = output_txt.split('/')[-1]
        output_txt_name
        with open(output_txt, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part_txt = MIMEBase("application", "octet-stream")
            part_txt.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part_txt)
        # Add header as key/value pair to attachment part
        part_txt.add_header(
            "Content-Disposition",
            f"attachment; filename= {output_txt_name}",
        )
        # Add attachment to message and convert message to string
        msg.attach(part_txt)
    #########################################end of TXT/LOG attach ################################################################

    msg_w_attachments = msg.as_string()

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg_w_attachments)
    smtp_server.quit()
