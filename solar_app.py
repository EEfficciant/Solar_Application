import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Apply custom styling for black text and uniform font
st.markdown(
    """
    <style>
    body {
        background-color: #e6ffe6;
        color: black !important;
        font-family: Arial, sans-serif !important;
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Solar_panels_on_a_roof.jpg/800px-Solar_panels_on_a_roof.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }
    .stApp, .stTable, .stDataFrame, .stMarkdown, .stTitle, .css-1aumxhk, .stButton, .stDownloadButton, .stTextInput, .stNumberInput, .stRadio, .stCheckbox, .stSelectbox, .stMultiselect, .stSlider, .stTextArea, .stColorPicker {
        color: black !important;
        font-family: Arial, sans-serif !important;
        background-color: rgba(230, 255, 230, 0.9) !important;
        border-color: black !important;
    }
    .stDownloadButton {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
    }
    .stButton>button {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
    }
    table {
        color: black !important;
        font-family: Arial, sans-serif !important;
    }
    th, td {
        color: black !important;
        font-family: Arial, sans-serif !important;
        text-align: left !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def calculate_solar_analysis(average_kwh_consumption):
    # Monthly kWh consumption
    monthly_kwh_consumption = average_kwh_consumption * 30

    # Electricity cost parameters
    current_rate_peak = 0.40  # Peak hour rate per kWh
    current_rate_regular = 0.25  # Regular hour rate per kWh
    annual_increase_rate = 0.07  # 7% yearly increase
    tax_rebate_percentage = 30  # Tax rebate percentage
    finance_rate = 0.0126  # Monthly finance rate

    # Electricity cost calculations
    current_cost_peak = average_kwh_consumption * current_rate_peak
    current_cost_regular = average_kwh_consumption * current_rate_regular
    future_cost_peak = current_cost_peak * ((1 + annual_increase_rate) ** 20)
    future_cost_regular = current_cost_regular * ((1 + annual_increase_rate) ** 20)

    # Monthly calculations
    monthly_current_cost_peak = current_cost_peak * 30
    monthly_current_cost_regular = current_cost_regular * 30
    monthly_future_cost_peak = future_cost_peak * 30
    monthly_future_cost_regular = future_cost_regular * 30

    # Solar panel calculation
    panel_wattage = 400  # Panel capacity in watts
    panel_efficiency_factor = 0.8  # Efficiency factor
    daily_solar_production_per_panel = (panel_wattage * panel_efficiency_factor * 5) / 1000
    monthly_solar_production_per_panel = daily_solar_production_per_panel * 30
    panels_needed = monthly_kwh_consumption / monthly_solar_production_per_panel
    panels_needed_with_buffer = panels_needed * 1.1

    # Solar panel cost estimation
    panel_cost_min = 2550
    panel_cost_max = 2800
    total_solar_cost_min = panels_needed_with_buffer * panel_cost_min
    total_solar_cost_max = panels_needed_with_buffer * panel_cost_max

    # Tax rebate calculation
    solar_tax_rebate_min = total_solar_cost_min * (tax_rebate_percentage / 100)
    solar_tax_rebate_max = total_solar_cost_max * (tax_rebate_percentage / 100)
    net_solar_cost_min = total_solar_cost_min - solar_tax_rebate_min
    net_solar_cost_max = total_solar_cost_max - solar_tax_rebate_max

    # Finance calculations
    monthly_finance_payment_min = net_solar_cost_min * finance_rate
    monthly_finance_payment_max = net_solar_cost_max * finance_rate

    # Comparison with electricity bill
    avg_monthly_electricity_cost = (monthly_current_cost_peak + monthly_current_cost_regular) / 2
    finance_vs_electricity_min = monthly_finance_payment_min - avg_monthly_electricity_cost
    finance_vs_electricity_max = monthly_finance_payment_max - avg_monthly_electricity_cost

    # Creating the table
    data = {
        "Category": [
            "1. Average Monthly kWh Consumption",
            "2. Number of Solar Panels Required (+10% Buffer)",  # Swapped with old number 3
            "3. Estimated Monthly Electricity Cost Today (Peak Hours)",  # Swapped with old number 2
            "4. Estimated Monthly Electricity Cost Today (Regular Hours)",
            "5. Estimated Monthly Cost in 20 Years (Peak Hours)",
            "6. Estimated Monthly Cost in 20 Years (Regular Hours)",
            "7. Estimated Solar System Cost (400W Panels)",
            "8. Tax Rebate Amount for Solar System (30%)",
            "9. Monthly Finance Payment After Tax Rebate",
            "10. Monthly Finance Payment Compared to Electricity Bill"
        ],
        "Value": [
            f"{monthly_kwh_consumption:,.0f}",
            f"{round(panels_needed_with_buffer)}",  # Swapped with old number 3
            f"${monthly_current_cost_peak:,.2f}",  # Swapped with old number 2
            f"${monthly_current_cost_regular:,.2f}",
            f"${monthly_future_cost_peak:,.2f}",
            f"${monthly_future_cost_regular:,.2f}",
            f"${total_solar_cost_min:,.2f} - ${total_solar_cost_max:,.2f}",
            f"${solar_tax_rebate_min:,.2f} - ${solar_tax_rebate_max:,.2f}",
            f"${monthly_finance_payment_min:,.2f} - ${monthly_finance_payment_max:,.2f}",
            f"${finance_vs_electricity_min:,.2f} - ${finance_vs_electricity_max:,.2f}"
        ]
    }

    return pd.DataFrame(data)

# Streamlit UI
st.title("Solar Energy Cost Analysis")

st.markdown("## The Importance of Green Energy")
st.markdown("""
Switching to solar energy is not just about reducing your electricity bills—it is about securing a sustainable future.
With rising electricity costs and environmental concerns, solar energy is the key to energy independence, lower
carbon footprints, and long-term savings. 

- **Save Money** - Protect yourself against future energy price hikes.
- **Eco-Friendly** - Reduce reliance on fossil fuels and cut CO₂ emissions.
- **Incentives & Rebates** - Get up to 30% tax credits for going solar.
- **Energy Independence** - Own your energy production and rely less on the grid.
""")

st.markdown("<span style='color:red;'>Enter your average daily kWh consumption:</span>", unsafe_allow_html=True)

average_kwh = st.number_input("Enter your average daily kWh consumption:", min_value=1, value=45)
df = calculate_solar_analysis(average_kwh)
st.table(df)

# Visualization
st.markdown("## Cost Comparison Over 20 Years")
fig, ax = plt.subplots()
years = list(range(1, 21))
cost_projection = [float(df.iloc[4, 1].replace('$', '').replace(',', '')) * ((1 + 0.07) ** i) for i in years]
ax.plot(years, cost_projection, marker='o', linestyle='-', color='green', label="Projected Cost with 7% Increase")
ax.set_xlabel("Years")
ax.set_ylabel("Estimated Cost ($)")
ax.legend()
st.pyplot(fig)
