import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🌟 Softer, easy-on-the-eyes color palette
midnight_blue = "#30597B"   # Soft Navy (Revenue & Net Profit)
warm_sand = "#D4A76A"       # Warm Sand (Expenses)
moss_green = "#6B8E23"      # Muted Green (Cash Flow)
deep_clay = "#A65A4D"       # Deep Clay (Operating Expenses)
soft_slate = "#666B6A"      # Soft Slate (General Labels & Heatmap)

# Apply a clean, minimalist Seaborn theme
sns.set_theme(style="white")

### 📈 1. Quarterly Revenue Breakdown (Bar Chart) ###
business_units = ["SaaS", "Hardware", "Services"]
quarterly_revenue = {
    "Q1 2025": [2.5, 1.1, 0.9],
    "Q2 2025": [2.8, 1.2, 1.0],
    "Q3 2025": [3.0, 1.3, 1.1],
    "Q4 2025": [3.2, 1.4, 1.2]
}

df_revenue = pd.DataFrame(quarterly_revenue, index=business_units).T

fig, ax = plt.subplots(figsize=(7, 4))
df_revenue.plot(kind="bar", stacked=False, ax=ax, color=[midnight_blue, warm_sand, moss_green])

ax.set_title("Quarterly Revenue Breakdown", fontsize=12, fontweight="bold", color=soft_slate)
ax.set_ylabel("Revenue ($M)", fontsize=10, color=soft_slate)
ax.set_xlabel("")
ax.tick_params(colors=soft_slate)

sns.despine()

# Direct labels on bars
for bar in ax.patches:
    height = bar.get_height()
    if height > 0:
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"${height:.1f}M",
                ha="center", va="bottom", fontsize=10, color="black")

plt.xticks(rotation=0, color=soft_slate)
plt.yticks(color=soft_slate)
plt.ylim(0, max(map(max, quarterly_revenue.values())) * 1.2)  # Adjusted Y-limit
plt.savefig("tufte_clean_revenue_breakdown.png", dpi=300, bbox_inches="tight")
plt.close()

### 💰 2. Expense Distribution (Bar Chart) ###
expense_categories = ["Marketing", "Salaries", "R&D", "General & Admin"]
expense_values = [900, 1550, 620, 850]  # In thousand dollars

df_expenses = pd.DataFrame({"Category": expense_categories, "Amount ($K)": expense_values})

fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(x="Amount ($K)", y="Category", data=df_expenses, color=warm_sand)

ax.set_title("Expense Distribution", fontsize=12, fontweight="bold", color=soft_slate)
ax.set_xlabel("")
ax.set_ylabel("")

sns.despine()

for bar in ax.patches:
    width = bar.get_width()
    ax.text(width + 50, bar.get_y() + bar.get_height()/2, f"${width:.0f}K",
            ha="left", va="center", fontsize=10, color="black")

plt.xticks(color=soft_slate)
plt.yticks(color=soft_slate)
plt.xlim(0, max(expense_values) * 1.2)  # Adjusted X-limit
plt.savefig("tufte_clean_expense_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

### 📊 3. Financial Trends (Line Chart) ###
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
net_profit = [500, 520, 580, 600, 640, 660]  # In thousand dollars
cash_flow = [900, 950, 1000, 1100, 1200, 1300]
operating_expenses = [3000, 3100, 3200, 3300, 3400, 3550]

df_trends = pd.DataFrame({
    "Month": months * 3,
    "Value ($K)": net_profit + cash_flow + operating_expenses,
    "Metric": ["Net Profit"] * 6 + ["Cash Flow"] * 6 + ["Operating Expenses"] * 6
})

plt.figure(figsize=(7, 4))
sns.lineplot(x="Month", y="Value ($K)", hue="Metric", data=df_trends, marker="o", 
             palette=[midnight_blue, moss_green, deep_clay])

plt.title("Financial Trends", fontsize=12, fontweight="bold", color=soft_slate)
sns.despine()

plt.xticks(rotation=30, ha="right", color=soft_slate)
plt.yticks(color=soft_slate)
plt.ylim(0, max(df_trends["Value ($K)"]) * 1.2)  # Adjusted Y-limit
plt.savefig("tufte_clean_financial_trends.png", dpi=300, bbox_inches="tight")
plt.close()

### 🔥 4. Financial Heatmap ###
quarters = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"]
financial_data = {
    "Revenue ($M)": [15.2, 16.0, 16.8, 17.5],
    "Operating Expenses ($M)": [10.8, 11.4, 11.9, 12.5],
    "Net Profit ($M)": [4.4, 4.6, 4.9, 5.0]
}

df_heatmap = pd.DataFrame(financial_data, index=quarters)

plt.figure(figsize=(7, 4))
sns.heatmap(df_heatmap, annot=True, cmap="Greens", linewidths=0.1, fmt=".1f", cbar=False)

plt.title("Quarterly Financial Performance", fontsize=12, fontweight="bold", color=soft_slate)
sns.despine()

plt.xticks(color=soft_slate)
plt.yticks(color=soft_slate)
plt.savefig("tufte_clean_financial_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()

### 📈 5. Forecast Trends (Bar Chart) ###
revenue_forecast = [16.2, 17.0, 18.1, 19.0]  # In million dollars
expense_forecast = [11.0, 11.5, 12.2, 12.8]  # In million dollars

df_forecast = pd.DataFrame({
    "Quarter": quarters * 2,
    "Amount ($M)": revenue_forecast + expense_forecast,
    "Type": ["Revenue"] * 4 + ["Expenses"] * 4
})

fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(x="Quarter", y="Amount ($M)", hue="Type", data=df_forecast, 
            palette=[midnight_blue, warm_sand], width=0.6)

ax.set_title("Projected Revenue & Expense Trends", fontsize=12, fontweight="bold", color=soft_slate)
ax.set_xlabel("")
ax.set_ylabel("")

sns.despine()

for bar in ax.patches:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.3, f"${height:.1f}M",
            ha="center", va="bottom", fontsize=10, color="black")

plt.xticks(color=soft_slate)
plt.yticks(color=soft_slate)
plt.ylim(0, max(revenue_forecast + expense_forecast) * 1.2)  # Adjusted Y-limit
plt.savefig("tufte_clean_forecast_trends.png", dpi=300, bbox_inches="tight")
plt.close()

print("✅ All FP&A charts generated successfully with corrected labels!")

