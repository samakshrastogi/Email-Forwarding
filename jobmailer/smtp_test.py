import smtplib
import ssl

EMAIL = "samakshrastogi885@gmail.com"
APP_PASSWORD = "knxlqjyvtojjlkrd"

context = ssl.create_default_context()

server = smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465,
    context=context,
    timeout=30
)

server.login(EMAIL, APP_PASSWORD)
print("LOGIN SUCCESS")
server.quit()
