from fastcrud import FilterConfig
from fastcrud import crud_router

from ..dependencies.database_dependency import get_async_session
from ..dependencies.item_dependency import hello_dep
from ..dependencies.user_dependency import current_active_user
from ..models.item_model import Item
from ..schemas.item_schema import CreateItemSchema
from ..schemas.item_schema import UpdateItemSchema


item_router = crud_router(
    session=get_async_session,
    model=Item,
    create_schema=CreateItemSchema,
    update_schema=UpdateItemSchema,
    path='/item',
    tags=['item'],
    create_deps=[],
    read_deps=[],
    read_multi_deps=[hello_dep],
    update_deps=[],
    delete_deps=[],
    db_delete_deps=[current_active_user],
    included_methods=[
        'create',
        'read',
        'read_multi',
        'update',
        'delete',
        'db_delete',
    ],
    filter_config=FilterConfig(
        is_deleted=lambda: False,
        category=None,
    ),
    select_schema=Item,
)
