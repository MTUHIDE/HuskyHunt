from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from catalog.models import CatalogItem, Category, SubCategory
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from accountant.models import user_profile
from datetime import datetime, timedelta
import pytz
from profanity_check.models import ArchivedType

# This helper function checks if a user is currently banned / timed out
def isUserNotBanned(username):
    if not (user_profile.objects.filter(user = username)[0].banned_until is None):
        banned_time = (user_profile.objects.filter(user = username)[0].banned_until).astimezone(pytz.timezone('UTC'))
        now = datetime.now().astimezone(pytz.timezone('UTC'))

        if (banned_time > now) :
            return False         # The user is banned and should not be allowed to enter the site

    return True              # The user is not banned

#This small helper function adds an appropriate error message to the page
#param: context - the context that's normally passed to the catalog pages;
#         it's modified appropriately during this function to contain recent items
#param: type - one of 'SearchFail', 'FilterFail', 'PageNotFoundFail', etc.
#param: num_items - The number of recent items displayed, default is 4 most recent
#returns: boolean whether or not
def addErrorOnEmpty(context, type, num_items = 4):
    context['failed_search'] = None
    if context['items'].paginator.count == 0:

        #Gets num_items most recent items from the database and sorts by date added
        recent_items = CatalogItem.objects.filter(
            archived='False',
            date_added__lte=timezone.now()
        ).order_by('-date_added')[:num_items]

        # Paginator will show up to num_items items. Always one page long.
        paginator = Paginator(recent_items, num_items, allow_empty_first_page=True)
        items = paginator.get_page(1)


        context['failed_search'] = type
        context['items'] = items
        return True
    return False


#This function takes information from the search textfield
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all items in the database that contain the string
#from the search text field in their name or description
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def search(request):

    #The CSS code for this function can be found here
    template = 'catalog/index.html'

    #The title for the webpage
    title = 'MTU Catalog'

    #Uses the filter function to get the data of the searched items
    recent_items = CatalogItem.objects.filter(
        Q(item_description__contains=request.GET['search']) | Q(item_title__contains=request.GET['search']),
        archived='False'
    )[:500]

    #Gets all the different categories
    filters = Category.objects.all()

    # Paginator will show 16 items per page
    paginator = Paginator(recent_items, 16, allow_empty_first_page=True)
    page = request.GET.get('page') # Gets the page number to display
    items = paginator.get_page(page)

    #Puts all the data to be displayed into context
    context = {
      'items': items,
      'title': title,
      'filters': filters,
    }

    addErrorOnEmpty(context, 'SearchFail')

    #Returns a render function call to display onto the website for the user to see
    return render(request, template, context)

#This function gets all the items from the database
#and displays them to the screen sorted by most recently added
#param: request - array variable that is passed around the website, kinda like global variables
#returns: all the items in the database, with the most recently item added at the top
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def index(request):

    #The CSS for this function can be found here
    template = 'catalog/index.html'
    #The title for the webpage
    title = "MTU Catalog"

    failed_search = None
    if request.session.has_key('index_redirect_failed_search') and request.session['index_redirect_failed_search'] is not None:
        failed_search = request.session['index_redirect_failed_search']
        request.session['index_redirect_failed_search'] = None

    #Gets 500 most recent items from the database and sorts by date added
    recent_items = CatalogItem.objects.filter(
        archived='False',
        date_added__lte=timezone.now()
    ).order_by('-date_added')[:500]

    # Paginator will show 16 items per page
    paginator = Paginator(recent_items, 16, allow_empty_first_page=True)
    page = request.GET.get('page') # Gets the page number to display
    items = paginator.get_page(page)

    #The filters dropdown containing all the categories (need to get a default category)
    filters = Category.objects.all()

    #Packages the information to be displayed into context
    context = {
        'title': title,
        'filters': filters,
        'items': items,
        'failed_search': failed_search,
    }

    #Displays all the items from the database with repect to the CSS template
    return render(request, template, context)

#This function sets a post to be reported, for review by moderators
#param: request - array variable that is passed around the website, kinda like global variables
#param: pk - a int variable that is used as the primary key for the item in the database
#returns: The same page that the user is currently on
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def report(request, pk):
    # Get the item
    item = CatalogItem.objects.get(pk=pk)
    report_functionality(request, pk, item)
    return HttpResponseRedirect('/catalog/' + str(pk))


