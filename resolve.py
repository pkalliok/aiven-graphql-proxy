
import json
import os

from aiven.client.client import AivenClient
from aiven.client.envdefault import AIVEN_WEB_URL, AIVEN_CA_CERT, AIVEN_CONFIG_DIR
from pprint import pprint
from typing import Any

from schema import (Project, Account, BillingDetails, Address, PaymentCard, FeatureFlag,
    Cloud, Service, ServiceParameters, ServiceResources, ServiceType)

client = AivenClient(base_url=(AIVEN_WEB_URL or "https://api.aiven.io"))
client.set_ca(AIVEN_CA_CERT)
auth_token_file_path = (
    os.environ.get("AIVEN_CREDENTIALS_FILE") or
    os.path.join(AIVEN_CONFIG_DIR, "aiven-credentials.json")
)
auth_token = json.load(open(auth_token_file_path))["auth_token"]
client.set_auth_token(auth_token)

def get_projects_by_auth() -> list[Project]:
    projects = client.get_projects()
    return [convert_project_to_graphql(p) for p in projects]

def get_project_by_name(name: str) -> Project:
    p = client.get_project(name)
    pprint(p)
    return convert_project_to_graphql(p)

def convert_project_to_graphql(p: dict[str,Any]) -> Project:
    return Project(
        name=p['project_name'],
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
            payment_card=convert_card_to_graphql(p['card_info'])
        ),
        available_credits=p['available_credits'],
        estimated_balance=p['estimated_balance'],
        trial_expiration_time=p['trial_expiration_time'],
        default_cloud=p['default_cloud'],
        features=convert_features_to_graphql(p.get('features')),
        tech_emails=p['tech_emails'],
        tenant_slug=p['tenant_id'],
    )

def convert_card_to_graphql(card_info: dict[str,Any]) -> PaymentCard:
    if not card_info: return None
    return PaymentCard(
        brand=card_info['brand'],
        card_id=card_info['card_id'],
        country=card_info['country'],
        country_code=card_info['country_code'],
        exp_month=card_info['exp_month'],
        exp_year=card_info['exp_year'],
        last4=card_info['last4'],
        name=card_info['name'],
        user_email=card_info['user_email']
    )

def convert_features_to_graphql(features: dict[str,Any]) -> list[FeatureFlag]:
    if not features: return []
    return [FeatureFlag(name=k, enabled=v) for k, v in features.items()]

def list_services_by_project(project: str) -> list[Service]:
    services = client.get_services(project)
    return [convert_service_to_graphql({**s, "project_name": project}) for s in services]

def get_service_by_name(project: str, name: str) -> Service:
    s = client.get_service(project, name)
    pprint(s)
    return convert_service_to_graphql({**s, "project_name": project})

def convert_service_to_graphql(s):
    cloud = Cloud(
        slug = s.pop("cloud_name"),
        description = s.pop("cloud_description"),
    )
    resources = ServiceResources(
        backups = s.pop("backups"),
        components = s.pop("components"),
        databases = s.pop("databases", []),
        users = s.pop("users", []),
    )
    parameters = ServiceParameters(
        disk_space_mb = s.pop("disk_space_mb"),
        node_count = s.pop("node_count"),
        node_cpu_count = s.pop("node_cpu_count"),
        node_memory_mb = s.pop("node_memory_mb"),
    )
    stype = ServiceType(
        name = s.pop("service_type"),
        description = s.pop("service_type_description"),
    )
    features = convert_features_to_graphql({**s.pop("features"),
        "termination_protection": s.pop("termination_protection")})
    vpc = s.pop("project_vpc_id")
    integrations = s.pop("service_integrations")
    name = s.pop("service_name")
    notifications = s.pop("service_notifications")
    s.pop("acl", None)
    s.pop("connection_info", None)
    s.pop("connection_pools", None)
    s.pop("group_list", None)
    s.pop("service_uri_params", None)
    s.pop("topics", None)
    s.pop("user_config", None)

    return Service(**s,
        project_vpc=vpc,
        cloud=cloud,
        features=features,
        name=name,
        integrations=integrations,
        notifications=notifications,
        resources=resources,
        service_parameters=parameters,
        service_type=stype,
    )

