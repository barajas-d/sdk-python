"""MercadoPago API resource classes.

Each class maps to a MercadoPago REST API domain (payments, orders,
customers, etc.) and exposes CRUD and action methods.  All resources
extend :class:`~mercadopago.core.mp_base.MPBase`.
"""
from mercadopago.config.request_options import RequestOptions
from mercadopago.http.http_client import HttpClient
from mercadopago.resources.advanced_payment import AdvancedPayment
from mercadopago.resources.card import Card
from mercadopago.resources.card_token import CardToken
from mercadopago.resources.chargeback import Chargeback
from mercadopago.resources.claims import Claims
from mercadopago.resources.customer import Customer
from mercadopago.resources.customer_address import CustomerAddress
from mercadopago.resources.disbursement_refund import DisbursementRefund
from mercadopago.resources.identification_type import IdentificationType
from mercadopago.resources.invoice import Invoice
from mercadopago.resources.invoices import Invoices
from mercadopago.resources.merchant_order import MerchantOrder
from mercadopago.resources.oauth import OAuth
from mercadopago.resources.order import Order
from mercadopago.resources.order_checkout_pro import (
    OrderCheckoutProConfig,
    OrderCheckoutProInstallments,
    OrderCheckoutProInterestFree,
    OrderCheckoutProOnlineConfig,
    OrderCheckoutProPaymentMethod,
    OrderCheckoutProTrack,
    OrderCheckoutProDict,
)
from mercadopago.resources.payment import Payment
from mercadopago.resources.payment_methods import PaymentMethods
from mercadopago.resources.payouts import Payouts
from mercadopago.resources.plan import Plan
from mercadopago.resources.point import Point
from mercadopago.resources.pos import POS
from mercadopago.resources.preapproval import PreApproval
from mercadopago.resources.preference import Preference
from mercadopago.resources.qr_integrator import QRIntegrator
from mercadopago.resources.qr_orders import QROrders
from mercadopago.resources.refund import Refund
from mercadopago.resources.releases_report import ReleasesReport
from mercadopago.resources.settlements_report import SettlementsReport
from mercadopago.resources.stores import Stores
from mercadopago.resources.subscription import Subscription
from mercadopago.resources.terminals import Terminals
from mercadopago.resources.user import User
from mercadopago.resources.wallet_connect import WalletConnect
from mercadopago.resources.chargebacks import Chargebacks


__all__ = (
    'AdvancedPayment',
    'Card',
    'CardToken',
    'Chargeback',
    'Chargebacks',
    'Claims',
    'Customer',
    'CustomerAddress',
    'DisbursementRefund',
    'HttpClient',
    'IdentificationType',
    'Invoice',
    'Invoices',
    'MerchantOrder',
    'OAuth',
    'Order',
    'OrderCheckoutProConfig',
    'OrderCheckoutProInstallments',
    'OrderCheckoutProInterestFree',
    'OrderCheckoutProOnlineConfig',
    'OrderCheckoutProPaymentMethod',
    'OrderCheckoutProTrack',
    'OrderCheckoutProDict',
    'Payment',
    'PaymentMethods',
    'Payouts',
    'Plan',
    'Point',
    'POS',
    'PreApproval',
    'Preference',
    'QRIntegrator',
    'QROrders',
    'Refund',
    'ReleasesReport',
    'SettlementsReport',
    'RequestOptions',
    'Stores',
    'Subscription',
    'Terminals',
    'User',
    'WalletConnect',
)
