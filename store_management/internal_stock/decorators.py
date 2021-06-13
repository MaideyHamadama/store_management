from django.http import HttpResponse
from django.shortcuts import redirect


def isStoreKeeper(user):
    return user.groups.filter(name="store_keeper").exists()

def isClientProviderMember(user):
    return user.groups.filter(name="client_provider_member").exists()

#decorator function to return the user to yassa page in case it is not a superuser.
def is_not_superuser(view_func):
    def wrapper_func(request,*args,**kwargs):
        if isStoreKeeper(request.user):
            return redirect('/yassa')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func
