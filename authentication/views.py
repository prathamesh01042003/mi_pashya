from collections import UserDict, UserList
from django.conf import Settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from apps import settings
from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse
from .forms import MyfileUploadForm
from .models import file_upload

from .models import assignment

from.models import myuploadjournels

from.models import myuploadSTUDENT

from.models import myclassnote

from.models import myuploadstaff
from datetime import datetime
import datetime

# from.models import Student




# import authentication

# Create your views here.
def home(request):
    return render(request,"authentication/index.html")

def signup(request):

    if request.method=="POST":
        # username=request.POST.get('username')
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']


        if User.objects.filter(username=username):
            messages.error(request,str(username)+"  Username alredy exist! Please try some other uername")
            return render(request,"authentication/signup.html")
        
        if User.objects.filter(email=email):
            messages.error(request,str(email)+" Email already registered!")
            return render(request,"authentication/signup.html")
        
        if pass1 != pass2:
            messages.error(request,str(fname)+" your password is not match")
            return render(request,"authentication/signup.html")
        
        if len(username)>12:
            messages.error(request,"Hyyy what is this (username must be less than " )
        myuser=User.objects.create_user(username,email,pass1)
        # myuser=User.objects.create_user(username=request.POST.get('username'),email=request.POST.get('email'),pass1=request.POST.get('pass1'))
        myuser.first_name=fname
        myuser.last_name=lname

        myuser.save()

        messages.success(request,"HELLO  "+str(fname)+".."+str(lname)+"  your accout has been successfully created...")  
         
        # Welcome email pomplates bro

        subject ="Welcom to PASHYAS WEBSITES !!"
        message = " Hello" + myuser.first_name + "!! \n" + "Welcome to website!!\n Thank you for visiting our websites \n reson behind the send email is just CONFIRMATION your email address \n\nThank You"+myuser.first_name +"\nyour faithfully: mipashya..." 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return render(request,"authentication/index.html")


    return render(request,"authentication/signup.html")

def signin(request):


    if request.method == "POST":
        username=request.POST['username']
        pass1=request.POST['pass1']



        user=authenticate(username=username,password=pass1)
        

        if user is not None:
           login(request,user)
           fname=user.first_name # type: ignore
           lname=user.last_name  # type: ignore
           return render(request,"authentication/department.html",{'fname':fname ,'lname':lname})
        


        else:
            messages.error(request,"ATTENTION PLS --"+str(username)+"<--Username OR *****  Passwords are not match...!")
           
        
      
    
    return render(request,"authentication/index.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out Successfully..!")
    return render(request,"authentication/index.html")

def ASSIGNMENT(request):
    if request.method == 'POST':
        form =MyfileUploadForm(request.POST,request.FILES)

        if form.is_valid():
            name=form.cleaned_data['file_name']
            the_files=form.cleaned_data['files_data']
            

            

            file_upload(file_name=name , my_file=the_files).save() 

            # return HttpResponse("file upload successfully " str{{name}})
            
            return HttpResponse(str(name)+"<==== THIS FILE IS SUCESSFULLY UPLOADED  ------->  "  + str(the_files))
            

        else:
            return HttpResponse(" sorry uploadation error")


    else:         
        context =  {
            'form':MyfileUploadForm()
        }
        return render(request,'authentication/upassignCR.html',context)
    
def show_file(request):
    all_data = file_upload.objects.all()

    context = {
        'data':all_data
    }

    return render(request,'authentication/view.html',context)



# for assignments okkk

def assignments(request):

    if request.method == 'POST':
        form =assignment(request.POST,request.FILES)

        if request.method == 'POST':
          fullname=request.POST.get('fullnamey')
          date_field=datetime.datetime.now()
          filedesc=request.POST.get('filedesc')
          filename=request.POST.get("filename")
          status=request.POST.get('status1')          
          
          myfile=request.FILES.getlist("assignment")

          for a in myfile:
               assignment(full_name=fullname,date_field=date_field,file_desc=filedesc,file_name=filename,status=status,myfiles=a).save()
           

            # return HttpResponse("file upload successfully " str{{name}})
            
          return HttpResponse(str(fullname)+"  " + str(filename)+"<==== THIS JOURNAL FILE OF TY CSE FIRST SEMISTER SUCESSFULLY UPLOADED  ------->  "  )

        else:
            return HttpResponse(" sorry uploadation error")


    else:         
        context =  {
            'form':MyfileUploadForm()
        }
        return render(request,'authentication/assignment.html',context)
    
def show_assignments(request):
    all_data = assignment.objects.all()

    context = {
        'data2':all_data
    }

    return render(request,'authentication/seeassignments.html',context)








