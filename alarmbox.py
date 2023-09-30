import daemonize
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

class AlarmBox:
    def __init__(self):
        _read_settings()
        self.settings = {}

    def _read_settings(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('=')
                    if len(parts) == 2:
                        name, value = parts
                        name = name.strip()
                        value = value.strip()
                        self.settings[name] = value

    def send_email(self):
        # Load SendGrid API key
        date_time = self.get_date_time_string()
        api_key = self.settings['API_KEY']
        from_email = self.settings['FROM_EMAIL']
        to_email = self.settings['TO_EMAIL']
        email_subject = self.settings.get('EMAIL_SUBJECT', 'Alert From AlarmBox')
        email_text = self.settings.get('EMAIL_TEXT', f'This is an alert from AlarmBox at {date_time}')
        # Creaubjte a SendGrid client
        sg = SendGridAPIClient(api_key)

        # Create a message
        message = Mail(
            from_email=from_email, 
            to_emails=to_email,  
            subject=email_subject,
            plain_text_content=email_text
        )

        # Send the email
        try:
            response = sg.send(message)
            print('Email sent successfully')
        except Exception as e:
            print(f'Error: {e}')

    def get_date_time_string(self):
        # Get the current date and time
        current_datetime = datetime.now()
        # Format the datetime object as yyyy-MM-dd HH:mm
        return current_datetime.strftime('%Y-%m-%d %H:%M')



def my_daemon_function():
    while True:
        with open('/tmp/daemon_example.txt', 'a') as f:
            f.write('Daemon is running...\n')

if __name__ == '__main__':
    # Define the options for daemonization
    daemon = daemonize.Daemonize(
        app="my_daemon",
        pid='/tmp/my_daemon.pid',
        action=my_daemon_function,
        foreground=False,
    )

    # Start the daemon
    daemon.start())
