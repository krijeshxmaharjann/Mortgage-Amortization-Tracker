class AmortizationTracker:
    def __init__(self, principal, annual_interest_rate, years, extra_monthly_payment=0):
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.years = years
        self.extra_monthly_payment = extra_monthly_payment

        # Convert annual interest rate into monthly parameters
        self.monthly_rate = (annual_interest_rate / 100) / 12
        self.total_payments = years * 12

        # Calculate the fixed monthly payment
        self.monthly_payment = self.calculate_monthly_payment()

    def calculate_monthly_payment(self):
        if self.monthly_rate == 0:
            return self.principal / self.total_payments

        p = self.principal
        r = self.monthly_rate
        n = self.total_payments

        payment = p * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return payment

    def generate_schedule(self):
        balance = self.principal
        schedule = []

        total_interest = 0
        total_principal = 0
        month = 0

        while balance > 0:
            month += 1

            interest = balance * self.monthly_rate

            principal_payment = (
                self.monthly_payment
                - interest
                + self.extra_monthly_payment
            )

            if principal_payment > balance:
                principal_payment = balance

            balance -= principal_payment

            total_interest += interest
            total_principal += principal_payment

            schedule.append(
                {
                    "Month": month,
                    "Monthly Payment": round(principal_payment + interest, 2),
                    "Interest Paid": round(interest, 2),
                    "Principal Paid": round(principal_payment, 2),
                    "Remaining Balance": round(max(balance, 0), 2),
                }
            )

        return (
            schedule,
            month,
            round(total_interest, 2),
            round(total_principal, 2),
        )

    def get_summary(self):
        (
            schedule,
            months,
            interest,
            principal,
        ) = self.generate_schedule()

        return {
            "Monthly Payment": round(self.monthly_payment, 2),
            "Months": months,
            "Years": round(months / 12, 2),
            "Interest Paid": interest,
            "Principal Paid": principal,
            "Total Cost": round(interest + principal, 2),
        }