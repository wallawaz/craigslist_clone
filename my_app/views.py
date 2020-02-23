import requests

from bs4 import BeautifulSoup
from django.shortcuts import render
from django.conf import settings

from random import random
from requests.compat import quote_plus

from .constants import *
from . import models

def home(request):
    return render(request, 'base.html')

def hit_craiglist(search_str):
    cl_url = BASE_CRAIGSLIST_URL.format(search_str)
    response = requests.get(cl_url)
    data = response.text
    return BeautifulSoup(data, "html.parser")

def parse_soup(soup):
    postings = []
    for post in soup.find_all("li", {"class": "result-row"}):
        post_title = post.find(class_="result-title").text
        post_href = post.find("a").get("href")

        post_price = "N/A"
        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text

        post_image_url = NO_IMAGE_URL
        data_ids = post.find(class_="result-image").get("data-ids")
        if data_ids:
            data_ids = data_ids.split(",")
            slug = data_ids[0].split(":")[1]
            post_image_url = BASE_IMAGE_URL.format(slug)
        
        postings.append(
            models.Posting(
                url=post_href,
                title=post_title,
                image_url=post_image_url,
                price=post_price,
            )
        )
    return postings

def new_search(request):
    payload = {
        "search": request.POST.get("search")
    } 
    if settings.DEV:
        src = "https://dailynewsdig.com/wp-content/uploads/2013/10/cat-stock-photos-{0}.jpg"
        postings = []
        for i in range(1,4):
            postings.append(
                models.Posting(
                    url=f"https:://example/com/{i}",
                    title=f"Example # {i}",
                    image_url=src.format(i),
                    price=i * random() * 10,
                )
            )
        payload["postings"] = postings
        return render(request, "my_app/new_search.html", payload)

    search = request.POST.get("search")
    models.Search.objects.create(search=search)
    soup = hit_craiglist(quote_plus(search))
    postings = parse_soup(soup)
    payload["postings"] = postings
    return render(request, "my_app/new_search.html", payload)
    