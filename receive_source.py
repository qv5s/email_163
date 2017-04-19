import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class Erec(object):
    def __init__(self,user,password):
        server_pop='pop.163.com'
        pop3=poplib.POP3(server_pop)
        pop3.user(user)
        pop3.pass_(password)
        self.pop3=pop3

    def FandT(self,data):
        f=data.get('From')
        name,addr=parseaddr(f)
        name,charset=decode_header(name)[0]
        if charset:
            name=name.decode(charset)
        return (name,addr)

    def s(self,data):
        subject=data.get('Subject')
        subject,charset=decode_header(subject)[0]
        if charset:
            subject=subject.decode(charset)
        return subject

    def content_rec(self,data):
        c=[]
        if data.is_multipart():
            part=data.get_payload()
            for i in part:
                content_type=i.get_content_type()
                if content_type == 'text/html' or content_type == 'text/plain':
                    content=i.get_payload(decode=True)
                    charset=i.get_charset()
                    if charset is None:
                        charset=i.get('Content-Type').lower()
                        pos=charset.find('charset=')
                        if pos>=0:
                            charset=charset[pos+8:]
                    if charset:
                        content=content.decode(charset)
                        c.append(content)
        return c


    def message(self):
        num,size=self.pop3.stat()
        choice_1=self.choice_1(num)
        for i in choice_1:
            i=int(i)
            data=self.pop3.retr(i)[1]
            data=b'\r\n'.join(data).decode('utf-8')
            data=Parser().parsestr(data)
            subject=self.s(data)
            message=self.content_rec(data)
            from_name,from_addr=self.FandT(data)
            print('主题：',subject)
            print('发件人:%s\n邮箱地址:%s'%(from_name,from_addr))
            n=1
            print('内容:')
            for i in message:
                print('part%d:\n%s'%(n,i))
                n=n+1
            print('---------------------------------')



    def choice_1(self,num):
        print('邮箱共有%d封邮件'%num)
        print('1.选择单封邮件')
        print('2.选择多封邮箱')
        c1=input('选择:')
        if c1 == '1':
            print('----------------------')
            c2=input('输入邮件编号:')
            return (c2,)
        elif c1 == '2':
            data=input('输入邮件编号(使用,分开):')
            data=data.split(',')
            return data
if __name__=='__main__':
    user=input('输入账号:')
    password=input('输入密码或授权码:')
    test=Erec(user,password)
    test.message()


