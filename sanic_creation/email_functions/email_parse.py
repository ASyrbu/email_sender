

#def validate_file(filename, filesize, get_config_field):
 #   file_extension = filename.split('.')[-1] if "." in filename else None

 #   valid_extension: bool = file_extension in get_config_field("extensions")
  #  valid_filesize: bool = filesize <= get_config_field("filesize_max")

   # return valid_extension & valid_filesize, file_extension


#def email_contact(request, sanic_config_get):
 #   request_dict = request.form
  #  get_field = request_dict.get

   # email_content = f'''Company: {get_field("company")}
#Name: {get_field("name")}
#Phone: {get_field("phone")}
#Email: {get_field("email")}
#Interest: {get_field("selected")}
    
#{get_field("message")}
#'''

 #   _subject = f'Contact us {get_field("company")}'

  #  emailMessage = MIMEMultipart()

   # emailMessage.preamble = _subject
    #emailMessage["Subject"] = _subject
#    emailMessage["From"] = sanic_config_get("endpoints").get("contact_us").get("from")
 #   emailMessage["To"] = sanic_config_get("endpoints").get("contact_us").get("to")

  #  emailMessage.attach(MIMEText(email_content, 'plain', 'utf-8'))

   # return emailMessage, 200


#def email_intership(request, sanic_config_get):
 #   request_dict = request.form
  #  get_field = request_dict.get

   # email_content = f"""Name: {get_field("name")}
#Phone: {get_field("phone")}
#Email: {get_field("email")}
#Job: {get_field("job")}

#{get_field("message")}
 #   """

  #  emailMessage = MIMEMultipart()
   # emailMessage["Subject"] = "Apply for Intership from %s" % get_field("name")
    #emailMessage["From"] = sanic_config_get("endpoints").get("intership").get("from")
 #   emailMessage["To"] = sanic_config_get("endpoints").get("intership").get("to")

  #  emailMessage.attach(MIMEText(email_content, 'plain', 'utf-8'))

   # return emailMessage, 200


#def email_applyjob(request, sanic_config_get):
 #   request_dict = request.form
  #  get_field = request_dict.get

   # emailMessage = MIMEMultipart()

    #file_ref = request.files.get("file")

    #if file_ref is not None:
     #   file_bytes = file_ref.body
      #  is_file_valid, extension = validate_file(file_ref.name, len(file_bytes) / 1_048_576, sanic_config_get)
       # if is_file_valid is False:
        #    return None, 400

#        filename = f'CV {get_field("name")}.{extension}'

 #       emailFile = MIMEApplication(file_bytes, Name=filename)
  #      emailFile['Content-Disposition'] = f'attachment; filename="{filename}"'

   #     emailMessage.attach(emailFile)

    #email_content = f"""Name: {get_field("name")}
#Phone: {get_field("phone")}
#Email: {get_field("email")}
#Job Position: {get_field("job")}
    
#{get_field("message")}
 #   """

  #  emailMessage["Subject"] = f'{get_field("name")} - Applied for Job {get_field("job")}'
   # emailMessage["From"] = sanic_config_get("endpoints").get("apply_job").get("from")
    #emailMessage["To"] = sanic_config_get("endpoints").get("apply_job").get("to")

  #  emailMessage.attach(
   #     MIMEText(email_content, 'plain', 'utf-8')
   # )

   # return emailMessage, 200
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def validate_file(filename, filesize, get_config_field):
    file_extension = filename.split('.')[-1] if "." in filename else None

    valid_extension: bool = file_extension in get_config_field("extensions")
    valid_filesize: bool = filesize <= get_config_field("filesize_max")

    return valid_extension & valid_filesize, file_extension

def create_email_message(request_dict, sanic_config_get, email_type):
    get_field = request_dict.get

    email_fields = {
        "contact": {"subject": "Contact us {company}", "recipient": "contact_us", "extra_fields": ["company", "language"]},
        "intership": {"subject": "Apply for Internship from {name}", "recipient": "intership", "extra_fields": ["job","message"]},
        "apply_job": {"subject": "{name} Applied for Job {job}", "recipient": "apply_job", "extra_fields": ["job"]}
    }

    email_content = "\n".join([f'{field.capitalize()}: {get_field(field)}' for field in ["name", "phone", "email"]])

    for field in email_fields.get(email_type, {}).get("extra_fields", []):
        email_content += f'\n{field.capitalize()}: {get_field(field)}'


    emailMessage = MIMEMultipart()

    # Remove the square brackets from the subject line
    emailMessage["Subject"] = email_fields.get(email_type, {}).get("subject", "").format_map({k: get_field(k) for k in request_dict})

    recipient = sanic_config_get("endpoints").get(email_fields.get(email_type, {}).get("recipient", ""), {})
    emailMessage["From"] = recipient.get("from")
    emailMessage["To"] = recipient.get("to")

    emailMessage.attach(MIMEText(email_content, 'plain', 'utf-8'))

    file_ref = request_dict.get("file")
    if file_ref:
        file_bytes = file_ref.body
        is_file_valid, extension = validate_file(file_ref.name, len(file_bytes) / 1_048_576, sanic_config_get)
        if is_file_valid:
            filename = f'CV {get_field("name")}.{extension}'
            emailFile = MIMEApplication(file_bytes, Name=filename)
            emailFile['Content-Disposition'] = f'attachment; filename="{filename}"'
            emailMessage.attach(emailFile)
        else:
            raise ValueError("Invalid file")

    return emailMessage, 200
