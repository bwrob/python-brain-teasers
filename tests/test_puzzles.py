"""Test user answer acceptance and rejection for all 40 Python brain teasers."""

from __future__ import annotations

from quiz import fuzzy_match


def _assert_answers(
    stdout: str,
    exc: str | None,
    accepted: list[str],
    rejected: list[str],
) -> None:
    failures: list[str] = [
        f"Answer {ans!r} should be accepted"
        for ans in accepted
        if not fuzzy_match(ans, stdout, exc)
    ]
    failures.extend(
        f"Answer {ans!r} should be rejected"
        for ans in rejected
        if fuzzy_match(ans, stdout, exc)
    )
    assert not failures, "\n".join(failures)


def test_puzzle_01_mul() -> None:
    _assert_answers(
        stdout="1.2100000000000002",
        exc=None,
        accepted=[
            "1.21",
            "1.2100000000000002",
            " 1.21 ",
            "1.210",
            "1.2100000000000002\n",
        ],
        rejected=[
            "1.2",
            "1.22",
            "1.1",
            "0",
            "1.210000000000000",
            "1.2100000000000001",
            "1.2100000000000003",
            "1",
            "2",
        ],
    )


def test_puzzle_02_round() -> None:
    _assert_answers(
        stdout="2 2",
        exc=None,
        accepted=[
            "2 2",
            "2, 2",
            "2,2",
            "  2   2  ",
            "2\n2",
            "2  2",
            "2 2\n",
        ],
        rejected=[
            "2 3",
            "2, 3",
            "3 2",
            "3 3",
            "2",
            "2 2 2",
            "1 2",
            "1 3",
            "2.0 2.0",
            "(2, 2)",
            "[2, 2]",
        ],
    )


def test_puzzle_03_div() -> None:
    _assert_answers(
        stdout="OK",
        exc=None,
        accepted=[
            "OK",
            "ok",
            "Ok",
            "'OK'",
            '"OK"',
            " ok ",
            "OK\n",
        ],
        rejected=[
            "ZeroDivisionError",
            "ZeroDivisionError: division by zero",
            "error",
            "div",
            "KO",
            "oopsie",
            "'oopsie'",
            "O",
            "K",
        ],
    )


def test_puzzle_04_pi() -> None:
    _assert_answers(
        stdout="3.142857142857143",
        exc=None,
        accepted=[
            "3.14",
            "3.142857",
            "3.142857142857143",
            " 3.14 ",
            "3.1429",
            "3.142857142857143\n",
        ],
        rejected=[
            "3.14159",
            "3.141592653589793",
            "3.15",
            "3.1",
            "22",
            "7",
            "3",
            "3.0",
            "SyntaxError",
        ],
    )


def test_puzzle_05_city() -> None:
    _assert_answers(
        stdout="7",
        exc=None,
        accepted=[
            "7",
            " 7 ",
            "'7'",
            '"7"',
            "7\n",
        ],
        rejected=[
            "8",
            "6",
            "5",
            "14",
            "0",
            "Kraków",
            "city",
            "len",
            "[7]",
        ],
    )


def test_puzzle_06_escape() -> None:
    _assert_answers(
        stdout="a\n™\n™\n™",
        exc=None,
        accepted=[
            "a\n™\n™\n™",
            "a ™ ™ ™",
            "a, ™, ™, ™",
            "a\n™\n™\n™\n",
            "a,™,\u2122,\u2122",
        ],
        rejected=[
            "a",
            "™",
            "a ™",
            "a b c",
            "TRADE MARK SIGN",
            "SyntaxError",
            "a\n™\n™",
            "a ™ ™",
            "™ ™ ™",
        ],
    )


def test_puzzle_07_winpath() -> None:
    _assert_answers(
        stdout=r"c:\path\to\nowhere",
        exc=None,
        accepted=[
            r"c:\path\to\nowhere",
            r"'c:\path\to\nowhere'",
            r'"c:\path\to\nowhere"',
            r"c:\path\to\nowhere" + "\n",
        ],
        rejected=[
            r"c:/path/to/nowhere",
            r"c:\path",
            "nowhere",
            "c:\\\\path\\\\to\\\\nowhere",
            "to\\nowhere",
            "SyntaxError",
            "c:",
        ],
    )


