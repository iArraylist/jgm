from django.http import HttpResponse


def home(request):
    if request.user.is_anonymous():
        return HttpResponse("Hello ROM world.")
    else:
        return HttpResponse("Hello ROM " + request.user.username)
