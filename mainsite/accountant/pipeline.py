from django.http import HttpResponseRedirect
from django.contrib import messages


def verify_scope(request, backend, user, response, *args, **kwargs):
    if not user.email.endswith('@mtu.edu'):
        messages.warning(request, 'Please log in with your MTU email.')
        user.delete()  # Delete the user since we don't need to keep track of users without an mtu email
        return HttpResponseRedirect('/')


def update_user_social_data(strategy, *args, **kwargs):
    response = kwargs['response']
    backend = kwargs['backend']
    user = kwargs['user']

    print(response, backend, user)

    # if response['picture'] and kwargs['is_new']:
    #     url = response['picture']
    #     userProfile_obj = user_profile.objects.get(pk=user.id)

    #     resp = requests.get(url)
    #     if resp.status_code != requests.codes.ok:
    #         return

    #     fp = BytesIO()
    #     fp.write(resp.content)
    #     file_name = url.split("/")[-1]

    #     userProfile_obj.picture.save(file_name, files.File(fp))
