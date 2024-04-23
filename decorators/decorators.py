from django.shortcuts import redirect


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.group:
                group = request.user.group
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('frontend-login')
        return wrapper_func

    return decorator


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('backend-dashboard-page')
        else:

            return view_func(request, *args, **kwargs)

    return wrapper_func
