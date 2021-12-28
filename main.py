import os
import smtplib, ssl, getpass
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("ACCOUNT")
password = os.getenv("PASS")

port = 465
receiver_email = "zach@shapeways.com"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(sender_email, password)
mail.list()
mail.select("inbox")

message = """
Account: 
Model(s): 
Directional Quote [D] or Production [P]: 
# of Models to Quote (Quantity): 
Quantities to quote of each Model: 
Technology: 
Material: 
Finish: 
Expected Lead Time: 
Additional Instructions/Comments: 
End Use:
"""

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("rfq.template.test@gmail.com", password)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)