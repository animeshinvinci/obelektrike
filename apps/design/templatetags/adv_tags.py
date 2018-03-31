from bs4 import BeautifulSoup as bs
from django import template

from apps.advert import models

# В HTML дергает такие элементы <div class="advert" value="advert-key">...</div>


register = template.Library()

ADVERT_CLASS = 'advert'


@register.filter(name='advfilter')
def advfilter(html_data):
    soup = bs(html_data, "html.parser")
    for i in soup.findAll('div', ADVERT_CLASS):
        i.attrs = filter(lambda x: x[0] != 'style', i.attrs)
        key = i.find(text=True)
        adv = models.Advert.objects.filter(key=key).first()
        if adv:
            key.replaceWith(adv.content)

    return soup.prettify()


@register.simple_tag(name="advert")
def advert(key):
    adv = models.Advert.objects.filter(key=key).first()
    if adv:
        return adv.content
