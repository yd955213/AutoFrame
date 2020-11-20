# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   myEmail.py
@Time   :   2020-11-20 9:23
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   SMTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件。

Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件

smtplib.SMTPAuthenticationError: (535, b'Error: authentication failed')
解决办法使用163邮箱服务器来发送邮件,我们需要去163邮箱开启POP3/SMTP服务,这时163邮件会让我们设置客户端授权码，
（参考链接https://jingyan.baidu.com/article/c275f6ba33a95de33d7567d9.html）

新浪邮箱smtp服务器
外发服务器:smtp.vip.sina.com
收件服务器:pop3.vip.sina.com
新浪免费邮件
外发服务器:smtp.sina.com.cn
收件服务器:pop3.sina.com.cn
163邮箱smtp服务器
pop： pop.163.com
smtp： smtp.163.com
QQ邮箱smtp服务器及端口
接收邮件服务器：imap.exmail.qq.com，使用SSL，端口号993
发送邮件服务器：smtp.exmail.qq.com，使用SSL，端口号465或587
yahoo邮箱smtp服务器
接：pop.mail.yahoo.com.cn
发：smtp.mail.yahoo.com
126邮箱smtp服务器
pop： pop.126.com
smtp： smtp.126.com
新浪免费邮箱
POP3：pop.sina.com
SMTP：smtp.sina.com
SMTP端口号：25
新浪VIP邮箱
POP3：pop3.vip.sina.com
SMTP：smtp.vip.sina.com
SMTP端口号：25
新浪企业邮箱
POP3：pop.sina.com
SMTP：smtp.sina.com
SMTP端口号：25
雅虎邮箱
POP3：pop.mail.yahoo.cn
SMTP：smtp.mail.yahoo.cn
SMTP端口号：25
搜狐邮箱
POP3：pop3.sohu.com
SMTP：smtp.sohu.com
SMTP端口号：25
TOM邮箱
POP3：pop.tom.com
SMTP：smtp.tom.com
SMTP端口号：25
Gmail邮箱
POP3：pop.gmail.com
SMTP：smtp.gmail.com
SMTP端口号：587 或 25
QQ邮箱
POP3：pop.exmail.qq.com
SMTP：smtp.exmail.qq.com
SMTP端口号：25
263邮箱
域名：263.net
POP3：263.net
SMTP：smtp.263.net
SMTP端口号：25
域名：x263.net
POP3：pop.x263.net
SMTP：smtp.x263.net
SMTP端口号：25
域名：263.net.cn
POP3：263.net.cn
SMTP：263.net.cn
SMTP端口号：25
域名：炫我型
POP3：pop.263xmail.com
SMTP：smtp.263xmail.com
SMTP端口号：25
21CN 免费邮箱
POP3：pop.21cn.com
SMTP：smtp.21cn.com
IMAP：imap.21cn.com
SMTP端口号：25
21CN 经济邮邮箱
POP3：pop.21cn.com
SMTP：smtp.21cn.com
SMTP端口号：25
21CN 商务邮邮箱
POP3：pop.21cn.net
SMTP：smtp.21cn.net
SMTP端口号：25
21CN 快感邮箱
POP3：vip.21cn.com
SMTP：vip.21cn.com
SMTP端口号：25
21CN Y邮箱
POP3：pop.y.vip.21cn.com
SMTP：smtp.y.vip.21cn.com
SMTP端口号：25
中华网任我邮邮箱
POP3：rwpop.china.com
SMTP：rwsmtp.china.com
SMTP端口号：25
中华网时尚、商务邮箱
POP3：pop.china.com
SMTP：smtp.china.com
SMTP端口号：25
"""
import smtplib
from email.utils import parseaddr, formataddr
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def _format_address(s):
    name, address = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), address))


from_addr = '664720125@qq.com'
password = 'yjlsrkowzszfbbhc'   # STMP服务授权码
to_addr = 'yd955213@163.com'
# smtp_server = 'smtp.163.com'
smtp_server = 'smtp.qq.com'

subject = "邮件标题"  # 主题
content = "邮件内容，我是邮件内容，哈哈哈"
# 生成一个MIMEText对象（还有一些其它参数）
msg = MIMEText(content)
# 放入邮件主题
msg['Subject'] = subject
# 也可以这样传参
# msg['Subject'] = Header(subject, 'utf-8')
# 放入发件人
msg['From'] = _format_address('yangd<%s>' % from_addr)
# 放入收件人
msg['To'] = _format_address('四大护法<%s>' % to_addr)
print(msg['To'])
# 使用ssl方式发送：发送邮件的服务器地址、端口
s = smtplib.SMTP_SSL(smtp_server)
# 打印日志信息
s.set_debuglevel(1)
# 登录邮箱
s.login(from_addr, password)
# 发送邮件：发送方，收件方，信息
s.sendmail(from_addr, to_addr, msg.as_string())
s.quit()
print('ok')