def report_functionality(request, pk, item):

    extra_tags = "R" + str(pk)
    # Times to compare
    last_flag_original = user_profile.objects.filter(user = request.user)[0].last_flag
    one_min_ago_original = datetime.now() - timedelta(minutes=1)
    twenty_four_hour_ago_original = datetime.now() - timedelta(hours=24)

    # Update the last flag original time if it is null
    if (last_flag_original == None):
        last_flag_original = twenty_four_hour_ago_original

    #Set same timezone
    last_flag = last_flag_original.astimezone(pytz.timezone('UTC'))
    one_min_ago = one_min_ago_original.astimezone(pytz.timezone('UTC'))
    twenty_four_hour_ago = twenty_four_hour_ago_original.astimezone(pytz.timezone('UTC'))

    # reset last flag count if it has been over 24 hours since last flag
    if (twenty_four_hour_ago > last_flag):
        profile = user_profile.objects.get(user = request.user)
        profile.flags_today = 0
        profile.save()

    # Checks if the user has flagged a post in the last 1 minute
    if (one_min_ago < last_flag):
        # flagged an item less than one minute ago
        messages.error(request, 'Please wait one minute between reporting posts!', extra_tags=extra_tags)

    # Check if user has maxed out on emails today
    elif (user_profile.objects.filter(user = request.user)[0].flags_today >= 5):
        time_remaining = timedelta(hours=24) - (datetime.now().astimezone(pytz.timezone('UTC')) - last_flag)
        messages.error(request, 'You can only report 5 posts per day! Please wait ' + strfdelta(time_remaining, "{hours} hours and {minutes} minutes."), extra_tags=extra_tags)

    else:
        # Set the reported to true
        item.reported = "True" # Report this item
        item.save()
        messages.error(request, 'Post successfully reported!', extra_tags=extra_tags)

        #Set last email sent time and increment number of emails
        profile = user_profile.objects.get(user = request.user)
        profile.last_flag = datetime.now().astimezone(pytz.timezone('UTC'))
        profile.flags_today = profile.flags_today + 1
        profile.save()

    #Caller should redirect the user to the same webpage (So nothing changes but the success message appearing)
    return # eg return HttpResponseRedirect('/catalog/' + str(pk))

# Used in formatting timedelta objects
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

#This function sends a prepared email message to a seller
#param: request - array variable that is passed around the website, kinda like global variables
#param: pk - a int variable that is used as the primary key for the item in the database
#returns: The same page that the user is currently on
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def email(request, pk):
    item = CatalogItem.objects.filter(pk=pk)[0]
    email_functionality(request, pk, item, "an", "item", "")
    #Redirects the user to the same webpage (So nothing changes but the success message appearing)
    return HttpResponseRedirect('/catalog/' + str(pk))

def email_functionality(request, pk, item, article, shortdesc, extra_tags):
    name = request.user.first_name

    MAX_EMAIL_COUNT = 10 # 5 seemed too little if you're buying and trying to coordinate rides

    # Gets the preferred name if not empty
    profile = user_profile.objects.filter(user = request.user)
    if (profile[0].preferred_name):
        name = profile[0].preferred_name

    user_email = request.user.email

    #The body of the email
    message = (name +
              ' has messaged you about ' + article + " " + shortdesc + ' you posted on HuskyHunt!\n\n' +
              'Message from ' + name + ': ' + request.GET['message'] +
              '\n\nYou can respond by replying to this email, or by contacting ' +
              name + ' directly: ' + user_email)

    #The email that this message is sent from
    from_email = name + ' via HuskyHunt <admin@huskyhunt.com>'
    #Gets the item that is currently being viewed
    item_list = (type(item)).objects.filter(pk=pk)
    #Gets the sellers email
    to_email = item_list[0].username.email

    # Times to compare
    last_email_original = user_profile.objects.filter(user = request.user)[0].last_email
    one_min_ago_original = datetime.now() - timedelta(minutes=1)
    twenty_four_hour_ago_original = datetime.now() - timedelta(hours=24)

    # Update the last email original time if it is null
    if (last_email_original == None):
        last_email_original = twenty_four_hour_ago_original

    #Set same timezone
    last_email = last_email_original.astimezone(pytz.timezone('UTC'))
    one_min_ago = one_min_ago_original.astimezone(pytz.timezone('UTC'))
    twenty_four_hour_ago = twenty_four_hour_ago_original.astimezone(pytz.timezone('UTC'))

    # reset last email count if it has been over 24 hours since last email
    if (twenty_four_hour_ago > last_email):
        profile = user_profile.objects.get(user = request.user)
        profile.emails_today = 0
        profile.save()

    # Checks if the user has sent an email in the last 1 minute
    if (one_min_ago < last_email):
        # sent an email less than two minutes ago
        messages.error(request, 'Please wait one minute between emails!', extra_tags=extra_tags)

    # Check if user has maxed out on emails today
    elif (user_profile.objects.filter(user = request.user)[0].emails_today >= MAX_EMAIL_COUNT):
        time_remaining = timedelta(hours=24) - (datetime.now().astimezone(pytz.timezone('UTC')) - last_email)
        messages.error(request, 'You can only send ' + MAX_EMAIL_COUNT + ' messages per day! Please wait ' + strfdelta(time_remaining, "{hours} hours and {minutes} minutes."), extra_tags=extra_tags)

    #Checks if the message is no empty
    elif (request.GET['message'] != ''):
        # Create the email object
        email = EmailMessage(
            'Interested in your ' + shortdesc, # subject
            message, #body
            from_email, # from_email
            [to_email],  # to email
            reply_to=[user_email],  # reply to email
            )

        # Sends the email
        email.send();

        #Set last email sent time and increment number of emails
        profile = user_profile.objects.get(user = request.user)
        profile.last_email = datetime.now().astimezone(pytz.timezone('UTC'))
        profile.emails_today = profile.emails_today + 1
        profile.save()

        #Displays that the email was sent successfully
        messages.error(request, 'Message sent successfully!', extra_tags=extra_tags)

    #If the message is empty then an error message is displayed
    else:
        messages.error(request, 'Please enter a message!', extra_tags=extra_tags)


