# -*- coding: utf-8 -*-

import csv
import os
import glob

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

EMAIL_ADDRESS = input("Please type your email address username: ")
PASSWORD      = input("Please type your email password: ")

EMAIL_DATA_FILEPATH = 'Email_Text_Files/email_data.txt'

##########################################################

###### STEPS:
######
###### 1.) Place the CSV file(s) downloaded from PayPal under MatsuriEmail
######
###### 2.) Edit subject (in "email_data.txt")
######
###### 3.) Edit messages (bodyEN in English and bodyJP in Japanese) (in "email_data.txt")
######
###### 4.) Uncomment run() at the very bottom of this file, then run
######
###### 5.) Input your email username and password when prompted

###### * TEST WITH YOUR OWN NAME AND EMAIL ADDRESS FIRST!!*

##########################################################

# copied from the 15-112 website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# read the email data from "email_data.txt"
def get_email_data(datafilepath):
    data = readFile(EMAIL_DATA_FILEPATH)
    step1 = data.split('*')
    subject = step1[1]
    # remove the \n from the subject line
    subject = subject.replace('\n', '')
    engBody = step1[3]
    engBody = engBody.strip() # get rid of trailing whitespace
    jpBody = step1[5]
    jpBody = jpBody.strip() # get rid of trailing whitespace
    return subject, engBody, jpBody

def setup(addressBook, names, emails):
    index = 0
    for name in names:
        addressBook[name] = emails[index]
        index += 1

def check_csv():
    ext1 = 'CSV'
    ext2 = 'csv'
    CSV = [i for i in glob.glob('*.{}'.format(ext1))]
    csv = [i for i in glob.glob('*.{}'.format(ext2))]
    if (len(CSV)==0):
        if (len(csv)==0):
            return ""
        else:
            return csv
    else:
        if (len(csv)==0):
            return CSV  
        else:
            return CSV + csv 

def organize(fileName):
    if (fileName != ""):
        with open(fileName, 'rU', encoding='utf8') as info:
            reader = csv.DictReader(info)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]
        names = data['Name']
        emails = data['From Email Address']
        addressBook = dict()
        setup(addressBook, names, emails)
        return addressBook

def create_message(from_addr, to_addr, subject, body, encoding):
    msg = MIMEText(body, 'plain', encoding)
    msg['Subject'] = Header(subject, encoding)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send_via_gmail(from_addr, to_addr, msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(EMAIL_ADDRESS, PASSWORD)
    s.sendmail([from_addr], [to_addr], msg.as_string())
    s.close()

def run():
    data = check_csv()
    if(data == ""):
        print("No file found in directory")
        return 
    for i in data:
        book = organize(i)
        for recepientName in book:
            if recepientName == "":
                print("ecountered NONE name!")
                continue # for errors

            from_addr = EMAIL_ADDRESS
            to_addr = book[recepientName]
            email_data = get_email_data(EMAIL_DATA_FILEPATH)

            # get email subject
            subject = email_data[0]
            # get english text and replace the name
            bodyEN = email_data[1]
            bodyEN.replace('RECIPIENT_NAME', recepientName)
            # get japanese text and replace the name
            bodyJP = email_data[2]
            bodyJP.replace('RECIPIENT_NAME', recepientName)

            textBreak = "---------------------------------------------------------------------------------\n\n"

            msg = create_message(from_addr, to_addr, subject,
                                 bodyEN+textBreak+bodyJP, 'ISO-2022-JP')
            send_via_gmail(from_addr, to_addr, msg)
            print (recepientName + "  sent!")

# run()
