from django.shortcuts import render, redirect
from django.http import JsonResponse,Http404
from .forms import UserSignUp, UserLogin, CoffeeForm
from .models import Bean, Roast, Syrup, Powder, Coffee
from django.contrib.auth import authenticate,login,logout
import json


def coffee_list(request):
    if not request.user.is_authenticated():
        return redirect("mycoffee:login")

    coffee_list = Coffee.objects.filter(user=request.user)
    return render(request, 'coffee_list.html', {'coffee_list': coffee_list})

def coffee_detail(request, coffee_id):
    if not request.user.is_authenticated():
        return redirect("mycoffee:login")
    coffee = Coffee.objects.get(id=coffee_id)
    if not (request.user == coffee.user or request.user.is_superuser or request.user.is_staff):
        raise Http404
    return render(request, 'coffee_detail.html', {'coffee': coffee})

    
def usersignup(request):
    form= UserSignUp()
    if request.method == 'POST':
        form= UserSignUp(request.POST)
        if form.is_valid():
            user = form.save()
            username= user.username
            password= user.password

            user.set_password(password)
            user.save()

            auth_user= authenticate(username=username, password=password)
            login(request, auth_user)
            return redirect('/')
        return redirect("mycoffee:signup")
    context={
    'form': form,
    }
    return render(request, 'sigup.html', context)

def userlogin(request):
        form= UserLogin()
        if request.method == 'POST':
            form= UserLogin(request.POST)
            if form.is_valid():

                username= form.cleaned_data['username']
                password= form.cleaned_data['password']

                auth_user= authenticate(username=username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    return redirect('/')
                return redirect("mycoffee:login")
        context={
        'form': form,
        }
        return render(request, 'login.html', context)


def userlogout(request):
    logout(request)
    return redirect("/")



def coffee_price(instance):
    total_price = instance.bean.price + instance.roast.price + (instance.espresso_shots*Decimal(0.250))
    if instance.steamed_milk:
        total_price+= Decimal(0.100)
    if instance.powders.all().count()>0:
        for powder in instance.powders.all():
            total_price+= powder.price
    if instance.syrups.all().count()>0:
        for syrup in instance.syrups.all():
            total_price+= syrup.price
    return total_price


def create_coffee(request):
    if not request.user.is_authenticated():
        return redirect("mycoffee:login")
    form = CoffeeForm()
    if request.method == "POST":
        form = CoffeeForm(request.POST)
        if form.is_valid():
            coffee = form.save(commit=False)
            coffee.user = request.user
            coffee.save()
            form.save_m2m()
            coffee.price = coffee_price(coffee)
            coffee.save()
            return redirect('/')
    context{
    'form': form,
    }
    return render(request, 'create_coffee.html', context)


def ajax_price(request):
    total_price = 0
    bean_id= request.GET.get('bean')
    if bean_id:
        total_price += Bean.objects.get(id=bean_id).price

    roast_id= request.Get.get('roast')
    if roast_id:
        total_price += Roast.objects.get(id=roast_id).price

    syrups= json.loads(request.GET.get('syrups'))
    if len(syrups)>0:
        for syrup_id in syrups:
            total_price += Syrup.objects.get(id=syrup_id).price

    powders = json.loads(request.GET.get('powders'))
    if len(powders)>0:
        for powder_id in powders:
            total_price += Powder.objects.get(id=powder_id).price

    milk = request.GET.get('milk')
    if milk=='true':
        total_price += Decimal(0.100)

    shots=request.GET.get('espresso_shots')
    if shots:
        total_price += (int(shots)*(0.250))

    return JsonResponse(round(total_price,3), safe=False)
