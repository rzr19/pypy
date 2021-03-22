import smtplib

DEFAULT_EMAIL_ADDRESS = None

def sendemail( message, subject, to_addr = None ):
    """ Simple function to send emails. Default server used is the localhost,
        so there should be a simple SMTP-able MTA agent on the server where you runt this.
        :param message: The body of the message.
        :param subject: The subject of the message.
        :param to_addr: The destination email address.
    """

    if (to_addr is None) or (not isinstance( to_addr, (str, unicode) ) ):
        to_addr = DEFAULT_EMAIL_ADDRESS

    sender = 'info@server.com'
    receivers = [ to_addr ]
    message = ("From: %s\n" % sender) + \
              ("To: %s\n" % to_addr) + \
              ("Subject: %s\n\n" % subject ) + \
              message

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        print( "Successfully sent email to '%s'" % to_addr )
    except:
        print( "Error: unable to send email to '%s'" % to_addr )
