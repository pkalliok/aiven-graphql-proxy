
from __future__ import annotations

import strawberry
from datetime import datetime, time
from enum import Enum
from typing import Optional
from uuid import UUID

@strawberry.type
class Project:
    name: str
    account: Account
    available_credits: str
    estimated_balance: str
    trial_expiration_time: datetime
    billing: BillingDetails
    features: list[FeatureFlag]
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
    payment_card: Optional[PaymentCard]

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
    cloud: Cloud
    # connection_info: Union[PgConnection,...] # including service_uri_params
    create_time: datetime
    features: list[FeatureFlag] # including termination_protection
    maintenance: MaintenanceInfo
    metadata: list[MetadataItem]
    node_states: list[Node]
    plan: str # should be enum
    project_vpc: str
    integrations: list[ServiceIntegration]
    notifications: list[UserNotification]
    resources: ServiceResources
    service_parameters: ServiceParameters
    service_type: ServiceType # service_type, service_type_description
    service_uri: str
    state: ServiceState # should be enum
    update_time: datetime
    # user_config: Union[PgUserConfig,...]
    name: str # service_name
    project: Project

@strawberry.enum
class ServiceState(Enum):
    POWEROFF = "POWEROFF"
    RUNNING = "RUNNING"
    REBUILDING = "REBUILDING"
    REBALANCING = "REBALANCING"

@strawberry.type
class Backup:
    backup_name: str
    backup_time: datetime
    data_size: int

@strawberry.type
class Cloud:
    slug: str # cloud_name, should be enum
    description: str

@strawberry.type
class FeatureFlag:
    name: str
    enabled: bool

@strawberry.type
class MaintenanceInfo:
    day_of_week: DayOfWeek # dow
    time_of_day: time # time
    updates: list[MaintenanceUpdate]

@strawberry.enum
class DayOfWeek(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    NEVER = "never"

@strawberry.type
class MaintenanceUpdate:
    deadline: Optional[datetime]
    description: str
    start_after: Optional[datetime]
    start_at: Optional[datetime]

@strawberry.type
class MetadataItem:
    name: str
    value: str

@strawberry.type
class Node:
    name: str
    # progress_updates: list[str]
    role: NodeRole
    state: NodeState

@strawberry.enum
class NodeRole(Enum):
    MASTER = "master"
    STANDBY = "standby"
    READ_REPLICA = "read-replica"

@strawberry.enum
class NodeState(Enum):
    SETTING_UP_VM = "setting_up_vm"
    SYNCING_DATA = "syncing_data"
    RUNNING = "running"
    LEAVING = "leaving"
    UNKNOWN = "unknown"

@strawberry.type
class ServiceComponent:
    name: str
    host: str
    path: Optional[str]
    port: int
    route: RouteType
    ssl: Optional[bool]
    usage: UsageRole

@strawberry.enum
class RouteType(Enum):
    DYNAMIC = "dynamic"
    PUBLIC = "public"
    PRIVATE = "private"
    PRIVATELINK = "privatelink"

@strawberry.enum
class UsageRole(Enum):
    PRIMARY = "primary"
    REPLICA = "replica"

@strawberry.type
class ServiceIntegration:
    id: UUID
    active: bool
    description: str
    destination: ServiceIntegrationTarget
    enabled: bool
    # status: IntegrationStatus # TODO
    integration_type: str # should be enum
    source: ServiceIntegrationTarget
    # user_config: Union[...]

@strawberry.type
class ServiceIntegrationTarget:
    endpoint: Optional[IntegrationEndpoint]
    project: Optional[Project]
    service: Optional[Service]

@strawberry.type
class IntegrationEndpoint:
    name: str
    id: UUID

@strawberry.type
class UserNotification:
    notification_type: NotificationType
    level: NotificationLevel
    message: str
    help_article_url: Optional[str] # end_of_life_help_article_url
    end_of_life_time: Optional[datetime]

@strawberry.enum
class NotificationLevel(Enum):
    NOTICE = "notice"
    WARNING = "warning"

@strawberry.enum
class NotificationType(Enum):
    END_OF_LIFE = "end_of_life"
    POWERED_OFF_REMOVAL = "powered_off_removal"

@strawberry.type
class ServiceResources:
    # acls: list[ServiceACLRule]
    backups: list[Backup]
    components: list[ServiceComponent]
    # connection_pools: list[ConnectionPool]
    databases: list[str]
    users: list[ServiceUser]

@strawberry.type
class ServiceParameters:
    disk_space_mb: int
    node_count: int
    node_cpu_count: int
    node_memory_mb: int

@strawberry.type
class ServiceType:
    name: str # should be enum
    description: str

@strawberry.type
class ServiceUser:
    password: str
    user_type: str # type, should be enum
    username: str

@strawberry.type
class Query:
    @strawberry.field
    def project(name: str) -> Project:
        from resolve import get_project_by_name
        return get_project_by_name(name)
    @strawberry.field
    def service(project: str, name: str) -> Service:
        from resolve import get_service_by_name
        return get_service_by_name(project, name)

schema = strawberry.Schema(query=Query)

