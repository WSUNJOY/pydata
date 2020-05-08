# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: Mail.py
@time: 2020/5/6 3:17 下午
@description: 
"""
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders
from pathlib import Path

from base.GetPath import GetPath


class Mail(object):

    def __init__(self):
        self._mail_server = 'smtp.126.com'
        self._from_who = ''
        self._to_who = []
        self._msg = None

    @property
    def mail_server(self):
        return self._mail_server

    @mail_server.setter
    def mail_server(self, value):
        if isinstance(value, str):
            self._mail_server = value
        else:
            raise Exception("value is None")

    @property
    def from_who(self):
        return self._from_who

    @from_who.setter
    def from_who(self, value):
        if isinstance(value, str):
            self._from_who = value
        else:
            raise Exception("value is None")

    @property
    def to_who(self):
        return self._to_who

    @to_who.setter
    def to_who(self, value):
        if isinstance(value, list):
            self._to_who = value
        else:
            raise Exception("value is None")

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        if isinstance(value, str):
            self._msg = value
        else:
            raise Exception("value is None")

    def send_mail(self, pwd):
        if self.mail_server:
            try:
                s = SMTP_SSL(self.mail_server, 465)
                print("login")
                s.login(self.from_who, pwd)
                print("sent")
                s.sendmail(self.from_who, self.to_who, self.msg.as_string())
                print('quit')
                s.quit()
                print("SSL mail sent!")
            except Exception as e:
                print(e)
        else:
            raise Exception("mail_server is None")

    def mail_content(self, subject=None, from_who=None,
                     to_alias=None, text=None, attachment=None):
        """
        :param subject: mail subject
        :param from_who: mail from who
        :param to_alias: mail to who's alias
        :param text: mail content text
        :param attachment: attachment file path
        :return:
        """
        content = MIMEMultipart()
        if isinstance(subject, str):
            content["Subject"] = Header(subject, 'utf-8')
        else:
            content["Subject"] = Header(None, 'utf-8')
        if isinstance(from_who, str):
            content["From"] = from_who
        else:
            content["From"] = self.from_who
        to = str(self.to_who).lstrip('[').rstrip(']')
        if isinstance(to_alias, str):
            # content["To"] = Header(to_alias, 'utf-8')  ## 接收者的别名
            content["To"] = formataddr((to_alias, to))
        else:
            content["To"] = formataddr((to, to))  ## 接收者的别名
        if isinstance(text, str):
            content.attach(MIMEText(text, "plain", 'utf-8'))
        if attachment:
            if Path(attachment).exists():
                att_path = Path(attachment)
                # way1
                # att = MIMEText(open(att_path).read(), 'base64', 'utf-8')
                # att["Content-Type"] = 'application/octet-stream'
                # att["Content-Disposition"] = 'attachment; filename={}'.format(att_path.name)

                # way2
                att = MIMEBase('file', att_path.suffix, filename=att_path.name)
                att.add_header('content-disposition', 'attachment',
                               filename=att_path.name)
                att.add_header('Content-ID', '<0>')
                att.add_header('X-Attachment-Id', '0')
                att_file = open(att_path, 'rb')
                att.set_payload(att_file.read())
                encoders.encode_base64(att)
                att_file.close()

                content.attach(att)
            else:
                raise Exception("attachment is not exists!")
        self._msg = content


if __name__ == "__main__":
    path_obj = GetPath()
    data_path = path_obj.data_path()
    att_html = data_path.joinpath('report.html')
    from_who = 'xxx@126.com'
    to_who = ['xxxxx@qq.com', 'xxxxxxx@126.com']
    mail_content = "hello ~"
    subject = 'hi~'
    pwd = 'xx'
    m = Mail()
    # m.mail_server = 'smtp.126.com'
    m.from_who = from_who
    m.to_who = to_who
    m.mail_content(subject=subject, to_alias='honey', text=mail_content,
                   attachment=att_html)
    m.send_mail(pwd=pwd)
