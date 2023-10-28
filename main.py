from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI(
    title='Trading App'
)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


users_base = [
    {'id': 1, 'role': 'admin', 'name': []},
    {'id': 2, 'role': 'investor', 'name': 'John'},
    {'id': 3, 'role': 'trader', 'name': 'Matt'},
    {'id': 4, 'role': 'investor', 'name': 'Homer', 'degree': [
        {'id': 1, 'created_at': '2020-01-01T00:00:00', 'type': 'expert'}
    ]}
]

users_base_2 = [
    {'id': 1, 'role': 'admin', 'name': 'Bob'},
    {'id': 2, 'role': 'investor', 'name': 'John'},
    {'id': 3, 'role': 'trader', 'name': 'Matt'}
]

trades_base = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in users_base if user.get('id') == user_id]


@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return trades_base[offset:][:limit]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trades(trades: List[Trade]):
    trades_base.extend(trades)
    return {'status': 200, 'data': trades_base}


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get('id') == user_id, users_base_2))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')

