import smtplib, ssl, getpass

port = 465
sender_email = "rfq.template.test@gmail.com"
receiver_email = "zach@shapeways.com"
password = getpass("Password:")

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