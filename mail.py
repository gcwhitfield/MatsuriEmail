# -*- coding: utf-8 -*-

import csv
import os
import glob

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

emailAddress = input("Please type your email address username: ")
password      = input("Please type your email password: ")

matsuriEmailData = 'mail-templates/matsuri-2018.txt'

##########################################################

###### STEPS:
######
###### 1.) Place the CSV file(s) downloaded from PayPal under MatsuriEmail
######
###### 2.) Edit subject (in "emailData.txt")
######
###### 3.) Edit messages (bodyEN in English and bodyJP in Japanese) (in "matsuri-2018.txt")
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

# read the email data from "emailData.txt"
def getEmailData(datafilepath):
    data = readFile(matsuriEmailData)
    subjectIndex = data.index('[email subject]')
    engBodyIndex = data.index('[body English]')
    jpBodyIndex = data.index('[body Japanese]')
    # remove the \n from the subject line
    subject = data[subjectIndex:engBodyIndex]
    subject = subject.strip()
    engBody = data[engBodyIndex:jpBodyIndex]
    engBody = engBody.strip() # get rid of trailing whitespace
    jpBody = data[jpBodyIndex:]
    jpBody = jpBody.strip() # get rid of trailing whitespace
    return subject, engBody, jpBody

def setup(addressBook, names, emails):
    index = 0
    for name in names:
        addressBook[name] = emails[index]
        index += 1

def checkCSV():
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

def create_message(fromAddr, toAddr, subject, body, encoding):
    msg = MIMEText(body, 'plain', encoding)
    msg['Subject'] = Header(subject, encoding)
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Date'] = formatdate()
    return msg

def send_via_gmail(fromAddr, toAddr, msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(emailAddress, password)
    s.sendmail([fromAddr], [toAddr], msg.as_string())
    s.close()

def run():
    data = checkCSV()
    if(data == ""):
        print("No file found in directory")
        return 
    for i in data:
        book = organize(i)
        for recepientName in book:
            if recepientName == "":
                print("ecountered NONE name!")
                continue # for errors

            fromAddr = emailAddress
            toAddr = book[recepientName]
            emailData = getEmailData(matsuriEmailData)

            # get email subject
            subject = emailData[0]
            # get english text and replace the name
            bodyEN = emailData[1]
            bodyEN.replace('$RECIPIENT_NAME', recepientName)
            # get japanese text and replace the name
            bodyJP = emailData[2]
            bodyJP.replace('$RECIPIENT_NAME', recepientName)

            textBreak = "---------------------------------------------------------------------------------\n\n"

            msg = create_message(fromAddr, toAddr, subject,
                                 bodyEN+textBreak+bodyJP, 'ISO-2022-JP')
            send_via_gmail(fromAddr, toAddr, msg)
            print (recepientName + "  sent!")

# run()