#This function displays more detailed information about a item
#while removing the other item from the view of the user
#param: request - array variable that is passed around the website, kinda like global variables
#param: pk - a int variable that is used as the primary key for the item in the database
#returns: A new page of the website that contains all information on one item
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def detail(request, pk):

    #The CSS for this page of the website can be found here
    template = 'catalog/details.html'

    #Gets the item from the database
    item_list = CatalogItem.objects.filter(pk=pk)

    #Packages the information to be displayed into context
    context = {
            'item_list': item_list,
    }

    # No page found
    if item_list.count() == 0:
        request.session['index_redirect_failed_search'] = 'PageNotFoundFail'
        return HttpResponseRedirect(reverse('catalog:index'))

    # Item is archived
    if item_list[0].archived:
        if not (item_list[0].username == request.user and ArchivedType.myContent(item_list[0].archivedType) ):
            request.session['index_redirect_failed_search'] = 'PageNotFoundFail'
            return HttpResponseRedirect(reverse('catalog:index'))

    #Changes what the user sees to be more detailed information on the one item
    return render(request, template, context)


#This function allows a user to choose from a dropdown
#what category/ies of items they want to see
#param: request - array passed throughout a website, kinda like global variables
#returns: render function that changes the items the user sees based on the category/ies
@login_required(login_url='/')
@user_passes_test(isUserNotBanned, login_url='/', redirect_field_name='/')
def filter(request):

    #The CSS code for this function can be found here
    template = 'catalog/index.html'

    #The title for the webpage
    title = 'MTU Catalog'

    # Check if no filters or search
    if not (request.GET.getlist('filter') or request.GET.getlist('search')):
        return HttpResponseRedirect('/catalog')

    recent_items = CatalogItem.objects.all()

    # Apply search if it exists
    if (request.GET.getlist('search')):
        recent_items = CatalogItem.objects.filter(
            Q(item_description__contains=request.GET['search']) | Q(item_title__contains=request.GET['search']),
            archived='False'
        ).order_by('-date_added')

    filters = Category.objects.all()
    misform = False
    failed_search = None

    # Apply filters, if they exist
    for filt in request.GET.getlist('filter'):
      if len([x for x in filters if x.category_name == filt]) == 0:
        misform = True
      recent_items = recent_items.filter(
        archived='False',
        category__category_name=filt
      ).order_by('-date_added')[:500]

    # Paginator will show 16 items per page
    paginator = Paginator(recent_items, 16, allow_empty_first_page=True)
    page = request.GET.get('page') # Gets the page number to display
    items = paginator.get_page(page)


    #Gets all the different categories
    curFilters = request.GET.getlist('filter')
        #Puts all the data to be displayed into context
    context = {
      'items': items,
      'title': title,
      'filters': filters,
      'curFilters': curFilters,
      'failed_search': failed_search
    }

    addErrorOnEmpty(context, 'FilterFail')
    if misform:
        context['failed_search'] = "MisformedFilterFail"

        #Returns a render function call to display onto the website for the user to see
    return render(request, template, context)
