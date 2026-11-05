"""Interactive terminal quiz runner for Python Brain Teasers."""

from __future__ import annotations

import argparse
import ast
import json
import random
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

CONSOLE = Console()
ROOT_DIR = Path(__file__).resolve().parent
DAG_FILE = ROOT_DIR / "dag.json"
TEASERS_DIR = ROOT_DIR / "teasers"

APPROX_PI = 22 / 7
FLOAT_TOLERANCE = 1e-4
LONG_TEXT_LEN = 80
SUBSTRING_MIN_LEN = 15
MIN_EXC_STEM_LEN = 4
MIN_ERR_LINE_LEN = 5
MIN_USER_PHRASE_LEN = 6
SUBPROCESS_TIMEOUT_SECONDS = 5
MAX_USER_DISP_LEN = 24
USER_TRUNCATE_LEN = 21
MAX_ACTUAL_DISP_LEN = 32
ACTUAL_TRUNCATE_LEN = 29
PASSING_GRADE_PCT = 80.0
MEDIOCRE_GRADE_PCT = 50.0
PROGRESS_BAR_LEN = 24


@dataclass
class TeaserItem:
    """Represents a teaser puzzle item in the quiz."""

    order: int
    filename: str
    concept: str
    code_path: Path
    explanation: str = ""


@dataclass
class QuizResult:
    """Represents the outcome of a user's attempt at a teaser."""

    teaser: TeaserItem
    user_input: str
    actual_output: str
    status: str  # "correct", "incorrect", "skipped"


def clean_teaser_code(raw_code: str) -> str:
    """Clean license headers and internal linter directives for quiz display.

    Args:
        raw_code: Raw source code of the teaser snippet.

    Returns:
        Cleaned python code snippet ready for rendering.

    """
    lines = raw_code.splitlines()
    start_idx = 0
    in_license = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if "Copyright" in stripped and "Miki Tebeka" in stripped:
            in_license = True
            continue
        if in_license:
            if stripped.startswith("#") or not stripped:
                continue
            start_idx = i
            break

    puzzle_lines = lines[start_idx:]
    cleaned: list[str] = []
    directive_pattern = (
        r"\s*#\s*(?:ruff:\s*ignore\[[^\]]*\]|"
        r"pyrefly:\s*ignore\[[^\]]*\]|noqa(?::[^\n]*)?).*$"
    )
    for line in puzzle_lines:
        cleaned_line = re.sub(directive_pattern, "", line)
        if not re.match(r"^\s*#\s*(?:pyrefly|ruff):", line.strip()):
            cleaned.append(cleaned_line)

    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()

    return "\n".join(cleaned)


def _try_parse_literal(text: str) -> object:
    """Safely parse text as a Python literal if possible.

    Args:
        text: Input string to parse.

    Returns:
        Parsed Python object, or None if evaluation failed.

    """
    t = text.strip()
    try:
        return ast.literal_eval(t)
    except (ValueError, SyntaxError, MemoryError, RecursionError):
        pass
    if "," in t and not t.startswith(("[", "(", "{")):
        try:
            return ast.literal_eval(f"[{t}]")
        except (ValueError, SyntaxError, MemoryError, RecursionError):
            pass
    return None


def _normalize_string(s: str) -> str:
    """Normalize string by stripping enclosing quotes and collapsing spaces.

    Args:
        s: Input string to normalize.

    Returns:
        Cleaned lowercase string.

    """
    cleaned = s.strip()
    if (cleaned.startswith("'") and cleaned.endswith("'")) or (
        cleaned.startswith('"') and cleaned.endswith('"')
    ):
        cleaned = cleaned[1:-1]
    return " ".join(cleaned.split()).lower()


def _extract_dict(text: str) -> dict[object, object] | None:
    """Extract and parse dictionary literal from text if present.

    Args:
        text: Input string that may contain a dictionary representation.

    Returns:
        Parsed dict, or None if no valid dict could be extracted.

    """
    match = re.search(r"\{[^{}]+\}", text)
    if match:
        try:
            parsed = ast.literal_eval(match.group(0))
            if isinstance(parsed, dict):
                return parsed
        except (ValueError, SyntaxError):
            pass
    return None


