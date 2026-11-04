"""Test user answer acceptance and rejection for all 40 Python brain teasers."""

from __future__ import annotations

from quiz import fuzzy_match


def _assert_answers(
    stdout: str,
    exc: str | None,
    accepted: list[str],
    rejected: list[str],
) -> None:
    for ans in accepted:
        assert fuzzy_match(ans, stdout, exc), f"Answer {ans!r} should be accepted"
    for ans in rejected:
        assert not fuzzy_match(ans, stdout, exc), f"Answer {ans!r} should be rejected"


def test_puzzle_01_mul() -> None:
    _assert_answers(
        stdout="1.2100000000000002",
        exc=None,
        accepted=["1.21", "1.2100000000000002", " 1.21 "],
        rejected=["1.2", "1.22", "1.1", "0"],
    )


def test_puzzle_02_round() -> None:
    _assert_answers(
        stdout="2 2",
        exc=None,
        accepted=["2 2", "2, 2", "2,2", "  2   2  ", "2\n2"],
        rejected=["2 3", "3 2", "3 3", "2", "2 2 2", "1 2"],
    )


def test_puzzle_03_div() -> None:
    _assert_answers(
        stdout="OK",
        exc=None,
        accepted=["OK", "ok", "'OK'", '"OK"', " ok "],
        rejected=["ZeroDivisionError", "error", "div", "KO"],
    )


def test_puzzle_04_pi() -> None:
    _assert_answers(
        stdout="3.142857142857143",
        exc=None,
        accepted=["3.14", "3.142857", "3.142857142857143", " 3.14 "],
        rejected=["3.14159", "3.15", "3.1", "22", "7"],
    )


def test_puzzle_05_city() -> None:
    _assert_answers(
        stdout="7",
        exc=None,
        accepted=["7", " 7 ", "'7'"],
        rejected=["8", "6", "14", "0"],
    )


def test_puzzle_06_escape() -> None:
    _assert_answers(
        stdout="a\n™\n™\n™",
        exc=None,
        accepted=["a\n™\n™\n™", "a ™ ™ ™", "a, ™, ™, ™"],
        rejected=["a", "™", "a ™", "a b c"],
    )


def test_puzzle_07_winpath() -> None:
    _assert_answers(
        stdout=r"c:\path\to\nowhere",
        exc=None,
        accepted=[
            r"c:\path\to\nowhere",
            r"'c:\path\to\nowhere'",
            r'"c:\path\to\nowhere"',
        ],
        rejected=[r"c:/path/to/nowhere", r"c:\path", "nowhere"],
    )


def test_puzzle_08_cat() -> None:
    _assert_answers(
        stdout="?was I tac a ti saW",
        exc=None,
        accepted=[
            "?was I tac a ti saW",
            "?was i tac a ti saw",
            "'?was I tac a ti saW'",
        ],
        rejected=["Was it a cat I saw?", "tac", "saw"],
    )


def test_puzzle_09_waldo() -> None:
    _assert_answers(
        stdout="Found Waldo",
        exc=None,
        accepted=["Found Waldo", "found waldo", "'Found Waldo'", '"found waldo"'],
        rejected=["Waldo", "Not Found", "found", "None"],
    )


def test_puzzle_10_colors() -> None:
    _assert_answers(
        stdout="['red', 'greenblue']",
        exc=None,
        accepted=[
            "['red', 'greenblue']",
            '["red", "greenblue"]',
            "['red','greenblue']",
            "red, greenblue",
            "[red, greenblue]",
        ],
        rejected=[
            "['red', 'green', 'blue']",
            "[red, green, blue]",
            "red, green, blue",
            "['red']",
        ],
    )


def test_puzzle_11_identity() -> None:
    _assert_answers(
        stdout="True",
        exc=None,
        accepted=["True", "true", "T", "t"],
        rejected=["False", "false", "F", "None"],
    )


def test_puzzle_12_add() -> None:
    _assert_answers(
        stdout="12",
        exc=None,
        accepted=["12", " 12 ", "'12'"],
        rejected=["3", "TypeError", "1", "2"],
    )


def test_puzzle_13_assign() -> None:
    _assert_answers(
        stdout="[1, 10, 20, 30, 3, 4]",
        exc=None,
        accepted=[
            "[1, 10, 20, 30, 3, 4]",
            "[1,10,20,30,3,4]",
            "1, 10, 20, 30, 3, 4",
            "  [1, 10, 20, 30, 3, 4]  ",
        ],
        rejected=[
            "[1, [10, 20, 30], 3, 4]",
            "[10, 20, 30, 3, 4]",
            "[1, 10, 20, 30, 4]",
            "[1, 2, 10, 20, 30, 3, 4]",
            "[1, 10, 20, 30]",
        ],
    )


