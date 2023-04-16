from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import PageUserLogin, PageUsers,\
    UserSubscriber, AddToCart,\
    UpdateProfileImage, UpdateUsername, \
    UpdatePhoneNumber, UpdateEmail
from .models import Page_users, Subscribers, InCart, CheckedOut
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth


# Create your views here.
def index(request):
    message = {'message':"Login or signup to access features"}
    if request.method == 'POST' and 'sign_up' in request.POST:
        registerForm = PageUsers(request.POST)
        if registerForm.is_valid():
            user = Page_users(username = request.POST.get('username'),
                         email = request.POST.get('email'),
                         phone = request.POST.get('phone'),
                         date_joined = timezone.localtime(timezone.now()),)
            user.set_password(request.POST.get('password'),)
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')
            messages.success(request, "User registered successfully")
            return HttpResponseRedirect(reverse("myCarbonApp:home"))

        messages.error(request, "Invalid Info. Registration Unsuccessful!")
        message = {'message':"Invalid Info. Registration Unsuccessful!"}
        return render(request, "myCarbonApp/Welcome.html", message)
    elif request.method == 'POST' and 'log_in' in request.POST:
        objec = Page_users.objects.get(username = request.POST.get('username'))
        loginForm = PageUserLogin(request.POST, instance=objec)
        for field in loginForm:
            print("Field Error: ", field.name, field.errors)
        if loginForm.is_valid():
            objec = loginForm.save()
            try:
                #user = Page_users.objects.filter(email = request.POST.get('email')).exists()
                if (request.POST.get('password') == objec.password):
                    #user = auth.authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
                    #print(user) #returns None. Don't know why
                    user = Page_users.objects.get(username=request.POST.get('username'))
                    if user is not None:
                        auth.login(request, user, backend='django.contrib.auth.backends.AllowAllUsersModelBackend')
                        messages.success(request, "Login Successful!")
                        return render(request, "myCarbonApp/Home.html")
                    else:
                        messages.error(request, "Password Invalid! Try Again")
                        message = {'message': "Authentication Error!"}
                        loginForm = PageUserLogin()
                        content = {'loginForm': loginForm, 'message': message}
                        return render(request, "myCarbonApp/Welcome.html", content)
                else:
                    messages.error(request, "Password Invalid! Try Again")
                    message = {'message': "Password Invalid! Try Again"}
                    loginForm = PageUserLogin()
                    content = {'loginForm': loginForm, 'message': message}
                    return render(request, "myCarbonApp/Welcome.html", content)

            except Page_users.DoesNotExist:
                message = {'message': "User Does Not Exist!"}
                loginForm = PageUserLogin()
                content = {'loginForm': loginForm, 'message': message}
                return render(request, "myCarbonApp/Welcome.html", content)
        else:
            messages.error(request, "Invalid Info. Login Unsuccessful!")
            message = {'message': "Invalid Info. Login Unsuccessful!"}
            loginForm = PageUserLogin()
            content = {'loginForm': loginForm, 'message': message}
            return render(request, "myCarbonApp/Welcome.html", content)
    loginForm = PageUserLogin()
    content = {'loginForm':loginForm, 'message':message}
    return render(request, "myCarbonApp/Welcome.html", content)

def home(request):
    message = "Register below to receive our newsletters"
    context = ''
    if request.user.is_authenticated:
        context = Page_users.objects.get(username=request.user)
    if request.method == "POST":
        subscriber = UserSubscriber(request.POST)
        if subscriber.is_valid():
            user = Subscribers(name=request.POST.get('name'),
                         email=request.POST.get('email'),
                         date_subscribed=timezone.localtime(timezone.now()), )
            user.save()
            message = {"You have successfully registered!"}
            return render(request, "myCarbonApp/Home.html", message)
    return render(request, "myCarbonApp/Home.html", {'message':message, 'userprofile':context})

def offsets(request):
    message = {'message': "Register below to receive our newsletters"}
    if request.method == "POST":
        subscriber = UserSubscriber(request.POST)
        if subscriber.is_valid():
            user = Subscribers(name=request.POST.get('name'),
                               email=request.POST.get('email'),
                               date_subscribed=timezone.localtime(timezone.now()), )
            user.save()
            message = {"You have successfully registered!"}
            return render(request, "myCarbonApp/Home.html", message)
    return render(request, 'myCarbonApp/pages/offset_now.html', message)

