from django.http import HttpResponseRedirect
from django.shortcuts import render
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone

#from django.views import generic

# Create your views here.
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

def detail(request, pk):
    template = 'catalog/details.html'
    if request.user.is_authenticated:
        item = CategoryItem.objects.filter(pk=pk)
        context = {
                'object': item,
        }
    else:
        context = {}
    return render(request, template, context)

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
