# Mr. Krabs - Automatic Stirpe invoice reminder for Slack

## Screenshot
![Screenshot of the Slack message this script generates](screenshot.png)

## Configuration
Environment variable `KRABS` should be a dict (as a string) containing the following keys:
- `StripeKey` (Your Stripe API key)
- `StripeCustomer` (The Stripe ID of the Customer you wish to monitor)
- `SlackHook` (The Slack Webhook generated for this use)