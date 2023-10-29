import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/long_operation')
@cache(expire=60)
def get_long_op():
    time.sleep(2)
    return 'Very heavy data with long calculation time'


# Вопрос - почему result.all() не возвращает привычный словарь?
@router.get('/get')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        # return [dict(zip(result.keys(), res)) for res in result.all()]
        return {
            'status': 'success',
            'data': [dict(zip(result.keys(), res)) for res in result.all()],
            'details': None
        }
    except Exception:
        # Занести ошибку в базу для обработки
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.post('/post')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    statement = insert(operation).values(new_operation.model_dump())
    await session.execute(statement)
    await session.commit()
    return {'status': 'success'}

# ORM Object-relational model
# SQL Injection
