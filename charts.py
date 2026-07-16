import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class MortgageCharts:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()


    # -----------------------------------------
    # 1. Remaining Balance Over Time
    # -----------------------------------------
    def remaining_balance_chart(self):

        fig = px.line(
            self.df,
            x="Month",
            y="Remaining Balance",
            title="Remaining Loan Balance Over Time",
            markers=False,
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Balance ($)",
            hovermode="x unified",
        )

        return fig



    # -----------------------------------------
    # 2. Principal vs Interest Pie Chart
    # -----------------------------------------
    def payment_breakdown_chart(self):

        total_principal = self.df["Principal Paid"].sum()
        total_interest = self.df["Interest Paid"].sum()

        data = pd.DataFrame(
            {
                "Category": [
                    "Principal",
                    "Interest"
                ],
                "Amount": [
                    total_principal,
                    total_interest
                ],
            }
        )

        fig = px.pie(
            data,
            names="Category",
            values="Amount",
            title="Principal vs Interest Breakdown",
            hole=0.4,
        )

        return fig



    # -----------------------------------------
    # 3. Monthly Payment Breakdown
    # -----------------------------------------
    def monthly_payment_chart(self):

        fig = go.Figure()


        fig.add_trace(
            go.Bar(
                x=self.df["Month"],
                y=self.df["Principal Paid"],
                name="Principal",
            )
        )


        fig.add_trace(
            go.Bar(
                x=self.df["Month"],
                y=self.df["Interest Paid"],
                name="Interest",
            )
        )


        fig.update_layout(
            title="Monthly Payment Breakdown",
            barmode="stack",
            xaxis_title="Month",
            yaxis_title="Payment ($)",
            hovermode="x unified",
        )


        return fig



    # -----------------------------------------
    # 4. Cumulative Interest Paid
    # -----------------------------------------
    def cumulative_interest_chart(self):

        df = self.df.copy()

        df["Cumulative Interest"] = (
            df["Interest Paid"].cumsum()
        )


        fig = px.line(
            df,
            x="Month",
            y="Cumulative Interest",
            title="Cumulative Interest Paid",
        )


        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Interest ($)",
        )


        return fig



    # -----------------------------------------
    # 5. Cumulative Principal Paid
    # -----------------------------------------
    def cumulative_principal_chart(self):

        df = self.df.copy()

        df["Cumulative Principal"] = (
            df["Principal Paid"].cumsum()
        )


        fig = px.line(
            df,
            x="Month",
            y="Cumulative Principal",
            title="Cumulative Principal Paid",
        )


        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Principal ($)",
        )


        return fig