def test_puzzle_14_avengers() -> None:
    _assert_answers(
        stdout="['Bruce', 'Carol', 'Natasha', 'Peter']",
        exc=None,
        accepted=[
            "['Bruce', 'Carol', 'Natasha', 'Peter']",
            "[Bruce, Carol, Natasha, Peter]",
            "Bruce, Carol, Natasha, Peter",
            "[Bruce,Carol,Natasha,Peter]",
            "bruce, carol, natasha, peter",
        ],
        rejected=[
            "[Bruce, Carol, Peter, Tony]",
            "[Bruce, Carol, Natasha]",
            "[Bruce, Carol, Natasha, Peter, Tony]",
            "Bruce, Carol, Peter",
        ],
    )


def test_puzzle_15_inside() -> None:
    _assert_answers(
        stdout="[1, 0, 1, 2]",
        exc=None,
        accepted=["[1, 0, 1, 2]", "[1,0,1,2]", "1, 0, 1, 2"],
        rejected=["[1, [0, 1, 2]]", "[1, 3]", "[0, 1, 2]", "[1, 0, 1]"],
    )


def test_puzzle_16_tasks() -> None:
    _assert_answers(
        stdout="",
        exc="TypeError",
        accepted=[
            "TypeError",
            "type error",
            "typeerror",
            "raises TypeError",
            "TypeError: not supported",
        ],
        rejected=["ValueError", "error", "crash", "exception"],
    )


def test_puzzle_17_sorted() -> None:
    _assert_answers(
        stdout="False",
        exc=None,
        accepted=["False", "false", "F", "f"],
        rejected=["True", "true", "T", "None"],
    )


def test_puzzle_18_loop() -> None:
    _assert_answers(
        stdout="0 1 2 3 4",
        exc=None,
        accepted=["0 1 2 3 4", "0, 1, 2, 3, 4", "0,1,2,3,4", " 0 1 2 3 4 "],
        rejected=["0 1 2 3", "0 1 2 3 4 5", "1 2 3 4", "0"],
    )


def test_puzzle_19_loop_internal() -> None:
    _assert_answers(
        stdout="0 1 2 3 4",
        exc=None,
        accepted=["0 1 2 3 4", "0, 1, 2, 3, 4", "0,1,2,3,4"],
        rejected=["0 1 2 3", "StopIteration", "5"],
    )


def test_puzzle_20_word_freq() -> None:
    raw_stdout = (
        "defaultdict(<class 'int'>, {'duck': 2, 'season': 2, 'rabbit': 2})\n"
        "defaultdict(<class 'int'>, {'duck': 2, 'season': 2, 'rabbit': 2})"
    )
    _assert_answers(
        stdout=raw_stdout,
        exc=None,
        accepted=[
            "{'duck': 2, 'season': 2, 'rabbit': 2}",
            "{'rabbit': 2, 'season': 2, 'duck': 2}",
            "defaultdict(int, {'duck': 2, 'season': 2, 'rabbit': 2})",
        ],
        rejected=[
            "{'duck': 2, 'season': 1, 'rabbit': 2}",
            "{'duck': 2, 'season': 1}",
            "{'duck': 1}",
        ],
    )


def test_puzzle_21_word_freq_none() -> None:
    raw_stdout = (
        "defaultdict(<class 'int'>, {'duck': 2, 'season': 1})\n"
        "defaultdict(<class 'int'>, {'rabbit': 2, 'season': 1})"
    )
    _assert_answers(
        stdout=raw_stdout,
        exc=None,
        accepted=[
            "{'duck': 2, 'season': 1}",
            "{'season': 1, 'duck': 2}",
        ],
        rejected=[
            "{'duck': 2, 'season': 2}",
            "{'rabbit': 2, 'season': 2}",
            "{}",
        ],
    )


def test_puzzle_22_scope() -> None:
    _assert_answers(
        stdout="23.1",
        exc=None,
        accepted=["23.1", " 23.1 ", "'23.1'"],
        rejected=["23", "24", "1.1", "0"],
    )


def test_puzzle_23_buttons() -> None:
    _assert_answers(
        stdout="[9]",
        exc=None,
        accepted=["[9]", "9", " [9] "],
        rejected=["[0]", "0", "[10]", "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]"],
    )


def test_puzzle_24_buttons_default() -> None:
    _assert_answers(
        stdout="[3]",
        exc=None,
        accepted=["[3]", "3", " [3] "],
        rejected=["[9]", "9", "[0]", "0"],
    )


def test_puzzle_25_buttons_make() -> None:
    _assert_answers(
        stdout="[3]",
        exc=None,
        accepted=["[3]", "3", " [3] "],
        rejected=["[9]", "9", "[0]", "0"],
    )


def test_puzzle_26_player() -> None:
    _assert_answers(
        stdout="0",
        exc=None,
        accepted=["0", " 0 ", "'0'"],
        rejected=["1", "10", "None", "AttributeError"],
    )


