from flask import Flask, request
import dialogflow
import os
import random
import datetime
import requests
import csv
import json
from google.protobuf.json_format import MessageToDict

with open('config.json', 'r') as f:
    config = json.load(f)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['GOOGLE_CRED']

app = Flask(__name__)

PROJECT_ID = config['PROJECT_ID']
LANGUAGE_CODE = config['LANGUAGE_CODE']
SESSION_ID = str(datetime.datetime.now())

session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, SESSION_ID)

default_negatives = [
    "I'm sorry. I'm having trouble understanding the question.",
    "I think I may have misunderstood your last statement.",
    "I'm sorry. I didn't quite grasp what you just said.",
    "I don't think I'm qualified to answer that yet.",
    "I'm a bit confused by that last part.",
    "I'm not totally sure about that.",
    "I'm not sure I follow.",
    "I'm afraid I don't understand.",
    "I'm a bit confused."
]


@app.route('/', methods=['POST'])
def hello():
    return "Hello World!"


headers = config['HEADERS']

cart_id = "6Qu9O8HYfUm5PY_Euf45Rg"
cart = dict()


class Api:
    def get_product_id(self, product):
        if product == "milk":
            return "0015001"
        elif product == 'cola':
            return "101"
        url = "http://localhost:5000/catalog/items"
        response = requests.request("GET", url, headers=headers, data={})
        ans = None
        try:
            ans = response.json()['pageContent']
        except:
            print(ans)
            return response.json()
        for each in ans:
            if each['packageIdentifiers'][0]['type'].lower() == product.lower():
                return each['itemId']['itemCode']
        return "False"

    def add_to_cart(self, product, quantity):
        if product not in cart:
            cart[product] = quantity
        else:
            cart[product] += quantity
        return "Added to cart!"
        pr_id = self.get_product_id(product)
        print(product)
        print(quantity)
        if pr_id == "False":
            return "False"
        if cart_id is None:
            self.create_cart()
        url = f"http://localhost:5000/emerald/selling-service/v1/carts/{cart_id}/items"
        body = {
            "scanData": pr_id,
            "quantity": {
                "unitOfMeasure": "EA",
                "value": quantity
            }
        }
        print(body)
        response = requests.request("POST", url, headers=headers, data=body)
        ans = response.json()
        return "Added to cart!"

    def create_cart(self):
        global cart_id
        url = "http://localhost:5000/emerald/selling-service/v1/carts"
        response = requests.request("POST", url, headers=headers, data={})
        c_id = response.headers['Location'].split("/")[2]
        cart_id = c_id
        return True

    def get_cart_contents(self):
        if cart_id is None:
            self.create_cart()
        url = f"http://localhost:5000/emerald/selling-service/v1/carts/{cart_id}/items"

        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        items = []
        try:
            ans = response.json()['pageContent']
        except:
            ans = response.text.encode('UTF-8')
            print(ans)
            # return json.dumps(items)
        for each in ans:
            items.append(each['description'])

        return json.dumps(cart)

    def clear_cart(self):
        url = "http://localhost:5000/emerald/selling-service/v1/carts/6Qu9O8HYfUm5PY_Euf45Rg"
        response = requests.request("DELETE", url, headers=headers, data={})
        global cart
        cart = dict()
        return response.text

    def checkout(self):
        pass

    def get_status(self):
        pass

    def get_all_details(self):
        url = "http://localhost:5000/catalog/items"

        payload = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        ans = None
        try:
            ans = response.json()['pageContent']
        except:
            print(ans)
            return response.json()

        items = []
        for each in ans:
            if each['status'] == 'ACTIVE':
                items.append(each)
        return json.dumps(items)

    def get_all_categories(self):
        url = "http://localhost:5000/catalog/items"
        response = requests.request("GET", url, headers=headers, data={})
        ans = None
        try:
            ans = response.json()['pageContent']
        except:
            print(ans)
            return response.json()
        items = []
        for each in ans:
            if each['status'] == 'ACTIVE':
                items.append(each['departmentId'])
        return json.dumps(list(set(items)))

    def get_all_items(self):
        url = "http://localhost:5000/catalog/items"
        response = requests.request("GET", url, headers=headers, data={})
        ans = response.json()['pageContent']
        items = []
        for each in ans:
            if each['status'] == 'ACTIVE':
                items.append(each['packageIdentifiers'][0]['type'])
        return json.dumps(items)


