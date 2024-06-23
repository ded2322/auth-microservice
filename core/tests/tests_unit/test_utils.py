import pytest
from httpx import AsyncClient
from core.utils.auth import verification_password, get_password_hash
@pytest.mark.parametrize("input_password, hashed_password, bool_value",
                         [
                        ("<PASSWORD>",
                         "$argon2id$v=19$m=65536,t=3,p=4$lXKOkZISgtA6J6SUslaqtQ$Nzh1RHpqgLq+ycakXPNttRFoIdHMug3xsswSb9yxfbs",
                         True),
                        ("Incorrect password",
                        "$argon2id$v=19$m=65536,t=3,p=4$LoUwBsAYI0RI6T3nXCulNA$wbExgjGLbFxN2ng57FoZW5qBS9i7adghqAjAIPsHU2o",
                         False),
                         ])
def test_verification_password(input_password, hashed_password, bool_value, ac: AsyncClient):
    bool_resulting = verification_password(input_password, hashed_password)
    assert bool_resulting == bool_value

@pytest.mark.parametrize("input_password",
                         ["<PASSWORD>"])
def test_get_password_hash(input_password,ac: AsyncClient):
    hash_pass = get_password_hash(input_password)
    assert hash_pass == hash_pass

