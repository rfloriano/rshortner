# from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson

from shorter.models import Bit
from shorter.forms import BitForm


def renderHome(request):
    history = []
    user = request.user
    host = request.META['HTTP_HOST']
    if user.is_authenticated():
        # will load user bits history
        history = Bit.objects.filter(user=user)

    return render_to_response(
        'home.html',
        {
            "history": history,
            "user": user,
            "host": host,
            "form": BitForm()
        },
        context_instance=RequestContext(request)
    )


def renderBit(request, bit):
    bit = get_object_or_404(Bit, short_url=bit)
    bit.increment_page_view()
    return redirect(bit, permanent=True)


def createBit(request):
    if not request.is_ajax():
        raise Exception("Only ajax call is permited")

    url = request.POST.get('url', None)
    if not url:
        return HttpResponse("You need send a url argument")

    form = BitForm(request.POST)
    errors = []
    if not form.is_valid():
        errors = form.errors
        data = {
            "errors": errors,
            "created": False,
            "url": url,
            "short_url": "",
            "created-at": "",
            "page-view": 0,
        }
        return HttpResponse(
            simplejson.dumps(data),
            'application/javascript'
        )

    params = {
        "url": url,
    }

    try:
        bit = Bit.objects.get(**params)
        created = False
    except Bit.DoesNotExist:
        created = True

    bit = form.save(commit=False)
    # bit, created = Bit.objects.get_or_create(url=url)

    user = request.user
    if user.is_authenticated():
        bit.user = user
        params["user"] = user

    bit.save()
    host = request.META['HTTP_HOST']
    data = {
        "errors": errors,
        "created": created,
        "url": bit.url,
        "short_url": "http://%s/%s" % (host, bit.short_url),
        "created-at": bit.created.strftime("%d/%m/%Y at %H:%M"),
        "page-view": bit.page_view,
    }
    return HttpResponse(
        simplejson.dumps(data),
        'application/javascript'
    )
