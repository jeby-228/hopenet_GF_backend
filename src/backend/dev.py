import warnings

from app.schemas.item_schema import CreateItemSchema
from app.schemas.task_schema import CreateTaskSchema
from hypothesis import find
from hypothesis import strategies as st
from hypothesis.errors import NonInteractiveExampleWarning


warnings.filterwarnings('ignore', category=NonInteractiveExampleWarning)


for m in [
    CreateItemSchema,
    CreateTaskSchema,
]:
    example_1 = find(st.builds(m), lambda x: True)
    print(f'{example_1=}')

    example_2 = st.from_type(m).example()
    print(f'{example_2=}')

    example_3 = st.builds(m).example()
    print(f'{example_3=}')
