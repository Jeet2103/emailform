from fastapi import FastAPI, HTTPException,Form,Request
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage
import ssl
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# import uvicorn

app = FastAPI()

class Email(BaseModel):
    receivers:str 
    subject: str
    body: str

@app.post("/send_email/")

def send_email(request: Request,
                     receivers: str = Form(...), subject: str = Form(...),
                     body: str = Form(...)):
    email = Email( receivers=receivers, subject=subject, body=body)
    try:
     
        smtp_username = "jeetnandigrami000@gmail.com"  # Replace with your SMTP server username
        smtp_password = "nbrjxifuxbfitbdz"  # Replace with your SMTP server password

        message = EmailMessage()
        message["Subject"] = email.subject
        message["From"] = email.sender
        message["To"] = email.receivers
        message.set_content(email.body)
        context = ssl.create_default_context()
       

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(email.sender, email.receivers, message.as_string())
        
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPException) as e:
        raise HTTPException(status_code=500, detail=str(e))
 

