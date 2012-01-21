from django import template

register = template.Library()


@register.filter
def shortly_url(short_url, host, *args, **kwargs):
    host = host.strip("/")
    if not host.startswith("http"):
        host = "http://%s" % host

    return "%s/%s" % (host, short_url)
