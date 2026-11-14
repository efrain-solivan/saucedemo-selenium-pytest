# SauceDemo UI Test Suite (Selenium + Pytest)

[![UI tests](https://github.com/efrain-solivan/saucedemo-selenium-pytest/actions/workflows/tests.yml/badge.svg)](https://github.com/efrain-solivan/saucedemo-selenium-pytest/actions/workflows/tests.yml)

Automated UI tests for [saucedemo.com](https://www.saucedemo.com/), a demo store published by Sauce Labs for test practice. The suite covers login, the product list, the cart and checkout. It runs headless in GitHub Actions on every push and once a week against the live site.

## What it shows

- **Page Object Model.** Locators live only in `pages/`. Tests read as user actions.
- **Pytest fixtures** chain the setup steps: `driver` → `login_page` → `inventory` (logged in).
- **Parametrized negative tests.** Four rejected-login cases and three required-field checks at checkout, each with its own readable test ID.
- **Calculation check.** The checkout total must equal subtotal + tax, to the cent.
- **Known defects as strict xfails.** SauceDemo's `problem_user` ships two deliberate bugs. They're tracked as `xfail(strict=True)`, so the suite fails if a bug ever disappears and the xfail goes stale.
- **Evidence on failure.** Any failing test attaches a screenshot to the self-contained HTML report.

## Coverage

| Area | Tests | Notes |
|---|---|---|
| Login | 7 | Valid login, locked-out user, wrong password, empty fields, logout, direct-URL access blocked |
| Inventory | 6 | Six-product catalog, four sort orders, `problem_user` price sort (known defect) |
| Cart | 4 | Badge count, add/remove, cart kept across navigation, empty state |
| Checkout | 6 | End-to-end order with total math, three required fields, cancel, `problem_user` Last Name field (known defect) |

Last local run: **21 passed, 2 xfailed** (Chrome, headless).

## Known defects found

| ID | User | Steps | Expected | Actual |
|---|---|---|---|---|
| KD-1 | `problem_user` | Products → Sort "Price (low to high)" | Prices ascending | Order unchanged |
| KD-2 | `problem_user` | Checkout → type First Name, then Last Name | Last Name holds the typed value | Last Name stays empty; the text overwrites First Name |

## Run it

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows; use source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
pytest                        # headless; report at reports/report.html
pytest --headed -m smoke      # watch the 3 critical-path tests run
```

Selenium Manager downloads the matching ChromeDriver automatically. To point the suite at another environment, set `BASE_URL`.

## Layout

```
pages/       page objects (base, login, inventory, cart, checkout)
tests/       test modules by feature
conftest.py  browser fixture, page fixtures, screenshot-on-failure hook
```

Built by Efrain Solivan as part of a QA engineering portfolio.
