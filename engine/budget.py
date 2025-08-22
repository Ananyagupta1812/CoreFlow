# engine/budget.py
# This file contains the core calculation logic for the financial navigator.

import pandas as pd

# --- CONFIGURATION CONSTANTS ---
# Using constants makes it easy to tweak the app's logic from one place.
LIFESTYLE_RULES = {
    "Student": {"necessities": 0.50, "wants": 0.35, "savings": 0.15},
    "Working Professional": {"necessities": 0.50, "wants": 0.30, "savings": 0.20},
    "Freelancer": {"necessities": 0.45, "wants": 0.25, "savings": 0.30},
    "Homemaker": {"necessities": 0.60, "wants": 0.25, "savings": 0.15},
}

MOOD_MODIFIERS = {
    "Disciplined": -0.10,  # Moves 10% of income from Wants to Savings
    "Splurge": 0.10,       # Moves 10% of income from Savings to Wants
    "Balanced": 0.0,       # No change
}

ANNUAL_RETURN_RATE = 0.07    # 7% assumed annual return on investments
ANNUAL_INFLATION_RATE = 0.06 # 6% assumed annual inflation rate

# --- CORE FUNCTIONS ---

def calculate_lifestyle_budget(income: float, fixed_commitments: float, lifestyle: str) -> dict:
    """Calculates a budget based on pre-defined lifestyle rules."""
    if income <= 0:
        return {"Necessities": 0, "Wants": 0, "Savings": 0, "Flex Necessities": 0}

    # Gracefully fall back to a default rule if an unknown lifestyle is provided.
    rules = LIFESTYLE_RULES.get(lifestyle, LIFESTYLE_RULES["Working Professional"])

    necessities_total = income * rules["necessities"]
    wants_total = income * rules["wants"]
    savings_total = income * rules["savings"]

    # Calculate what's left for flexible necessities after fixed costs.
    flex_necessities = necessities_total - fixed_commitments
    if flex_necessities < 0:
        flex_necessities = 0

    return {
        "Necessities": necessities_total,
        "Wants": wants_total,
        "Savings": savings_total,
        "Fixed Commitments": fixed_commitments,
        "Flex Necessities": flex_necessities,
    }

def generate_budget_plan(income: float, fixed_commitments: float, lifestyle: str, mood: str) -> dict:
    """
    Main orchestrator function to generate the final budget plan.
    It first gets the lifestyle budget, then applies the mood modifier.
    """
    # 1. Get the base budget for the user's lifestyle.
    budget = calculate_lifestyle_budget(income, fixed_commitments, lifestyle)

    # 2. Apply the mood-based adjustment.
    modifier = MOOD_MODIFIERS.get(mood, 0.0)
    shift_amount = income * modifier

    # 3. Reallocate funds between Wants and Savings.
    original_wants = budget["Wants"]
    original_savings = budget["Savings"]

    budget["Wants"] = original_wants + shift_amount
    budget["Savings"] = original_savings - shift_amount

    # 4. Add validation to prevent negative budget categories.
    if budget["Wants"] < 0:
        budget["Savings"] += budget["Wants"] # Shift the deficit from savings
        budget["Wants"] = 0
    if budget["Savings"] < 0:
        budget["Wants"] += budget["Savings"] # Shift the deficit from wants
        budget["Savings"] = 0

    return budget

def project_wealth_growth(monthly_savings: float, duration_months: int = 12) -> pd.DataFrame:
    """Projects wealth growth, calculating both nominal and real (inflation-adjusted) values."""
    if monthly_savings <= 0:
        return pd.DataFrame({
            'Month': range(1, duration_months + 1),
            'Nominal Growth': [0] * duration_months,
            'Real Growth': [0] * duration_months
        })

    monthly_return_rate = ANNUAL_RETURN_RATE / 12
    monthly_inflation_rate = ANNUAL_INFLATION_RATE / 12
    
    records = []
    current_wealth = 0

    for month in range(1, duration_months + 1):
        # Calculate compound growth for the month.
        current_wealth += monthly_savings
        interest = current_wealth * monthly_return_rate
        current_wealth += interest
        
        # Discount for inflation to find the "real" value in today's money.
        real_wealth = current_wealth / ((1 + monthly_inflation_rate) ** month)
        
        records.append({
            'Month': month,
            'Nominal Growth': round(current_wealth, 2),
            'Real Growth': round(real_wealth, 2)
        })

    return pd.DataFrame(records)

def calculate_financial_score(income: float, savings: float, necessities: float) -> dict:
    """Analyzes a budget to provide a financial fitness score and recommendations."""
    savings_rate = savings / income if income > 0 else 0

    # Grade the savings rate against common financial health benchmarks.
    if savings_rate >= 0.25:
        grade, emoji, comment = "A", "💪", "Excellent! Your savings rate is exceptional."
    elif savings_rate >= 0.20:
        grade, emoji, comment = "B", "👍", "Great job! You are on track with the recommended savings rate."
    elif savings_rate >= 0.15:
        grade, emoji, comment = "C", "🙂", "Good start! Aiming for 20% will accelerate your goals."
    elif savings_rate >= 0.10:
        grade, emoji, comment = "D", "👀", "There's room for improvement. Try reallocating from 'Wants'."
    else:
        grade, emoji, comment = "F", "💸", "Warning! Your current savings rate is critically low."

    # Calculate progress towards a 3-month emergency fund.
    emergency_fund_goal = necessities * 3
    # Progress is this month's contribution towards the total goal.
    progress = (savings / emergency_fund_goal) if emergency_fund_goal > 0 else 0
    
    return {
        "savings_rate": savings_rate,
        "grade": grade,
        "emoji": emoji,
        "comment": comment,
        "emergency_fund_progress": min(progress, 1.0) # Cap at 100%
    }

def generate_narrative_insights(lifestyle: str, score_details: dict, budget_plan: dict, income: float) -> str:
    """Generates a 2-3 sentence personalized financial summary using a rule-based engine."""
    savings_rate = score_details['savings_rate']
    grade = score_details['grade']
    wants_percentage = budget_plan['Wants'] / income if income > 0 else 0

    # Part 1: Opening sentence based on overall performance.
    if grade in ["A", "B"]:
        narrative = f"As a {lifestyle}, your financial discipline is impressive! A savings rate of {savings_rate:.1%} puts you in a strong position. "
    elif grade == "C":
        narrative = f"You're building a solid foundation as a {lifestyle}. Your savings rate of {savings_rate:.1%} is a good start. "
    else:
        narrative = f"As a {lifestyle}, your current budget needs attention. A savings rate of {savings_rate:.1%} is a critical area to improve. "

    # Part 2: Actionable advice tailored to the user's situation.
    if lifestyle == "Freelancer" and score_details['emergency_fund_progress'] < 1.0:
        narrative += "For freelancers, a robust emergency fund is key; prioritize building 3-6 months of savings."
    elif wants_percentage > 0.35:
        narrative += f"The quickest way to boost your savings is to review your 'Wants' (currently at {wants_percentage:.0%}) and reallocate funds to your goals."
    elif savings_rate < 0.20 and grade not in ["A", "B"]:
        shortfall = (income * 0.20) - budget_plan['Savings']
        narrative += f"Consider boosting your monthly savings by just ₹{shortfall:,.0f} to hit the recommended 20% target."
    else:
        narrative += "Keep up the consistent effort to see significant long-term growth."

    return narrative