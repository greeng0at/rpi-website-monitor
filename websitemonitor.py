"""Simple Website Monitor Script."""
"""sudo pip3 install Beautify4"""
"""sudo pip3 install lxml"""
"""https://bobbyhadz.com/blog/python-unicodeencodeerror-charmap-codec-cant-encode-characters-in-position"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

# paste this at the start of code

SMTP_USER=''
SMTP_PASSWORD=''
SMTP_HOST='smtp.gmail.com'
SMTP_PORT='465'
SMTP_SSL=True

SMTP_FROM_EMAIL='Richard.MittenTwo@gmail.com'
SMTP_TO_EMAIL='Richard.Mitten@gmail.com'

def email_notification(subject, message):
    """Send an email notification.

    message - The message to send as the body of the email.
    """
    if (SMTP_SSL):
        smtp_server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    else:
        smtp_server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)

    smtp_server.ehlo()
    smtp_server.login(SMTP_USER, SMTP_PASSWORD)

    email_text = \
"""From: %s
To: %s
Subject: %s 

%s
""" % (SMTP_FROM_EMAIL, SMTP_TO_EMAIL, subject, message)

    smtp_server.sendmail(SMTP_FROM_EMAIL, SMTP_TO_EMAIL, email_text)

    smtp_server.close()




def cleanup_html(html):
    """Cleanup the HTML content.

    html - A string containg HTML.
    """
    soup = BeautifulSoup(html, features="lxml")

    for s in soup.select('script'):
        s.extract()

    for s in soup.select('style'):
        s.extract()

    for s in soup.select('meta'):
        s.extract()

    return str(soup.encode("utf-8"))

def difference(string1, string2):
      # Split both strings into list items
  string1 = string1.split()
  string2 = string2.split()

  A = set(string1) # Store all string1 list items in set A
  B = set(string2) # Store all string2 list items in set B
 
  str_diff = A.symmetric_difference(B)
  isEmpty = (len(str_diff) == 0)
 
  if isEmpty:
    print("No Difference. Both Strings Are Same")
  else:
    print("The Difference Between Two Strings: ")
    print(str_diff)


def has_website_changed(website_url, website_name):
    """Check if a website has changed since the last request.

    website_url - URL that you want to monitor for changes.
    website_name - Name used for the cache file.
    """
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; PIWEBMON)',
        'Cache-Control': 'no-cache'
    }

    response = requests.get(website_url, headers=headers)

    if (response.status_code < 200 or response.status_code > 299):
        return -1

    response_text = cleanup_html(response.text)
    
    cache_filename = website_name + "_cache.txt"

    if not os.path.exists(cache_filename):
        file_handle = open(cache_filename, "wt")
        file_handle.write(response_text)
        file_handle.close()
        return 0

    file_handle = open(cache_filename, "r+")
    previous_response_text = file_handle.read()
    file_handle.seek(0)

    if response_text == previous_response_text:
        file_handle.close()

        return 0
    else:
        file_handle.truncate()
        file_handle.write(response_text)
        file_handle.close()
        difference( previous_response_text, response_text )
        return 1

def main():
    """Check if the passed in website has changed."""
    website_status = has_website_changed(sys.argv[1], sys.argv[2])
   

    if website_status == -1:
        email_notification("An Error has Occurred", "Error While Fetching " + sys.argv[1])
        print("Non 2XX response while fetching")
    elif website_status == 0:
        print("Website is the same")
    elif website_status == 1:
        email_notification("A Change has Occurred", sys.argv[1] + " has changed.")
        print("Website has changed")
        
if __name__ == "__main__":
    main()