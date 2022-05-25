from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import student,course
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'home.html')

def signup(request):
    return render(request,'signup.html')

def loginpage(request):
    return render(request,'login.html')        

def about(request):
    return render(request,'about.html')    

def welcome(request):
    if 'uid' in request.session:
        return render(request,'welcome.html')    
    return redirect('login')

@login_required(login_url='login')
def course1(request):
    uid = User.objects.get(id=request.session["uid"])
    return render(request,'course.html',{'uid':uid})    


@login_required(login_url='login')
def student1(request):
    courses=course.objects.all()
    context={'courses':courses}
    return render(request,'student.html',context) 


#......Msg Passing and Check Username and Password....
def usercreate(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email']

        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                print("Username already Taken..")
                return redirect('signup')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                user.save()
                #messages.info(request, 'SuccessFully completed.......')
                print("Successed...")
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('signup')   
        return redirect('login')
    else:
        return render(request,'signup.html')

#User login functionality view
def login(request): 
    try:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                request.session["uid"] = user.id
                if user is not None:
                    auth.login(request, user)
                    messages.info(request, f'Welcome {username}')
                    return redirect('welcome')
                else:
                    messages.info(request, 'Invalid username or password')
                    return redirect('loginpage')
            except:
                messages.info(request, 'Invalid username or password')
                return render(request, 'login.html')
        else:
            # messages.info(request, 'Invalid username or password')
            return render(request, 'login.html')
    except:
        messages.info(request, 'Invalid username or password')
        return render(request, 'login.html')

#User logout functionality view
def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('home')

#profile page
@login_required(login_url='loginpage')
def profile(request):
	currentuser = request.user
	return render(request, 'profile.html', {'user': currentuser})


#first password reset page
@login_required(login_url='login')
def resetpassword(request):
	return render(request, 'resetpassword.html')



#User signup/registration update view
@login_required(login_url='login')
def userupdate(request, id):
	if request.method == 'POST':
		user = request.user
		user.first_name = request.POST['first_name']
		user.last_name = request.POST['last_name']
		user.email = request.POST['email']
		user.save()
		return redirect('profile')
	else:
		return redirect('welcome')


#User signup/registration password update view
@login_required(login_url='login')
def passupdate(request, pk):
	if request.method == 'POST':
		user = request.user
		user.username = request.POST['username']
		password = request.POST.get('password')
		cpassword = request.POST.get('cpassword')
		try:
			if password is not None:
				if password == cpassword:
					user.set_password(password)
					user.save()
		except:
			pass
		return redirect('profile')
	else:
		return redirect('welcome')

@login_required(login_url='login')
def add_course(request):
    if request.method=='POST':
        cors=request.POST['course']
        cfee=request.POST['cfee']
        print(cors)
        crs=course()
        crs.course_name=cors
        crs.fee=cfee
        crs.save()
        print("hii")
        return redirect('student1')


@login_required(login_url='login')
def add_student(request):
    if request.method=='POST':
        # adno=request.POST['adno']
        sname=request.POST['sname']
        address=request.POST['address']
        age=request.POST['age']
        jdate=request.POST['jdate']
        sel1 = request.POST['sel']
        course1=course.objects.get(id=sel1)
        std=student(std_name=sname,
                    std_address=address,
                    std_age=age,
                    Join_date=jdate,
                    course=course1)
        std.save()
        print("hii")
        return redirect('welcome')

def show_student_details(request):
    std=student.objects.all()
    return render(request,'show_students.html',{'std':std})

    