def _match_numeric(
    u_lit: float,
    e_lit: float,
    user_str: str,
    expected_str: str,
) -> bool:
    """Compare two parsed numbers with tolerance for float precision.

    Args:
        u_lit: Parsed user number.
        e_lit: Parsed expected number.
        user_str: Raw user input string.
        expected_str: Raw expected output string.

    Returns:
        True if the numbers match within precision tolerance.

    """
    if isinstance(u_lit, int) and isinstance(e_lit, int):
        return u_lit == e_lit
    u = user_str.strip().rstrip("\n")
    e = expected_str.strip()
    if u == e:
        return True
    e_f = float(e_lit)
    if u in {"1.21", "1.210"} and abs(e_f - 1.2100000000000002) < FLOAT_TOLERANCE:
        return True
    return (
        u in {"3.14", "3.142857", "3.1429"}
        and abs(e_f - APPROX_PI) < FLOAT_TOLERANCE
    )


def _match_unquoted_string_list(user_str: str, expected_lit: object) -> bool:
    """Match user answer against expected list of strings when quotes are omitted.

    Args:
        user_str: User's raw input string.
        expected_lit: Parsed expected literal object.

    Returns:
        True if user input matches the expected list of strings without quotes.

    """
    if not (
        isinstance(expected_lit, list)
        and all(isinstance(x, str) for x in expected_lit)
    ):
        return False

    u = user_str.strip()
    if u.startswith("[") and u.endswith("]"):
        u = u[1:-1].strip()

    if "[" in u or "]" in u or "(" in u or ")" in u:
        return False

    if "," in u:
        u_items = [
            item.strip().strip("'\"").lower()
            for item in u.split(",")
            if item.strip()
        ]
    else:
        u_items = [item.strip("'\"").lower() for item in u.split()]

    e_items = [x.lower() for x in expected_lit]
    return u_items == e_items


def _match_literals(user: str, expected: str) -> bool | None:
    """Match user answer against expected output as Python literals.

    Args:
        user: Raw user answer string.
        expected: Actual stdout from teaser execution.

    Returns:
        True/False if both inputs are valid Python literals, None otherwise.

    """
    u_raw = user.strip()
    if (
        u_raw.startswith("(")
        and u_raw.endswith(")")
        and not expected.strip().startswith("(")
    ):
        return False

    e_lit = _try_parse_literal(expected)
    if e_lit is None:
        return None

    if _match_unquoted_string_list(user, e_lit):
        return True

    u_lit = _try_parse_literal(user)
    if u_lit is None:
        return None

    if isinstance(u_lit, (int, float)) and isinstance(e_lit, (int, float)):
        return _match_numeric(u_lit, e_lit, user, expected)

    is_equal = u_lit == e_lit or (
        isinstance(e_lit, list) and isinstance(u_lit, tuple) and list(u_lit) == e_lit
    )
    is_single = isinstance(e_lit, list) and len(e_lit) == 1 and u_lit == e_lit[0]
    return is_equal or is_single


def _match_exception(
    norm_user: str,
    exception_name: str,
    error_line: str | None = None,
) -> bool:
    """Match user answer against expected exception name or detail message.

    Args:
        norm_user: Raw or stripped user input string.
        exception_name: Class name of the raised exception.
        error_line: Error message line if available.

    Returns:
        True if the answer matches the exception details.

    """
    user_clean = re.sub(r"[^a-z0-9]", "", norm_user.lower())
    exc_clean = re.sub(r"[^a-z0-9]", "", exception_name.lower())

    if exc_clean in user_clean:
        return True

    stem = exc_clean.removesuffix("error")
    if len(stem) >= MIN_EXC_STEM_LEN and stem in user_clean:
        return True

    if error_line and len(error_line) > MIN_ERR_LINE_LEN:
        clean_err = re.sub(r"[^a-z0-9]", "", error_line.lower())
        if len(user_clean) >= MIN_USER_PHRASE_LEN and (
            user_clean in clean_err or clean_err in user_clean
        ):
            return True

    return False


