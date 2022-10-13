from flask import request

def get_argument(argument):
    return request.args.get(argument, None)
