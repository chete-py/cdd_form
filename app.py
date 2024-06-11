import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = '001supersecretkey'

from dotenv import load_dotenv  # pip install python-dotenv

PORT = 587  
EMAIL_SERVER = "smtp.gmail.com" 

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")


@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':       

        # Pull the user inputs from the form
        fname = request.form['fname']
        sname = request.form['sname']
        id_number = request.form['id_number']
        phone = request.form['phone_number']
        address = request.form['address']
        employment = request.form['employment']
        employer = request.form['employer']
        job = request.form['job']
        funds = request.form['funds']

        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Client Due Diligence</title>
        </head>
        <body>
            
            
            <table border="1" style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td colspan="2" style="padding: 8px; font-weight:bold; color: #9955bb ;  text-align: left;"> Willis Towers Watson</td>
                </tr>
                
                <tr>
                    <td colspan="2" style="padding: 8px; color: black ; background-color: #848482; text-align: center;"> CUSTOMER DUE DILIGENCE FORM (Individual) </td>
                </tr>
                               
                <tr>
                    <td style="padding: 8px;">First Name</td>
                    <td style="padding: 8px;">{fname}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Last Name</td>
                    <td style="padding: 8px;">{sname}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">ID Number</td>
                    <td style="padding: 8px;">{id_number}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Phone Number</td>
                    <td style="padding: 8px;">{phone}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Address</td>
                    <td style="padding: 8px;">{address}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Employment Status</td>
                    <td style="padding: 8px;">{employment}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Employer</td>
                    <td style="padding: 8px;">{employer}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Job Title</td>
                    <td style="padding: 8px;">{job}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">Source Of Funds</td>
                    <td style="padding: 8px;">{funds}</td>
                </tr>

            </table>


           
        </body>
        </html>
        """

        # Send the email with the HTML content
        try:
            send_email(
                subject=f"{fname} CLIENT DUE DILIGENCE FORM",
                receiver_email="collins.chetekei@ke.grassavoye.com",  # Change to your desired recipient
                html_content=html_content
            )
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send email: {e}', 'danger')

    return render_template('form.html')



def send_email(subject, receiver_email, html_content):
    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("CDD Form.", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.add_alternative(html_content, subtype='html')


    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    app.run(debug=True)
    