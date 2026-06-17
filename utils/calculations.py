def calculate_total_assets(snapshot: dict) -> float:
    return (
        snapshot.get("bank_balance", 0)
        + snapshot.get("savings_balance", 0)
        + snapshot.get("investments_value", 0)
        + snapshot.get("crypto_value", 0)
        + snapshot.get("pension_value", 0)
        + snapshot.get("business_cash", 0)
        + snapshot.get("other_assets", 0)
    )


def calculate_total_liabilities(snapshot: dict) -> float:
    return (
        snapshot.get("student_debt", 0)
        + snapshot.get("credit_card_debt", 0)
        + snapshot.get("loans", 0)
        + snapshot.get("tax_debt", 0)
        + snapshot.get("other_debt", 0)
    )


def calculate_net_worth(snapshot: dict) -> float:
    return calculate_total_assets(snapshot) - calculate_total_liabilities(snapshot)


def calculate_total_income(entry: dict) -> float:
    return (
        entry.get("salary_income", 0)
        + entry.get("side_income", 0)
        + entry.get("business_income", 0)
        + entry.get("dividend_income", 0)
        + entry.get("other_income", 0)
    )


def calculate_total_expenses(entry: dict) -> float:
    return (
        entry.get("housing_expense", 0)
        + entry.get("groceries_expense", 0)
        + entry.get("eating_out_expense", 0)
        + entry.get("transport_expense", 0)
        + entry.get("travel_expense", 0)
        + entry.get("fun_expense", 0)
        + entry.get("other_expense", 0)
    )


def calculate_cashflow(entry: dict) -> float:
    return calculate_total_income(entry) - calculate_total_expenses(entry)


def calculate_savings_rate(entry: dict) -> float:
    total_income = calculate_total_income(entry)

    if total_income == 0:
        return 0

    return calculate_cashflow(entry) / total_income


def calculate_investment_rate(entry: dict) -> float:
    total_income = calculate_total_income(entry)

    if total_income == 0:
        return 0

    return entry.get("invested_amount", 0) / total_income


def calculate_goal_progress(current_amount: float, target_amount: float) -> float:
    if target_amount == 0:
        return 0

    return current_amount / target_amount


def calculate_fire_target(annual_expenses: float, withdrawal_rate: float = 0.04) -> float:
    if withdrawal_rate == 0:
        return 0

    return annual_expenses / withdrawal_rate


def calculate_fire_progress(current_invested_assets: float, fire_target: float) -> float:
    if fire_target == 0:
        return 0

    return current_invested_assets / fire_target
