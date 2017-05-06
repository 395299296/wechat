import re

s = '电话:18910248080，微信号：weiweiq1234，联系QQ号码12345678，陌陌yueba4321,INSTAGRAMlalalademaxiya三围:83-62-88鞋码:37，请备注\n'
pattern = re.compile(r'三围.*?\d{2}\D?\d{2}\D?\d{2}', re.IGNORECASE)
sanwei = re.findall(pattern, s)
if sanwei:
    pattern = re.compile(r'\d{2}\D?\d{2}\D?\d{2}', re.IGNORECASE)
    sanwei = re.findall(pattern, sanwei[0])
    print('三围:'+sanwei[0])

pattern = re.compile(r'1\d{10}', re.IGNORECASE)
phone = re.findall(pattern, s)
if phone:
    print('手机:'+phone[0])

pattern = re.compile(r'微信.*?[A-Za-z0-9_]+', re.IGNORECASE)
wechat = re.findall(pattern, s)
if wechat:
    pattern = re.compile(r'[A-Za-z0-9_]+', re.IGNORECASE)
    wechat = re.findall(pattern, wechat[0])
    print('微信:'+wechat[0])

pattern = re.compile(r'Q.*?[1-9]\\d{4,10}', re.IGNORECASE)
qq = re.findall(pattern, s)
if qq:
    pattern = re.compile(r'[1-9]\\d{4,10}', re.IGNORECASE)
    qq = re.findall(pattern, qq[0])
    print('QQ:'+qq[0])

pattern = re.compile(r'陌陌.*?[A-Za-z0-9_]+', re.IGNORECASE)
momo = re.findall(pattern, s)
if momo:
    pattern = re.compile(r'[A-Za-z0-9_]+', re.IGNORECASE)
    momo = re.findall(pattern, momo[0])
    print('陌陌:'+momo[0])

pattern = re.compile(r'instagram.*?[A-Za-z0-9_]+', re.IGNORECASE)
instagram = re.findall(pattern, s)
if instagram:
    pattern = re.compile(r'instagram', re.IGNORECASE)
    instagram = re.sub(pattern, '', instagram[0])
    pattern = re.compile(r'[A-Za-z0-9_]+', re.IGNORECASE)
    instagram = re.findall(pattern, instagram)
    print('Instagram:'+instagram[0])

if s[-1] == '\n':
    print("======================")