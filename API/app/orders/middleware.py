from fastapi import FastAPI, Request
import re




regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


async def check_order(request: Request, call_next):
    print(request.body)
    return 'ok'