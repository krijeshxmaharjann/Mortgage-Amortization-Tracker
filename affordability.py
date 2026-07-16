class MortgageAffordabilityCalculator:

    def __init__(
        self,
        annual_income: float,
        monthly_debts: float,
        down_payment: float,
        interest_rate: float,
        years: int,
    ):

        self.annual_income = annual_income
        self.monthly_debts = monthly_debts
        self.down_payment = down_payment
        self.interest_rate = interest_rate
        self.years = years


    # -----------------------------------------
    # Monthly Income
    # -----------------------------------------
    @property
    def monthly_income(self):

        return self.annual_income / 12



    # -----------------------------------------
    # Monthly Interest Rate
    # -----------------------------------------
    @property
    def monthly_interest_rate(self):

        return (
            self.interest_rate / 100
        ) / 12



    # -----------------------------------------
    # Total Loan Payments
    # -----------------------------------------
    @property
    def total_payments(self):

        return self.years * 12



    # -----------------------------------------
    # Maximum Affordable Monthly Payment
    # Using 36% DTI Rule
    # -----------------------------------------
    def maximum_monthly_payment(self):

        max_housing_payment = (
            self.monthly_income * 0.36
        ) - self.monthly_debts

        return max(max_housing_payment, 0)



    # -----------------------------------------
    # Maximum Loan Amount
    # -----------------------------------------
    def maximum_loan_amount(self):

        payment = self.maximum_monthly_payment()

        r = self.monthly_interest_rate

        n = self.total_payments


        if r == 0:

            return payment * n


        loan = (
            payment *
            (((1 + r) ** n - 1)
             /
             (r * (1 + r) ** n))
        )


        return loan



    # -----------------------------------------
    # Maximum Home Price
    # -----------------------------------------
    def maximum_home_price(self):

        return (
            self.maximum_loan_amount()
            +
            self.down_payment
        )



    # -----------------------------------------
    # Debt To Income Ratio
    # -----------------------------------------
    def debt_to_income_ratio(self):

        if self.monthly_income == 0:

            return 0


        return (
            self.monthly_debts
            /
            self.monthly_income
        ) * 100



    # -----------------------------------------
    # Summary For Streamlit
    # -----------------------------------------
    def summary(self):

        return {

            "Annual Income":
                round(
                    self.annual_income,
                    2
                ),


            "Monthly Income":
                round(
                    self.monthly_income,
                    2
                ),


            "Monthly Debts":
                round(
                    self.monthly_debts,
                    2
                ),


            "Debt-to-Income (%)":
                round(
                    self.debt_to_income_ratio(),
                    2
                ),


            "Estimated Affordable Monthly Payment":
                round(
                    self.maximum_monthly_payment(),
                    2
                ),


            "Estimated Maximum Loan":
                round(
                    self.maximum_loan_amount(),
                    2
                ),


            "Estimated Home Price":
                round(
                    self.maximum_home_price(),
                    2
                ),
        }