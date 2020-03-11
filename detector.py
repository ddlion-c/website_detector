# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scape runs)
import time

# Import smtplib (to allow us to email)
import smtplib

import sys
import os.path
import urllib.request as urllib

# This is a pretty simple script. The script downloads the homepage of VentureBeat, and if it finds some text, emails me.
# If it does not find some text, it waits 60 seconds and downloads the homepage again.

class Detector:
    def __init__(self):
        url = 'https://www.ontario.ca/page/2020-ontario-immigrant-nominee-program-updates'
        saved_time_file = 'last time check.txt'

        request = urllib.Request(url)
        if os.path.exists(saved_time_file):
            """ If we've previously stored a time, get it and add it to the request"""
            last_time = open(saved_time_file, 'r').read()
            request.add_header("If-Modified-Since", last_time)

        try:
            response = urllib.urlopen(request)  # Make the request
        except urllib.HTTPError as err:
            if err.code == 304:
                print
                "Nothing new."
                sys.exit(0)
            raise  # some other http error (like 404 not found etc); re-raise it.

        last_modified = response.info().get('Last-Modified', False)
        if last_modified:
            open(saved_time_file, 'w').write(last_modified)
        else:
            print("Server did not provide a last-modified property. Continuing...")
            """
            Alternately, you could save the current time in HTTP-date format here:
            http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3
            This might work for some servers that don't provide Last-Modified, but do
            respect If-Modified-Since.
            """

        """
        You should get here if the server won't confirm the content is old.
        Hopefully, that means it's new.
        HTML should be in response.read().
        """

        if last_time != last_modified:
            # create an email message with just a subject line,
            msg = 'Subject: https://www.ontario.ca/page/2020-ontario-immigrant-nominee-program-updates'
            # set the 'from' address,
            fromaddr = 'From'
            # set the 'to' addresses,
            toaddrs = ['To']

            # setup the email server,
            server = smtplib.SMTP('smtp.gmail.com', 587)
            # server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            # add my account login name and password,
            server.login('acc', 'pw')

            # Print the email's contents
            print('MODIFIED!')
            print('From: ' + fromaddr)
            print('To: ' + str(toaddrs))
            print('Message: ' + msg)

            # send the email
            server.sendmail(fromaddr, toaddrs, msg)
            # disconnect from the server
            server.quit()


def main():
    Detector()


if __name__ == '__main__':
    main()

