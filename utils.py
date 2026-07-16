import pandas as pd

def format_currency(value):
    return f"${value:,.2f}"

def fromat_percentage(value):
    return f"{value:,.2f}%"

def schedule_to_dataframe(schedule):
    return pd.DataFrame(schedule)

def dataframe_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def create_summary_dataframe(summary):
    return pd.DataFrame(
        {
            "Metric": summary.keys(),
            "Value": summary.values(),
        }
    )


def validate_inputs(principal, interest_rate, years):
    errors = []

    if principal <= 0:
        errors.append("Loan amount must be greater than $0.")

    if interest_rate < 0:
        errors.append("Interest rate cannot be negative.")

    if years <= 0:
        errors.append("Loan term must be greater than zero.")

    return errors


def validate_affordability_inputs(annual_income, monthly_debts, down_payment):
    errors = []

    if annual_income <= 0:
        errors.append("Annual income must be greater than $0.")

    if monthly_debts < 0:
        errors.append("Monthly debts cannot be negative.")

    if down_payment < 0:
        errors.append("Down payment cannot be negative.")

    return errors


def calculate_interest_savings(standard_interest,accelerated_interest):
    return max(0, standard_interest - accelerated_interest)


def calculate_time_saved(standard_months,accelerated_months):
    months_saved = standard_months - accelerated_months

    return {"months": months_saved, "years": months_saved / 12}


def payment_summary(monthly_payment,extra_payment):
    return monthly_payment + extra_payment