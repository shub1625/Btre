from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    """
    Register user
    """
    if request.method == 'POST':
        
        #Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check if password match
        if password == password2:
            # Check if username is already used
            if User.objects.filter(username=username).exists():
                messages.error(request,'Opps Username already taken')
                return redirect('register')
            else:
                # check email
                if User.objects.filter(email=email).exists():
                    messages.error((request,'Opps Email already exists'))
                    return redirect('register')
                else:
                    # All good shoot.!
                    user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)

                    # Login after register
                    # auth.login(request,user)
                    # messages.success(request,f'Congrats , { user.username } Logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request,f'{user.username} is now registered and can log in ..!')
                    return redirect('login')

        else:
            messages.error(request,'Password Don\'t match' )
            return redirect('register')


    else:
        return render(request,'accounts/register.html')


def login(request):
    """
    Log in of user
    """
    if request.method == 'POST':
       
       username = request.POST['username']
       password = request.POST['password']

       user = auth.authenticate(username=username,password=password)

       if user is not None:
           auth.login(request,user)
           messages.success(request,f'{ user.username } is Now logged in ..!')
           return redirect('dashboard')
       else:
            messages.error(request,'Sorry Invalid credentials')
            return redirect('login')

    else:
        return render(request,'accounts/login.html')    

def dashboard(request):
    """
    dashboard
    """
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    contaxt ={
        'contacts' : user_contacts

    }
    return render(request,'accounts/dashboard.html',contaxt) 

def logout(request):
    """
    logout view
    """
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are logged Out now ..!')
        return redirect('index')