# coreflow_app/app.py

import streamlit as st
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Core Flow Financial Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. IMPORT OUR ENGINE ---
from engine.budget import (
    generate_budget_plan,
    project_wealth_growth,
    calculate_financial_score,
    generate_narrative_insights,
    LIFESTYLE_RULES,
    MOOD_MODIFIERS
)

# --- 4. APP STRUCTURE ---
st.title("🧭 Core Flow Financial Navigator")
st.markdown("Your personalized guide to financial clarity and control.")

# --- 5. SIDEBAR FOR USER INPUTS ---
with st.sidebar:
    st.header("👤 Your Profile")
    st.markdown("Enter your details to generate a personalized budget plan.")
    
    lifestyle_options = list(LIFESTYLE_RULES.keys())
    mood_options = list(MOOD_MODIFIERS.keys())

    lifestyle = st.selectbox("🧑‍💻 What is your lifestyle?", options=lifestyle_options, index=1)
    income = st.number_input("💰 What is your monthly income?", min_value=0, value=50000, step=1000, format="%d")
    fixed_commitments = st.number_input("🏠 What are your fixed monthly commitments?", min_value=0, value=15000, step=500, format="%d")
    mood = st.radio("🧘 What is your current financial mood?", options=mood_options, index=1, horizontal=True)

# --- MAIN PAGE CONTENT ---
st.header("📊 Your Recommended Budget Plan")

