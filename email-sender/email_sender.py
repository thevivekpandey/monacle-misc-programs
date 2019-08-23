import os
from os.path import basename
import sys
import json
import requests
import time
import smtplib
import traceback
import monacle_aws
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def run_via_google(process_name, parameters, server, email_credentials):
    msg = MIMEMultipart()
    msg['From'] = parameters['sender']
    msg['To'] = ', '.join(parameters['email_to'])
    msg['Subject'] = parameters['subject']
    if 'html' in parameters:
        msg.attach(MIMEText(parameters['html'], 'html'))

    try:
        if 'attachment_data' in parameters and parameters['attachment_data']:
            s3_path = parameters['attachment_data']
            s3_path_arr = s3_path.split('/')
            filename = s3_path_arr[len(s3_path_arr) - 1]
            monacle_aws.s3_download(s3_path, filename)
            f = open(filename)
            part = MIMEApplication(f.read(), Name=basename(filename))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
            msg.attach(part)
            text = msg.as_string()
            server.sendmail('getmonacle@gmail.com', parameters['email_to'], text)
            #server.sendmail('getmonacle@gmail.com', mysql_db.get_email_recipients()['external'], text)
            os.remove(filename)
        else:
            text = msg.as_string()
            server.sendmail('getmonacle@gmail.com', parameters['email_to'], text)
            #server.sendmail('getmonacle@gmail.com', mysql_db.get_email_recipients()['external'], text)
    except Exception as e:
        traceback.print_exc()
    server.quit()

def get_smtp_server(email_credentials):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_credentials['email'], email_credentials['password'])
    return server

if __name__ == '__main__':
    while(1):
        queue = monacle_aws.receive_sqs_message()
        email_credentials = {'email': 'getmonacle@gmail.com', 'password': os.getenv('EMAIL_PASSWORD')}

        for message in queue.receive_messages():
            jsonified_message = json.loads(message.body)
            process_name = jsonified_message['process_name']
            parameters = jsonified_message['parameters']
            print('Got an sqs message')
            server = get_smtp_server(email_credentials)
            run_via_google(process_name, parameters, server, email_credentials)
            message.delete()
        time.sleep(5)
