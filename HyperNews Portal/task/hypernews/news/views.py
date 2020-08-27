from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views import View
import json
import sys
import random
from datetime import datetime


class Index(View):
    def get(self, request):
        return redirect('/news/')


def my_dict(*newlink):
    with open(settings.NEWS_JSON_PATH, 'r') as f:
        x = json.load(f)
        if newlink:
            if not newlink in x:
                x.append(*newlink)
                with open(settings.NEWS_JSON_PATH, 'w') as f:
                    json.dump(x, f)
    return x


class NewsView(View):
    def get(self, request, link, *args, **kwargs):
        articles = my_dict()
        for news in articles:
            if news['link'] == link:
                return render(request, 'news/links.html', context=news)
        raise Http404


class MainView(View):
    @classmethod
    def searched_news(cls,articles, searches):
        new_dict = []
        for i in articles:
            if searches in i['title']:
                new_dict.append(i)
        return new_dict

    def get(self, request, *args, **kwargs):
        articles = my_dict()
        query = request.GET.get('q')
        if query:
            try:
                query = ''.join(query.split('+'))
                articles = self.searched_news(articles, query)
            except:
                pass
        context = {'de': articles}

        return render(request, 'news/main.html', context=context)



class AddView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/newlink.html')

    @classmethod
    def create_random(cls,articles):
        links = [i['link'] for i in articles]
        while True:
            x = random.randint(1, sys.maxsize)
            if x not in links:
                return x

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        deflink = {}
        articles = my_dict()
        deflink['created'] = str(datetime.now())

        deflink['link'] = self.create_random(articles)
        deflink['title'] = title
        deflink['text'] = text
        my_dict(deflink)
        return redirect('/news/')
