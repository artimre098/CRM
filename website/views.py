from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
	#Check to see if logging in
	records = Record.objects.all()

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		#authenticate
		user = authenticate(request, username=username,password=password)
		if user is not None:
			login(request,user)
			messages.success(request,"You have been logged In!")
			return redirect('home')
		else:
			messages.success(request,"There was an error Logging in, Please try again...")
			return redirect('home')
	else:
		return render(request, 'home.html',{'records':records})



def logout_user(request):
	logout(request)
	messages.success(request,"You have been Looged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			#Authenticate and Login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			login(request,user)
			messages.success(request,"You have successfully registered")
			return redirect('home')
		
	else:
		form = SignUpForm()
		return render(request, 'register.html',{'form':form})
	
	return render(request, 'register.html',{'form':form})


def employee_record(request,pk):
	if request.user.is_authenticated:
		#look up the record
		employee_record = Record.objects.get(id=pk)
		return render(request, 'record.html',{'employee_record':employee_record})
	else:
		messages.success(request,"You Must be Logged In to View That Page")
		return redirect('home')


def delete_record(request,pk):
	delete_it = Record.objects.get(id=pk)
	
	if request.user.is_authenticated:
		delete_it.delete()
		messages.success(request,"Employee Records has been deleted")
		return redirect('home')
	else:
		messages.success(request,"You Must be Logged In to View That Page")
		return redirect('home')
	
def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request,"Employee Records has been Saved")
				return redirect('home')
		return render(request, 'add_record.html',{'form':form})
	else:
		messages.success(request,"You Must be Logged In to View That Page")
		return redirect('home')