def test_puzzle_27_user() -> None:
    _assert_answers(
        stdout="",
        exc="AttributeError",
        accepted=[
            "AttributeError",
            "attribute error",
            "attributeerror",
            "raises AttributeError",
            "attribute",
        ],
        rejected=["TypeError", "error", "crash", "None", "42"],
    )


def test_puzzle_28_seeker() -> None:
    _assert_answers(
        stdout="",
        exc="RecursionError",
        accepted=[
            "RecursionError",
            "recursion error",
            "recursionerror",
            "raises RecursionError",
            "recursion",
        ],
        rejected=["AttributeError", "error", "crash", "None", "<not found>"],
    )


def test_puzzle_29_get_attr() -> None:
    _assert_answers(
        stdout="found a in A\nfound b in class\nfound c in obj",
        exc=None,
        accepted=[
            "found a in A\nfound b in class\nfound c in obj",
            "found a in A found b in class found c in obj",
        ],
        rejected=["found a in A", "found b in class", "found c in obj"],
    )


def test_puzzle_30_timer() -> None:
    _assert_answers(
        stdout="div - ERROR",
        exc=None,
        accepted=["div - ERROR", "div - error", "'div - ERROR'", "div - ERROR\n"],
        rejected=["div", "ERROR", "div - OK", "ZeroDivisionError"],
    )


def test_puzzle_31_vote() -> None:
    _assert_answers(
        stdout="21 1 0",
        exc=None,
        accepted=["21 1 0", "21, 1, 0", "21,1,0", " 21 1 0 "],
        rejected=["21 0 1", "21 1", "21", "1 0"],
    )


def test_puzzle_32_eval() -> None:
    _assert_answers(
        stdout="",
        exc="SyntaxError",
        accepted=[
            "SyntaxError",
            "syntax error",
            "syntaxerror",
            "raises SyntaxError",
            "syntax",
        ],
        rejected=["TypeError", "ValueError", "error", "7", "None"],
    )


def test_puzzle_33_future() -> None:
    _assert_answers(
        stdout="",
        exc="ValueError",
        accepted=[
            "ValueError",
            "value error",
            "valueerror",
            "raises ValueError",
            "value",
        ],
        rejected=["TypeError", "OverflowError", "error", "crash", "2020"],
    )


def test_puzzle_34_email() -> None:
    email_out = (
        "From: prince@palace.ng\n"
        "To: Scrooge McDuck <scoorge@disney.com>\n"
        'Content-Type: text/plain; charset="utf-8"\n'
        "Content-Transfer-Encoding: 7bit\n"
        "MIME-Version: 1.0\n\n"
        "Dear Sir.\n\n"
        "I'm a Nigerian prince who came into some misfortune.\n"
        "..."
    )
    _assert_answers(
        stdout=email_out,
        exc=None,
        accepted=[
            email_out,
            "I'm a Nigerian prince who came into some misfortune",
            "From: prince@palace.ng",
        ],
        rejected=["ImportError", "error", "Scrooge", "Nigerian"],
    )


def test_puzzle_35_metrics() -> None:
    _assert_answers(
        stdout="",
        exc="UnboundLocalError",
        accepted=[
            "UnboundLocalError",
            "unbound local error",
            "unboundlocalerror",
            "raises UnboundLocalError",
            "unbound local",
        ],
        rejected=["NameError", "TypeError", "error", "1", "None"],
    )


def test_puzzle_36_metrics_nl() -> None:
    _assert_answers(
        stdout="inc called 1 times",
        exc=None,
        accepted=["inc called 1 times", "Inc Called 1 Times", "'inc called 1 times'"],
        rejected=["inc called 0 times", "inc called 2 times", "1", "UnboundLocalError"],
    )


def test_puzzle_37_metrics_box() -> None:
    _assert_answers(
        stdout="inc called 1 times",
        exc=None,
        accepted=["inc called 1 times", "Inc Called 1 Times", "'inc called 1 times'"],
        rejected=["inc called 0 times", "inc called 2 times", "1", "UnboundLocalError"],
    )


def test_puzzle_38_printer() -> None:
    _assert_answers(
        stdout="0",
        exc=None,
        accepted=["0", " 0 ", "'0'"],
        rejected=["1", "2", "3", "None"],
    )


def test_puzzle_39_printer_join() -> None:
    _assert_answers(
        stdout="0 1 2",
        exc=None,
        accepted=["0 1 2", "0, 1, 2", "0,1,2", " 0 1 2 "],
        rejected=["0 1", "0 1 2 3", "0", "1 2"],
    )


def test_puzzle_40_jury() -> None:
    _assert_answers(
        stdout="0",
        exc=None,
        accepted=["0", " 0 ", "'0'"],
        rejected=["1", "12", "None", "ConnectionResetError"],
    )
