from aiosmtplib import SMTP

async def send_email(email_mime, sanic_config_get):
    smtp_connection, status_code = await create_connection(sanic_config_get)
    if not status_code == 200:
        return None, 500
    await smtp_connection.send_message(email_mime)
    await smtp_connection.quit()
    return None, 200


async def create_connection(sanic_config_get) -> SMTP:
    connection = SMTP(
        hostname=sanic_config_get("smtp").get("server"),
        port=sanic_config_get("smtp").get("port")
    )
    await connection.connect()
    await connection.login(
       username=sanic_config_get("credentials").get("email_id"),
      password=sanic_config_get("credentials").get("password")
    )
    return connection, 200