def projects(request):
    offset_type = 'donation'
    if request.method == "POST":
        customer = AddToCart(request.POST)
        if customer.is_valid():
            add_item_to_cart = InCart(amount=request.POST.get('amount'),
                                      offset_type=offset_type,
                                      customer = request.user)
            if request.user.is_authenticated:
                add_item_to_cart.save()
                return HttpResponseRedirect(reverse("myCarbonApp:add-to-cart"))
            else:
                return redirect('myCarbonApp:index')
        else:
            return redirect('myCarbonApp:projects')
    return render(request, 'myCarbonApp/pages/projects.html')

def car_emission_offset(request):
    offset_type = 'car'
    if request.method == "POST":
        customer = AddToCart(request.POST)
        if customer.is_valid():
            add_item_to_cart = InCart(amount = request.POST.get('amount'),
                                      offset_type = offset_type,
                                      customer = request.user)
            print(request.user)
            if request.user.is_authenticated:
                add_item_to_cart.save()
                return HttpResponseRedirect(reverse("myCarbonApp:add-to-cart"))
                #return render(request, 'myCarbonApp/components/add_to_cart.html')
            else:
                return redirect('myCarbonApp:index')
        else:
            return redirect('myCarbonApp:car-emission-offset')
    return render(request, 'myCarbonApp/offsets/car_emission_offset.html')

def household_emission_offset(request):
    offset_type = 'household'
    if request.method == "POST":
        customer = AddToCart(request.POST)
        if customer.is_valid():
            add_item_to_cart = InCart(amount = request.POST.get('amount'),
                                      offset_type = offset_type,
                                      customer = request.user)
            if request.user.is_authenticated:
                add_item_to_cart.save()
                return HttpResponseRedirect(reverse("myCarbonApp:add-to-cart"))
                #return render(request, 'myCarbonApp/components/add_to_cart.html')
            else:
                return redirect('myCarbonApp:index')
        else:
            return redirect('myCarbonApp:house-emission-offset')
    return render(request, 'myCarbonApp/offsets/household_emission_offset.html')

def tours_offset(request):
    offset_type = 'tours'
    if request.method == "POST":
        customer = AddToCart(request.POST)
        if customer.is_valid():
            add_item_to_cart = InCart(amount = request.POST.get('amount'),
                                      offset_type = offset_type,
                                      customer = request.user)
            if request.user.is_authenticated:
                add_item_to_cart.save()
                return HttpResponseRedirect(reverse("myCarbonApp:add-to-cart"))
                #return render(request, 'myCarbonApp/components/add_to_cart.html')
            else:
                return redirect('myCarbonApp:index')
        else:
            return redirect('myCarbonApp:tours-offset')
    return render(request, 'myCarbonApp/offsets/tours_offset.html')

def business_offset(request):
    offset_type = 'business'
    if request.method == "POST":
        customer = AddToCart(request.POST)
        if customer.is_valid():
            add_item_to_cart = InCart(amount = request.POST.get('amount'),
                                      offset_type = offset_type,
                                      customer = request.user)
            if request.user.is_authenticated:
                add_item_to_cart.save()
                return HttpResponseRedirect(reverse("myCarbonApp:add-to-cart"))
                #return render(request, 'myCarbonApp/components/add_to_cart.html')
            else:
                return redirect('myCarbonApp:index')
        else:
            return redirect('myCarbonApp:business-offset')
    return render(request, 'myCarbonApp/offsets/business_offset.html')

def buy_gift_certificate(request):
    offset_type = 'gift_certificate'
    if request.method == "POST":
        customer = AddToCart(request.POST)
        if customer.is_valid():
            add_item_to_cart = InCart(amount = request.POST.get('amount'),
                                      offset_type = offset_type,
                                      customer = request.user)
            if request.user.is_authenticated:
                add_item_to_cart.save()
                return HttpResponseRedirect(reverse("myCarbonApp:add-to-cart"))
                #return render(request, 'myCarbonApp/components/add_to_cart.html')
            else:
                return redirect('myCarbonApp:index')
        else:
            return redirect('myCarbonApp:gift-cert')
    return render(request, 'myCarbonApp/extras/buy_gift_cert.html')

