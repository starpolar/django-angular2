import os
from django.shortcuts import get_object_or_404, render
from .models import PubUser
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.query import Query, QueryResult
from django.http import HttpResponse
from django.shortcuts import redirect

def index(request):
    if request.method == 'GET':
        pub_users = PubUser.objects.all()
        return render(request, 'polls/user_list.html', {'pub_users': pub_users})

    if request.method == 'POST':
        pass


def detail(request):

    if request.method == 'GET':
        pub_users = PubUser.objects.all()
        user_id = request.GET["id"]
        user_id = int(user_id)
        res = getCloudantData(user_id)

        response_data = {
            'pub_users': pub_users,
            'cl_data': res
        }
        return render(request, 'polls/user_list.html', response_data)

    if request.method == 'POST':
        data = request.POST
        updateDoc(data)
        return redirect('/')

def updateDoc(data):
    print(data)
    USERNAME = os.environ['cloudant_username']
    PASSWORD = os.environ['cloudant_password']
    URL = os.environ['cloudant_url']
    APIKEY = os.environ['cloudant_apikey']
    DATABASENAME = os.environ['cloudant_databasename']

    # IBM Cloudant Legacy authentication
    client = Cloudant(USERNAME, PASSWORD, url=URL)
    client.connect()

    # IAM Authentication (uncomment if needed, and comment out IBM Cloudant Legacy authentication section above)
    # client = Cloudant.iam(USERNAME, APIKEY)
    # client.connect()
    myDatabase = client[DATABASENAME]
    mydoc = myDatabase[data['_id']]
    data = dict(data)
    for key, value in data.items():
        if 'csrfmiddlewaretoken' != key and '_id' != key and '_rev'!=key and 'user_id' != key:
            mydoc[key] = value[0]
    mydoc.save()
    return "ok"

def getCloudantData(id):
    USERNAME = os.environ['cloudant_username']
    PASSWORD = os.environ['cloudant_password']
    URL = os.environ['cloudant_url']
    APIKEY = os.environ['cloudant_apikey']
    DATABASENAME = os.environ['cloudant_databasename']

    # IBM Cloudant Legacy authentication
    client = Cloudant(USERNAME, PASSWORD, url=URL)
    client.connect()

    # IAM Authentication (uncomment if needed, and comment out IBM Cloudant Legacy authentication section above)
    # client = Cloudant.iam(USERNAME, APIKEY)
    # client.connect()


    myDatabase = client[DATABASENAME]
    # query = Query(myDatabase, skip=10, limit=100)
    # result = QueryResult(query, skip=10, limit=100)
    # if myDatabase.exists():
    #     print("'{0}' successfully created.\n".format(databaseName))

    query = Query(myDatabase,
                  selector={"user_id": id}
                  )
    doc = query()['docs'][0]

    # for doc in query()['docs']:
    #     print(doc)


    # client.disconnect()
    return doc