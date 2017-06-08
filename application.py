from flask import Flask, jsonify, request, abort, render_template
import requests
import json
import socket
import numpy as np 
from sklearn import linear_model, datasets, svm
import csv
import pickle
import sys

TCP_IP = '192.168.18.60'
TCP_PORT = 30

accounts = [
    {
        'id': 1,
        "first_name": u'Rich',
        "last_name": u'Fairbanks',
        "email": u'sealteam6@cap1.com',
        'phone': 12345678,
        'wifi_address': 123456789,
        'card_number': 5412753456789010,
        'rewards': 11567,
        'customer_id': u'5938555aa73e4942cdafd84a',
        'balance': 8158,
        'type': u'Savings',
        'id': u'5938555aa73e4942cdafd84a',
        'nickname': u'Big Baller'
    
    }
]
cards = []

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
        #'id': accounts[-1]['id'] + 1,
        'first_name': request.json['first_name'],
        'last_name': request.json.get('last_name', ""),
        'phone': request.json.get('phone', ""),
        'wifi_address': request.json.get('wifi_address', ""),
        'card_number': request.json.get('card_number', ""),
        'email': request.json.get('email', ""),
        'rewards': result['rewards'],
        'customer_id': result['customer_id'],
        'balance': result['balance'],
        'type': result['type'],
        'balance': result['balance'],
        'id': result['_id'],
        'nickname': result['nickname']
    }
    accounts.append(account)
    return jsonify( { 'account': account } ), 201

@application.route('/new_card', methods = ['POST'])
def create_card():
    #if not request.json or not 'first_name' in request.json:
        #abort(400)
    json = request.get_json(silent=True)
    print json
    sys.stdout.flush()
    card = {
        #'id': accounts[-1]['id'] + 1,
        'age': request.json.get('age', "30"),
        'income': request.json.get('income', "50000"),
        'cost_of_living': request.json.get('cost_of_living', "3000"),
        'dependents': request.json.get('dependents', "2"),
        'spending/month': request.json.get('spending/month', "5000"),
        'credit_score': request.json.get('credit_score', "600"),
        'delinquency': request.json.get('delinquency', "0"),
        'marital_status': request.json.get('marital_status', "1"),
    }
    #print card
    sys.stdout.flush()
    x = []
    for k in card:
        print(card[k])
        x.append(int(card[k]))
    with open('logmodel.pkl', 'rb') as f:
        logreg = pickle.load(f)
    pkl_file = open('logmodel.pkl', 'rb')
    pred = logreg.predict(x)
    card['recommended'] = pred[0]
    #print card
    print pred[0] 
    sys.stdout.flush()
    cards.append(card)
    return jsonify( { 'recommended_card': card['recommended'] } ), 201

@application.route('/cards', methods=['GET'])
def get_cards():
    return jsonify({'cards': cards})

if __name__ == '__main__':
    application.run(debug=True)