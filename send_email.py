import os
import smtplib
import matplotlib.pyplot as plt
from email.message import EmailMessage
from robin_stocks import robinhood as r

# Load credentials
EMAIL = os.environ["EMAIL_ADDRESS"]
PASSWORD = os.environ["EMAIL_PASSWORD"]
RECIPIENT = os.environ["RECIPIENT_EMAIL"]
RH_USERNAME = os.environ["RH_USERNAME"]
RH_PASSWORD = os.environ["RH_PASSWORD"]

# Log in to Robinhood
r.login(username=RH_USERNAME, password=RH_PASSWORD)

# Get stock positions
positions = r.account.build_holdings()
holdings = [(symbol, float(info['equity'])) for symbol, info in positions.items()]

# Sort by size, group small ones
holdings.sort(key=lambda x: x[1], reverse=True)
total_value = sum(v for _, v in holdings)
threshold = 0.03 * total_value

filtered = [(sym, val) for sym, val in holdings if val >= threshold]
other_total = sum(val for sym, val in holdings if val < threshold)
if other_total > 0:
    filtered.append(("Other", other_total))

# Prepare pie chart
labels = [sym for sym, _ in filtered]
sizes = [val for _, val in filtered]

fig, ax = plt.subplots(figsize=(6, 6))
wedges, _, autotexts = ax.pie(
    sizes, labels=None, autopct='%1.1f%%', startangle=140
)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)
ax.legend(wedges, labels, title="Stocks", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
plt.title("Your Robinhood Portfolio")
plt.tight_layout()
chart_path = "portfolio_pie_chart.png"
plt.savefig(chart_path)
plt.close()

# Build summary text
summary_lines = []
for symbol, value in filtered:
    pct = (value / total_value) * 100
    summary_lines.append(f"{symbol:<6}  ${value:,.2f} ({pct:.1f}%)")
summary_lines.append("-" * 30)
summary_lines.append(f"Total:  ${total_value:,.2f}")
summary_text = "\n".join(summary_lines)

# Create email
msg = EmailMessage()
msg["Subject"] = "📊 Your Robinhood Portfolio Snapshot"
msg["From"] = EMAIL
msg["To"] = RECIPIENT
msg.set_content(f"Here is your current Robinhood portfolio:\n\n{summary_text}")

# Attach chart
with open(chart_path, "rb") as f:
    msg.add_attachment(f.read(), maintype="image", subtype="png", filename="portfolio_pie_chart.png")

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, PASSWORD)
    smtp.send_message(msg)
