
import json
import os

from aiven.client.client import AivenClient
from aiven.client.envdefault import AIVEN_WEB_URL, AIVEN_CA_CERT, AIVEN_CONFIG_DIR
from pprint import pprint

from schema import Project, Account, BillingDetails, Address, PaymentCard

client = AivenClient(base_url=(AIVEN_WEB_URL or "https://api.aiven.io"))
client.set_ca(AIVEN_CA_CERT)
auth_token_file_path = (
    os.environ.get("AIVEN_CREDENTIALS_FILE") or
    os.path.join(AIVEN_CONFIG_DIR, "aiven-credentials.json")
)
auth_token = json.load(open(auth_token_file_path))["auth_token"]
client.set_auth_token(auth_token)

def get_project(name: str):
    p = client.get_project(name)
    pprint(p)
    return Project(
        name=name,
        account=Account(
            id=p['account_id'],
            name=p['account_name'],
        ),
        billing=BillingDetails(
            id=p['billing_group_id'],
            name=p['billing_group_name'],
            address=Address(
                address_lines=[p['billing_address']],
                city=p['city'],
                country=p['country'],
                country_code=p['country_code'],
                state=p['state'],
                zip_code=p['zip_code'],
            ),
            company_name=p['company'],
            currency=p['billing_currency'],
            emails=p['billing_emails'],
            extra_text=p['billing_extra_text'],
            payment_method=p['payment_method'],
            vat_id=p['vat_id'],
            payment_card=None,
            #payment_card=PaymentCard(p['card_info']),
        ),
        available_credits=p['available_credits'],
        estimated_balance=p['estimated_balance'],
        trial_expiration_time=p['trial_expiration_time'],
        default_cloud=p['default_cloud'],
        tech_emails=p['tech_emails'],
        services=[],
        tenant_slug=p['tenant_id'],
    )
