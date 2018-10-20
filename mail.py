# -*- coding: utf-8 -*-
import smtplib
import csv
import os
import glob
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

EMAIL_ADDRESS = 'your_email_adress@xyz.com'
PASSWORD      = 'your_password'

##########################################################

###### STEPS:
###### 
###### 1.) Modify line EMAIL_ADDRESS and PASSWORD above 
######     ----> account has to be configured on gmail to permit 3rd party access
######
###### 2.) Place the CSV file with the information in the same directory as this file
######
###### 3.) Edit subject
######
###### 4.) Edit messages (bodyEN in English and bodyJP in Japanese)
######
###### 5.) uncomment run() at the very bottom of this file, then run


###### * TEST WITH YOUR OWN NAME AND EMAIL ADDRESS FIRST!!*

##########################################################

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
        with open(fileName, 'rU') as info:
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
    for i in data:
        if(data == ""):
            print("No file found in directory")
            return 
            
        book = organize(i)
        
        for recepientName in book:
            
            if recepientName == "":
                print("ecountered NONE name!")
                continue # for errors
            
            from_addr = EMAIL_ADDRESS
            to_addr = book[recepientName]
            subject = "Matsuri 2018 Ticketing //「祭」チケットについて"
            
            bodyEN = "Dear %s, \n\n\
    Hello!\n\n\
    You are receiving this message because you have purchased a ticket for Matsuri last year. \n\n\
    We are excited to invite you back to the flagship event of the Japanese Student Association, MATSURI.\n\n\
    The event will be held on the 10th of April (Tuesday) this year. We hope to deliver the uniqueness of Japanese culture in the Wiegand Gym this year!\n\n\
    With that being said, we would like to announce the release of the online tickets for Matsuri 2018, and offer you the notification of details. \n\n\
        - Tickets preordered online will have a 10 percent discount\n\
        - Tickets can be picked up at a booth during the event without queueing\n\
        - Tickets can be ordered via https://cmujsa.com/matsuri/tickets/\n\n\
    For questions or more information about the event, please contact rkhorana@cmu.edu (JSA President) \n\n\
    We hope you come back and enjoy the event with us! \n\n\
    Matsuri website: https://matsuri.cmujsa.com\n\n" % recepientName
            
            textBreak = "---------------------------------------------------------------------------------\n\n"
            
            bodyJP = "%s様、 \n\n\
    こんにちは！\n\n\
    昨年カーネギーメロン大学で開催された「祭」というイベントでチケットをオンライン予約購入していただいた方にメールを送らせていただいております。 \n\n\
    今年度は4月10日（火）に「祭」を開催することになりました。\n\n\
    つきましては、昨年大変お世話になりました皆様に２０１８年度オンラインチケット予約のご案内をさせていただきます。\n\n\
        - オンライン予約されたチケットはすべて10パーセント割引とさせて頂きます\n\
        - 当日、予約されたチケットは別カウンターにて待ち時間０でお手渡し致します\n\
        - チケット予約はこちらから https://cmujsa.com/matsuri/tickets/\n\n\
    ご質問等ございましたら rkhorana@cmu.edu (JSA会長) までよろしくお願い致します。\n\n\
    「祭」でお会いしましょう！ \n\n\
    祭ウェブサイト：https://matsuri.cmujsa.com\n\n" % recepientName
            
            msg = create_message(from_addr, to_addr, subject, bodyEN+textBreak+bodyJP,'ISO-2022-JP')
            
            send_via_gmail(from_addr, to_addr, msg)
            
            print (recepientName + "  sent!")

#run()