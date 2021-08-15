import json
import statistics

import requests


from flask import Flask, request, redirect, session, url_for, Response, json, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask.json import jsonify
from flask_cors import CORS




def loadeq():
    infile = "equalityindex.json"
    with open(infile, encoding="utf8") as f:
        data = json.load(f)

    print ("data loaded")

    return data


edata = loadeq()




# ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'mov'}

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)




def getGoogleData(q):

    # set up the request parameters
    params = {
    'api_key': API_KEY,             ##put api key here
    'q': q,
    'search_type': 'shopping',
    'location': 'United States',
    'shopping_condition': 'new',
    'num': '20',
    'gl': 'us',
    'hl': 'en',
    'google_domain': 'google.com',
    'include_html': 'false'
    }

    # make the http GET request to Scale SERP
    api_result = requests.get('https://api.scaleserp.com/search', params)

    # print the JSON response from Scale SERP
    # print(json.dumps(api_result.json()))

    return api_result.json()

def jfread(filename):
    with open(filename, encoding="utf8") as f:
        data = json.load(f)

    print ("processing data for " + data['search_parameters']['q'])    
    return data



def getei(name, data):
    # infile = "equalityindex.json"
    # with open(infile, encoding="utf8") as f:
    #     data = json.load(f)

    # print ("data loaded")

    n = name.split()[0]  ##might not work always, need stop word detection perhaps
    # print(name)
    n = n.lower()

    # print (n)

    for c in data['cei']:
        x = c['name'].lower()

        # print (x)
        
        if n in x or n == x:
            if c['cei_2020'] == "":
                return c['cei_2021']
            return c['cei_2020']
    
    return -1


    return data


def getavprice(data):
    sum = 0.0
    num = 0.0

    prices = []

    for i in data['shopping_results']:
        # if 'refill' in i['title'] or 'Refill' in i['title']:
        #     continue

        if 'count' in i['title'] or 'pack' in i['title']:
            continue

        prices.append(i['price'])


        sum = sum + float(i['price'])
        num +=1.0
    
    if num == 0:
        return 0.0, 0.0
    
    
    return statistics.mean(prices), statistics.median(prices)


def getmerchants(data):
    m = []
    for i in data['shopping_results']:
        merch = i['merchant']

        if '.' in merch:
            ms = merch.split('.')
            merch = ms[0]


        m.append(merch)

    return m




@app.route("/getInfo", methods=['POST'])
def getinfo():

    print(request)

    res = request.get_json()
    print (res)

    resraw = request.get_data()
    print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()

    q = res['query']

    q = q.lower()


    if q == 'gillette razor':

        
        data = jfread("grazormen.json")

        products = []
        products = data['shopping_results']


        p1, mp1 = getavprice(data)

        merch1 = getmerchants(data)

        mscores1 = []

        for mx in merch1:
            s = getei(mx, edata)
            print (mx + " : " + str(s))
            m = {}
            m["name"] = mx
            m["score"] = s
            mscores1.append(m)


        data = jfread("grazorwomen.json")

        products = products + data['shopping_results']


        p2, mp2 = getavprice(data)

        merch2 = getmerchants(data)

        mscores2 = []

        for mx in merch2:
            s = getei(mx, edata)
            print (mx + " : " + str(s))
            m = {}
            m["name"] = mx
            m["score"] = s
            mscores2.append(m)

        pt = (p2-p1)/p2
        ptm = (mp2-mp1)/mp2
        
        prods = sorted(products, key = lambda i: i['price'])[:5]



    
    if q == 'shampoo' :

        data = jfread("shampoomen.json")

        products = []
        products = data['shopping_results']

        p1, mp1 = getavprice(data)

        merch1 = getmerchants(data)

        mscores1 = []

        for mx in merch1:
            s = getei(mx, edata)
            print (mx + " : " + str(s))
            m = {}
            m["name"] = mx
            m["score"] = s
            mscores1.append(m)


        data = jfread("shampoowomen.json")

        products = products + data['shopping_results']

        p2, mp2 = getavprice(data)

        merch2 = getmerchants(data)

        mscores2 = []

        for mx in merch2:
            s = getei(mx, edata)
            print (mx + " : " + str(s))
            m = {}
            m["name"] = mx
            m["score"] = s
            mscores2.append(m)

        pt = (p2-p1)/p2
        ptm = (mp2-mp1)/mp2

        prods = sorted(products, key = lambda i: i['price'])[:5]







    if q != 'shampoo' and q != 'gillette razor':

        ##live api - uncomment to activate

        # q1 = q + " men"

        # data = getGoogleData(q1)

        # products = []
        # products = data['shopping_results']

        # p1, mp1 = getavprice(data)

        # merch1 = getmerchants(data)

        # mscores1 = []

        # for m in merch1:
        #     s = getei(m, edata)
        #     print (m + " : " + str(s))
        #     m = {}
        #     m["name"] = m
        #     m["score"] = s
        #     mscores1.append(m)


        # q2 = q + " women"

        # data = getGoogleData(q2)

        # products = products + data['shopping_results']

        # p2, mp2 = getavprice(data)

        # merch2 = getmerchants(data)

        # mscores2 = []

        # for m in merch2:
        #     s = getei(m, edata)
        #     print (m + " : " + str(s))
        #     m = {}
        #     m["name"] = m
        #     m["score"] = s
        #     mscores2.append(m)

        # pt = (p2-p1)/p2
        # ptm = (mp2-mp1)/mp2

        # prods = sorted(products, key = lambda i: i['price'])[:5]


