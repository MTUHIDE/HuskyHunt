from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone
from django.db.models import Q
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages


#from django.views import generic

# Create your views here.
def search(request):
	template = 'catalog/index.html'
	title = 'MTU Catalog'
	if request.user.is_authenticated:
		recent_items = CatalogItem.objects.filter(
			Q(item_description__contains=request.GET['search']) | Q(item_title__contains=request.GET['search'])
		)
		filters = Category.objects.all()
		context = {
			'item_list': recent_items,
			'title': title,
			'filters': filters,
		}
		return render(request, template, context)
	else:
		return HttpResponseRedirect('/')

def index(request):
	template = 'catalog/index.html'
	title = "MTU Catalog"
	if request.user.is_authenticated:
		recent_items = CatalogItem.objects.filter(
			date_added__lte=timezone.now()
		).order_by('-date_added')[:5]
		filters = Category.objects.all()
		context = {
			'item_list': recent_items,
			'title': title,
			'filters': filters,
		}
		return render(request, template, context)
	else:
		return HttpResponseRedirect('/')

def email(request, pk):
    if request.user.is_authenticated:
        subject = "Interested in your item"
        message = (request.user.username + 
                  ' has messaged you about an item you posted on HuskyHunt!\n\n' + 
                  request.user.username + ': ' + request.GET['message'] + 
                  '\n\nReply at: ' + request.user.email + 
                  '\n*Do not reply to this email. Your reply will be forever ' + 
                  'lost in the interweb and your will be sad')
        from_email = 'admin@huskyhunt.com'
        item_list = CatalogItem.objects.filter(pk=pk)
        to_email = ''
        #need to add an email to category item. for now assume username is mtu username
        for item in item_list:
            to_email = item.username.email
        if message:
            send_mail(subject, message, from_email, [to_email], fail_silently=False,)
            messages.error(request, 'Message sent successfully!')
        return HttpResponseRedirect('/catalog/' + str(pk))
    else:
        return HttpResponseRedirect('/')

def detail(request, pk):
    template = 'catalog/details.html'
    if request.user.is_authenticated:
        item_list = CatalogItem.objects.filter(pk=pk)
        context = {
                'item_list': item_list,
        }
    else:
        context = {}
    return render(request, template, context)

def filter(request, category):
    template = 'catalog/index.html'
    title = "MTU Catalog"
    if request.user.is_authenticated:
        recent_items = CatalogItem.objects.filter(category__category_name=category)
        filters = Category.objects.all()
        context = {
            'item_list': recent_items,
            'title': title,
            'filters': filters,
        }
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')


"""
item = get_object_or_404(CategoryItem, pk=pk)
try:
    selected_choice = item.choice_set.get(pk=request.POST['choice'])
except (KeyError, CategoryItem.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "You didn't select a choice.",
    })
else:
    selected_choice.votes += 1
    selected_choice.save()
    #Always return an HttpResponseRedirect after successfully
    #dealing with POST data.  This prevents data from being posted twice
    #if a user hits the Back button in the browser.
    return HttpResponseRedirect(reverse('polls:results', args=(question.pk,)))
"""
