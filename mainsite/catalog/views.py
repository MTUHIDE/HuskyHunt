from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages

#This function takes information from the search textfield
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all items in the database that contain the string 
#         from the search text field in their name or description
def search(request):
    #The CSS code for this function can be found here                 
	template = 'catalog/index.html'      
    #The title for the webpage
	title = 'MTU Catalog' 

    #Checks to make sure the user has logged in               
	if request.user.is_authenticated:    
        #Uses the filter function to get the data of the searched items
		recent_items = CatalogItem.objects.filter(
			Q(item_description__contains=request.GET['search']) | Q(item_title__contains=request.GET['search'])
		)
        #Gets all the different categories
		filters = Category.objects.all()

        #Puts all the data to be displayed into context
		context = {
			'item_list': recent_items,
			'title': title,
			'filters': filters,
		}

        #Returns a render function call to display onto the website for the user to see
		return render(request, template, context)

    #If the user is not logged in then they get redirected to the HuskyStatue screen
	else:
		return HttpResponseRedirect('/')

#This function gets all the items from the database 
#and displays them to the screen sorted by most recently added
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all the items in the database, with the most recently item added at the top
def index(request):

    #The CSS for this function can be found here
    template = 'catalog/index.html'
    #The title for the webpage
    title = "MTU Catalog"

    #Checks if the user is logged in
    if request.user.is_authenticated:

        #Gets all the items from the database and sorts by date added
        recent_items = CatalogItem.objects.filter(
            date_added__lte=timezone.now()
        ).order_by('-date_added')[:5]

        #The filters dropdown containing all the categories (need to get a default category)
        filters = Category.objects.all()

        #Packages the information to be displayed into context
        context = {
            'item_list': recent_items,
            'title': title,
            'filters': filters,
        }

        #Displays all the items from the database with repect to the CSS template
        return render(request, template, context)
    else:
        return HttpResponseRedirect('/')

#This function sends a prepared email message to a seller
#param: request - array variable that is passed around the website, kinda like global variables
#param: pk - a int variable that is used as the primary key for the item in the database
#returns: The same page that the user is currently on
def email(request, pk):
    #Checks if the user has logged in
    if request.user.is_authenticated:
        
        #The subject line of the email
        subject = "Interested in your item"
        
        #The body of the email
        message = (request.user.username + 
                  ' has messaged you about an item you posted on HuskyHunt!\n\n' + 
                  request.user.username + ': ' + request.GET['message'] + 
                  '\n\nReply at: ' + request.user.email + 
                  '\n*Do not reply to this email. Your reply will be forever ' + 
                  'lost in the interweb and your will be sad')
        
        #The email that this message is sent from
        from_email = 'admin@huskyhunt.com'
        #Gets the item that is currently being viewed
        item_list = CatalogItem.objects.filter(pk=pk)
        #Creates a variable to later store the sellers email
        to_email = ''

        #need to add an email to category item. for now assume username is mtu username

        #For each loop that iterates on the number of items being currently viewed? Need to ask isaac about this
        for item in item_list:
            #Sets the recipient of the email as the sellers email from the database
            to_email = item.username.email
        
        #Checks if the message is no empty
        if (request.GET['message'] != ''):
            #Sends the email with a subject, body, the sender, and the recipient
            send_mail(subject, message, from_email, [to_email], fail_silently=False,)
            #Displays that the email was sent successfully
            messages.error(request, 'Message sent successfully!')
        
        #If the message is empty then an error message is displayed
        else:
            messages.error(request, 'Please enter a message!')
        
        #Redirects the user to the same webpage (So nothing changes but the success message appearing)
        return HttpResponseRedirect('/catalog/' + str(pk))
    
    #If not logged in then the user is sent to the Husky Statue 
    else:
        return HttpResponseRedirect('/')

#This function displays more detailed information about a item
#while removing the other item from the view of the user
#param: request - array variable that is passed around the website, kinda like global variables
#param: pk - a int variable that is used as the primary key for the item in the database
#returns: A new page of the website that contains all information on one item 
def detail(request, pk):

    #The CSS for this page of the website can be found here
    template = 'catalog/details.html'
    
    #Checks if the user is logged in
    if request.user.is_authenticated:
        
        #Gets the item from the database
        item_list = CatalogItem.objects.filter(pk=pk)
        
        #Packages the information to be displayed into context
        context = {
                'item_list': item_list,
        }
    
    #Changes what the user sees to be more detailed information on the one item
        return render(request, template, context)
    #If the user is not logged in, redirect to login
    else:
        return HttpResponseRedirect('/')


#This function allows a user to choose from a dropdown
#what category of items they want to see
#param: request - array passed throughout a website, kinda like global variables
#param: category - variable that contains the category name the user clicked on
#returns: render function that changes the items the user sees based on the category
def filter(request, category):

    #The CSS for this function can be found here
    template = 'catalog/index.html'
    #The title of the webpage
    title = "MTU Catalog"

    #Checks if the user is logged in
    if request.user.is_authenticated:

        #Gets the category to be filtered by from the database
        #Finds the desired category from the passed in argument
        recent_items = CatalogItem.objects.filter(category__category_name=category)
        #Keeps the filters dropdown containing all the categories (need to get a default category)
        filters = Category.objects.all()
        context = {
            'item_list': recent_items,
            'title': title,
            'filters': filters,
        }
        #Displays the new view with items only in the desired category
        return render(request, template, context)
    
    #If the user is not logged in then they are sent to the Husky Statue
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
