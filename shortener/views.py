# from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.db.models import Count

from shortener.models import Bit, StatisticsBit
from shortener.forms import BitForm
from shortener.templatetags.shortly_url import naturaltime


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
    bit.increment_click()
    if bit.user:
        statistic = StatisticsBit(bit=bit)
        statistic.process_request(request)
        statistic.save()
    return redirect(bit, permanent=True)


def renderStatistic(request, bit):
    bit = get_object_or_404(Bit, short_url=bit)
    host = request.META['HTTP_HOST']
    statistics = bit.statistics()
    by_os = statistics.values('plataform').annotate(dcount=Count('plataform'))
    by_browser = statistics.values('browser').annotate(dcount=Count('browser'))
    by_geolocalization = statistics.values('geolocalization').annotate(dcount=Count('geolocalization'))
    by_date = statistics.order_by('-created_at')[:7].values('created_at').annotate(dcount=Count('geolocalization'))

    return render_to_response(
        'statistic.html',
        {
            "bit": bit,
            "host": host,
            "by_os": by_os,
            "by_browser": by_browser,
            "by_geolocalization": by_geolocalization,
            "by_date": by_date,
        },
        context_instance=RequestContext(request)
    )


def createBit(request):
    if not request.is_ajax():
        raise OnlyAjaxException("Only ajax call is permited")

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
            "created_at": "",
            "page_view": 0,
            "details": "",
        }
        return HttpResponse(
            simplejson.dumps(data),
            'application/javascript'
        )

    bit = form.save(commit=False)

    params = {
        "url": bit.url,
    }

    user = request.user
    params["user"] = user if user.is_authenticated() else None

    created = False
    try:
        bit = Bit.objects.get(**params)
    except Bit.DoesNotExist:
        created = True
    # bit, created = Bit.objects.get_or_create(url=url)

    if user.is_authenticated():
        bit.user = user

    if created:
        bit.save()

    host = request.META['HTTP_HOST']
    data = {
        "errors": errors,
        "created": created,
        "url": bit.url,
        "short_url": "http://%s/%s" % (host, bit.short_url),
        "created_at": naturaltime(bit.created),
        "page_view": bit.click,
        "details": bit.get_statistic_url(),
    }
    return HttpResponse(
        simplejson.dumps(data),
        'application/javascript'
    )

class OnlyAjaxException(Exception):
    pass
