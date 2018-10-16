# -*- coding: utf-8 -*-
import smtplib
import pandas
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate
from names.names import Info

EMAIL_ADDRESS = 'your_email_adress@xyz.com'
PASSWORD      = 'your_password'

##########################################################

###### STEPS:
###### 
###### 1.) Modify line EMAIL_ADDRESS and PASSWORD above 
######     ----> account has to be configured on gmail to permit 3rd party access
######
###### 2.) Go to names.py in names folder
######
###### 3.) Go to downloaded .csv file
######
###### 4.) Copy and paste names column to self.names, emails to self.emails
######     ----> Has to be in correct order (sorted) from spreadsheet
######     ----> e.g. first name in self.names should correspond to
######                first email in self.emails
######
###### 5.) Edit subject
######
###### 6.) Edit messages (bodyEN in English and bodyJP in Japanese)
######
###### 7.) uncomment run() at the very bottom of this file, then run


###### * TEST WITH YOUR OWN NAME AND EMAIL ADDRESS IN names.py FIRST!!*

##########################################################

def setup(addressBook, names, emails):
    index = 0
    for name in names:
        addressBook[name] = emails[index]
        index += 1

def organize():
    data = pandas.read_csv('./sample.csv')
    names = data['Name'].tolist()
    emails = data['To Email Address'].tolist()
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
    book = organize()

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

# run()
