import typing as t

from fastapi import APIRouter
from fastapi import Form
from fastcrud import FilterConfig
from fastcrud import crud_router

from ..dependencies.database_dependency import SessionDepends
from ..dependencies.database_dependency import get_async_session
from ..dependencies.user_dependency import CurrentActiveUserDepends
from ..dependencies.user_dependency import current_active_user
from ..models.task_model import Task
from ..schemas.task_schema import CreateTaskSchema
from ..schemas.task_schema import UpdateTaskSchema


task_router = APIRouter()


@task_router.post(
    '/task_form/',
    tags=['!form'],  # TODO
)
async def task_form(
    data: t.Annotated[CreateTaskSchema, Form()], user: CurrentActiveUserDepends, session: SessionDepends
) -> Task:
    return await create_task(data=data, user=user, session=session)


@task_router.post(
    '/task',
    tags=['task'],
)
async def create_task(data: CreateTaskSchema, user: CurrentActiveUserDepends, session: SessionDepends) -> Task:
    model = Task(**data.model_dump(), creator_id=user.id)
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model


task_router.include_router(
    crud_router(
        session=get_async_session,
        model=Task,
        create_schema=CreateTaskSchema,
        update_schema=UpdateTaskSchema,
        path='/task',
        tags=['task'],
        create_deps=[],
        read_deps=[],
        read_multi_deps=[],
        update_deps=[current_active_user],
        delete_deps=[current_active_user],
        db_delete_deps=[current_active_user],
        included_methods=[
            # 'create',
            'read',
            'read_multi',
            'update',
            'delete',
            # 'db_delete',
        ],
        filter_config=FilterConfig(
            is_deleted=lambda: False,
            creator_id=None,
            status=None,
        ),
        select_schema=Task,
    )
)
