#from django.views.generic import ListView, CreateView, UpdateView
#from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import AccountForm
from .models import Account

# Create your views here.
#class AccountListView(ListView):
#    model = Account
#    contex_object_name = 'obj'
#
#class AccountCreateView(CreateView):
#    model = Account
#    fields = ('item_title', 'item_description', 'item_price', 'category')
#    success_url = reverse_lazy('index')
#
#class AccountUpdateView(UpdateView):
#    model = Account
#    fields = ('item_title', 'item_description', 'item_price', 'category')
#    success_url = reverse_lazy('index')


def catalogRedirect(request):
    return HttpResponseRedirect('/')

def index(request):
    template = 'accountant/index.html'
    user = None
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            user = request.user
            zipcode = form.cleaned_data['zipcode']
            return redirect('index')

    else:
        form = AccountForm()
    context = {
            'form': form,
            'user': user,
            }
    return render(request, template, context)