def test_puzzle_08_cat() -> None:
    _assert_answers(
        stdout="?was I tac a ti saW",
        exc=None,
        accepted=[
            "?was I tac a ti saW",
            "?was i tac a ti saw",
            "'?was I tac a ti saW'",
            '"?was I tac a ti saW"',
            "?was I tac a ti saW\n",
        ],
        rejected=[
            "Was it a cat I saw?",
            "tac",
            "saw",
            "was I tac a ti saW",
            "saw? I cat a it Was",
            "saw I cat a it was",
            "was",
            "?was",
        ],
    )


def test_puzzle_09_waldo() -> None:
    _assert_answers(
        stdout="Found Waldo",
        exc=None,
        accepted=[
            "Found Waldo",
            "found waldo",
            "FOUND WALDO",
            "'Found Waldo'",
            '"found waldo"',
            "Found Waldo\n",
        ],
        rejected=[
            "Waldo",
            "Not Found",
            "found",
            "Found",
            "None",
            "Cannot find Waldo",
            "'Cannot find Waldo'",
            "cannot find waldo",
            "-1",
            "False",
        ],
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
            "[ 'red', 'greenblue' ]",
            "['red', 'greenblue']\n",
        ],
        rejected=[
            "['red', 'green', 'blue']",
            "[red, green, blue]",
            "red, green, blue",
            "['red']",
            "('red', 'greenblue')",
            "['red', 'green blue']",
            "SyntaxError",
            "greenblue",
            "red",
        ],
    )


def test_puzzle_11_identity() -> None:
    _assert_answers(
        stdout="True",
        exc=None,
        accepted=[
            "True",
            "true",
            "TRUE",
            "T",
            "t",
            "'True'",
            "True\n",
        ],
        rejected=[
            "False",
            "false",
            "F",
            "None",
            "36",
            "36 is 36",
            "x is y",
            "1",
        ],
    )


def test_puzzle_12_add() -> None:
    _assert_answers(
        stdout="12",
        exc=None,
        accepted=[
            "12",
            " 12 ",
            "'12'",
            '"12"',
            "12\n",
        ],
        rejected=[
            "3",
            "3.0",
            "TypeError",
            "1",
            "2",
            "1 + 2",
            '"1" + "2"',
            "None",
            "(12)",
        ],
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
            "[ 1, 10, 20, 30, 3, 4 ]",
            "[1, 10, 20, 30, 3, 4]\n",
        ],
        rejected=[
            "[1, [10, 20, 30], 3, 4]",
            "[10, 20, 30, 3, 4]",
            "[1, 10, 20, 30, 4]",
            "[1, 2, 10, 20, 30, 3, 4]",
            "[1, 10, 20, 30]",
            "(1, 10, 20, 30, 3, 4)",
            "[1, 2, 3, 4]",
            "TypeError",
            "[10, 20, 30]",
        ],
    )


def test_puzzle_14_avengers() -> None:
    _assert_answers(
        stdout="['Bruce', 'Carol', 'Natasha', 'Peter']",
        exc=None,
        accepted=[
            "['Bruce', 'Carol', 'Natasha', 'Peter']",
            '["Bruce", "Carol", "Natasha", "Peter"]',
            "[Bruce, Carol, Natasha, Peter]",
            "Bruce, Carol, Natasha, Peter",
            "[Bruce,Carol,Natasha,Peter]",
            "bruce, carol, natasha, peter",
            "['Bruce', 'Carol', 'Natasha', 'Peter']\n",
        ],
        rejected=[
            "[Bruce, Carol, Peter, Tony]",
            "['Bruce', 'Carol', 'Peter', 'Tony']",
            "Bruce, Carol, Peter, Tony",
            "[Bruce, Carol, Natasha]",
            "[Bruce, Carol, Natasha, Peter, Tony]",
            "Bruce, Carol, Peter",
            "('Bruce', 'Carol', 'Natasha', 'Peter')",
            "[Bruce, Carol, Natasha, Tony]",
            "Peter",
        ],
    )


