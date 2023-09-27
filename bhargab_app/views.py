from django.shortcuts import render

from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect,Http404

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your views here.
def index(req):
    try: 
        x = req.session["sent_mail"]
        data={'mail':False, 'data':x}
    except:
        data={'mail':True}
    return render(req, 'index.html', data)

def mail(req):
    name_text = str(req.POST["name"])
    email_text = str(req.POST["email"]).lower()

    try:
        validate_email(email_text)
    except ValidationError as e:
        messages.success(req,"Enter a valid email address")
        return HttpResponseRedirect("/")
    else:    
        if len(name_text) == 0 or len(email_text)==0:
            messages.success(req,"Please mention your name and your email adress")
            return HttpResponseRedirect("/")
        else:
            body=f"""
                Listed email id: {email_text}
                Listed name: {name_text}
                """ 
            try:
                subject_text=req.POST["subject"]
            except:
                subject_text="not mentioned"
            try:
                message_text= body+req.POST["message"]
            except:
                message_text=  body + " message not mentioned"
        
            subject = subject_text
            message = message_text + "This is generated from my website developed by django."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ["bhargab.analytics@gmail.com"]
            
            send_mail( subject, message, email_from, recipient_list )
            req.session["sent_mail"]=email_text
            messages.success(req,"Thanks for your visit, I will mail you soon.")
            return HttpResponseRedirect("/")