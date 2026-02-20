from d2_widget import parse_magic_arguments


def test_parse_magic_arguments_handles_empty_input() -> None:
    assert parse_magic_arguments("   ") == {}


def test_parse_magic_arguments_parses_json_payload() -> None:
    assert parse_magic_arguments('{"themeID": 200, "sketch": true, "pad": 0}') == {
        "themeID": 200,
        "sketch": True,
        "pad": 0,
    }


def test_parse_magic_arguments_parses_key_value_pairs() -> None:
    args = (
        "themeID=200 sketch=True pad=0 layout=elk "
        "name=\"hello world\" label='quoted text' url=https://example.com?a=1&b=2"
    )
    assert parse_magic_arguments(args) == {
        "themeID": 200,
        "sketch": True,
        "pad": 0,
        "layout": "elk",
        "name": "hello world",
        "label": "quoted text",
        "url": "https://example.com?a=1&b=2",
    }


def test_parse_magic_arguments_falls_back_from_invalid_json() -> None:
    assert parse_magic_arguments("{invalid_json} themeID=100") == {"themeID": 100}