def test_puzzle_15_inside() -> None:
    _assert_answers(
        stdout="[1, 0, 1, 2]",
        exc=None,
        accepted=[
            "[1, 0, 1, 2]",
            "[1,0,1,2]",
            "1, 0, 1, 2",
            "[ 1, 0, 1, 2 ]",
            "[1, 0, 1, 2]\n",
        ],
        rejected=[
            "[1, [0, 1, 2]]",
            "[1, 3]",
            "[0, 1, 2]",
            "[1, 0, 1]",
            "(1, 0, 1, 2)",
            "[1, 1, 2, 3]",
            "TypeError",
            "[1]",
            "None",
        ],
    )


def test_puzzle_16_tasks() -> None:
    _assert_answers(
        stdout="",
        exc="TypeError",
        accepted=[
            "TypeError",
            "type error",
            "typeerror",
            "TYPEERROR",
            "raises TypeError",
            "TypeError: not supported",
            "TypeError: '<' not supported",
            "TypeError\n",
        ],
        rejected=[
            "ValueError",
            "error",
            "crash",
            "exception",
            "wake up",
            "IndexError",
            "KeyError",
            "None",
        ],
    )


def test_puzzle_17_sorted() -> None:
    _assert_answers(
        stdout="False",
        exc=None,
        accepted=[
            "False",
            "false",
            "FALSE",
            "F",
            "f",
            "'False'",
            "False\n",
        ],
        rejected=[
            "True",
            "true",
            "T",
            "None",
            "[1, 2, 3, 4]",
            "0",
            "StopIteration",
            "False == False",
        ],
    )


def test_puzzle_18_loop() -> None:
    _assert_answers(
        stdout="0 1 2 3 4",
        exc=None,
        accepted=[
            "0 1 2 3 4",
            "0, 1, 2, 3, 4",
            "0,1,2,3,4",
            " 0 1 2 3 4 ",
            "0  1  2  3  4",
            "0 1 2 3 4\n",
        ],
        rejected=[
            "0 1 2 3",
            "0 1 2 3 4 5",
            "1 2 3 4",
            "0",
            "0 5",
            "1 2 3 4 5",
            "[0, 1, 2, 3, 4]",
            "4",
        ],
    )


def test_puzzle_19_loop_internal() -> None:
    _assert_answers(
        stdout="0 1 2 3 4",
        exc=None,
        accepted=[
            "0 1 2 3 4",
            "0, 1, 2, 3, 4",
            "0,1,2,3,4",
            " 0 1 2 3 4 ",
            "0 1 2 3 4\n",
        ],
        rejected=[
            "0 1 2 3",
            "StopIteration",
            "5",
            "0 5",
            "0",
            "[0, 1, 2, 3, 4]",
            "1 2 3 4 5",
        ],
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
            "{'season': 2, 'duck': 2, 'rabbit': 2}",
            "defaultdict(int, {'duck': 2, 'season': 2, 'rabbit': 2})",
            "{'duck': 2, 'season': 2, 'rabbit': 2}\n",
        ],
        rejected=[
            "{'duck': 2, 'season': 1, 'rabbit': 2}",
            "{'duck': 2, 'season': 1}",
            "{'duck': 1}",
            "{'rabbit': 2, 'season': 1}",
            "{'duck': 2, 'season': 1}\n{'rabbit': 2, 'season': 1}",
            "duck",
            "season",
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
            "{'duck': 2, 'season': 1}\n",
            "defaultdict(int, {'duck': 2, 'season': 1})",
        ],
        rejected=[
            "{'duck': 2, 'season': 2}",
            "{'rabbit': 2, 'season': 2}",
            "{}",
            "{'duck': 2, 'season': 2, 'rabbit': 2}",
            "duck",
            "rabbit",
        ],
    )


def test_puzzle_22_scope() -> None:
    _assert_answers(
        stdout="23.1",
        exc=None,
        accepted=[
            "23.1",
            " 23.1 ",
            "'23.1'",
            '"23.1"',
            "23.1\n",
        ],
        rejected=[
            "23",
            "24",
            "1.1",
            "0",
            "21",
            "21.0",
            "7.7",
            "3.3",
        ],
    )


def test_puzzle_23_buttons() -> None:
    _assert_answers(
        stdout="[9]",
        exc=None,
        accepted=[
            "[9]",
            "9",
            " [9] ",
            "[ 9 ]",
            "[9]\n",
        ],
        rejected=[
            "[0]",
            "0",
            "[10]",
            "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]",
            "[3]",
            "3",
            "(9,)",
            "[8]",
        ],
    )


