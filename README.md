# 🧭 Core Flow Financial Navigator

**A personalized, interactive budgeting application that acts as a mini-financial advisor, helping users understand the real-world impact of their financial habits.**

---

### ✨ [**View the Live Application Here!**](https://coreflow-app-financial-navigator.streamlit.app/) ✨

---

### [**Core Flow Dashboard**](https://github.com/Ananyagupta1812/CoreFlow/blob/main/assests/dashboard.png)


## 📖 Introduction

Traditional budgeting apps are often static and uninspiring. They tell you *what* you spent, but they fail to show you the *why* behind your habits or the *future consequences* of your choices. 

The **Core Flow Financial Navigator** is a fintech prototype built to solve this problem. It's a dynamic, BI-style dashboard that combines a rule-based budgeting engine with principles of behavioral finance to provide users with a truly personalized and insightful financial planning experience.

This application doesn't just create a budget; it tells a story about your financial health and future potential.

## 🚀 Key Features

The application is built around a powerful set of features designed to be both functional and engaging:

#### 🧠 **Core Logic & Personalization**
*   **Lifestyle-Aware Templates:** Budgeting rules are automatically adjusted for different lifestyles (`Student`, `Working Professional`, `Freelancer`, `Homemaker`).
*   **Mood-Based Simulation:** Users can select a financial mood (`Disciplined`, `Splurge`, `Balanced`) to see in real-time how their attitude affects their budget and future wealth.
*   **Narrative Insights:** Auto-generates a personalized 2-3 sentence summary of the user's financial health, acting like a mini-advisor.

#### 📊 **Interactive Dashboard & Visualizations**
*   **Dynamic Budget Allocation:** A clean, interactive donut chart visualizes the breakdown of necessities, wants, and savings.
*   **Wealth Growth Projection:** A 12-month line graph forecasts the growth of savings, complete with an **inflation-adjusted "real value"** view.
*   **Gamified Scorecard:** Grades the user's financial fitness from A to F with emoji badges and provides a progress bar for their emergency fund.

#### 🔮 **"What-If?" Scenario Planning**
*   **Consequence Simulation:** Instantly shows the "Future Savings Lost" or "Extra Wealth Gained" over 12 months based on the selected mood.
*   **Interactive Sliders:** Allows users to see the long-term trade-offs of adjusting their savings or cutting back on wants.
*   **Splurge Simulator:** A powerful tool that calculates the 5-year opportunity cost of a recurring monthly splurge, demonstrating the power of compound interest.

## 🛠️ Tech Stack

This project was built using a modern, efficient data science and web development stack:

*   **Backend & Logic:** Python, Pandas
*   **Frontend & Dashboard:** Streamlit
*   **Data Visualization:** Plotly Express
*   **Deployment:** Streamlit Community Cloud

## 🏃‍♀️ Running the Project Locally

To run this application on your local machine, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ananyagupta1812/CoreFlow.git
    cd CoreFlow
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your default web browser.

## 📂 Project Structure

The project is organized with a clear separation of concerns:

```
├── app.py              # Main Streamlit frontend application
├── requirements.txt    # Project dependencies
├── .gitignore          # Files to be ignored by Git
└── engine/
    └── budget.py       # All backend calculation logic and functions
```

This structure ensures that the user interface logic (`app.py`) is decoupled from the business logic (`budget.py`), making the codebase clean and maintainable.
