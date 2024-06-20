from punq import Container
from pytest import fixture

from app.tests.fixtures import init_dummy_container


@fixture(scope='module')
def get_dummy_container() -> Container:
    return init_dummy_container()
