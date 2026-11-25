#CRUD Routers to tie everything together
from fastapi import FastAPI, Query
from typing import Annotated
from ..database import check_database_connection 

app = FastAPI(title="Users")

#Use authentication, HTTPS/TLS everywhere, authorization, Validate and sanatize inputs, rate limit + quota(long term)
#versioning, caching, keep servers stateless, filter/paginate, offload heavy tasks asynchronously and use message queue(RabbitMQ,)
#Kafka, prevent N+1, indice columns corrects, use connection pooling, tests

#Common Edge Cases
'''
Null/empty fields, Type checking or 0/1 instead of bools, Unicode/emoji/special characters/UTF-8, boundaries(0, negatives
MAX_INT, floating point), dates for daylight savings/leap years, duplicate requests(idempotency), race condition, invalid
state transition(two users buying last item in stock or withdrawing remainig account balance or refunding order without
paid), when 3rd party service dies it should die gracefully with 502 bad gateway, ect. empty endpoints should return []
200 OK without 404, Out of bounds pagination, Cursor drift on shifting data if record is deleted or inserted, BOLA/IDOR 
swapping your info for someone elses (ex. /users/123/orders -> /users/456/orders), expired/revoked/malformed tokens, privillege
escelation via extra fields
'''

@app.get("/users")
def get_all_users(limit: Annotated[int, Query()] = 10, offset: Annotated[int, Query()] = 0):
    
