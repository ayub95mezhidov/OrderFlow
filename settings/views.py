from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import PriceSettingsForms, PriceAccessoriesForm
from .models import PriceSettings, PriceAccessories

# Цены за полотна
@login_required(login_url='/users/login/')
def price_settings(request):
    prices = PriceSettings.objects.filter(user=request.user)
    prices_ac = PriceAccessories.objects.filter(user=request.user)

    context = {'prices': prices, 'prices_ac': prices_ac}
    return render(request, 'settings/price_settings.html', context)

# Создать цену
@login_required
def price_create_canvases(request):
    if request.method == 'POST':
        form = PriceSettingsForms(request.POST)
        if form.is_valid():
           # PriceSettings.objects.filter(user=request.user).delete()
            price = form.save(commit=False)
            price.user = request.user
            price.save()
            return redirect('price_settings')
    else:
        form = PriceSettingsForms()
    context = {'form': form}
    return render(request, 'settings/price_create.html', context)

# Обнавить цену
@login_required
def price_update(request, price_id):
    price = get_object_or_404(PriceSettings, id=price_id, user=request.user)

    if request.method == 'POST':
        form = PriceSettingsForms(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect('price_settings')
    else:
        form = PriceSettingsForms(instance=price)

    context = {'form': form, 'price': price}
    return render(request, 'settings/price_update.html', context)

# Создать цену для комплектующих
@login_required
def price_accessories_create(request):
    if request.method == 'POST':
        form = PriceAccessoriesForm(request.POST)
        if form.is_valid():
            price = form.save(commit=False)
            price.user = request.user
            price.save()
            return redirect('price_settings')
    else:
        form = PriceAccessoriesForm()
    context = {'form': form}
    return render(request, 'settings/price_accessories_create.html', context)

@login_required
def price_accessories_update(request, price_id):
    price = get_object_or_404(PriceAccessories, id=price_id, user=request.user)

    if request.method == 'POST':
        form = PriceAccessoriesForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect('price_settings')
    else:
        form = PriceAccessoriesForm(instance=price)
    context = {'form': form, 'price': price}
    return render(request, 'settings/price_acc_update.html', context)

def price_ceiling_remove(request, price_id):
    price = PriceSettings.objects.get(id=price_id)
    price.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def price_accessories_remove(request, price_id):
    price = PriceAccessories.objects.get(id=price_id)
    price.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
