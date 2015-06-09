# -*- coding: utf-8 -*-
"""
    flaskbb.emails
    ~~~~~~~~~~~~~~~~~~~~

    This module adds the functionality to send emails

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import render_template
from flask.ext.mail import Message

from metabomatch.extensions import mail


def send_reset_token(user, token):
    send_email(
        subject="Password Reset",
        recipients=[user.email],
        text_body=render_template(
            "email/reset_password.txt",
            user=user,
            token=token
        ),
        html_body=render_template(
            "email/reset_password.html",
            user=user,
            token=token
        )
    )


def send_reply_notification(users, topic_title, link):
    print 'IN send_reply_notification'
    send_email(
        subject="[metabomatch: new reply]",
        recipients=[u.email for u in users],
        text_body=render_template(
            "email/reply_notification.txt",
            topic_title=topic_title,
            link=link
        ),
        html_body=render_template(
            "email/reply_notification.html",
            topic_title=topic_title,
            link=link
        )
    )


def send_email(subject, recipients, text_body, html_body, sender=None):
    msg = Message(subject, recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
