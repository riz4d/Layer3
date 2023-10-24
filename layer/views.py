from django.shortcuts import render,redirect,HttpResponse
from .forms import user_login,user_cr
from .models import userlog
from django.contrib.auth import authenticate
import random
from twilio.rest import Client
import pyrebase
import string
from django.contrib import messages
from django.contrib.auth.models import User
from .config import keys,firebase_config,auth_token,account_sid,registered_twilio_number
from .otp import generate_otp
characters = string.ascii_letters + string.digits

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

client = Client(account_sid, auth_token)


def send_verification_code(phone_number, verification_code):
    try:
        message = client.messages.create(
            to=phone_number,
            from_=registered_twilio_number,
            body=f"Your verification code Of Three Layer Sec : {verification_code}"
        )
        phno = str(phone_number).lstrip("+")
        data = {"code" : verification_code,"status" : "pending"}
        db.child(phno).set(data)
        print(f"Verification code sent to {phone_number}.")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        
def logged(request):
    if 'username' in request.session:
        return render(request,'home.html')
    else:
        return redirect(login)
def signup(request):
    form = user_cr()
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get("userid")
        password = request.POST.get("passwd")
        email = request.POST.get("email")
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = request.POST.get("firstnm")
        user.last_name = request.POST.get("lastnm")
        user.save()
        request.session['layer3'] = "true"
        request.session['iuser'] = username
        return redirect(threelayercr)
    context={'form':form}
    return render(request,'signup.html',context)
def threelayercr(request):
    print(request.session['iuser'])
    if request.session['layer3']=='true':
        if request.method == "POST":
            try:
                selected_order=request.POST.get("passphrase")
                str_select_odr = str(selected_order).replace(', ','')
                list_select_odr = list(str_select_odr)
                pwd_len = len(list_select_odr)
                user_pwd=""
                for i in list_select_odr:
                    user_pwd+=keys[int(i)-1]
                print(user_pwd)
                user_num = "91"+request.session['iuser']
                data={"hash" : user_pwd}
                pwdphrase = db.child("passphrases").child(user_num).set(data)
                if True:
                    request.session.flush()
                    return redirect(login)
                else:
                    return HttpResponse("Invalid Login")
            except:
                pass
        else:
            return render(request,'index.html')
    else:
        return redirect(login)
def home(request):
    if 'username' in request.session:
        if "layer3pass" in request.session:
            return redirect(logged)
        else:
            print(request.session['username'])
            user_num = "91"+request.session['username']
            auth_satus = db.child(user_num).get().val().get("status")
            print(auth_satus)
            if auth_satus == "approved":
                if request.method == "POST":
                    try:
                        selected_order=request.POST.get("passphrase")
                        str_select_odr = str(selected_order).replace(', ','')
                        list_select_odr = list(str_select_odr)
                        pwd_len = len(list_select_odr)
                        user_pwd=""
                        for i in list_select_odr:
                            user_pwd+=keys[int(i)-1]
                        print(user_pwd)
                        pwdphrase = db.child("passphrases").child(user_num).get().val().get("hash")
                        print(pwdphrase)
                        if user_pwd == pwdphrase:
                            request.session['layer3pass'] = "true"
                            return redirect(logged)
                        else:
                            messages.error(request, 'Incorrect method')
                            return redirect(login)
                    except Exception as e:
                        print(e)
                        pass
                else:
                    return render(request,'index.html')
            else:
                request.session.flush()
                return redirect(login)
    else:
        return redirect(login)

def login(request):
    form = user_login()
    if 'username' in request.session:
        if "2fauth" in request.session:
            return redirect(home)
        else:
            if request.method == "POST":
                otpcred = request.POST
                first= otpcred.get("first")
                second= otpcred.get("second")
                third= otpcred.get("third")
                fourth= otpcred.get("fourth")
                fifth= otpcred.get("fifth")
                otp_no = first+second+third+fourth+fifth
                user_num = "91"+request.session['username']
                print(otp_no)
                auth_code = db.child(user_num).get().val().get("code")
                print(auth_code)
                if auth_code == otp_no:
                    request.session['2fauth'] = "true"
                    data = {"code" : auth_code,"status" : "approved"}
                    db.child(user_num).set(data)
                    return redirect(home)
            return render(request,'2fa.html')
    else:
        if request.method == "POST":
            user_login_cred = request.POST
            print(user_login_cred)
            inputed_userid = user_login_cred.get('userid')
            inputed_passwd = user_login_cred.get('passwd')
            user = authenticate(username=inputed_userid,password=inputed_passwd)

            if user is not None:
                try:
                  request.session['username'] = inputed_userid
                  send_verification_code('+91'+inputed_userid,generate_otp())
                  return render(request,'2fa.html')
                except Exception as e:
                    print(e)
            else:
                messages.error(request, 'Incorrect Credentials')
                return redirect(login)
        context={'form':form}
        return render(request,'login.html',context)


def logout(request):
    user_num = "91"+request.session['username']
    db.child(user_num).remove()
    request.session.flush()
    return redirect(login)
