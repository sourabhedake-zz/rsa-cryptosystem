from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required	
from django.shortcuts import render,redirect,render_to_response
from django.template import loader, Context
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from rsa.models import *
import os
import math
import calendar
import time
def firstpage(request):
		return render(request,'login.html')

@csrf_exempt
def showsignup(request):
	return render(request,"register.html")

@csrf_exempt
def homepage(request):
	print "ss"
	if request.method=='POST':
		print "ssgot"
		username=request.POST.get("username")
		passwd=request.POST.get("password")
		print username, passwd	
		res=authenticate(username=username,password=passwd)

		if res is not None:
			print username , "logged in with passwd ", passwd
			login(request,res)
			return render(request,"home.html")
		else :
		
			return HttpResponse("failed")	
	else:
		return render(request,"login.html")
	

@csrf_exempt
def download(request):
	if not request.GET.get('x'):
		our_file=open("/home/sourabh/crypto/upload/" + str(request.user.username) + "/output.txt","r+")
		data=our_file.read()
		our_file.close()
		response     = HttpResponse(data,'application/text')
		response['Content-Length']      = "/home/sourabh/crypto/upload/" + str(request.user.username) + "/output.txt" 
		response['Content-Disposition'] = 'attachment; filename="encrpted.txt"'
	else:
		our_file=open("/home/sourabh/crypto/upload/" + str(request.user.username) + "/decrypt.txt","r+")
		data=our_file.read()
		our_file.close()
		response     = HttpResponse(data,'application/text')
		response['Content-Length']      = "/home/sourabh/crypto/upload/" + str(request.user.username) + "/decrypt.txt" 
		response['Content-Disposition'] = 'attachment; filename="decrpted.txt"'
	return response

@csrf_exempt
def signup(request):									

	if request.POST.get("permit"):
		uid=request.POST.get("username")									
		password=request.POST.get("password")
		
		if uid and password : 

			u2 =user.objects.filter(user_id  = uid)
			if(len(u2)>0):
				return render(request,'register.html',{'log': 'failed'})
			else:

				lst = generateKey()
				user1=User.objects.create_user(uid)
				user1.set_password(password)
				user1.n = lst[0]
				user1.e = lst[1]
				user1.d = lst[2]
				user1.save()

				u = user(user_id=uid)
				u.n = lst[0]
				u.e = lst[1]
				u.d = lst[2]
				u.save()

				return render(request,"login.html")
		else:
			u="****ALL FIELDS REQUIRED****"
			return render(request,"register.html",{'message':u})


	else:
		return render(request,"login.html")


@csrf_exempt
def upload(request):
	if request.FILES:													#if user uploadds file
		for filename,file in request.FILES.iteritems():
			name=request.FILES[filename].name							#getting data and name of the uploaded file
			data=request.FILES[filename].read()

		os.system("mkdir /home/sourabh/crypto/upload")
		os.system("rm -r /home/sourabh/crypto/upload/" + str(request.user.username))
		os.system("mkdir /home/sourabh/crypto/upload/" + str(request.user.username))
		if not request.GET.get('x'):
			os.system("touch /home/sourabh/crypto/upload/" + str(request.user.username) + "/data.txt")
			our_file=open("/home/sourabh/crypto/upload/" + str(request.user.username) + "/data.txt","r+")
			our_file.write(data)
			our_file.close()
			rsa(request)
		else:
			os.system("touch /home/sourabh/crypto/upload/" + str(request.user.username) + "/output.txt")
			our_file=open("/home/sourabh/crypto/upload/" + str(request.user.username) + "/output.txt","r+")
			our_file.write(data)
			our_file.close()
			decrypt(request)

		if not request.GET.get('x'):
			return render(request, "enc.html",{"rsaDone":"1"})
		return render(request, "dec.html",{"rsaDone":"1"})
	else:
		if not request.GET.get('x'):
			return render(request, "enc.html")
		return render(request, "dec.html")


@csrf_exempt
def enc(request):
	return render(request, "enc.html")

@csrf_exempt
def dec(request):
	return render(request, "dec.html")


def isprime(num):
	if (num<=1):
		return 0;
	elif (num<=3):
		return 1;
	elif (num%2==0) or (num%3==0):
		return 0;
	i=5;
	sqrtofnum=math.sqrt(num);
	while(i<=sqrtofnum):
		if (num%i==0) or ((num%(i+2))==0):
			return 0;
		i=i+6;
	return 1;

#to calculate inverse function
def modinverse(a ,m):
	a=a%m;
	for x in range(1,m-1):
		if((a*x)%m==1):
			return x;

def generateKey():
	year=(int)(time.strftime("%y"));
	month=(int)(time.strftime("%m"));
	date=(int)(time.strftime("%d"));
	tm=(calendar.timegm(time.gmtime()));

	finalvalue=year+month+date+tm;

	flag=0;

	# fi random range bcoz for needs 2 arg
	fi=finalvalue+1200;

	#for first prime number
	p1=0
	for p1 in range(finalvalue,fi):
		p1=p1%90
		if (isprime(p1)):
			if (p1>10):
				prm1=p1;	
				print "first prime: ",prm1;
				break;

	counter=0;
	#for second prime number
	for p1 in range(finalvalue+prm1,fi):
		p1=p1%90
		if (isprime(p1)):
			if (p1>10 and p1!=prm1):
				prm2= p1;
				print "2nd prime: ",prm2
				break;

	#now multiplication of two prime numbers
	n=prm1*prm2;

	#compute Euler's totient function
	tfun=(prm1-1)*(prm2-1)
	#print "totient fun: ",tfun

	#calculate e
	for i in range(2,tfun):
		if(isprime(i)):
			if(tfun%i!=0):
				e=i;
				#print e;
				break;

	#calculate multiplicative modulo inverse
	d=modinverse(e,tfun);
	return [n,e,d]

def rsa(request):
	#public key=(e,n)
	#private key=(d,n)
	uid=str(request.user.username)
	u2 =user.objects.filter(user_id  = uid)
	
	n = u2[0].n
	e = u2[0].e
	d = u2[0].d
	f=open('/home/sourabh/crypto/upload/' + str(request.user.username) + '/data.txt','r')
	fo=open('/home/sourabh/crypto/upload/' + str(request.user.username) + '/output.txt','w+')
	print e , n, d

	i=1
	for ch in iter(lambda: f.read(1), ''):
		data = ord(ch)
		m1=pow(int(data),e)
		encrypted=m1%n
		encrypted=str(encrypted)+" "	
		fo.write(encrypted)
		i+=1
		if i%10==0:
			fo.write("\n")		
	fo.close()		
	f.close()


def decrypt(request):
	uid=str(request.user.username)
	u2 =user.objects.filter(user_id  = uid)
	
	n = u2[0].n
	e = u2[0].e
	d = u2[0].d
	f1=open('/home/sourabh/crypto/upload/' + str(request.user.username) + '/output.txt','rb')
	
	f=open('/home/sourabh/crypto/upload/' + str(request.user.username) + '/decrypt.txt','w+')
	txt =""

	for line in f1:
		spl = line.split()
		tmp=""
		for x in spl:
			m2=pow(int(x),d)
			decrypted=m2%n
			txt += unichr(decrypted)
			tmp += unichr(decrypted)
		f.write(tmp)
	print txt
	f.close()
	f1.close()

