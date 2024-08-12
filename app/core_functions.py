"""
Convert CSV to Dictionary, Write and Send Emails.
"""

import csv, os, glob
from Google import create_service
import base64
import email_utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def csv_to_map(csv_file):
    """
    converts csv of services to map, returns services map
    Ex: services["AcmeData"]["privacy_dept_contact_email"] = "privacy@acmedata.com"...
    """
    all_services = {}
    top_choice = {}
    people_search = {}
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        cols = next(csv_reader)
        # cols = ['service_name', 'service_source', 'category', 'topchoice', 'service_privacy_url', 'privacy_dept_contact_email', ...]
        for line in csv_reader:
            # LINE: ['databroker1', 'service_source1', 'category1', 'YES/NO', 'https://someprivacyurl.com/', 'privacy@this.does.not.exist', 'T/F', 'T/F',...]
            line = [True if x == 'TRUE' else False if x == 'FALSE' else x for x in line]
            # creates the map schemas we want
            submap = dict(zip(cols[1:], line[1:]))
            all_services[line[0]] = submap
            if submap['top_choice'] == 'YES':
                top_choice[line[0]] = submap
                people_search[line[0]] = submap
            elif submap['category'] == 'people search':
                people_search[line[0]] = submap
    return all_services, top_choice, people_search

def create_gmail_label(service):
    '''
    Creates a new label/gets the ID of label already named "PrivacyBot".
    '''
    # Create a label called PrivacyBot if it doesn't exist.
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        create_label = True
    else:
        for label in labels:
            if label["name"] == "PrivacyBot":
                label_id = label["id"]
                create_label = False
                print("Label PrivacyBot with id %s already exists. Using the same label for the mails being sent..." % label_id)
                break
        else:
            create_label = True
    if create_label:
        created_label = service.users().labels().create(userId='me', body={"name": "PrivacyBot", "labelListVisibility": "label_show", "messageListVisibility": "show"}).execute()
        label_id = created_label["id"]
        print("Label PrivacyBot does not exist. Creating label with name PrivacyBot with id %s..." % label_id)

    return label_id

def send_email(usrjson, services_map):
    '''
    This function:
    - initiates the OAuth flow with GMAIL API and upon successful authentication,
    - Creates a label named "PrivacyBot"
    - Drafts and sends the CCPA Data Delete request email to the chosen list of data brokers
    '''
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    gmail_service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Create a new label or use an existing label named "PrivacyBot"
    label_id = create_gmail_label(gmail_service)

    # List of brokers used in confirmation email sent to the end user at the end of the transaction
    sent_brokers = ""
    notsent_brokers = ""

    # Allowed PII Attributes
    pii = {
        "firstname":"First Name",
        "lastname":"Last Name",
        "email":"Email",
        "full_address":"Address",
        "city":"City",
        "state":"State",
        "zip":"Zip",
        "country":"Country",
        "dob":"Date of birth",
        "age":"Age",
        "phone_num":"Phone Number",
        "cc_last4":"Last 4 digits of credit card",
        "device_ad_id":"Device Advertising ID",
        "twitter_handle":"Twitter handle",
        "link_to_profile":"Profile link"}

    # Create the chosen_services_map

    for service in services_map:
        submap = services_map[service] # build the service submap
        broker_email = submap["privacy_dept_contact_email"]

        # Build the user's data that will be sent to the data broker.
        userdata = []
        # go through info that a specific service wants
        for attribute in pii:
            if submap[attribute] == True and attribute in usrjson:
                    userdata.append(pii[attribute] + ": " + usrjson[attribute])

        ordered_list = ""
        for item in userdata:
            ordered_list += "<li>" + str(item) + "</li>"

        # Write the message body - using usrjson, fill only those details as required from each data broker
        emailMsg = email_utils.format_body(ordered_list)

        # Fill the email fields
        # Set reply-to address. All the follow up emails from data brokers will be sent to this address.
        reply_to_addr = usrjson['email']
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = broker_email
        mimeMessage['subject'] = 'CCPA Data Deletion Request - ' + service
        mimeMessage.add_header('reply-to', reply_to_addr)
        mimeMessage.attach(MIMEText(emailMsg, 'html'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        email_not_sent = False

        # Try sending the email. Catch an exception in case the email cannot be sent.
        try:
            message = gmail_service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
            message_id = message['id']
            label_msg = gmail_service.users().messages().modify(userId='me', id=message_id, body={"addLabelIds":[label_id,]}).execute()
        except:
            print("Email could not be sent to", service)
            email_not_sent = True

        # List of data brokers to be used for confirmation email
        if email_not_sent == False:
            if sent_brokers == "":
                sent_brokers += service
            else:
                sent_brokers += ", " + service
        else:
            if notsent_brokers == "":
                notsent_brokers += service
            else:
                notsent_brokers += ", " + service

    if notsent_brokers == "":
        sent_result = "Emails were sent to all chosen data brokers successfully."
    else:
        sent_result = "Emails could not be sent to " + notsent_brokers

    cnf_email = email_utils.format_confirmation_email(sent_result)
    # Send confirmation email
    # reply_to_addr = usrjson['email']
    cnfMessage = MIMEMultipart()
    cnfMessage['to'] = usrjson['email']
    cnfMessage['subject'] = 'PrivacyBot Confirmation'
    cnfMessage.attach(MIMEText(cnf_email, 'html'))
    cnf_string = base64.urlsafe_b64encode(cnfMessage.as_bytes()).decode()
    cnf_message = gmail_service.users().messages().send(userId='me', body={'raw': cnf_string}).execute()
    cnf_message_id = cnf_message['id']
    cnf_label = gmail_service.users().messages().modify(userId='me', id=cnf_message_id, body={"addLabelIds":[label_id,]}).execute()

    # Delete the token file
    for filename in glob.glob("token_gmail*"):
        os.remove(filename)

def privacy_api(usrjson, service_map):
    '''
    This function initiates the logic of sending request-to-delete emails to data brokers.
    '''
    send_email(usrjson, service_map)