def buy_certified_cos(request):
    offset_type = 'certified_cos'
    if request.method == "POST":
        customer = AddToCart(request.POST)
        if customer.is_valid():
            add_item_to_cart = InCart(amount = request.POST.get('amount'),
                                      offset_type = offset_type,
                                      customer = request.user)
            if request.user.is_authenticated:
                add_item_to_cart.save()
                return HttpResponseRedirect(reverse("myCarbonApp:add-to-cart"))
                #return render(request, 'myCarbonApp/components/add_to_cart.html')
            else:
                return redirect('myCarbonApp:index')
        else:
            return redirect('myCarbonApp:buy-cert-cos')
    return render(request, 'myCarbonApp/extras/buy_certified_carbon_offsets.html')

def add_to_cart(request):
    if request.user.is_authenticated:
        customer_items = InCart.objects.filter(customer=request.user).values()
        return render(request, 'myCarbonApp/components/add_to_cart.html', {"items_in_cart": customer_items})
    else:
        return redirect('myCarbonApp:index')

def delete_from_cart(request, items):
    if request.user.is_authenticated:
        delete_items = InCart.objects.get(id=items)
        delete_items.delete()
        if InCart.objects.all():
            return redirect("myCarbonApp:add-to-cart")
        else:
            return redirect("myCarbonApp:offset-now")
    else:
        return redirect('myCarbonApp:index')

def pay_page(request):
    if request.user.is_authenticated:
        delete_items = InCart.objects.filter(customer=request.user).values()
        #perform transactions and confirm here
        #then
        complete_payments = CheckedOut(amount=delete_items.amount, customer=request.user)
        complete_payments.save()
        delete_items.delete()
        #create and print payment receipt
    else:
        return redirect('myCarbonApp:index')
    return render(request, 'myCarbonApp/components/pay_page.html')

def user_profile(request):
    if request.user.is_authenticated:
        context = Page_users.objects.get(username=request.user)
        if request.method == 'POST' and 'username-profile' in request.POST:
            userProfUsernameUpdate = UpdateUsername(request.POST)
            if userProfUsernameUpdate.is_valid():
                username = request.POST.get('username')
                user = Page_users.objects.get(username=request.user)
                user.username = username
                user.save()
                context = Page_users.objects.get(username=request.user)
                return render(request, 'myCarbonApp/pages/user_profile.html', {'userprofile': context})
        elif request.method == 'POST' and 'email-profile' in request.POST:
            userProfEmailUpdate = UpdateEmail(request.POST)
            if userProfEmailUpdate.is_valid():
                email = request.POST.get('email')
                user = Page_users.objects.get(username=request.user)
                user.email = email
                user.save()
                context = Page_users.objects.get(username=request.user)
                return render(request, 'myCarbonApp/pages/user_profile.html', {'userprofile': context})
        elif request.method == 'POST' and 'phone-profile' in request.POST:
            userProfPhoneUpdate = UpdatePhoneNumber(request.POST)
            if userProfPhoneUpdate.is_valid():
                phone = request.POST.get('phone')
                user = Page_users.objects.get(username=request.user)
                user.phone = phone
                user.save()
                context = Page_users.objects.get(username=request.user)
                return render(request, 'myCarbonApp/pages/user_profile.html', {'userprofile': context})
        elif request.method == 'POST' and 'image-profile' in request.POST:
            userProfImgUpdate = UpdateProfileImage(request.POST, request.FILES)
            if userProfImgUpdate.is_valid():
                profile_picture = request.FILES.get('profile_picture')
                user = Page_users.objects.get(username=request.user)
                user.profile_picture = profile_picture
                user.save()
                #userProfImgUpdate.save()
                context = Page_users.objects.get(username=request.user)
                return render(request, 'myCarbonApp/pages/user_profile.html', {'userprofile': context})
    else:
        return redirect('myCarbonApp:index')
    return render(request, 'myCarbonApp/pages/user_profile.html', {'userprofile':context})

def logout(request):
    auth.logout(request)
    return render(request, 'myCarbonApp/Home.html')