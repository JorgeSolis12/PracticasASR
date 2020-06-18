#!/usr/bin/env pythongns
import os
import time
import rrdtool
import tempfile
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from path import *

COMMASPACE = ', '
# Define params

width = '500'
height = '200'
# Generate charts for last 48 hours
enddate = 1509453300 #ultimo valor del XML
begdate = enddate - 172800


mailsender = "practicaasr4cv5@gmail.com"
mailreceip = "practicaasr4cv5@gmail.com"
mailserver = 'smtp.gmail.com: 465'
password = 'infinito12.'

def send_alert_attached(subject, name):
    """ Will send e-mail, attaching png
    files in the flist.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = COMMASPACE.join(mailreceip)
    png_file = pngpath + name + '.png'
    print (png_file)
    fp = open(png_file, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    mserver = smtplib.SMTP(mailserver)
    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()