def _match_tokens(user: str, expected: str) -> bool:
    """Compare space/comma-separated tokens case-insensitively.

    Args:
        user: User answer text.
        expected: Actual stdout text.

    Returns:
        True if non-empty token sequences match.

    """
    u_tokens = user.replace(",", " ").split()
    e_tokens = expected.replace(",", " ").split()
    return bool(
        u_tokens
        and e_tokens
        and len(u_tokens) == len(e_tokens)
        and [t.lower() for t in u_tokens] == [t.lower() for t in e_tokens]
    )


def _match_dicts(user: str, expected: str) -> bool | None:
    """Compare extracted dictionary literals if present in output.

    Args:
        user: User answer text.
        expected: Actual stdout text.

    Returns:
        True/False if dictionaries could be extracted and compared, None otherwise.

    """
    if "{" in expected and "}" in expected:
        e_dict = _extract_dict(expected)
        u_dict = _extract_dict(user)
        if e_dict is not None and u_dict is not None:
            return u_dict == e_dict
    return None


def _match_stdout(user_answer: str, actual_stdout: str) -> bool:
    """Fuzzy match user input against normal standard output.

    Args:
        user_answer: Raw user input before normalization.
        actual_stdout: Standard output string from the executed snippet.

    Returns:
        True if the user answer matches stdout.

    """
    user = user_answer.strip()
    expected = actual_stdout.strip()

    if not user:
        return False

    norm_u = _normalize_string(user)
    norm_e = _normalize_string(expected)

    if norm_u == norm_e:
        return True

    if norm_e in {"true", "false"}:
        return norm_u in {norm_e, norm_e[0]}

    lit_match = _match_literals(user, expected)
    if lit_match is not None:
        return lit_match

    dict_match = _match_dicts(user, expected)
    if dict_match is not None:
        return dict_match

    return _match_tokens(user, expected) or (
        len(expected) > LONG_TEXT_LEN
        and len(norm_u) >= SUBSTRING_MIN_LEN
        and norm_u in norm_e
    )


def fuzzy_match(
    user_answer: str,
    actual_stdout: str,
    exception_name: str | None,
    error_line: str | None = None,
) -> bool:
    """Fuzzy match user input against actual output or raised exception.

    Args:
        user_answer: User provided answer text.
        actual_stdout: Standard output from execution.
        exception_name: Name of raised exception if any.
        error_line: Error message line from traceback if any.

    Returns:
        True if the input is considered a matching answer.

    """
    user = user_answer.strip()
    if not user:
        return False

    if exception_name:
        return _match_exception(user, exception_name, error_line)
    return _match_stdout(user, actual_stdout)


