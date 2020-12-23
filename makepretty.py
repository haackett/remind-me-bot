import json
import base62


def todo_json_to_string(json_list, view='all'):
    if view == 'all':
        post = 'ALL TODOS' + '\n\n'
        if json.loads:
            for todo in json_list:
                if todo['completed'] == False:
                    post +=  ':exclamation:'+ str(base62.encode(todo['id'])) + ' : ' + todo['text'] + '\n'
                elif todo['completed'] == True:
                    post += ':white_check_mark:' + str(base62.encode(todo['id'])) + ' : ' + todo['text'] + '\n'
        return post
    elif view == 'completed':
        post = 'COMPLETED TODOS' + '\n\n'
        if json.loads:
            for todo in json_list:
                if todo['completed'] == True:
                    post += ':white_check_mark:' + str(base62.encode(todo['id'])) + ' : ' + todo['text'] + '\n'
        return post
    elif view == 'incompleted':
        post = 'INCOMPLETED TODOS' + '\n\n'
        if json.loads:
            for todo in json_list:
                if todo['completed'] == False:
                    post += ':exclamation:'+ str(base62.encode(todo['id'])) + ' : ' + todo['text'] + '\n'
        return post

def todo_json_to_string_with_mentions(json_list):
    header = 'STUFF TO BE DONE'
    string = header + '\n\n'
    if json.loads:
        for todo in json_list:
            if todo['completed'] == False:
                string +=  ':exclamation:' + str(base62.encode(todo['id'])) + ' : ' 
                for user in todo['dependent_users']:
                    string += user + ' '
                string += todo['text'] + '\n'
            elif todo['completed'] == True:
                string += ':white_check_mark:' + str(base62.encode(todo['id'])) + ' : ' +  todo['text']  + '\n'
    return string

def todo_post_response_to_string(response):
        todo = response[1]
        return '`Todo {0} Added for {1} : {2}`'.format(base62.encode(todo['id']), user_list_to_string(todo['dependent_users']), todo['text'])

def todo_delete_response_to_string(response):
        todo = response[1]
        return '`Todo {0} Deleted`'.format(base62.encode(todo['id']))

def todo_put_response_to_string(response):
        todo = response[1]
        return '`Todo {0} Updated : {1} {2}`'.format(base62.encode(todo['id']), todo['text'], todo['completed'])

def user_list_to_string(userlist):
    """ Helper method to turn response's dependent_users list to a printable string for discord"""
    s = ''
    if len(userlist) == 1:
        return userlist[0]
    for user in userlist:
        s += (user + ', ')
    return s