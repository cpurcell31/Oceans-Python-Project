import apicheck


def test_get_key():
    result = apicheck.get_key(None)
    assert result is not None
