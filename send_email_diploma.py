import email
import smtplib
import ssl
import csv
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_email_diploma(navn, firmanavn, kursnavn, email, kursdato, kurssted, kursnavn2, kursdato2, pdf_filename, lenke, attestID, navnASCII):
    sender_email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')

    message = MIMEMultipart("alternative")
    subject = "Sertifisering for Questback Essentials"
    message["From"] = "Håkon Kavli, Questback Academy"
    message["To"] = email
    message["Subject"] = subject

    PORT = 465  # For SSL
    text = " "
    html = " "
    # Oppretter med server og sender email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(sender_email, password)
        if kurssted == "Oslo" or kurssted == "Trondheim":
            f1 = open("texts/textNO.txt", "r", encoding='utf-8')
            f2 = open("texts/htmlNOdiplom.txt", "r", encoding='utf-8')
            text = f1.read()
            html = f2.read()

        elif kurssted == "Stockholm":
            f1 = open("texts/textSV.txt", "r", encoding='utf-8')
            f2 = open("texts/htmlSVdiplom.txt", "r", encoding='utf-8')
            text = f1.read()
            html = f2.read()
            message["Subject"] = "Questback Essentials Kursbevis"

        text2 = text.format(navn=navn, kursnavn=kursnavn, kursdato=kursdato,
                            kursnavn2=kursnavn2, kursdato2=kursdato2,
                            attestID=attestID, lenke=lenke)
        html2 = html.format(navn=navn, kursnavn=kursnavn, kursdato=kursdato,
                            kursnavn2=kursnavn2, kursdato2=kursdato2,
                            attestID=attestID, lenke=lenke)
        part1 = MIMEText(text2, "plain")
        part2 = MIMEText(html2, "html")
        message.attach(part1)
        message.attach(part2)

        with open(pdf_filename, "rb") as attachement:
            part3 = MIMEBase("application", "octet-stream")
            part3.set_payload(attachement.read())
            encoders.encode_base64(part3)

            part3.add_header(
                "Content-Disposition",
                f"attachment; filename= {pdf_filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part3)

            print(f"Sender mail til {navnASCII}")

            server.sendmail(
                sender_email,
                email,
                message.as_string())
