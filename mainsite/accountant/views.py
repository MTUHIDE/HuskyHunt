#from django.views.generic import ListView, CreateView, UpdateView
#from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import AccountForm
from .models import Account
from django.contrib import auth
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone
from django.urls import reverse

from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from django.forms import ModelForm

from django.forms.widgets import ClearableFileInput, TextInput, Textarea
from django.template import loader
from django.utils.safestring import mark_safe

from django.utils.translation import gettext_lazy as _

class PreviewImageWidget(ClearableFileInput):
    template_name = "accountant/preview_image.html"

    clear_button_label = _('Reset')
    default_width = 150
    default_height = 150
    defaultPictureURL = 'https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg'

    def clear_button_name(self, name):
        return name + '-clear'
    def clear_button_id(self, name):
        return name + '_id'
    def preview_image_name(self, name):
        return name + '-preview'
    def preview_image_id(self, name):
        return name + '_id'
    #def format_value:

    def get_context(self, name, value, attrs):
        width = attrs.get('width', self.default_width)
        height = attrs.get('height', self.default_height)

        button_name = self.clear_button_name(name)
        button_id = self.clear_button_id(button_name)
        preview_name = self.preview_image_name(name)
        preview_id = self.preview_image_id(preview_name)

        context = super().get_context(name, value, attrs)
        some_unneeded_fields = ['checkbox_name', 'checkbox_id', 'clear_button_label', 'is_initial', 'initial_text']
        for i in some_unneeded_fields:
            context.pop(i, None)

        context['widget'].update({
            #'value':  #presumably passed up in the ModelForm
            'defaultPictureURL': self.defaultPictureURL,

            'button_name': button_name,
            'button_id': button_id,
            'clear_button_label': self.clear_button_label,

            #name, attrs -- inherited
            'id': (name + '_id'),

            'preview_text': "Uploaded Image",
            'preview_id': preview_id,
            'preview_width': width,
            'preview_height': height,
        })

        return context

    def value_from_datadict(self, data, files, name):
        return files.get(name)

class EditModelForm(ModelForm):
    class Meta:
        model = Account
        fields = ['bio', 'street_address', 'city', 'zipcode', 'common_destination_zipcode', 'picture']
        widgets = {
            'bio': Textarea(attrs={'rows': 5}),
            'picture': PreviewImageWidget()
        }

def edit(request):
    try:
        currentUser = Account.objects.get(user = request.user)
    except Account.DoesNotExist:
        createDefaultAccount(request.user)
        currentUser = Account.objects.get(user = request.user)

    if request.method == "POST":
        if request.FILES.get('picture') is None:
            currentUser.picture = None
        form = EditModelForm(request.POST, request.FILES, instance = currentUser)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accountant:index'))
    else: # request.method == "GET"
        form = EditModelForm(instance = currentUser)

    return render(request, 'accountant/account_detail.html', {'form': form})


def catalogRedirect(request):
    return HttpResponseRedirect('/catalog')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def index(request):
   if request.user.is_authenticated:
      try:
          currentUser = Account.objects.get(user = request.user)
      except Account.DoesNotExist:
          createDefaultAccount(request.user)
          currentUser = Account.objects.get(user = request.user)

      template = 'accountant/index.html'
      defaultPicture = 'https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg'
      my_items = CatalogItem.objects.filter(username = request.user)
      filters = Category.objects.all()
      title = 'My items'
      context = {
                  'item_list':my_items,
                  'title': title,
                  'filters': filters,
                  'defaultPicture': currentUser.picture.url if currentUser.picture else defaultPicture,
        }
      return render(request, template, context)
   else:
      return HttpResponseRedirect('/')

def deleteItem(request, pk):
  if request.user.is_authenticated:
    # delete item from database
    item = CatalogItem.objects.filter(pk=pk)

    # delete only if this user owns the item, a precautionary measure
    if item.get(pk=pk).username == request.user:
      item.delete();

    # redirect to accountant page
    return HttpResponseRedirect('/accountant')
  else:
    return HttpResponseRedirect('/')