def test_puzzle_24_buttons_default() -> None:
    _assert_answers(
        stdout="[3]",
        exc=None,
        accepted=[
            "[3]",
            "3",
            " [3] ",
            "[ 3 ]",
            "[3]\n",
        ],
        rejected=[
            "[9]",
            "9",
            "[0]",
            "0",
            "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]",
            "[2]",
            "(3,)",
            "[10]",
        ],
    )


def test_puzzle_25_buttons_make() -> None:
    _assert_answers(
        stdout="[3]",
        exc=None,
        accepted=[
            "[3]",
            "3",
            " [3] ",
            "[ 3 ]",
            "[3]\n",
        ],
        rejected=[
            "[9]",
            "9",
            "[0]",
            "0",
            "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]",
            "[2]",
            "(3,)",
            "[10]",
        ],
    )


def test_puzzle_26_player() -> None:
    _assert_answers(
        stdout="0",
        exc=None,
        accepted=[
            "0",
            " 0 ",
            "'0'",
            '"0"',
            "0\n",
        ],
        rejected=[
            "1",
            "10",
            "None",
            "AttributeError",
            "2",
            "Parzival",
            "[0]",
            "Player.count",
        ],
    )


def test_puzzle_27_user() -> None:
    _assert_answers(
        stdout="",
        exc="AttributeError",
        accepted=[
            "AttributeError",
            "attribute error",
            "attributeerror",
            "ATTRIBUTEERROR",
            "raises AttributeError",
            "attribute",
            "AttributeError: 'User' object has no attribute '__id'",
            "AttributeError\n",
        ],
        rejected=[
            "TypeError",
            "error",
            "crash",
            "None",
            "42",
            "name=daffy, id=1",
            "NameError",
            "KeyError",
            "name=daffy",
        ],
    )


def test_puzzle_28_seeker() -> None:
    _assert_answers(
        stdout="",
        exc="RecursionError",
        accepted=[
            "RecursionError",
            "recursion error",
            "recursionerror",
            "RECURSIONERROR",
            "raises RecursionError",
            "recursion",
            "RecursionError: maximum recursion depth exceeded",
            "RecursionError\n",
        ],
        rejected=[
            "AttributeError",
            "error",
            "crash",
            "None",
            "<not found>",
            "RuntimeError",
            "StackOverflowError",
            "id",
        ],
    )


def test_puzzle_29_get_attr() -> None:
    _assert_answers(
        stdout="found a in A\nfound b in class\nfound c in obj",
        exc=None,
        accepted=[
            "found a in A\nfound b in class\nfound c in obj",
            "found a in A found b in class found c in obj",
            "found a in A, found b in class, found c in obj",
            "found a in A\nfound b in class\nfound c in obj\n",
        ],
        rejected=[
            "found a in A",
            "found b in class",
            "found c in obj",
            "found a in A\nfound b in class",
            "found b in class\nfound c in obj",
            "1\n2\n3",
            "1 2 3",
            "found a in class\nfound b in class\nfound c in obj",
        ],
    )


def test_puzzle_30_timer() -> None:
    _assert_answers(
        stdout="div - ERROR",
        exc=None,
        accepted=[
            "div - ERROR",
            "div - error",
            "DIV - ERROR",
            "'div - ERROR'",
            '"div - ERROR"',
            "div - ERROR\n",
        ],
        rejected=[
            "div",
            "ERROR",
            "div - OK",
            "ZeroDivisionError",
            "ZeroDivisionError: division by zero",
            "True",
            "- ERROR",
            "div -",
        ],
    )


def test_puzzle_31_vote() -> None:
    _assert_answers(
        stdout="21 1 0",
        exc=None,
        accepted=[
            "21 1 0",
            "21, 1, 0",
            "21,1,0",
            " 21 1 0 ",
            "21  1  0",
            "21 1 0\n",
        ],
        rejected=[
            "21 0 1",
            "21 1",
            "21",
            "1 0",
            "21 13 10",
            "21, 13, 10",
            "(21, 1, 0)",
            "[21, 1, 0]",
            "21 13",
        ],
    )


