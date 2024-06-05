import pytest
from httpx import AsyncClient

from core.dao.user_dao import UserDao


@pytest.mark.parametrize("username, hash_password, is_superuser", [
    ("test user dao", "hash_pass", False),
    ("test admin dao", "hash_pass", True),
])
async def test_insert_data(username, hash_password, is_superuser, ac: AsyncClient):
    user = await UserDao.insert_data(username=username, hash_password=hash_password, is_superuser=is_superuser)
    assert user == True


@pytest.mark.parametrize("id_user, expectation", [(1, {'id': 1, 'username': 'admin',
                                                       'hash_password': '$argon2id$v=19$m=65536,t=3,p=4$LoUwBsAYI0RI6T3nXCulNA$wbExgjGLbFxN2ng57FoZW5qBS9i7adghqAjAIPsHU2o',
                                                       'is_active': True, 'is_superuser': False}),
                                                  (999, None)])
async def test_found_one_or_none(id_user, expectation, ac: AsyncClient):
    user = await UserDao.found_one_or_none(id=id_user)

    assert user == expectation