if income > 0:
    # --- ALL LOGIC AND DISPLAY HAPPENS INSIDE THIS BLOCK ---
    budget_plan = generate_budget_plan(income=income, fixed_commitments=fixed_commitments, lifestyle=lifestyle, mood=mood)
    score_details = calculate_financial_score(income=income, savings=budget_plan["Savings"], necessities=budget_plan["Necessities"])
    narrative = generate_narrative_insights(lifestyle=lifestyle, score_details=score_details, budget_plan=budget_plan, income=income)

    # --- Section 0: The "Health Summary" Card ---
    st.subheader("📝 Your Financial Health Summary")
    st.info(narrative)

    # --- Section 1: Budget Allocation & Mood Impact ---
    st.subheader("Budget Allocation Breakdown")
    col1, col2 = st.columns([2, 1])
    with col1:
        necessities_for_chart = budget_plan["Fixed Commitments"] + budget_plan["Flex Necessities"]
        chart_data = [
            {"Category": "Necessities 🏠", "Amount": necessities_for_chart},
            {"Category": "Wants 🎉", "Amount": budget_plan["Wants"]},
            {"Category": "Savings 💰", "Amount": budget_plan["Savings"]},
        ]
        category_colors = {"Necessities 🏠": "#FF6347", "Wants 🎉": "#FFD700", "Savings 💰": "#32CD32"}
        fig_pie = px.pie(chart_data, values='Amount', names='Category', color='Category', color_discrete_map=category_colors, hole=0.4)
        fig_pie.update_traces(textinfo='percent+label', pull=[0, 0, 0.05])
        fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.markdown("### Mood Impact")
        balanced_plan = generate_budget_plan(income, fixed_commitments, lifestyle, "Balanced")
        # --- BUG FIX APPLIED HERE ---
        monthly_delta = budget_plan['Savings'] - balanced_plan['Savings']
        
        if monthly_delta != 0:
            impact_projection = project_wealth_growth(abs(monthly_delta))
            total_impact = impact_projection['Nominal Growth'].iloc[-1]
        else:
            total_impact = 0
            
        if mood == "Disciplined":
            st.metric(label="✅ Extra Wealth Gained in 12 Months", value=f"₹{total_impact:,.0f}", delta="proactive")
        elif mood == "Splurge":
            st.metric(label="⚠️ Future Savings Lost in 12 Months", value=f"₹{total_impact:,.0f}", delta="- reactive", delta_color="inverse")
        else:
            st.info("You're on a balanced path.")

    # --- Section 2: Key Monthly Figures ---
    st.markdown("---")
    st.subheader("Key Monthly Figures")
    c1, c2 = st.columns(2)
    c1.metric(label="🏠 Fixed Commitments", value=f"₹{budget_plan['Fixed Commitments']:.0f}", help="Rent, EMIs, etc.")
    c2.metric(label="🛒 Flexible Necessities", value=f"₹{budget_plan['Flex Necessities']:.0f}", help="Groceries, Utilities, etc.")

    # --- Section 3: Wealth Growth Projection ---
    st.markdown("---")
    st.subheader("📈 12-Month Wealth Projection")
    show_inflation = st.toggle("Adjust for Inflation (Show Real Value)", value=True)
    monthly_savings = budget_plan["Savings"]
    projection_df = project_wealth_growth(monthly_savings)
    plot_columns = ['Nominal Growth']
    if show_inflation:
        plot_columns.append('Real Growth')
    if not projection_df.empty and monthly_savings > 0:
        fig_line = px.line(projection_df, x='Month', y=plot_columns, labels={"value": "Projected Wealth (₹)", "variable": "Growth Type"})
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Start saving to see your wealth projection.")

    # --- Section 4: Financial Fitness Scorecard ---
    st.markdown("---")
    st.subheader("⭐ Your Financial Fitness Scorecard")
    scol1, scol2 = st.columns(2)
    with scol1:
        st.markdown(f"""<div style='text-align: center; border: 2px solid #32CD32; border-radius: 10px; padding: 20px;'>
            <p style='font-size: 24px; margin-bottom: 5px;'>Your Grade</p>
            <p style='font-size: 72px; font-weight: bold; margin: 0;'>{score_details['grade']} {score_details['emoji']}</p>
            </div>""", unsafe_allow_html=True)
    with scol2:
        st.metric(label="Savings Rate", value=f"{score_details['savings_rate']:.1%}")
        st.markdown("**Emergency Fund Preparedness**")
        st.progress(score_details['emergency_fund_progress'])
    st.markdown(f"**💡 Insight:** {score_details['comment']}")

    # --- Section 5: "What-If?" Scenario Planner ---
    st.markdown("---")
    with st.expander("🔮 What-If? Scenario Planner"):
        savings_adjustment = st.slider("Adjust Savings (+/- % of Income)", -10, 20, 0, 1, format="%d%%")
        if savings_adjustment != 0:
            change_amount = income * (savings_adjustment / 100.0)
            new_monthly_savings = max(0, budget_plan["Savings"] + change_amount)
            new_monthly_wants = max(0, budget_plan["Wants"] - change_amount)
            new_projection_df = project_wealth_growth(new_monthly_savings)
            new_total_wealth = new_projection_df['Nominal Growth'].iloc[-1] if not new_projection_df.empty else 0
            original_projection_df = project_wealth_growth(budget_plan["Savings"])
            original_total_wealth = original_projection_df['Nominal Growth'].iloc[-1] if not original_projection_df.empty else 0
            st.markdown("#### Scenario Impact:")
            pcol1, pcol2 = st.columns(2)
            pcol1.metric("New Monthly Savings", f"₹{new_monthly_savings:,.0f}", f"₹{new_monthly_savings - budget_plan['Savings']:,.0f}")
            pcol1.metric("New Monthly Wants", f"₹{new_monthly_wants:,.0f}", f"₹{new_monthly_wants - budget_plan['Wants']:,.0f}", delta_color="inverse")
            pcol2.metric("New 12-Month Projected Wealth", f"₹{new_total_wealth:,.0f}", f"₹{new_total_wealth - original_total_wealth:,.0f}")
        else:
            st.info("Move the slider to explore a new scenario.")
        
        # --- NEW CODE: SPLURGE SIMULATOR ---
        st.markdown("---")
        st.markdown("#### 💸 Splurge Simulator")
        # This is the corrected line
        splurge_amount = st.number_input("Enter a recurring monthly splurge (₹):", min_value=0, value=1000, step=100, format="%d")
        if splurge_amount > 0:
            splurge_projection_df = project_wealth_growth(monthly_savings=splurge_amount, duration_months=60)
            lost_wealth = splurge_projection_df['Nominal Growth'].iloc[-1] if not splurge_projection_df.empty else 0
            st.metric(
                label="Potential Wealth Lost Over 5 Years",
                value=f"₹{lost_wealth:,.0f}",
                help="This is the amount you could have if you invested that monthly splurge instead."
            )
        else:
            st.info("Enter a splurge amount to see its long-term cost.")

else:
    st.info("Please enter your monthly income in the sidebar to generate a budget plan.")