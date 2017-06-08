from flask import Flask, jsonify, request, abort, render_template
import requests
import json
import socket
import numpy as np 
from sklearn import linear_model, datasets, svm
import csv
import pickle

TCP_IP = '192.168.18.60'
TCP_PORT = 30

accounts = [
    {
        'id': 1,
        "first_name": u'Bob',
        "last_name": u'Bob',
        "email": u'sealteam6@cap1.com',
        'phone': 12345678,
        'wifi_address': 123456789,
        'card_number': 1234567890,
    
    },
    {
        'id': 2,
        "first_name": u'Jax',
        "last_name": u'Jax',
        "email": u'sealteam6@cap3.com',
        'phone': 12,
        'wifi_address': 8,
        'card_number': 5412753456789010,
    
    },
    {
        'id': 3,
        "first_name": u'Jax',
        "last_name": u'Jax',
        "email": u'sealteam6@cap3.com',
        'phone': 10,
        'wifi_address': 4,
        'card_number': 5,
    
    }
]

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('purchase.html')

@application.route('/buy')
def buy():

    # s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # s.connect((TCP_IP,TCP_PORT))
    # s.send("B")
    # s.close()

    return render_template('buy.html')

@application.route('/accounts', methods=['GET'])
def get_accounts():
    return jsonify({'accounts': accounts})

@application.route('/accounts/<int:account_id>', methods = ['GET'])
def get_account(account_id):
    account = filter(lambda t: t['id'] == account_id, accounts)
    if len(account) == 0:
        abort(404)
    return jsonify( { 'account': account[0] } )

@application.route('/card_number/<int:account_card_number>', methods = ['GET'])
def get_with_card_number(account_card_number):
    account = filter(lambda x: x['card_number'] == account_card_number, accounts)
    if len(account) == 0:
        abort(404)
    return jsonify( { 'account': account[0] } )

@application.route('/card_number/<int:account_wifi_address>', methods = ['GET'])
def get_with_wifi_address(account_wifi_address):
    account = filter(lambda x: x['wifi_address'] == account_wifi_address, accounts)
    if len(account) == 0:
        abort(404)
    return jsonify( { 'account': account[0] } )

@application.route('/accounts', methods = ['POST'])
def create_account():
    #if not request.json or not 'first_name' in request.json:
        #abort(400)
    key = '96b793f91ac0b4f2fd94584dbf2e4e8f'
    customer_id = '5938555aa73e4942cdafd84a'
    customer_url = 'http://api.reimaginebanking.com/customers/'
    url = customer_url + customer_id + '/accounts?key=' + key
    result = requests.get(url).json()[0] # returns result as json

    account = {
        'id': accounts[-1]['id'] + 1,
        'first_name': request.json['first_name'],
        'last_name': request.json.get('last_name', ""),
        'phone': request.json.get('phone', ""),
        'wifi_address': request.json.get('wifi_address', ""),
        'card_number': request.json.get('card_number', ""),
        'email': request.json.get('email', ""),
        'rewards': result['rewards'],
        'customer_id': result['customer_id'],
        'type': result['type'],
        'id': result['_id'],
        'nickname': result['nickname']
    }
    accounts.append(account)
    return jsonify( { 'account': account } ), 201
    
@application.route('/new_card', methods = ['POST'])
def create_card():
    #if not request.json or not 'first_name' in request.json:
        #abort(400)
    card = {
        'id': accounts[-1]['id'] + 1,
        'age': request.json.get('age', ""),
        'income': request.json.get('income', ""),
        'cost_of_living': request.json.get('cost_of_living', ""),
        'dependents': request.json.get('dependents', ""),
        'spending/month': request.json.get('spending/month', ""),
        'credit_score': request.json.get('credit_score', ""),
        'delinquency': request.json.get('delinquency', ""),
        'marital_status': request.json.get('marital_status', ""),
        'recommended': ""
    }
    with open("x.csv", 'rb') as x_file: 
        reader = csv.reader(x_file, delimiter=' ')
        X_train = []
        for row in reader: 
            temp = row[0].split(',')
            temp[5] = float(temp[5])
            for i in range(len(temp)):
                temp[i] = int(temp[i])
            X_train.append(temp)
    with open("y.csv", 'rb') as y_file: 
        reader = csv.reader(y_file, delimiter=' ')
        Y_train_pre = [] 
        for row in reader: 
            Y_train_pre.append(int(row[0]))

    Y_train = []
    Y_train.append(Y_train_pre) 
    Y_train = np.array(Y_train).reshape((-1,1))


    logreg = linear_model.LogisticRegression(C=1e5)
    logreg.fit(X_train, Y_train.ravel())
    s = pickle.dumps(logreg)
    logreg2 = pickle.load(s)

    X = ([[card['age'], card['income'], card['cost_of_living'], card['dependents'], card['spending/month'], card['credit_score'], card['delinquency'], card['marital_status']]])
    result = logreg2.predict(X)
    card['recommended'] = result;

    cards.append(card)
    return jsonify( { 'card': card } ), 201

if __name__ == '__main__':
    application.run(debug=True)