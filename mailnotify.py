"""
Module that facilitates several ways to send email notifications.

Assumes the presence of the following environment variables:

- EMAIL_USER
- EMAIL_PASSWORD
- EMAIL_RECIPIENTS (as a comma separated string)

It also supports ignoring mail notifications
in development mode (defined by FLASK_ENV=dev).
"""
import smtplib
import logging
import os
import traceback
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(subject, body):
    """
    Basic synchronous email sending function given subject and body.

    Only requires subject and body, since recipients and credentails
    are assumed to be configured.

    If the environment variable FLASK_ENV is set to 'dev', nothing
    is sent, and configurations variables are not loaded.
    """
    if os.getenv('FLASK_ENV') == 'dev':
        logging.info('Ignoring notification "%s"', subject)
        return
    try:
        message = _createmessage(subject, body)
        server_ssl = _login()
        server_ssl.sendmail(os.environ['EMAIL_USER'],
                            _recipients(),
                            message.as_string())
        logging.info('Notification "%s"', subject)
    except smtplib.SMTPException:
        logging.exception('Failed to send email %s', subject)
    except:
        logging.exception('Failed to send message %s', subject)


def asyncsend(subject, body):
    """
    Same as 'send', but performed in a background thread.

    The thread is automatically started, but not joined on.
    Still, the thread object is returned in case it is
    required.
    """
    thread = Thread(target=send, args=(subject, body))
    thread.start()
    return thread


def sendexception(exception, tracebacktxt=None, async=True):
    """
    Deliver an email with useful exception information.

    If no formatted traceback is specified, the current
    one is used. The async parameter is for calling asyncsend
    or send, respectively.
    """
    subject = 'An exception occurred at the map server'
    body = """
    An exception has ocurred:
    
    %s

    %s
    """ % (exception.message,
           tracebacktxt or traceback.format_exc())
    if async:
        asyncsend(subject, body)
    else:
        send(subject, body)


def send500(exception, tracebacktxt, request):
    """
    Asynchronously deliver a message in case of a 500 error.

    It uses information from the request, the
    exception object and the non-optional fromatted
    traceback.
    """
    subject = '500 error on banking maps api'
    body = """
    Internal server error at %s
    
    Arguments:
    %s

    Exception '%s':

    %s
    """ % (request.path, repr(dict(request.args)),
           exception.message, tracebacktxt)

    asyncsend(subject, body)


def _loadcredentials():
    return os.environ['EMAIL_USER'], os.environ['EMAIL_PASSWORD']


def _recipients():
    return os.environ['EMAIL_RECIPIENTS'].split(',')


def _recipientsstr():
    return ', '.join(_recipients())


def _createmessage(subject, body):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = os.environ['EMAIL_USER']
    message['To'] = _recipientsstr()
    message.attach(MIMEText(body, 'plain', 'utf-8'))
    return message


def _login():
    user, password = _loadcredentials()
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.login(user, password)
    return server_ssl