##comment out response to activate live api

        resp = Response({"status" : "not found"}, status=200, mimetype='application/json')
        ##resp.headers['Link'] = 'http://google.com'

        return resp
 
 

    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["keyword"] = q 
    status['menmerchants'] = mscores1
    status['womenmerchants'] = mscores2
    status['alternates'] = prods

    men = {}
    price = []
    price.append(p1)
    price.append(mp1)
    
    men['price'] = price
    status['men'] = men

    women = {}
    price2 = []
    price2.append(p2)
    price2.append(mp2)
    
    women['price'] = price
    status['women'] = women

    tax = []
    tax.append(pt)
    tax.append(ptm)
    
    status['tax'] = tax


    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp




@app.route("/dummyJson", methods=['GET', 'POST'])
def dummyJson():

    print(request)

    res = request.get_json()
    print (res)

    resraw = request.get_data()
    print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()
 

    status = {}
    status["server"] = "up"
    status["message"] = "some random message here"
    status["request"] = res 

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp



@app.route("/dummy", methods=['GET', 'POST'])
def dummy():

    ##res = request.json

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp

@app.route("/api", methods=["GET"])
def index():
    if request.method == "GET":
        return {"hello": "world"}
    else:
        return {"error": 400}


if __name__ == "__main__":
    app.run(debug=True, host = 'localhost', port = 8003)
    # app.run(debug=True, host = '#SERVER IP HERE', port = 8003)










##testing


# edata = loadeq()

# # data = getGoogleData('gillette razor men')


# # edata = loadeq()


# data = jfread("grazormen.json")
# p1, mp1 = getavprice(data)
# merch1 = getmerchants(data)

# ##get inclusivity scores
# for m in merch1:
#     s = getei(m, edata)
#     print (m + " : " + str(s))


# # data = jfread("grazorwomen.json")
# # p2, mp2 = getavprice(data)
# # merch2 = getmerchants(data)



# # ##get inclusivity scores
# # for m in merch2:
# #     s = getei(m, edata)
# #     print (m + " : " + str(s))
     

# print ("men average price is " + str(p1))
# print ("men median price is " + str(mp1))
# print("mens merchants :")
# print(merch1)


# print ("--------------------------------------")

# print ("women average price is " + str(p2))
# print ("women median price is " + str(mp2))
# print("womens merchants :")
# print(merch2)

# print ("--------------------------------------")


# pt = (p2-p1)/p2
# print ('raw pink tax on mean is ' + str(pt)) 


# pt = (mp2-mp1)/mp2
# print ('raw pink tax on median is ' + str(pt)) 

# print ("********************************************")
# print ("********************************************")


# data = jfread("shampoomen.json")
# p1, mp1 = getavprice(data)
# merch1 = getmerchants(data)


# ##get inclusivity scores
# for m in merch1:
#     s = getei(m, edata)
#     print (m + " : " + str(s))
     


# data = jfread("shampoowomen.json")
# p2, mp2 = getavprice(data)
# merch2 = getmerchants(data)


# ##get inclusivity scores
# for m in merch2:
#     s = getei(m, edata)
#     print (m + " : " + str(s))
     

# print ("men average price is " + str(p1))
# print ("men median price is " + str(mp1))
# print("mens merchants :")
# print(merch1)


# print ("--------------------------------------")

# print ("women average price is " + str(p2))
# print ("women median price is " + str(mp2))
# print("womens merchants :")
# print(merch2)

# print ("--------------------------------------")


# pt = (p2-p1)/p2
# print ('raw pink tax on mean is ' + str(pt)) 


# pt = (mp2-mp1)/mp2
# print ('raw pink tax on median is ' + str(pt)) 
