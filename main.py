
from __future__ import annotations

import strawberry
from datetime import datetime
from enum import Enum
from uuid import UUID

@strawberry.type
class Project:
    name: str
    account: Account
    available_credits: str
    estimated_balance: str
    trial_expiration_time: datetime
    billing: BillingDetails
    default_cloud: str  # should probably be enum
    services: list[Service]
    tech_emails: list[Email]
    tenant_slug: str  # tenant_id, should probably be enum

@strawberry.type
class Account:
    id: UUID
    name: str

@strawberry.type
class Email:
    # for some reason, emails are wrapped in such a type.
    # Maybe it makes sense to keep the extensibility.
    email: str

@strawberry.type
class BillingDetails:
    id: UUID  # billing_group_id
    name: str  # billing_group_name
    company_name: str
    vat_id: str
    address: Address
    currency: Currency
    emails: list[Email]
    extra_text: str
    payment_method: str  # should probably be enum
    payment_card: PaymentCard

@strawberry.type
class Address:
    address_lines: list[str]
    city: str
    zip_code: str
    state: str
    country: str
    country_code: str

@strawberry.enum
class Currency(Enum):
    AUD = "AUD"
    CAD = "CAD"
    CHF = "CHF"
    DKK = "DKK"
    EUR = "EUR"
    GBP = "GBP"
    NOK = "NOK"
    SEK = "SEK"
    USD = "USD"

@strawberry.type
class PaymentCard:
    brand: str
    card_id: str
    country: str
    country_code: str
    exp_month: int
    exp_year: int
    last4: str
    name: str
    user_email: str

@strawberry.type
class Service:
    name: str
    project: Project
    # TODO rest of fields

@strawberry.type
class Query:
    project: Project # = strawberry.field(resolver=get_project)

schema = strawberry.Schema(query=Query)

