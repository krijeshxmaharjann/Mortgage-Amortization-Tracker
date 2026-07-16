import pandas as pd
from amortization import AmortizationTracker

class LoanComparison:
    def __init__(self, principal, annual_interest_rate, years,extra_monthly_payment):
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.years = years
        self.extra_monthly_payment = extra_monthly_payment

    def compare_terms(self):
        terms = [5, 10, 15, 20, 25, 30]
        results =[]

        for term in terms:
            tracker = AmortizationTracker(
                principal = self.principal,
                annual_interest_rate = self.annual_interest_rate,
                years = term,
                extra_monthly_payment= self.extra_monthly_payment,
            )
            summary = tracker.get_summary()

            results.append(
                {
                    "Loan Term (Years)": term,
                    "Monthly Payment ($)": round(summary["Monthly Payment"], 2),
                    "Payoff Time (Years)": round(summary["Years"], 2),
                    "Interest Paid ($)": round(summary["Interest Paid"], 2),
                    "Total Loan Cost ($)": round(summary["Total Cost"], 2),
                }
            )

        return pd.DataFrame(results)
    
    def lowest_interest(self):
        df = self.compare_terms()
        return df.loc[df["Interest Paid ($)"].idxmin()]
    
    def lowest_payment(self):
        df = self.compare_terms()
        return df.loc[df["Monthly Payment ($)"].idxmin()]