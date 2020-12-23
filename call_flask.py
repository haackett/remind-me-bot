import requests
import json
import base62

API_URL = 'https://secret-plateau-28364.herokuapp.com/'

def get_todos():
    response = requests.get(API_URL + '/todos/')
    if response.status_code == 200:
        print(response.json())
        return(response.json())
    else:
        print('Uh oh! Something went wrong: ' + str(response.status_code))
        return('Uh oh! Something went wrong: ' + str(response.status_code))

def post_todo(text, dependent_users):
    post_body = {}
    post_body['text'] = text
    post_body['dependent_users'] = dependent_users
    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

    response = requests.post(API_URL + '/todos/', data=json.dumps(post_body), headers=headers)
    if response.status_code == 200:
        print(response.json())
        return(response.json())
    else:
        print('Uh oh! Something went wrong: ' + str(response.status_code))
        return('Uh oh! Something went wrong: ' + str(response.status_code))

def put_todo(todo_id, completed): 
    int_todo_id = base62.decode(todo_id)
    put_body = {}
    put_body['completed'] = completed
    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

    response = requests.put(API_URL + '/todos/' + str(int_todo_id), data=json.dumps(put_body), headers=headers)
    if response.status_code == 200:
        print(response.json())
        return(response.json())
    else:
        print('Uh oh! Something went wrong: ' + str(response.status_code))
        return('Uh oh! Something went wrong: ' + str(response.status_code))


def delete_todo(todo_id):
    int_todo_id = base62.decode(todo_id)
    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    response = requests.delete(API_URL + '/todos/' + str(int_todo_id), headers=headers)
    if response.status_code == 200:
        print(response.json())
        return(response.json())
    else:
        print('Uh oh! Something went wrong: ' + str(response.status_code))
        return('Uh oh! Something went wrong: ' + str(response.status_code))
