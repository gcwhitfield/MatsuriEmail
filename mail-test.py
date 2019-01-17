# George Whitfield
# gwhitfie@andrew.cmu
# Jan 2019

import mail

# test the subject line, the english email, and the japanese email
def testEmailContents():
    # subject
    print('Subject: ', end='')
    print(mail.get_email_data(mail.EMAIL_DATA_FILEPATH)[0])
    print('__________________________________\n')
    # english email
    print("English Matsuri email:\n")
    print(mail.get_email_data(mail.EMAIL_DATA_FILEPATH)[1])
    print('__________________________________\n')
    # 日本語のメール
    print("日本語で書かれた「祭」メール:\n")
    print(mail.get_email_data(mail.EMAIL_DATA_FILEPATH)[2])

def testAll():
    testEmailContents()

testAll()