import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'
OWNER_TOKEN = None
CUSTOMER_TOKEN = None
RESTAURANT_ID = None
MENU_ITEM_ID = None
ORDER_ID = None

def test_register_owner():
    global OWNER_TOKEN
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'email': 'owner@test.com',
        'password': 'test123',
        'first_name': 'Restaurant',
        'last_name': 'Owner',
        'role': 'restaurant_owner'
    })
    print('Register Owner:', response.status_code)
    print(json.dumps(response.json(), indent=2))
    if response.status_code == 201:
        OWNER_TOKEN = response.json()['access_token']

def test_register_customer():
    global CUSTOMER_TOKEN
    response = requests.post(f'{BASE_URL}/auth/register', json={
        'email': 'customer@test.com',
        'password': 'test123',
        'first_name': 'Test',
        'last_name': 'Customer',
        'address': '456 Customer St'
    })
    print('Register Customer:', response.status_code)
    print(json.dumps(response.json(), indent=2))
    if response.status_code == 201:
        CUSTOMER_TOKEN = response.json()['access_token']

def test_create_restaurant():
    global RESTAURANT_ID
    headers = {'Authorization': f'Bearer {OWNER_TOKEN}'}
    response = requests.post(f'{BASE_URL}/restaurants', headers=headers, json={
        'name': 'Test Restaurant',
        'address': '123 Test St',
        'phone': '1234567890',
        'cuisine_type': 'Italian',
        'opening_time': '09:00',
        'closing_time': '22:00',
        'delivery_fee': 5.00,
        'minimum_order': 15.00
    })
    print('Create Restaurant:', response.status_code)
    print(json.dumps(response.json(), indent=2))
    if response.status_code == 201:
        RESTAURANT_ID = response.json()['id']

def test_add_menu_item():
    global MENU_ITEM_ID
    headers = {'Authorization': f'Bearer {OWNER_TOKEN}'}
    response = requests.post(f'{BASE_URL}/restaurants/{RESTAURANT_ID}/menu', headers=headers, json={
        'name': 'Margherita Pizza',
        'description': 'Classic tomato and mozzarella pizza',
        'price': 12.99,
        'category': 'Pizza',
        'is_vegetarian': True
    })
    print('Add Menu Item:', response.status_code)
    print(json.dumps(response.json(), indent=2))
    if response.status_code == 201:
        MENU_ITEM_ID = response.json()['id']

def test_create_order():
    global ORDER_ID
    headers = {'Authorization': f'Bearer {CUSTOMER_TOKEN}'}
    response = requests.post(f'{BASE_URL}/orders', headers=headers, json={
        'restaurant_id': RESTAURANT_ID,
        'items': [{
            'menu_item_id': MENU_ITEM_ID,
            'quantity': 2,
            'special_instructions': 'Extra cheese please'
        }],
        'delivery_address': '456 Customer St',
        'delivery_instructions': 'Ring the doorbell'
    })
    print('Create Order:', response.status_code)
    print(json.dumps(response.json(), indent=2))
    if response.status_code == 201:
        ORDER_ID = response.json()['id']

def test_update_order_status():
    headers = {'Authorization': f'Bearer {OWNER_TOKEN}'}
    statuses = ['confirmed', 'preparing', 'out_for_delivery', 'delivered']
    
    for status in statuses:
        response = requests.put(f'{BASE_URL}/orders/{ORDER_ID}/status', headers=headers, json={
            'status': status
        })
        print(f'Update Order Status to {status}:', response.status_code)
        print(json.dumps(response.json(), indent=2))
        time.sleep(2)  # Wait between status updates

def test_get_orders():
    # Test customer view
    headers = {'Authorization': f'Bearer {CUSTOMER_TOKEN}'}
    response = requests.get(f'{BASE_URL}/orders', headers=headers)
    print('Get Customer Orders:', response.status_code)
    print(json.dumps(response.json(), indent=2))
    
    # Test restaurant owner view
    headers = {'Authorization': f'Bearer {OWNER_TOKEN}'}
    response = requests.get(f'{BASE_URL}/orders', headers=headers)
    print('Get Restaurant Orders:', response.status_code)
    print(json.dumps(response.json(), indent=2))

def run_tests():
    print("Starting API Tests...")
    test_register_owner()
    test_register_customer()
    test_create_restaurant()
    test_add_menu_item()
    test_create_order()
    test_update_order_status()
    test_get_orders()
    print("API Tests completed!")

if __name__ == '__main__':
    run_tests() 