import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

#config
fromaddr = "" # Write From address
toaddr =[""] # Write To address
toCc=[""] #Write address to be kept in cc
path=r"" # Attach the file to send
Subject="" # Add subject for the mail
body_message="" #Add text to the body

# open the file to be sent 
filename = "" #Add the filename that will appear on mail
attachment = open(path, "rb")

class mail:
    
    def __init__(self):
        self.msg=MIMEMultipart()
        self.attachment=MIMEBase('application', 'octet-stream')
    
    def _email_main_body(self):
        self.msg['From'] = fromaddr
        self.msg['To'] ="; ".join(toaddr)
        self.msg['Cc']="; ".join(toCc)
        self.msg['Subject'] = Subject
    
    def _email_attachment(self):
        self.attachment.set_payload((attachment).read())
        encoders.encode_base64(self.attachment)
        self.attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        self.msg.attach(self.attachment)
        text = self.msg.as_string()
        return text
    
    def _smtp_connect(self):
        smtpObj = smtplib.SMTP('mail.tpc.co.in', 25)
        smtpObj.ehlo()
        smtpObj.starttls()
        return smtpObj
    
    def trigger_mail(self):
        self._email_main_body()
        body = body_message
        self.msg.attach(MIMEText(body,'plain'))
        
        text=self._email_attachment()
        self._run(text)

    def _send_mail(self,message,smtpObj):
        smtpObj.sendmail(fromaddr, toaddr+toCc, message)
        smtpObj.quit()        
        print ("Successfully sent email") 
    
    def _run(self, message):
        tries = 0
        smtpObj=self._smtp_connect()
        try:
            self._send_mail(message,smtpObj)
            tries += 1
        except:
            if tries <=2:
                time.sleep(20)
                self._send_mail(message,smtpObj)