@app.route('/get-all-items', methods=['POST'])
def return_all_items():
    api = Api()
    return api.get_all_items()


@app.route('/get-all-details', methods=['POST'])
def return_all_details():
    api = Api()
    return api.get_all_details()


@app.route('/get-all-categories', methods=['POST'])
def return_all_categories():
    api = Api()
    return api.get_all_categories()


@app.route('/create-cart', methods=['POST'])
def create_my_cart():
    api = Api()
    return api.create_cart()


@app.route('/get-cart', methods=['POST'])
def get_my_cart():
    api = Api()
    return api.get_cart_contents()


@app.route('/add-product', methods=['POST'])
def add_a_product():
    api = Api()
    data = json.loads(request.data)
    product = data['product']
    quantity = data['quantity']
    return api.add_to_cart(product, quantity)


def data_in_sheets(query):
    CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSNNDte3XsS6Br573NXm9YsSqa-d9FwN10SWKWjTBSM8jEbpf5cOmtyqHh5feOXZyBXz6tQFioMaeFs/pub?output=csv'
    with requests.Session() as s:
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for q, a in my_list:
            if q.lower() == query.lower():
                return a
    return False


@app.route('/chatbot', methods=['POST'])
def runSample():
    text = request.json['text']
    api = Api()
    text_input = dialogflow.types.TextInput(
        text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    query = response.query_result.query_text
    print('Query text: {}'.format(response.query_result.query_text))
    intent = response.query_result.intent.display_name
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    print("Params: {}\n".format(response.query_result.parameters))

    if intent == "add.item":
        product_to_add = MessageToDict(response.query_result.parameters.fields['product_to_add'])
        quantity_to_add = MessageToDict(response.query_result.parameters.fields['quantity_to_add'])
        if product_to_add != '' and quantity_to_add != '':
            x = api.add_to_cart(product_to_add, quantity_to_add)
            if x == "False":
                return f'Successfully added {quantity_to_add} of {product_to_add} into your cart.'
            else:
                return f'Product not in catalog'
    if intent == "cart.check":
        products = eval(api.get_cart_contents())
        if not products:
            return "Your cart is empty"
        else:
            return f"Your cart contains {len(products)} products: {', '.join([str(i) for i in products])}."
    if intent == "check_out":
        card_number = MessageToDict(response.query_result.parameters.fields['card-number'])
        email = MessageToDict(response.query_result.parameters.fields['email'])
        name = MessageToDict(response.query_result.parameters.fields['name'])
        password = MessageToDict(response.query_result.parameters.fields['password'])
        cvv = MessageToDict(response.query_result.parameters.fields['security-code'])
        if card_number != '' and email != '' and name != '' and password != '' and cvv != '':
            api.checkout()
            return "Congratulations! Your order has been placed!"
    if intent == "Default Fallback Intent":
        qna = data_in_sheets(query)
        if not qna:
            return random.choice(default_negatives)
        else:
            return qna
    if intent == "Default Welcome Intent":
        return "Hello! How can I assist you?"
    if intent == "order.cancel":
        order_no = MessageToDict(response.query_result.parameters.fields['order_number'])
        if order_no != '':
            return f"Your order {order_no} has been successfully cancelled"
    if intent == "order.change":
        order_no = MessageToDict(response.query_result.parameters.fields['phone-number'])
        if order_no != '':
            return f"Your order {order_no} has been changed successfully cancelled"
    if intent == "clear.cart":
        api.clear_cart()
        return f'Your cart has been emptied.'
    if intent == "order.status":
        order_no = MessageToDict(response.query_result.parameters.fields['order-number'])
        email = MessageToDict(response.query_result.parameters.fields['email'])
        if email != '' and order_no != '':
            st = api.get_status()
            return f'The status of your order is processing'
    if intent == "product.query":
        items = eval(api.get_all_items())
        for x in items:
            print(x)
        return f"We sell the following items: {', '.join(items)}"

    return response.query_result.fulfillment_text


if __name__ == '__main__':
    app.run(debug=False)
