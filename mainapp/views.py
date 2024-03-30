from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student
# Create your views here.

# Register /Signup user
# check if the form is bieng posted
# to popolate the form with the posted data 
# If the form is valid  save it 
# then authenticate the user
# redirect to the home page

def user_signup(request):
      if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                 user = form.save()
                 print('new user:', user)
                 login(request, user)
                 messages.success(request, 'Registration successful.')
                 return redirect('home')
            else:    
            # If the form is invalid, render it again with it previous value
                  messages.error(request, 'invalid form')
                  return render(request, 'Registration/signup.html', {'form': form})
# If it's a GET request Not POST, render an empty instance of SignupForm. 
      else:
            form = SignupForm()
            return render(request, 'Registration/signup.html', {'form': form})
  

# -------------------------------------------------------------- # 
#  Login user
# check if the form is bieng posted
# to popolate the form with the posted data 
#  If the form is valid  
# check the user credentials
# if its not none loging it
# So redirect the user to the home page
# If the request method is not POST, render an empty instance of LoginForm.
 
def user_login(request):
      if request.method =='POST':
            form=LoginForm(request.POST)
            if form.is_valid:
                  username= request.POST.get('Username')
                  password= request.POST.get('Password')
                  user = authenticate(request, username= username, password= password )
                  print("Authenticated user:", user)

                  if user is not None:
                        login(request, user)
                        messages.success(request, 'You have been logged in successfully!')
                        return redirect ('home')
                  else:
                        messages.error(request,"Invalid username or password.")
            else:
                  messages.error(request,"Login failed. Please try again.")
      else:
            form = LoginForm()
      #executed regardless of the request method
      return render(request, 'Registration/login.html', {'form':form}) 

# ------------------------------------------------------------ # 


def user_logout(request):
      if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'You have been Logged out...')
            return redirect('login')
# ------------------------------------------------------------ # 
# home view
      #  filters the students based on the logged-in user
      # render the home page template with the filtered students 
def home(request):
      if (request.user.is_authenticated): 
      # filter students based on the logged in User   
            students= Student.objects.filter(user=request.user)
            return render(request, 'home.html',{'students': students} )
      else: 
            return redirect('login')

# ------------------------------------------------------------ # 
# create a student
      # check if the user is authenticated
      # check if its a POST request 
      # a new student object is created with the form data
      # check if its valid 
      # do not save it to the db yet
      # assign user to the student object created
      # save it to the db , so redirect user to home page
      # if its a GET request or form is inavlid  create a new form
      # if its not authenticated redirect user to the login page
def create_student(request):
      if request.user.is_authenticated:
            if request.method == 'POST':
                  form = StudentForm( request.POST)
                  if form.is_valid():
                        student=form.save(commit= False) # commit=False do not save it to the db yet
                        student.user= request.user
                        student.save() 
                        return redirect('home')
                  else:
                        messages.error(request, 'invalid format')
            else:
                  form= StudentForm()
                  return render(request, 'CRUD/create.html', {'form':form})
      else:
            messages.error(request, 'Please Login to your account')
            return redirect('login')

            
# ------------------------------------------------------------ # 
# Read/view a student
      # CHECK if the user is authenticated 
      # FETCH the student from DB with the given pK
      # RENDER the student Template
      # else if the user is not authenticated redirect the user to the  login page
      
def view_student(request, pk):
      if request.user.is_authenticated:
            try:
                  student= Student.objects.get(user=request.user.id, id=pk)
                  return render(request, 'CRUD/view.html', {'student': student})
            except Student.DoesNotExist:
                  messages.error(request, 'student not found')
                  return redirect('home')
      else:
            messages.error(request, 'Please Login to your account')
            return redirect('login')

# ------------------------------------------------------------ # 
# update a student
      # CHECK if the user is authenticated 
      # FETCH the student from DB where field value matches the current logged-in user & the id passed it to view
      # except block to handle the case where the student with the specified id doesn't exist or doesn't belong to the current logged in user.
      # Initialize a form instance with a pre-filled data in case POST for form submissions
      # OR initialize with no data case GET request   
      # CHECK THE form if its valid
      # redirect the user to the home view presenting student datatable 
      # else error validation form render the update template 
      # else User not logged in redirect user to the Login  page

def update_student(request, pk):
      if request.user.is_authenticated:
            try: 
                  current_student= Student.objects.get(user= request.user, id=pk)
                  print('student want to be updated', current_student)
            except Student.DoesNotExist:
                  messages.error(request, 'student may not be exist.')
                  return redirect('home')
            if current_student.user!= request.user:
                  messages.error(request, 'you do not have permission to update this student')
                  return redirect('home')
            elif request.method =='POST':
                  form = StudentForm(request.POST, instance= current_student)
                  if form.is_valid():
                        form.save()
                        messages.success(request, f'Student: {current_student.name} has been updated')
                        return redirect('home')
                  else:
                        messages.error(request, 'invalid form')
            else: 
                  form= StudentForm(instance=current_student)
                  return render(request, 'CRUD/update.html', {'form': form})
      else:
            messages.error(request, 'You must be logged in')
            return redirect('login')


# ------------------------------------------------------------ # 
# delete a student

def delete_student(request, pk=None):
      if request.user.is_authenticated:
      # if the request contains a 'pk' parameter => it's from view.html
            if pk is not None:
                  current_student= Student.objects.get(user= request.user, id= pk)
                  if request.method== 'POST':
      # so if request is POST hundling pk delete student belng to the logged in user
      # delete the student from the database
      # redirect the user to the home page
                        current_student.delete()
                        messages.success(request, f'The student with the id={pk} has been deleted!')
                        return redirect('home')
      # if it's a GET request, render the view template with the fetched student
                  return render(request, 'CRUD/view.html', {'current_student': current_student})
      # if the request doesn't contain a 'pk' parameter => it's from home.html
            elif request.method== 'POST':
      # get the id of the student  
                  pk= request.POST.get('delete_student')
      # check if the id exist
                  if pk: 
                        current_student= Student.objects.get(user=request.user, id=pk)
                        current_student.delete()
                        messages.success(request, f'The student with the id={pk} has been deleted!!')
                        return redirect('home') 
                  else:
                        messages.error(request, 'invalid request')
            else:
      # if the request is not POST or after processing it  (user viewing the page without submitting)
      # render the view page with student data belong to the current logged in user
                  student= Student.objects.filter(user= request.user)
                  return render(request, 'CRUD/view.html', {'student': student})
      else:
            messages.error(request, 'You must be logged in to delete a student.')
            return redirect('login')

