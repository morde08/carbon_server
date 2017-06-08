# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

def main():
    key = '96b793f91ac0b4f2fd94584dbf2e4e8f'
    customer_id = '5938555aa73e4942cdafd84a'
    customer_url = 'http://api.reimaginebanking.com/customers/'
    url = customer_url + customer_id + '/accounts?key=' + key
    result = requests.get(url).json()
    print(type(result))
    print(result)
    # result = requests.get(url).json()[0] # returns result as json
    # for key in result:
    #     if isinstance(result[key], int):
    #         print(key.encode("utf-8"), result[key])
    #     else:
    #         print(key.encode("utf-8"), result[key].encode("utf-8"))

if __name__ == "__main__":
    main()
