from django.shortcuts import render
from .models import Cart, CartItem,Order,UserAddress
from mycoffee.models import Coffee
from .forms import AddressForm, AddressSelectForm


def cart(request):
    cart,created= Cart.objects.get_or_create(user=request.user)
    item_id= request.GET.get("item")
    qty= request.GET.get("qty",1)
    if item_id:
        coffee = Coffee.objects.get(id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=coffee)
        if int(qty) < 1:
            cart_item.delete()
        else:
            cart_item.quantity= qty
            cart_item.save()
    return render(request, 'cart.html', {'cart':cart})

def checkout(request):
    cart,created= Cart.objects.get_or_create(user=request.user)
    order,created= Order.objects.get_or_create(cart=cart, user=request.user)

    if order.address == None:
        return redirect ("cart:select_address")
    return redirect("/")

def select_address(request):
    if UserAddress.objects.filter(user=request.user).count()<1:
        return redirect("cart:create_address")
    form= AddressSelectForm()
    form.fields['address'].queryset = UserAddress.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddressSelectForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            order = Order.objects.get(user=request.user)
            order.address=address
            order.save()
            return redirect("cart:checkout")
    context = {
        'form':form
    }
    return render(request, 'select_address.html', context)

def create_address(request):
    form=AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address =form.save(commit=False)
            address.user = request.user
            address.save()
            form.save()
            return redirect("cart:select_address")
    context = {
        "form": form
    }
    return render(request, 'create_address.html', context)
