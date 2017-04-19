import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr,formataddr
from email.header import Header
class Esend(object):
    def __init__(self,user,password,send_name,subject,receive_name,receive_addr,*args):
        self.user=user
        self.password=password
        self.receive_name=receive_name
        self.attached=args[0]
        self.smtp_server='smtp.163.com'
        self.send_name=send_name
        self.receive_addr=receive_addr
        self.subject=subject
        self.base=os.path.dirname(__file__)

    def PandF(self,s):
        name,addr=parseaddr(s)
        return formataddr((Header(name,'utf-8').encode(),addr))

    def message_config(self):
        message=MIMEMultipart()
        message['Subject']=self.subject
        message['From']=self.PandF('%s<%s>'%(self.send_name,self.user))
        message['To']=self.PandF('%s<%s>'%(self.receive_name,self.receive_addr))
        part=[]
        with open(os.path.join(self.base,self.attached[0]),'rb') as f:
            content=f.read()
        if os.path.splitext(self.attached[0])[1] !='html':
            part.append(MIMEText(content,'plain','utf-8'))
        else:
            part.append(MIMEText(content,'html','utf-8'))
        for fj in self.attached[1:]:
            if os.path.splitext(fj)[1] == '.jpg' or os.path.splitext(fj)[1] =='.png':
                with open(os.path.join(self.base, fj),'rb') as f:
                    p=MIMEImage(f.read())
                    p['Content-Type']='application/octet-stream'
                    p['Content-Disposition']='attachment;filename="%s"'%(fj)
                print(fj)
                part.append(p)
            else:
                with open(os.path.join(self.base, fj),'rb') as f:
                    content = f.read()
                    p=MIMEText(content,'plain','utf-8')
                    p['Content-Type']='application/octet-stream'
                    p['Content-Disposition']='attachment;filename="%s"'%(fj)
                part.append(p)
        for i in part:
            message.attach(i)
        return message




    def smtp_config(self):
        smtp=smtplib.SMTP()
        smtp.connect(self.smtp_server,25)
        smtp.login(self.user,self.password)
        message=self.message_config()
        smtp.sendmail(self.user,self.receive_addr,message.as_string())
        smtp.quit()
        print('发送成功')
def email_send_init():
    user=input('输入发送者邮箱:')
    password=input('输入密码或授权码:')
    send_name=input('发送者名字:')
    subject=input('发送主题:')
    receive_name=input('接收者名字:')
    receive_addr=input('接收者邮箱:')
    fj=[]
    f=input('正文文件(程序所在文件夹):')
    fj.append(f)
    while True:
        f=input('附件文件，输入exit结束(程序所在文件夹):')
        if f != 'exit':
            fj.append(f)
        else:
            break
    message=[user,password,send_name,subject,receive_name,receive_addr,fj]
    return message
if __name__=='__main__':
    message=email_send_init()
    test=Esend(*message)
    test.smtp_config()