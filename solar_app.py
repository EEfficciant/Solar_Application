import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

def calculate_solar_analysis(average_kwh_consumption):
    # Monthly kWh consumption
    monthly_kwh_consumption = average_kwh_consumption * 30

    # Electricity cost parameters
    current_rate_peak = 0.40  # Peak hour rate per kWh
    current_rate_regular = 0.25  # Regular hour rate per kWh
    annual_increase_rate = 0.07  # 7% yearly increase
    tax_rebate_percentage = 30  # Tax rebate percentage

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

    # Creating the table
    data = {
        "Category": [
            "Average Monthly kWh Consumption",
            "Estimated Monthly Electricity Cost Today (Peak Hours)",
            "Number of Solar Panels Required (+10% Buffer)",
            "Estimated Monthly Electricity Cost Today (Regular Hours)",
            "Estimated Monthly Cost in 20 Years (Peak Hours)",
            "Estimated Monthly Cost in 20 Years (Regular Hours)",
            "Estimated Solar System Cost (400W Panels)",
            "Tax Rebate Amount for Solar System (30%)"
        ],
        "Value": [
            f"{monthly_kwh_consumption} kWh",
            f"${monthly_current_cost_peak:.2f}",
            f"{round(panels_needed_with_buffer)} panels",
            f"${monthly_current_cost_regular:.2f}",
            f"${monthly_future_cost_peak:.2f}",
            f"${monthly_future_cost_regular:.2f}",
            f"${total_solar_cost_min:,.2f} - ${total_solar_cost_max:,.2f}",
            f"${solar_tax_rebate_min:,.2f} - ${solar_tax_rebate_max:,.2f}"
        ]
    }

    return pd.DataFrame(data)

# Streamlit UI
st.title("Solar Energy Cost Analysis")
st.markdown("## The Importance of Green Energy")
st.markdown("""
Switching to solar energy is not just about reducing your electricity bills—it's about securing a sustainable future.
With rising electricity costs and environmental concerns, solar energy is the key to energy independence, lower
carbon footprints, and long-term savings. 

✅ **Save Money** - Protect yourself against future energy price hikes.
✅ **Eco-Friendly** - Reduce reliance on fossil fuels and cut CO₂ emissions.
✅ **Incentives & Rebates** - Get up to 30% tax credits for going solar.
✅ **Energy Independence** - Own your energy production and rely less on the grid.
""")

average_kwh = st.number_input("Enter your average daily kWh consumption:", min_value=1, value=45)
df = calculate_solar_analysis(average_kwh)
st.table(df)

# Visualization
st.markdown("## Cost Comparison Over 20 Years")
fig, ax = plt.subplots()
years = list(range(1, 21))
cost_projection = [df.iloc[4, 1] * ((1 + 0.07) ** i) for i in years]
ax.plot(years, cost_projection, marker='o', linestyle='-', label="Projected Cost with 7% Increase")
ax.set_xlabel("Years")
ax.set_ylabel("Estimated Cost ($)")
ax.legend()
st.pyplot(fig)

if st.button("Download Excel Report"):
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    st.download_button(label="Click to Download", data=excel_buffer.getvalue(), file_name="solar_analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

