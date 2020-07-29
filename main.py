import schedule, time, json, requests, stripe


def selfConfig():
    import os, sys

    if "KRABS" in os.environ:
        intermediateDict = json.loads(os.environ["KRABS"])
        global StripeKey, StripeCustomer, SlackHook
        StripeKey, StripeCustomer, SlackHook = (
            intermediateDict["StripeKey"],
            intermediateDict["StripeCustomer"],
            intermediateDict["SlackHook"],
        )
    else:
        sys.exit("Could not find KRABS envvar.")


class Krabs:
    def __init__(self, cusId, key):
        stripe.api_key = key
        self.CustomerID = cusId

    def getCustomerInfo(self):
        return stripe.Customer.retrieve(id=self.CustomerID)

    def getCusInvList(self):
        return stripe.Invoice.list(customer=self.CustomerID, status="open")["data"]

    def isPaid(Self):
        if stripe.Customer.retrieve(id=self.customerID)["amount_due"] != 0:
            return False
        else:
            return True


class Slack:
    def __init__(self, webhook):
        self.webhook = webhook

    def sendMessage(self, txt):
        requests.post(self.webhook, data="{'blocks': %s}" % txt)

    def generateMsgHeader(self, stripeCustomerObj):
        msgTemplate = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": f"Hello yes, I have detected unpaid invoices for {stripeCustomerObj['description']}:",
                },
            },
            {"type": "divider"},
        ]
        return msgTemplate

    def generateInvBlock(self, inv):
        templateDict = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f'*Invoice ID: {inv["number"]} *\n Due on {time.ctime(inv["due_date"])}',
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "View Invoice"},
                "url": inv["hosted_invoice_url"],
            },
        }
        return templateDict


def checkCusStatus(Krabs, Slack):
    if Krabs.isPaid != True:
        InvList = Krabs.getCusInvList()
        linkList = Slack.generateMsgHeader(Krabs.getCustomerInfo())
        for x in InvList:
            linkList.append(Slack.generateInvBlock(x))
        Slack.sendMessage(json.dumps(linkList))


if __name__ == "__main__":
    selfConfig()
    schedule.every(12).hours.do(
        checkCusStatus, Krabs(StripeCustomer, StripeKey), Slack(SlackHook)
    )

    while True:
        schedule.run_pending()
        time.sleep(5)
