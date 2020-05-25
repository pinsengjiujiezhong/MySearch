#coding=utf-8
from django.shortcuts import render

# Create your views here.
import pymongo
from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
from elasticsearch import Elasticsearch
from redis import StrictRedis
from asn1crypto.ocsp import Request

redis = StrictRedis.from_url('redis://@localhost:6379/1', decode_responses=True)

KEYWORDS = 'keywords'


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})


def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        type = request.GET.get('type', '')
        curr_page = request.GET.get('n', '')
    elif request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        type = request.POST.get('type', '')
        curr_page = request.POST.get('n', '')
    if not keyword:
        return render(request, 'index.html', {})
    if not curr_page:
        curr_page = 1
    curr_page = int(curr_page)
    es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
    items = es.search(index='search', doc_type='hot_search', body={
        "query": {
            "match": {
                "keyword": keyword
            }
        },
        "from": 0,
        'size': 1,
    })
    es_dict = {'blog': 'wenzhang','leyoujia': 'secondhouse'}
    items = es.search(index=type, doc_type=es_dict[type], body={
        "query": {
            "match": {
                "title": keyword
            }
        },
        "from": (int(curr_page) - 1) * 10,
        "size": 10,
    })
    total = items['hits']['total']
    if type == 'blog':
        result = [{'title': item['_source']['title'],
                   'img': item['_source']['img'],
                   'date': item['_source']['date'],
                   'subtitle': item['_source']['subtitle'],
                   'classes': item['_source']['classes'],
                   'url': '/only/' + item['_source']['id'],
                   }
                  for item in items['hits']['hits']]
        for item in result:
            if item['img'].count('http') > 1:
                url = item['img']
                url = url.replace("http://127.0.0.1:8000", "")
                item['img'] = "http://127.0.0.1:8000/static/img/" + url.split(r'//')[1].split('/', 1)[1]
    elif type == 'leyoujia':
        result = [{'title': item['_source']['title'],
                   'url': item['_source']['url'],
                   'img_url': item['_source']['img_url'],
                   'plot': item['_source']['plot'],
                   'plot_url': item['_source']['plot_url'],
                   'location': item['_source']['location'],
                   'tags': item['_source']['tags'],
                   'price': item['_source']['price'],
                   'unitprice': item['_source']['unitprice'],
                   'type': item['_source']['type'],
                   'orientation': item['_source']['orientation'],
                   'size': item['_source']['size'],
                   'big_size': item['_source']['big_size'],
                   'finish': item['_source']['finish'],
                   'floor': item['_source']['floor'],
                   'year': item['_source']['year'],
                   }
                  for item in items['hits']['hits']]
    print({'my_result': result, 'keyword': keyword, 'type': type})
    print('total: ', total)
    page_num = (total // 10 + 2)
    print('page_num: ', page_num)
    pageList = range(1, page_num)
    if curr_page < 5:
        pageList = range(1, page_num)[:10]
    elif curr_page > page_num - 5:
        pageList = range(1, page_num)[page_num-11:]
    else:
        pageList = range(1, page_num)[curr_page - 5: curr_page + 5]
    print()
    return render(request, 'result.html', {'my_result': result, 'keyword': keyword, 'type': type, 'pageList': pageList, 'n': curr_page, 'pagecount': page_num - 1})

def search_title(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        type = request.GET.get('type', '')
    elif request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        type = request.POST.get('type', '')
    if not keyword:
        return render(request, 'index.html', {})
    es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
    es_dict = {'blog': 'wenzhang', 'leyoujia': 'secondhouse'}
    items = es.search(index=type, doc_type= es_dict[type], body={
        "query": {
            "match": {
                "title": keyword
            }
        },
        "from": 0,
        "size": 10,
    })
    if type == 'blog':
        result = [{'title': item['_source']['title'],
                   'url': 'http://127.0.0.1:8000/only/' + item['_source']['id'],
                   }
                  for item in items['hits']['hits']]
    elif type == 'leyoujia':
        result = [{'title': item['_source']['title'],
                   'url': item['_source']['plot_url'],
                   }
                  for item in items['hits']['hits']]
    result = json.dumps(result)
    return HttpResponse(result)


def only(request, only_id):
    es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
    item = es.search(index='blog', doc_type='wenzhang', body={
        "query": {
            "match": {
                "id": only_id
            }
        },
        "from": 0,
        "size": 1,
    })
    result = item['hits']['hits'][0]['_source']
    return render(request, 'blog.html', {'my_result': result})


def onlyOne(request, only_id):
    es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
    item = es.search(index='blog', doc_type='wenzhang', body={
        "query": {
            "match": {
                "id": only_id
            }
        },
        "from": 0,
        "size": 1,
    })
    result = item['hits']['hits'][0]['_source']
    result = json.dumps(result)
    return HttpResponse(result)


def redisKey(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
    elif request.method == 'POST':
        keyword = request.POST.get('keyword', '')
    keys = redis.hkeys(KEYWORDS)
    if keyword in keys:
        redis.hincrby(KEYWORDS, keyword, amount=1)
    else:
        redis.hset(KEYWORDS, keyword, 2)
    return HttpResponse()


def getRedisKey(request):
    result = redis.hgetall(KEYWORDS)
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    #     result = result.sort(key=lambda x : x[1], reverse=True)
    if len(result) > 5:
        result = result[:5]
    keys = []
    for item in result:
        keys.append(item[0])
    keys = json.dumps(keys)
    return HttpResponse(keys)