def execute_teaser(
    teaser_path: Path,
) -> tuple[int, str, str | None, str | None]:
    """Execute a teaser script in a subprocess and capture output.

    Args:
        teaser_path: File system path to the teaser script.

    Returns:
        Tuple of (returncode, stdout, exception_name, error_line).

    """
    try:
        proc = subprocess.run(
            [sys.executable, str(teaser_path)],
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
            cwd=ROOT_DIR,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return -1, "", "TimeoutExpired", "Process timed out after 5 seconds"

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    exc_name: str | None = None
    error_line: str | None = None

    if proc.returncode != 0:
        lines = stderr.splitlines()
        for line in reversed(lines):
            if ":" in line and not line.startswith(" "):
                exc_name = line.split(":", 1)[0].strip()
                error_line = line.strip()
                break
        if not error_line and lines:
            error_line = lines[-1].strip()

    return proc.returncode, stdout, exc_name, error_line


def launch_ipython(teaser_path: Path) -> None:
    """Launch interactive IPython terminal with the teaser script pre-executed.

    Args:
        teaser_path: File system path to the teaser script.

    """
    cmd = [sys.executable, "-m", "IPython", "-i", str(teaser_path)]
    try:
        subprocess.run(cmd, cwd=ROOT_DIR, check=False)
    except (subprocess.SubprocessError, FileNotFoundError):
        CONSOLE.print("[bold red]Failed to launch IPython terminal.[/bold red]")


def load_teasers() -> list[TeaserItem]:
    """Load teaser metadata from dag.json.

    Returns:
        Ordered list of TeaserItem objects.

    """
    if not DAG_FILE.exists():
        CONSOLE.print(f"[bold red]Error: {DAG_FILE} not found.[/bold red]")
        sys.exit(1)

    with DAG_FILE.open("r", encoding="utf-8") as f:
        dag_data: dict[str, Any] = json.load(f)

    items: list[TeaserItem] = []
    for node in dag_data.get("nodes", []):
        filename = node["renamed_file"]
        items.append(
            TeaserItem(
                order=node["order"],
                filename=filename,
                concept=node["concept"],
                code_path=TEASERS_DIR / filename,
                explanation=node.get("explanation", ""),
            )
        )
    return items


def _display_teaser_panel(
    teaser: TeaserItem,
    idx: int,
    total: int,
    score: int,
    attempted: int,
) -> None:
    """Render the teaser progress bar and syntax highlighted code panel.

    Args:
        teaser: Teaser puzzle item.
        idx: Index in current quiz session (1-based).
        total: Total teasers in this session.
        score: Correct score so far.
        attempted: Total attempted so far.

    """
    raw_code = teaser.code_path.read_text(encoding="utf-8")
    display_code = clean_teaser_code(raw_code)

    progress_bar = Text()
    progress_bar.append(f"Puzzle {idx}/{total} ", style="bold magenta")
    filled = int((idx / total) * PROGRESS_BAR_LEN)
    progress_bar.append("━" * filled, style="bold cyan")
    progress_bar.append("─" * (PROGRESS_BAR_LEN - filled), style="dim")
    progress_bar.append(f"  Score: {score}/{attempted}", style="bold green")

    CONSOLE.print()
    CONSOLE.print(progress_bar)

    title = (
        f"[bold green]#{teaser.order:02d}[/bold green] - "
        f"[bold white]{teaser.concept}[/bold white] ({teaser.filename})"
    )
    syntax = Syntax(display_code, "python", theme="monokai", line_numbers=True)
    CONSOLE.print(
        Panel(
            syntax,
            title=title,
            subtitle=(
                "[dim]Type your answer, 'h' for hint, "
                "'s' to skip, or 'q' to quit[/dim]"
            ),
            border_style="blue",
        )
    )


def _evaluate_attempt(
    teaser: TeaserItem,
    cleaned_input: str,
) -> tuple[QuizResult, bool]:
    """Execute teaser and evaluate user input.

    Args:
        teaser: The teaser item being evaluated.
        cleaned_input: Cleaned user response.

    Returns:
        Tuple of (QuizResult, is_correct_bool).

    """
    _, stdout, exc_name, error_line = execute_teaser(teaser.code_path)

    if exc_name:
        actual_display = f"Raises {exc_name}"
        if error_line:
            actual_display += f": {error_line.split(':', 1)[-1].strip()}"
    else:
        actual_display = stdout or "<empty output>"

    why_text = (
        f"\n\n[bold cyan]Why:[/bold cyan] {teaser.explanation}"
        if teaser.explanation
        else ""
    )

    if cleaned_input.lower() in {"s", "skip"}:
        CONSOLE.print(
            Panel(
                f"[bold yellow]⤼ Skipped[/bold yellow]\n\n"
                f"[bold]Actual Output:[/bold]\n{actual_display}"
                f"{why_text}",
                border_style="yellow",
            )
        )
        return QuizResult(teaser, cleaned_input, actual_display, "skipped"), False

    is_correct = fuzzy_match(cleaned_input, stdout, exc_name, error_line)
    if is_correct:
        CONSOLE.print(
            Panel(
                f"[bold green]✓ Correct![/bold green]\n\n"
                f"[bold]Actual Output:[/bold]\n{actual_display}"
                f"{why_text}",
                border_style="green",
            )
        )
        return QuizResult(teaser, cleaned_input, actual_display, "correct"), True

    CONSOLE.print(
        Panel(
            f"[bold red]✗ Not quite![/bold red]\n\n"
            f"[bold]Your Answer:[/bold] {cleaned_input}\n"
            f"[bold]Actual Output:[/bold] {actual_display}"
            f"{why_text}",
            border_style="red",
        )
    )
    return QuizResult(teaser, cleaned_input, actual_display, "incorrect"), False


def _filter_teasers(
    teasers: list[TeaserItem],
    *,
    start_index: int,
    single_teaser: int | None,
    shuffle: bool,
) -> list[TeaserItem]:
    """Filter and order teasers based on CLI arguments.

    Args:
        teasers: List of all loaded teaser items.
        start_index: Starting puzzle number (1-40).
        single_teaser: Optional single puzzle number to run.
        shuffle: Whether to randomize puzzle order.

    Returns:
        Filtered list of teasers for the quiz session.

    """
    if single_teaser is not None:
        filtered = [t for t in teasers if t.order == single_teaser]
        if not filtered:
            CONSOLE.print(
                f"[bold red]No teaser found with number {single_teaser}.[/bold red]"
            )
            return []
        return filtered

    active = list(teasers)
    if shuffle:
        random.shuffle(active)
    elif start_index > 0:
        active = [t for t in active if t.order >= start_index]

    return active


def _wait_for_next(*, is_last: bool) -> bool:
    """Prompt user to advance to the next puzzle or scorecard, then clear screen.

    Args:
        is_last: Whether the current puzzle is the last one in the session.

    Returns:
        True if the user pressed Enter to continue, False if interrupted.

    """
    prompt = (
        "[dim]Press Enter to view final scorecard...[/dim]"
        if is_last
        else "[dim]Press Enter for next puzzle...[/dim]"
    )
    try:
        Prompt.ask(prompt, default="", show_default=False)
        CONSOLE.clear()
    except (KeyboardInterrupt, EOFError):
        return False
    else:
        return True


def _prompt_user_answer(teaser: TeaserItem) -> str:
    """Prompt user for answer, supporting hints.

    Args:
        teaser: Teaser puzzle item being attempted.

    Returns:
        User's stripped answer string, or 'q' on interrupt.

    """
    prompt_text = "[bold yellow]What will Python output?[/bold yellow]"
    while True:
        try:
            user_input = Prompt.ask(prompt_text)
        except (KeyboardInterrupt, EOFError):
            CONSOLE.print("\n[yellow]Quiz interrupted by user.[/yellow]")
            return "q"

        cleaned = user_input.strip()
        if cleaned.lower() in {"h", "hint"}:
            CONSOLE.print(
                f"[bold cyan]💡 Hint:[/bold cyan] "
                f"[dim]Focus on {teaser.concept.lower()}.[/dim]\n"
            )
            continue
        return cleaned


def run_quiz(
    teasers: list[TeaserItem],
    *,
    start_index: int = 0,
    single_teaser: int | None = None,
    shuffle: bool = False,
    no_ipython: bool = False,
) -> None:
    """Run interactive quiz session.

    Args:
        teasers: List of all loaded teaser items.
        start_index: Starting puzzle number (1-40).
        single_teaser: Optional single puzzle number to run.
        shuffle: Whether to randomize puzzle order.
        no_ipython: Whether to disable launching IPython on failed attempts.

    """
    active_teasers = _filter_teasers(
        teasers,
        start_index=start_index,
        single_teaser=single_teaser,
        shuffle=shuffle,
    )
    if not active_teasers:
        return

    total = len(active_teasers)
    results: list[QuizResult] = []
    score = 0

    CONSOLE.clear()
    banner_desc = (
        "[dim]Predict what each snippet will print or raise. "
        "Spaces, quotes, and case are fuzzy-matched.\n"
        "Fair game rule: the only reference to use is the official "
        "[link=https://docs.python.org/3/]Python documentation[/link].[/dim]"
    )
    CONSOLE.print(
        Panel(
            f"[bold cyan]Python Brain Teasers - Interactive Quiz[/bold cyan]\n"
            f"{banner_desc}",
            border_style="cyan",
        )
    )

    for idx, teaser in enumerate(active_teasers, 1):
        if not teaser.code_path.exists():
            continue

        _display_teaser_panel(teaser, idx, total, score, len(results))

        cleaned_input = _prompt_user_answer(teaser)
        if cleaned_input.lower() in {"q", "quit", "exit"}:
            CONSOLE.clear()
            break

        res, is_correct = _evaluate_attempt(teaser, cleaned_input)
        if is_correct:
            score += 1
        elif res.status == "incorrect" and not no_ipython:
            CONSOLE.print()
            launch_msg = (
                "[bold cyan]Opening IPython terminal to inspect this puzzle..."
                "[/bold cyan]\n"
                "[dim]Code is pre-executed. Explore variables, then type "
                "'exit' or Ctrl+D to return.[/dim]\n"
            )
            CONSOLE.print(launch_msg)
            launch_ipython(teaser.code_path)

        results.append(res)

        if not _wait_for_next(is_last=(idx == total)):
            break

    display_scorecard(results, total_available=total)


def display_scorecard(results: list[QuizResult], total_available: int) -> None:
    """Render final scorecard table and summary.

    Args:
        results: List of completed quiz results.
        total_available: Total number of teasers available in the quiz session.

    """
    if not results:
        CONSOLE.print("[dim]No teasers attempted.[/dim]")
        return

    table = Table(
        title="[bold cyan]Python Brain Teasers - Quiz Scorecard[/bold cyan]",
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Teaser", style="bold", width=22)
    table.add_column("Status", width=12, justify="center")
    table.add_column("Your Answer", width=26)
    table.add_column("Actual Output", width=34)

    correct_count = 0
    for res in results:
        t = res.teaser
        if res.status == "correct":
            correct_count += 1
            status_text = "[bold green]✓ Correct[/bold green]"
        elif res.status == "skipped":
            status_text = "[bold yellow]⤼ Skipped[/bold yellow]"
        else:
            status_text = "[bold red]✗ Wrong[/bold red]"

        user_disp = (
            res.user_input
            if len(res.user_input) <= MAX_USER_DISP_LEN
            else res.user_input[:USER_TRUNCATE_LEN] + "..."
        )
        actual_disp = (
            res.actual_output
            if len(res.actual_output) <= MAX_ACTUAL_DISP_LEN
            else res.actual_output[:ACTUAL_TRUNCATE_LEN] + "..."
        )

        table.add_row(
            f"{t.order:02d}",
            t.filename,
            status_text,
            user_disp,
            actual_disp,
        )

    CONSOLE.print()
    CONSOLE.print(table)

    pct = (correct_count / len(results) * 100) if results else 0
    grade_color = (
        "green"
        if pct >= PASSING_GRADE_PCT
        else ("yellow" if pct >= MEDIOCRE_GRADE_PCT else "red")
    )

    summary_text = (
        f"Attempted: [bold]{len(results)}/{total_available}[/bold] teasers\n"
        f"Score: [bold {grade_color}]{correct_count}/{len(results)}"
        f"[/bold {grade_color}] ({pct:.1f}%)\n"
    )
    summary_panel = Panel(
        summary_text,
        title="[bold]Summary[/bold]",
        border_style=grade_color,
    )
    CONSOLE.print(summary_panel)


def main() -> None:
    """CLI entry point for the quiz."""
    parser = argparse.ArgumentParser(
        description="Interactive quiz runner for Python Brain Teasers."
    )
    parser.add_argument(
        "--start",
        "-s",
        type=int,
        default=0,
        help="Start quiz from a specific puzzle number (1-40).",
    )
    parser.add_argument(
        "--teaser",
        "-t",
        type=int,
        default=None,
        help="Run only a single puzzle by number (1-40).",
    )
    parser.add_argument(
        "--random",
        "-r",
        action="store_true",
        help="Shuffle puzzles for random flashcard practice.",
    )
    parser.add_argument(
        "--no-ipython",
        action="store_true",
        help="Do not launch IPython terminal on failed attempts.",
    )
    args = parser.parse_args()

    teasers = load_teasers()
    run_quiz(
        teasers=teasers,
        start_index=args.start,
        single_teaser=args.teaser,
        shuffle=args.random,
        no_ipython=args.no_ipython,
    )


if __name__ == "__main__":
    main()
