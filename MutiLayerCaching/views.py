from django.shortcuts import render
from django.http import HttpResponse
from .utils import build_cache_manager, fetch_from_taaghche_book_api

cache = build_cache_manager(fetch_from_taaghche_book_api)


def get_data(request, id):
    response, content_type = cache.get(id)
    print("---------------------------------------")

    return HttpResponse(response, content_type=content_type)

