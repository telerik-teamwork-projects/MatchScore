import os
from dotenv import load_dotenv

from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from jinja2 import Environment, FileSystemLoader

load_dotenv()

template_folder = "../templates"
jinja_env = Environment(loader=FileSystemLoader(template_folder))

class Envs:
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_FROM = os.environ['MAIL_FROM']
    MAIL_PORT = int(os.environ['MAIL_PORT'])
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_FROM_NAME = os.environ['MAIL_FROM_NAME']


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_welcome_email_async(subject: str, email_to: str, body: dict):
    title = str(body.get("title", ""))
    name = str(body.get("name", ""))
    cta_link = str(body.get("ctaLink", ""))

    template = jinja_env.get_template('welcome-email.html')
    rendered_body = template.render(title=title, name=name, cta_link=cta_link, body=body)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=rendered_body,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_tournament_accept_email_async(subject: str, email_to: str, body: dict):
    title = str(body.get("title", ""))
    name = str(body.get("name", ""))
    cta_link = str(body.get("ctaLink", ""))

    template = jinja_env.get_template('tournament-accept.html')
    rendered_body = template.render(title=title, name=name, cta_link=cta_link, body=body)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=rendered_body,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_player_accept_email_async(subject: str, email_to: str, body: dict):
    title = str(body.get("title", ""))
    name = str(body.get("name", ""))
    cta_link = str(body.get("ctaLink", ""))

    template = jinja_env.get_template('player-accept.html')
    rendered_body = template.render(title=title, name=name, cta_link=cta_link, body=body)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=rendered_body,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_director_accept_email_async(subject: str, email_to: str, body: dict):
    title = str(body.get("title", ""))
    name = str(body.get("name", ""))
    cta_link = str(body.get("ctaLink", ""))

    template = jinja_env.get_template('director-accept.html')
    rendered_body = template.render(title=title, name=name, cta_link=cta_link, body=body)

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=rendered_body,
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )

    fm = FastMail(conf)
    background_tasks.add_task(
       fm.send_message, message, template_name='email.html')