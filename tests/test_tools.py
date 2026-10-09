"""The computing tools: money_model.py, channel_math.py, journal.py.

    pytest tests
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cli(name: str, *args: str, env: dict | None = None) -> tuple[int, dict | None, str]:
    out = subprocess.run([sys.executable, str(SCRIPTS / f"{name}.py"), *args], capture_output=True,
                         text=True, encoding="utf-8", env=env)
    lines = out.stdout.strip().splitlines()
    data = json.loads(lines[-1]) if out.returncode == 0 and lines else None
    return out.returncode, data, out.stdout + out.stderr


# --- money_model -------------------------------------------------------------------------

mm = load("money_model")


def test_client_financed_acquisition_met():
    r = mm.evaluate(cac=100, profit_30d=250, ltgp=700, humans=1)
    assert r["ratio_30d"] == 2.5 and r["thirty_day_rule"] == "target"
    assert r["customers_funded_in_30d"] == 1
    assert r["ltgp_cac"] == 7.0 and r["ltgp_bar"] == 6.0 and r["ltgp_pass"] is True
    assert r["verdict"] == "can buy growth"


def test_thirty_day_rule_failed():
    r = mm.evaluate(cac=300, profit_30d=150, ltgp=2400, humans=0)
    assert r["thirty_day_rule"] == "fail"
    assert r["verdict"] == "fix the first 30 days first"


def test_lifetime_value_below_the_bar_for_two_humans():
    r = mm.evaluate(cac=100, profit_30d=120, ltgp=800, humans=2)
    assert r["thirty_day_rule"] == "pass" and r["ltgp_bar"] == 9.0 and r["ltgp_pass"] is False
    assert r["verdict"] == "fix lifetime value before scaling spend"


def test_more_than_three_humans_uses_the_last_bar():
    assert mm.evaluate(cac=10, profit_30d=10, ltgp=200, humans=7)["ltgp_bar"] == 12.0


def test_profit_derived_from_revenue_and_margin():
    profit_30d, ltgp = mm.derive(upfront=200, monthly=100, months=6, margin_pct=50)
    assert profit_30d == pytest.approx(150) and ltgp == pytest.approx(400)


@pytest.mark.parametrize("cac,p30,ltgp", [(0, 10, 20), (100, -1, 20), (100, 50, 20)])
def test_invalid_numbers_are_refused(cac, p30, ltgp):
    with pytest.raises(ValueError):
        mm.evaluate(cac=cac, profit_30d=p30, ltgp=ltgp, humans=0)


def test_money_model_cli():
    code, data, _ = cli("money_model", "--cac", "120", "--profit-30d", "300", "--ltgp", "900", "--humans", "1")
    assert code == 0 and data["ratio_30d"] == 2.5 and data["ltgp_pass"] is True
    code, _, out = cli("money_model", "--cac", "120")
    assert code == 2 and "error" in out


# --- channel_math ------------------------------------------------------------------------

cm = load("channel_math")


def test_forty_sends_at_three_percent_make_a_zero_uninformative():
    r = cm.compute(40, 0.03)
    assert r["expected_replies"] == 1.2
    assert r["p_zero_replies"] == pytest.approx(0.97 ** 40, abs=1e-4)
    assert r["zero_is_informative"] is False
    assert r["sends_for_informative_zero"] == 76


def test_enough_sends_make_a_zero_informative():
    assert cm.compute(100, 0.03)["zero_is_informative"] is True


def test_deal_arithmetic():
    r = cm.compute(100, 0.05, positive_rate=0.4, close_rate=0.25)
    assert r["deal_rate_per_send"] == pytest.approx(0.005)
    assert r["expected_deals"] == pytest.approx(0.5)
    assert r["sends_for_one_deal_90pct"] == 460


@pytest.mark.parametrize("text,expected", [("0.03", 0.03), ("3%", 0.03), ("3", 0.03)])
def test_rates_accept_fraction_and_percent(text, expected):
    assert cm.rate(text) == pytest.approx(expected)


def test_channel_math_cli_refuses_a_rate_of_zero():
    code, _, _ = cli("channel_math", "--sends", "10", "--reply-rate", "0")
    assert code != 0


# --- journal -----------------------------------------------------------------------------


@pytest.fixture
def journal_env(tmp_path):
    env = dict(__import__("os").environ, WEALTH_JOURNAL=str(tmp_path / "j" / "journal.jsonl"),
               PYTHONIOENCODING="utf-8")
    return env, tmp_path / "j" / "journal.jsonl"


def add(env, decision, verdict="conditions", deadline="2026-10-20", laws="FLE-3,FLS-12"):
    return cli("journal", "add", "--decision", decision, "--verdict", verdict, "--laws", laws,
               "--test", "46 prospects x 3 touches", "--deadline", deadline,
               "--decides", "1 reply asking for the audit", "--date", "2026-10-09", env=env)


def test_full_loop_add_due_close_stats(journal_env):
    env, path = journal_env
    code, first, _ = add(env, "Cold email, local SEO")
    assert code == 0 and first["id"] == 1 and first["laws"] == ["FLE-3", "FLS-12"]
    assert add(env, "Second build", verdict="go", deadline="2026-12-01")[1]["id"] == 2

    _, due, _ = cli("journal", "due", "--today", "2026-10-25", env=env)
    assert [d["id"] for d in due] == [1]

    _, closed, _ = cli("journal", "close", "1", "--executed", "yes", "--outcome", "not_met",
                       "--note", "0 replies on 46", env=env)
    assert closed["outcome"] == "not_met"
    _, due_after, _ = cli("journal", "due", "--today", "2026-10-25", env=env)
    assert due_after == []

    _, stats, _ = cli("journal", "stats", env=env)
    assert stats["decisions"] == 2 and stats["open"] == 1 and stats["closed"] == 1
    assert stats["execution_rate"] == 1.0 and stats["met_rate_when_run"] == 0.0
    assert stats["by_verdict"]["conditions"]["not_met"] == 1
    assert stats["laws_in_missed_tests"] == {"FLE-3": 1, "FLS-12": 1}
    assert path.exists()


def test_a_test_not_run_is_void_not_a_failure(journal_env):
    env, _ = journal_env
    add(env, "Cold email, local SEO")
    _, closed, _ = cli("journal", "close", "1", "--executed", "no", env=env)
    assert closed["outcome"] == "void"
    _, stats, _ = cli("journal", "stats", env=env)
    assert stats["execution_rate"] == 0.0 and stats["met_rate_when_run"] is None


def test_executed_test_needs_an_outcome(journal_env):
    env, _ = journal_env
    add(env, "Cold email, local SEO")
    code, _, out = cli("journal", "close", "1", "--executed", "yes", env=env)
    assert code == 2 and "outcome" in out


def test_unknown_id_and_bad_date_are_refused(journal_env):
    env, _ = journal_env
    assert cli("journal", "close", "9", "--executed", "no", env=env)[0] == 2
    assert cli("journal", "add", "--decision", "x", "--verdict", "go", "--test", "t",
               "--deadline", "next week", "--decides", "d", env=env)[0] != 0


def test_unreadable_lines_are_skipped_not_fatal(journal_env):
    env, path = journal_env
    add(env, "Cold email, local SEO")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("{not json\n")
    code, stats, _ = cli("journal", "stats", env=env)
    assert code == 0 and stats["decisions"] == 1 and stats["unreadable_lines"] == 1