def test_puzzle_32_eval() -> None:
    _assert_answers(
        stdout="",
        exc="SyntaxError",
        accepted=[
            "SyntaxError",
            "syntax error",
            "syntaxerror",
            "SYNTAXERROR",
            "raises SyntaxError",
            "syntax",
            "SyntaxError: invalid syntax",
            "SyntaxError\n",
        ],
        rejected=[
            "TypeError",
            "ValueError",
            "NameError",
            "error",
            "7",
            "21",
            "21.0",
            "None",
        ],
    )


def test_puzzle_33_future() -> None:
    _assert_answers(
        stdout="",
        exc="ValueError",
        accepted=[
            "ValueError",
            "value error",
            "valueerror",
            "VALUEERROR",
            "raises ValueError",
            "value",
            "ValueError: year 10000 is out of range",
            "ValueError\n",
        ],
        rejected=[
            "TypeError",
            "OverflowError",
            "RangeError",
            "IndexError",
            "error",
            "crash",
            "2020",
            "10000",
            "The party started on January, 01 10000 and lasted a 10 days",
        ],
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
            email_out + "\n",
            "I'm a Nigerian prince who came into some misfortune",
            "From: prince@palace.ng",
            "To: Scrooge McDuck <scoorge@disney.com>",
        ],
        rejected=[
            "ImportError",
            "ModuleNotFoundError",
            "error",
            "Scrooge",
            "Nigerian",
            "Nigeria",
            "prince",
            "palace.ng",
        ],
    )


def test_puzzle_35_metrics() -> None:
    _assert_answers(
        stdout="",
        exc="UnboundLocalError",
        accepted=[
            "UnboundLocalError",
            "unbound local error",
            "unboundlocalerror",
            "UNBOUNDLOCALERROR",
            "raises UnboundLocalError",
            "unbound local",
            "UnboundLocalError: local variable 'ncalls' referenced before assignment",
            "UnboundLocalError\n",
        ],
        rejected=[
            "NameError",
            "TypeError",
            "AttributeError",
            "ValueError",
            "error",
            "1",
            "4",
            "None",
            "inc called 1 times",
        ],
    )


def test_puzzle_36_metrics_nl() -> None:
    _assert_answers(
        stdout="inc called 1 times",
        exc=None,
        accepted=[
            "inc called 1 times",
            "Inc Called 1 Times",
            "'inc called 1 times'",
            '"inc called 1 times"',
            "inc called 1 times\n",
        ],
        rejected=[
            "inc called 0 times",
            "inc called 2 times",
            "1",
            "4",
            "SyntaxError",
            "UnboundLocalError",
            "inc",
            "inc called 1",
        ],
    )


def test_puzzle_37_metrics_box() -> None:
    _assert_answers(
        stdout="inc called 1 times",
        exc=None,
        accepted=[
            "inc called 1 times",
            "Inc Called 1 Times",
            "'inc called 1 times'",
            '"inc called 1 times"',
            "inc called 1 times\n",
        ],
        rejected=[
            "inc called 0 times",
            "inc called 2 times",
            "1",
            "4",
            "UnboundLocalError",
            "inc called [1] times",
            "inc",
            "inc called 1",
        ],
    )


def test_puzzle_38_printer() -> None:
    _assert_answers(
        stdout="0",
        exc=None,
        accepted=[
            "0",
            " 0 ",
            "'0'",
            '"0"',
            "0\n",
        ],
        rejected=[
            "1",
            "2",
            "3",
            "None",
            "0 1 2",
            "0 1",
            "0 1 2 3",
            "[0]",
        ],
    )


def test_puzzle_39_printer_join() -> None:
    _assert_answers(
        stdout="0 1 2",
        exc=None,
        accepted=[
            "0 1 2",
            "0, 1, 2",
            "0,1,2",
            " 0 1 2 ",
            "0  1  2",
            "0 1 2\n",
        ],
        rejected=[
            "0 1",
            "0 1 2 3",
            "0",
            "1 2",
            "[0, 1, 2]",
            "(0, 1, 2)",
            "1 2 3",
            "2",
        ],
    )


def test_puzzle_40_jury() -> None:
    _assert_answers(
        stdout="0",
        exc=None,
        accepted=[
            "0",
            " 0 ",
            "'0'",
            '"0"',
            "0\n",
        ],
        rejected=[
            "1",
            "11",
            "12",
            "None",
            "ConnectionResetError",
            "RuntimeError",
            "[0]",
        ],
    )
