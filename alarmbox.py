import daemonize
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
import logging
import random
import argparse


class AlarmBox:

    def __init__(self, settings_file):
        self.settings = {}
        self._read_settings(settings_file)
        logfile = self.settings.get('LOG_FILE', 'alarmbox.log')
        logging.basicConfig(filename=logfile, 
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s]: %(message)s')
        self.last_time = datetime.now()

    '''
    This is where the code for the sensor goes. For testing it will 
    simulate the sensor not detecting motion to trigger the alarm at
    random intervals
    '''
    def _poll_sensor(self):
        threshold = self.settings['THRESHOLD']
        sleepy_time = int(threshold * 1.2)
        # make a random number with a 20% chance of triggering the alam
        random_number = random.randint(1, sleepy_time)
        tgime.sleep(random_number)



    def run(self):
        sent_email = False
        threshold = self.settings['THRESHOLD']
        while True:
            self.last_time = datetime.now()
            self._poll_sensor()
            time_since_last_signal = self._seconds_since_last_time()
            if (time_since_last_signal > threshold) and not sent_email:
                self._send_emai()
                sent_email = True
            elif (time_since_last_signal < threshold) and sent_email:
                # We got movement bel
                sent_email = False

    def _read_settings(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('=')
                    if len(parts) == 2:
                        name, value = parts
                        name = name.upper().strip()
                        value = value.upper().strip()
                        self.settings[name] = value

    def _send_email(self):
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

    def _seconds_since_last_time(self):
        now = datetime.now()
        diff_time = now - self.last_time
        self.last_time = now
        return diff_time.total_seconds()

def parse_args():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Command line argument example')

    # Add the '--fg' argument
    parser.add_argument('--fg', action='store_true', help='Run in the foreground')

    # Add the '--settings_file' argument with a required filename
    parser.add_argument('--settings_file', required=True, help='Specify a settings file')

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    run_in_foreground = args.fg
    settings_filename = args.settings_file

def my_daemon_function():
    a = AlarmBox(settings_file)
    a.run()


if __name__ == '__main__':

    parse_args()
    
    # Define the options for daemonization
    if run_in_foreground:
        my_daemon_function()
    else:
        daemon = daemonize.Daemonize(
            app='alarmbbox',
            pid='/tmp/alarmbox.pid',
            action=my_daemon_function,
            foreground=False,
        )

        # Start the daemon)
        daemon.start()
