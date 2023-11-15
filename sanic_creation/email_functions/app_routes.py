#from sanic import json
#from sanic_creation.email_functions.email_parse import email_intership, email_applyjob, email_contact
#from sanic_creation.email_functions.safe_calls import safe_call, async_safe_call
#from sanic_creation.email_functions.smtp_api import send_email


#async def route_apply_job(request):
   # emailMessage, mail_status_code = safe_call(email_applyjob, request, request.route.ctx.config_get)

  #  if not mail_status_code == 200:
   #     return json({"description": "Composing EmailObject failed.", "status": mail_status_code, "error": True})

 #   _, request_status_code = await async_safe_call(send_email, emailMessage, request.route.ctx.config_get)

  #  if not request_status_code == 200:
   #     return json({"description": "Request failed to SMTP API.", "status": request_status_code, "error": True})

   # return json({"description": None, "status": request_status_code, "error": False})


#async def route_contact_us(request):
   # emailMessage, mail_status_code = safe_call(email_contact, request, request.route.ctx.config_get)

  #  if not mail_status_code == 200:
    #    return json({"description": "Composing EmailObject failed.", "status": mail_status_code, "error": True})

 #   _, request_status_code = await async_safe_call(send_email, emailMessage, request.route.ctx.config_get)

  #  if not request_status_code == 200:
      #  return json({"description": "Request failed to SMTP API.", "status": request_status_code, "error": True})

   # return json({"description": None, "status": request_status_code, "error": False})


#async def route_intership(request):
   # emailMessage, mail_status_code = safe_call(email_intership, request, request.route.ctx.config_get)

  #  if not mail_status_code == 200:
   #     return json({"description": "Composing EmailObject failed.", "status": mail_status_code, "error": True})

  # _, request_status_code = await async_safe_call(send_email, emailMessage, request.route.ctx.config_get)

  #  if not request_status_code == 200:
     #   return json({"description": "Request failed to SMTP API.", "status": request_status_code, "error": True})

  #  return json({"description": None, "status": request_status_code, "error": False})

from sanic import json
from sanic_creation.email_functions.email_parse import create_email_message
from sanic_creation.email_functions.safe_calls import safe_call, async_safe_call
from sanic_creation.email_functions.smtp_api import send_email

async def handle_email_request(request, email_type):
    request_dict = request.form
    email_message, mail_status_code = safe_call(create_email_message, request_dict, request.route.ctx.config_get, email_type)

    if not mail_status_code == 200:
        return json({"description": f"Composing EmailObject failed for {email_type}.", "status": mail_status_code, "error": True})

    _, request_status_code = await async_safe_call(send_email, email_message, request.route.ctx.config_get)

    if not request_status_code == 200:
        return json({"description": f"Request failed to SMTP API for {email_type}.", "status": request_status_code, "error": True})

    return json({"description": None, "status": request_status_code, "error": False})

async def route_apply_job(request):
    return await handle_email_request(request, "apply_job")

async def route_contact_us(request):
    return await handle_email_request(request, "contact")

async def route_intership(request):
    return await handle_email_request(request, "intership")
