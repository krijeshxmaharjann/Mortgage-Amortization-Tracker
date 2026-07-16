import streamlit as st
import pandas as pd

from amortization import AmortizationTracker
from compariosn import LoanComparison
from affordability import MortgageAffordabilityCalculator
from charts import MortgageCharts
from utils import (
    dataframe_to_csv,
    format_currency,
    validate_inputs,
    validate_affordability_inputs,
    calculate_interest_savings,
    calculate_time_saved,
)

# --------------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------------

st.set_page_config(
    page_title="Enterprise Mortgage Dashboard",
    page_icon="🏠",
    layout="wide",
)

# --------------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title{
        font-size:42px;
        font-weight:700;
        color:#1f77b4;
    }

    .section-title{
        font-size:28px;
        font-weight:600;
        margin-top:20px;
    }

    footer{
        visibility:hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------
# TITLE
# --------------------------------------------------------

st.markdown(
    "<div class='main-title'>🏠 Enterprise Mortgage Amortization Dashboard</div>",
    unsafe_allow_html=True,
)

st.write(
    """
Analyze mortgage payments, compare loan terms,
estimate affordability, visualize payoff progress,
and export a complete amortization schedule.
"""
)

st.divider()

# --------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------

st.sidebar.header("Mortgage Inputs")

principal = st.sidebar.number_input(
    "Loan Amount ($)",
    min_value=10000,
    max_value=5000000,
    value=300000,
    step=10000,
)

interest_rate = st.sidebar.slider(
    "Interest Rate (%)",
    min_value=1.0,
    max_value=15.0,
    value=6.5,
    step=0.1,
)

years = st.sidebar.selectbox(
    "Loan Term",
    [15, 20, 30],
    index=2,
)

extra_payment = st.sidebar.number_input(
    "Extra Monthly Payment ($)",
    min_value=0.0,
    value=250.0,
    step=50.0,
)

st.sidebar.divider()

st.sidebar.header("Affordability Calculator")

annual_income = st.sidebar.number_input(
    "Annual Income ($)",
    min_value=10000,
    value=120000,
    step=5000,
)

monthly_debts = st.sidebar.number_input(
    "Monthly Debts ($)",
    min_value=0.0,
    value=500.0,
    step=50.0,
)

down_payment = st.sidebar.number_input(
    "Down Payment ($)",
    min_value=0.0,
    value=60000.0,
    step=5000.0,
)

# --------------------------------------------------------
# INPUT VALIDATION
# --------------------------------------------------------

loan_errors = validate_inputs(
    principal,
    interest_rate,
    years,
)

affordability_errors = validate_affordability_inputs(
    annual_income,
    monthly_debts,
    down_payment,
)

for error in loan_errors:
    st.error(error)

for error in affordability_errors:
    st.error(error)

if loan_errors or affordability_errors:
    st.stop()

# --------------------------------------------------------
# CREATE TRACKERS
# --------------------------------------------------------

tracker = AmortizationTracker(
    principal=principal,
    annual_interest_rate=interest_rate,
    years=years,
    extra_monthly_payment=extra_payment,
)

standard_tracker = AmortizationTracker(
    principal=principal,
    annual_interest_rate=interest_rate,
    years=years,
    extra_monthly_payment=0,
)

schedule, months, interest_paid, principal_paid = (
    tracker.generate_schedule()
)

summary = tracker.get_summary()

standard_schedule, standard_months, standard_interest, _ = (
    standard_tracker.generate_schedule()
)

interest_saved = calculate_interest_savings(
    standard_interest,
    interest_paid,
)

time_saved = calculate_time_saved(
    standard_months,
    months,
)

df = pd.DataFrame(schedule)

# --------------------------------------------------------
# SUMMARY DASHBOARD
# --------------------------------------------------------

st.markdown(
    "<div class='section-title'>📊 Mortgage Payoff Summary</div>",
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        label="Monthly Payment",
        value=format_currency(
            tracker.monthly_payment
        ),
    )

    st.caption(
        f"With extra payment: "
        f"{format_currency(tracker.monthly_payment + extra_payment)}"
    )


with col2:
    st.metric(
        label="Payoff Time",
        value=f"{summary['Years']} Years",
    )

    if extra_payment > 0:
        st.caption(
            f"Saved: {time_saved['years']:.2f} years"
        )


with col3:
    st.metric(
        label="Total Interest",
        value=format_currency(
            interest_paid
        ),
    )

    if interest_saved > 0:
        st.caption(
            f"Saved: {format_currency(interest_saved)}"
        )


with col4:
    st.metric(
        label="Total Loan Cost",
        value=format_currency(
            summary["Total Cost"]
        ),
    )


st.divider()


# --------------------------------------------------------
# AMORTIZATION TABLE
# --------------------------------------------------------

st.markdown(
    "<div class='section-title'>📋 Amortization Schedule</div>",
    unsafe_allow_html=True,
)

with st.expander(
    "View Full Month-by-Month Payment Schedule"
):

    st.dataframe(
        df,
        use_container_width=True,
        height=400,
    )


# --------------------------------------------------------
# CSV DOWNLOAD
# --------------------------------------------------------

csv_file = dataframe_to_csv(df)

st.download_button(
    label="📥 Download Amortization CSV",
    data=csv_file,
    file_name="mortgage_amortization_schedule.csv",
    mime="text/csv",
)


st.divider()


# --------------------------------------------------------
# LOAN COMPARISON
# --------------------------------------------------------

st.markdown(
    "<div class='section-title'>🏦 Loan Term Comparison</div>",
    unsafe_allow_html=True,
)


comparison = LoanComparison(
    principal,
    interest_rate,
    years,
    extra_payment,
)

comparison_df = comparison.compare_terms()


st.dataframe(
    comparison_df,
    use_container_width=True,
)


best_interest = comparison.lowest_interest()

best_payment = comparison.lowest_payment()


col5, col6 = st.columns(2)


with col5:

    st.success(
        f"""
        💰 Lowest Interest Option
        
        {int(best_interest['Loan Term (Years)'])} Year Loan
        
        Interest:
        {format_currency(best_interest['Interest Paid ($)'])}
        """
    )


with col6:

    st.info(
        f"""
        💵 Lowest Monthly Payment
        
        {int(best_payment['Loan Term (Years)'])} Year Loan
        
        Payment:
        {format_currency(best_payment['Monthly Payment ($)'])}
        """
    )


st.divider()

# --------------------------------------------------------
# VISUAL ANALYTICS
# --------------------------------------------------------

st.markdown(
    "<div class='section-title'>📈 Mortgage Analytics</div>",
    unsafe_allow_html=True,
)


# Create chart object
mortgage_charts = MortgageCharts(df)


# --------------------------------------------------------
# BALANCE CHART
# --------------------------------------------------------

st.subheader("📉 Remaining Loan Balance")

st.plotly_chart(
    mortgage_charts.remaining_balance_chart(),
    use_container_width=True,
)


# --------------------------------------------------------
# PRINCIPAL VS INTEREST
# --------------------------------------------------------

col7, col8 = st.columns(2)


with col7:

    st.subheader(
        "🥧 Principal vs Interest"
    )

    st.plotly_chart(
        mortgage_charts.payment_breakdown_chart(),
        use_container_width=True,
    )


with col8:

    st.subheader(
        "📊 Monthly Payment Breakdown"
    )

    st.plotly_chart(
        mortgage_charts.monthly_payment_chart(),
        use_container_width=True,
    )


# --------------------------------------------------------
# CUMULATIVE CHARTS
# --------------------------------------------------------

st.subheader(
    "💰 Cumulative Interest Paid"
)

st.plotly_chart(
    mortgage_charts.cumulative_interest_chart(),
    use_container_width=True,
)



st.subheader(
    "🏠 Cumulative Principal Paid"
)

st.plotly_chart(
    mortgage_charts.cumulative_principal_chart(),
    use_container_width=True,
)


st.divider()

# --------------------------------------------------------
# AFFORDABILITY ANALYSIS
# --------------------------------------------------------

st.markdown(
    "<div class='section-title'>🏡 Mortgage Affordability Analysis</div>",
    unsafe_allow_html=True,
)


affordability = MortgageAffordabilityCalculator(
    annual_income=annual_income,
    monthly_debts=monthly_debts,
    down_payment=down_payment,
    interest_rate=interest_rate,
    years=years,
)


affordability_summary = affordability.summary()


col9, col10, col11 = st.columns(3)


with col9:

    st.metric(
        "Estimated Affordable Home Price",
        format_currency(
            affordability_summary[
                "Estimated Home Price"
            ]
        ),
    )


with col10:

    st.metric(
        "Maximum Loan Amount",
        format_currency(
            affordability_summary[
                "Estimated Maximum Loan"
            ]
        ),
    )


with col11:

    st.metric(
        "Debt-to-Income Ratio",
        f"{affordability_summary['Debt-to-Income (%)']}%",
    )


st.divider()


# --------------------------------------------------------
# AFFORDABILITY DETAILS TABLE
# --------------------------------------------------------

st.subheader(
    "📋 Affordability Breakdown"
)


affordability_df = pd.DataFrame(
    {
        "Metric": affordability_summary.keys(),
        "Value": affordability_summary.values(),
    }
)


st.dataframe(
    affordability_df,
    use_container_width=True,
)


st.divider()


# --------------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------------

st.markdown(
    """
## 🚀 About This Project

**Enterprise Mortgage Amortization Dashboard**

Built with:

- Python
- Object-Oriented Programming
- Streamlit
- Pandas
- Plotly

Features:

✅ Mortgage payment calculation  
✅ Amortization schedule generation  
✅ Extra payment payoff analysis  
✅ Loan term comparison  
✅ Mortgage affordability calculator  
✅ Interactive financial charts  
✅ CSV export  

This application demonstrates software engineering,
financial modeling, and data visualization concepts.
"""
)


st.caption(
    "Mortgage Analytics Dashboard | Built with Python + Streamlit"
)