def student(request):

    if request.method == 'POST':
        form =myuploadSTUDENT(request.POST,request.FILES)

        if request.method == 'POST':
          fullname=request.POST.get('fullnamey')
          date_field=datetime.datetime.now()
          filedesc=request.POST.get('filedesc')
          filename=request.POST.get("filename")
          status=request.POST.get('status1')          
          
          myfile=request.FILES.getlist("myuploadSTUDENT")

          for w in myfile:
               myuploadSTUDENT(full_name=fullname,date_field=date_field,file_desc=filedesc,file_name=filename,status=status,fileupload=w).save()
           
            # return HttpResponse("file upload successfully " str{{name}})
            
          return HttpResponse(str(fullname)+"  " + str(filename)+"<==== THIS JOURNAL FILE OF TY CSE FIRST SEMISTER SUCESSFULLY UPLOADED  ------->  "  )

        else:
            return HttpResponse(" sorry uploadation error")


    else:         
        context =  {
            'form':MyfileUploadForm()
        }
        return render(request,'authentication/studentclass.html',context)
    
def show_student(request):
    all_data =myuploadSTUDENT.objects.all()

    context = {
        'data4':all_data
    }

    return render(request,'authentication/seestudentassignement.html',context)














def index3(request):

    if request.method == 'POST':
        form =myuploadjournels(request.POST,request.FILES)

        if request.method == 'POST':
          fullname=request.POST.get('fullnamey')
          date_field=datetime.datetime.now()
          filedesc=request.POST.get('filedesc')
          filename=request.POST.get("filename")
          status=request.POST.get('status1')          
          
          myfile=request.FILES.getlist("myuploadjournels")

          for J in myfile:
               myuploadjournels(full_name=fullname,date_field=date_field,file_desc=filedesc,file_name=filename,status=status,myfiles=J).save()
           

            # return HttpResponse("file upload successfully " str{{name}})
            
          return HttpResponse(str(fullname)+"  " + str(filename)+"<==== THIS JOURNAL FILE OF TY CSE FIRST SEMISTER SUCESSFULLY UPLOADED  ------->  "  )

        else:
            return HttpResponse(" sorry uploadation error")


    else:         
        context =  {
            'form':MyfileUploadForm()
        }
        return render(request,'authentication/journels.html',context)
    
def show_j(request):
    all_data = myuploadjournels.objects.all()

    context = {
        'data3':all_data
    }

    return render(request,'authentication/seej.html',context)









# for class_notes


def class_note(request):

    if request.method == 'POST':
        form =myclassnote(request.POST,request.FILES)

        if request.method == 'POST':
          fullname=request.POST.get('fullnamey')
          date_field=datetime.datetime.now()
          filedesc=request.POST.get('filedesc')
          filename=request.POST.get("filename")
          status=request.POST.get('status1')          
          
          myfile=request.FILES.getlist("uploadfiles")

          for m in myfile:
               myclassnote(full_name=fullname,date_field=date_field,file_desc=filedesc,file_name=filename,status=status,myfiles=m).save()
           

            # return HttpResponse("file upload successfully " str{{name}})
            
          return HttpResponse(str(fullname)+"  " + str(filename)+"<==== THIS JOURNAL FILE OF TY CSE FIRST SEMISTER SUCESSFULLY UPLOADED  ------->  "  )

        else:
            return HttpResponse(" sorry uploadation error")


    else:         
        context =  {
            'form':MyfileUploadForm()
        }
        return render(request,'authentication/upclassnote.html',context)
    
def show_classnote(request):
    all_data = myclassnote.objects.all()

    context = {
        'data2':all_data
    }

    return render(request,'authentication/seeclassnote.html',context)
















# FOR FEES






def fees(request):
    if request.method == 'POST':
        form =myuploadstaff(request.POST,request.FILES)

        if request.method == 'POST':
          rollno=request.POST.get ('Roll_No')
          firstname=request.POST.get('FirstName')
          desc=request.POST.get('filedesc')
          name=request.POST.get("filename")
          
          myfile=request.FILES.getlist("uploadfiles")

          for j in myfile:
               myuploadstaff(roll_no=rollno,f_desc=desc,first_name=firstname,f_name=name,myfiles=j).save()
           

            # return HttpResponse("file upload successfully " str{{name}})
            
          return HttpResponse(str(firstname)+"  " + str(name)+"<==== THIS JOURNAL FILE OF TY CSE FIRST SEMISTER SUCESSFULLY UPLOADED  ------->  "  )

        else:
            return HttpResponse(" sorry uploadation error")


    else:         
        context =  {
            'form':myuploadstaff()
        }
        return render(request,'authentication/staffupload.html',context)
    
def show_fees(request):
    all_data = myuploadstaff.objects.all()

    context = {
        'datafees':all_data
    }

    return render(request,'authentication/seefees.html',context)












    

def degree(request):
           return render(request,'authentication/degree.html')



def subject(request):
           return render(request,'authentication/subject.html')

def show_file2(request):
    return render(request,'authentication/view2.html')

def adminpashya(request):
    return render(request,'authentication/signin.html')