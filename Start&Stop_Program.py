import imaplib
import email
import subprocess as sp
from datetime import datetime
import EndProcess_Email_Notification as end

# Email account credentials
email_user = "erockrpidevicealert@gmail.com"
email_password = "zfarpmyhbgwomytx"
email_host = "imap.gmail.com"
email_port = 993

# Process File Locations
startNotificationScript = "C:\\Users\\KellieGlasgow\\OneDrive - Enchanted Rock\\Documents\\RPI Data Capture\\StartProcess_Email_Notification.py"
runningNotificationScript = "C:\\Users\\KellieGlasgow\\OneDrive - Enchanted Rock\\Documents\\RPI Data Capture\\ProcessRunning_Email_Notification.py"

global  running_process, start_time
running_process = None 

# Initialize runningProcess outside of the loop and declare it as global

def start_process(script):
    process = sp.Popen(['python', script])
    status = sp.Popen.poll(process)
    return process, status

def end_process(process):
    global start_time
    process.terminate()  # Sends a termination signal to the process
    try:
        process.wait(timeout=10)  # Wait for the process to terminate within a timeout period
        status = process.poll()  # Check the status of the terminated process
        if status is not None:
            print("Process successfully terminated!")
            end_time = datetime.now()
            end.collection_complete_notification(start_time, end_time)
        else:
            print("Failed to terminate process")
    except sp.TimeoutExpired:
        print("Process did not terminate within the timeout period.")
        status = None

    return status

def check_email():
    global running_process, start_time
    # Connect to the email server
    mail = imaplib.IMAP4_SSL(email_host, email_port)
    mail.login(email_user, email_password)
    mail.select("inbox")

    # Search for unread emails
    result, data = mail.search(None, "UNSEEN")
    if result == "OK": # Correctly searched without errors
        if data[0]: # Found unread email(s)
            email_ids = data[0].split() 
            for num in email_ids: # Go through every unread emails
                num_bytes = bytes(num)
                result, email_data = mail.fetch(num_bytes, "(RFC822)") # Fetch the email
                if result == "OK": # Correctly fetched
                    raw_email = email_data[0][1] 
                    msg = email.message_from_bytes(raw_email) # Get the message data
                    # Extract email content
                    subject = msg["Subject"]
                    if subject == 'START': # If subject is 'START' then call scripts to begin running
                        print("\nStarting program............")
                        running_process, running_status = start_process(runningNotificationScript)  # Update running_process
                        #To add a process, use below line and add process_instance to global as None
                        #process_instance, process_status = start_process(path to script)
                        start_time = datetime.now()
                        if running_status is None:
                            print("Started program successfully!")
                        else:
                            print("Status: ", running_status)
                            print("Failed to start process")
                            
                    if subject == 'STOP': # If subject is 'STOP then call scripts to stop running
                        print("\nTerminating program............")
                        running_status = end_process(running_process)
                        # If another process was added, use below line and add process_instance to global as None
                        #process_status = end_process(process_instance)
                        
                else:
                    print("Error fetching email data.")
        else:
            print("\n")
    else:
        print("Error searching for unread emails.")
    # Close the connection
    mail.close()
    mail.logout()

while True: 
    check_email()