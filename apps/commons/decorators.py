from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.views import View


def redirect_to_home_if_authenticated(func):
    def inner_func(*args, **kwargs):
        # For Handling ViewClass Methods
        if isinstance(args[0], View):
            request = args[0].request

        # For Handling View Function
        elif isinstance(args[0], WSGIRequest):
            request = args[0]
        else:
            return func(*args, **kwargs)
        if request.user.is_authenticated:
            return redirect('home')
        return func(*args, **kwargs)
    return inner_func
