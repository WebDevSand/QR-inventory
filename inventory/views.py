from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import FormView
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from .models import Item
import pyqrcode
from PIL import Image
from  django.core.files import File
from QRinventory import settings
import pyzbar.pyzbar as pyzbar
import random, string
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

def get_qrcode(tag):
    qr = pyqrcode.create(tag)
    a = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7)) 
    filename = a + '.png'
    qr.png('media/temp/' + filename, scale=7)
    
    return filename

class ItemForm(forms.Form):
    privacy_choices = [
        ('Private', 'Private'),
        ('Public', 'Public'),
    ]

    name = forms.CharField(label='Item Name')
    itemtype = forms.CharField(label='Item Type')
    desc = forms.CharField(label='Short Description', widget=forms.Textarea)
    privacy= forms.CharField(label='Privacy', widget=forms.Select(choices=privacy_choices))

class Create_item_Form(FormView):
    template_name = "item/create_item.html"
    form_class = ItemForm
    success_url = '/'

    def form_valid(self, form):
        try:
            newly_created_item = Item()
            newly_created_item.owner = self.request.user    
            newly_created_item.name = form.cleaned_data['name']
            newly_created_item.type = form.cleaned_data['itemtype']
            newly_created_item.desc = form.cleaned_data['desc']

            a = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
            b = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            tag = b + form.cleaned_data['name'][:7] + a + '_@' + str(self.request.user.id) 
            filename = get_qrcode(tag)
            filepath = settings.MEDIA_ROOT + "/temp/" + filename
            newly_created_item.qrcode = filepath
            newly_created_item.tag = tag
            newly_created_item.privacy = form.cleaned_data['privacy']
            newly_created_item.save()

            messages.add_message(self.request, messages.INFO, 'Item has been created!')
            return HttpResponseRedirect('/profile')
        except IntegrityError as e:
            return redirect('/profile')

class SearchItemForm(forms.Form):
    qrcode = forms.ImageField(label='Upload QR Code')
    searching = forms.BooleanField(label='Search in All Public Inventories', required=False)

class search_item_Form(FormView):
    template_name = "item/search_item.html"
    form_class = SearchItemForm
    success_url = '/'

    def form_valid(self, form):
        try:
            user = self.request.user
            
            text = pyzbar.decode(Image.open(form.cleaned_data['qrcode']))
            text = text[0].data.decode("utf-8")
            searching = form.cleaned_data['searching']
            if searching:
                items = Item.objects.filter(tag=text, privacy='Public')
            else:
                items = Item.objects.filter(tag=text, owner=user)
                
            return render(self.request, 'item/search_results.html', {'items': items})
        except IntegrityError as e:
            return render(self.request, 'item/search_results.html')

def search_results(request):
    return render(request, 'item/search_results.html')

def show_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'item/show_item.html', {'item': item})

@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)

    if item.owner != request.user:
        messages.add_message(request, messages.INFO, 'You can not delete the item!')
        return redirect('/profile')
    else:
        item.delete()

        messages.add_message(request, messages.INFO, 'Item has been deleted!')
        return redirect('/profile')

class ItemUpdate(UpdateView):
    model = Item
    fields = ['name', 'type', 'desc', 'privacy']
    template_name = "item/item_update_form.html"

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Item has been edited!')
        return reverse_lazy('profile')