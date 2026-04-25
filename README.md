# Robinhood Stock Emailer

A GitHub Actions workflow that automatically emails you a pie chart snapshot of your Robinhood portfolio. It runs on a schedule (or on demand) and sends a chart + text summary directly to your inbox — no server required.

---

## What you get

Each email contains:

- A **donut pie chart** showing portfolio allocation by stock
- A **text summary** listing each position's value and percentage
- Positions that are less than 3% of your portfolio are grouped into "Other" to keep the chart clean

---

## Prerequisites

Before you set this up, make sure you have:

- A **Robinhood account** with stock holdings
- A **Gmail account** to send from (see the App Password note below)
- A **GitHub account** to fork and run the workflow

---

## Setup

### 1. Fork this repository

Click **Fork** in the top-right corner of this page to copy it to your own GitHub account.

### 2. Create a Gmail App Password

Gmail blocks regular password logins from scripts. You need to create an **App Password** instead:

1. Go to your [Google Account Security settings](https://myaccount.google.com/security)
2. Make sure **2-Step Verification** is turned on (required)
3. Search for **"App passwords"** and open it
4. Choose **Mail** as the app, then click **Generate**
5. Copy the 16-character password — you'll need it in the next step

> **Note:** If you don't see "App passwords", your account may be managed by a Google Workspace admin, or 2FA is not enabled.

### 3. Add GitHub Secrets

Your credentials are stored as encrypted GitHub Secrets so they're never visible in the code.

1. In your forked repo, go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret** for each of the following:

| Secret Name | What to put in it |
|---|---|
| `EMAIL_ADDRESS` | The Gmail address you're sending **from** (e.g. `you@gmail.com`) |
| `EMAIL_PASSWORD` | The **App Password** you generated in step 2 (not your regular Gmail password) |
| `RECIPIENT_EMAIL` | The email address to send the report **to** (can be the same as above) |
| `RH_USERNAME` | Your Robinhood login email |
| `RH_PASSWORD` | Your Robinhood password |

### 4. Enable the schedule (optional)

By default the workflow only runs when you push to `main` or trigger it manually. To run it automatically at market open and close, edit `.github/workflows/send-email.yml` and uncomment the `schedule` block:

```yaml
on:
  schedule:
    - cron: '0 13 * * 1-5'   # 9:00 AM ET (market open), Mon–Fri
    - cron: '0 20 * * 1-5'   # 4:00 PM ET (market close), Mon–Fri
  workflow_dispatch:
```

Commit and push the change — the schedule will activate automatically.

> **Tip:** Cron times in GitHub Actions use UTC. `13:00 UTC` = `9:00 AM ET` in summer (EDT). Adjust by 1 hour in winter (EST): `14:00 UTC` = `9:00 AM ET`.

### 5. Run it manually to test

1. Go to the **Actions** tab in your forked repo
2. Click **Send Robinhood Portfolio Email** in the left sidebar
3. Click **Run workflow → Run workflow**
4. Check your inbox — the email should arrive within a minute or two

---

## Customization

**Change the "Other" grouping threshold**

In `send_email.py`, the threshold for grouping small positions is set to 3%:

```python
threshold = 0.03 * total_value
```

Change `0.03` to any percentage you like (e.g. `0.05` for 5%).

**Change the email schedule**

Edit the `cron` expressions in `.github/workflows/send-email.yml`. Use [crontab.guru](https://crontab.guru) to build a custom schedule.

**Send to a different email provider**

The script uses Gmail's SMTP server. To use a different provider, update these lines in `send_email.py`:

```python
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
```

Replace `smtp.gmail.com` and `465` with your provider's SMTP host and port.

---

## Troubleshooting

**The workflow fails with an authentication error**
- Double-check that you used an App Password, not your regular Gmail password
- Make sure all 5 secrets are added and spelled exactly as shown in the table above

**I don't see "App passwords" in my Google account**
- Ensure 2-Step Verification is enabled — App Passwords require it
- If your account is managed by a school or employer, the admin may have disabled this feature

**The workflow ran but I didn't get an email**
- Check your spam/junk folder
- Verify `RECIPIENT_EMAIL` is set correctly in your secrets
- Look at the workflow run logs in the Actions tab for any Python errors

**Robinhood login fails**
- If your account has MFA (SMS or authenticator app) enabled, `robin_stocks` will prompt for the code interactively, which won't work in an automated workflow. You may need to disable MFA or pre-authorize the device.

---

## Dependencies

- [matplotlib](https://matplotlib.org/) — chart generation
- [robin_stocks](https://robin-stocks.readthedocs.io/) — Robinhood API client

---

## License

[MIT](LICENSE)
