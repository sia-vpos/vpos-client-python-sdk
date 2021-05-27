from VPOSClient.utils import TagConstants
from VPOSClient.utils.Utils import get_tag_value


class OrderStatusResponse:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        # Header
        self.shop_id = None
        self.order_id = None
        self.req_ref_num = None
        self.auth_list = []
        self.card_holder_info = None
        self.pan_alias_data = None


class AuthorizeResponse:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        self.authorization = None
        self.pan_alias_data = None


class OperationResponse:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        self.operation = None


class ThreeDSAuthorize0Response:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        self.three_DS_Method = None
        self.three_DS_Challenge = None
        self.authorization = None
        self.pan_alias_data = None


class ThreeDSAuthorize1Response:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        self.three_DS_Challenge = None
        self.authorization = None
        self.pan_alias_data = None


class ThreeDSAuthorize2Response:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        self.pan_alias_data = None
        self.authorization = None


class Authorization:
    def __init__(self, authorization_xml):
        self.payment_type = get_tag_value(authorization_xml, TagConstants.getPaymentTypeTag())
        self.authorization_type = get_tag_value(authorization_xml, TagConstants.getAuthorizationTypeTag())
        self.transaction_ID = get_tag_value(authorization_xml, TagConstants.getTransactionIDTag())
        self.network = get_tag_value(authorization_xml, TagConstants.getNetworkTag())
        self.order_ID = get_tag_value(authorization_xml, TagConstants.getOrderIDTag())
        self.transaction_amount = get_tag_value(authorization_xml, TagConstants.getTransactionAmountTag())
        self.authorized_amount = get_tag_value(authorization_xml, TagConstants.getAuthorizedAmountTag())
        self.refunded_amount = get_tag_value(authorization_xml, TagConstants.getRefundedAmountTag())
        self.transaction_result = get_tag_value(authorization_xml, TagConstants.getTransactionResultTag())
        self.timestamp = get_tag_value(authorization_xml, TagConstants.getTimestampTag())
        self.authorization_number = get_tag_value(authorization_xml, TagConstants.getAuthorizationNumberTag())
        self.acquire_BIN = get_tag_value(authorization_xml, TagConstants.getAcquirerBinTag())
        self.merchant_ID = get_tag_value(authorization_xml, TagConstants.getMerchantIdTag())
        self.transaction_status = get_tag_value(authorization_xml, TagConstants.getTransactionStatusTag())
        self.response_code_ISO = get_tag_value(authorization_xml, TagConstants.getResponseCodeIsoTag())
        self.pan_tail = get_tag_value(authorization_xml, TagConstants.getPanTailTag())
        self.pan_expiry_date = get_tag_value(authorization_xml, TagConstants.getPanExpiryDateTag())
        self.payment_type_PP = get_tag_value(authorization_xml, TagConstants.getPaymentTypePPTag())
        self.rRN = get_tag_value(authorization_xml, TagConstants.getRRNTag())
        self.card_type = get_tag_value(authorization_xml, TagConstants.getCardType())
        self.card_holder_info = get_tag_value(authorization_xml, TagConstants.getCardHolderInfoTag())
        self.installments_number = get_tag_value(authorization_xml, TagConstants.getInstallmentsNumberTag())
        self.tickler_merchant_code = get_tag_value(authorization_xml, TagConstants.getTicklerMerchantCodeTag())
        self.tickler_plan_code = get_tag_value(authorization_xml, TagConstants.getTicklerPlanCodeTag())
        self.tickler_subscription_code = get_tag_value(authorization_xml, TagConstants.getTicklerSubscriptionCodeTag())

class CardHolderData:
    def __init__(self, card_holder_info_xml):
        self.card_holder_name = get_tag_value(card_holder_info_xml, TagConstants.getCardHolderNameTag())
        self.card_holder_email = get_tag_value(card_holder_info_xml, TagConstants.getCardHolderEmailTag())
        self.billing_address_postal_code = get_tag_value(card_holder_info_xml, TagConstants.getBillingAddressPostalcodeTag())
        self.billing_address_city = get_tag_value(card_holder_info_xml, TagConstants.getBillingAddressCityTag())
        self.billing_address_line_1 = get_tag_value(card_holder_info_xml, TagConstants.getBillingAddressLine1Tag())
        self.billing_address_line_2 = get_tag_value(card_holder_info_xml, TagConstants.getBillingAddressLine2Tag())
        self.billing_address_line_3 = get_tag_value(card_holder_info_xml, TagConstants.getBillingAddressLine3Tag())
        self.billing_address_state = get_tag_value(card_holder_info_xml, TagConstants.getBillingAddressStateTag())
        self.billing_address_country = get_tag_value(card_holder_info_xml, TagConstants.getBillingAddressCountryTag())

class ThreeDSMethod:
    def __init__(self, three_ds_method_xml):
        self.three_ds_mtd_url = get_tag_value(three_ds_method_xml, TagConstants.getThreeDSMtdUrlTag())
        self.three_ds_method_data = get_tag_value(three_ds_method_xml, TagConstants.getThreeDSMtdDataTag())
        self.three_ds_tran_id = get_tag_value(three_ds_method_xml, TagConstants.getThreeDSTransactionIDTag())


class ThreeDSChallenge:
    def __init__(self, three_ds_challenge):
        self.acs_url = get_tag_value(three_ds_challenge, TagConstants.getACSUrlTag())
        self.creq = get_tag_value(three_ds_challenge, TagConstants.getCreqTag())
        self.three_ds_tran_id = get_tag_value(three_ds_challenge, TagConstants.getThreeDSTransactionIDTag())


class PanAliasData:
    def __init__(self, pan_alias_xml):
        self.pan_alias = get_tag_value(pan_alias_xml, TagConstants.getCreatePanAliasTag())
        self.pan_alias_rev = get_tag_value(pan_alias_xml, TagConstants.getPanAliasRevTag())
        self.pan_alias_exp_date = get_tag_value(pan_alias_xml, TagConstants.getPanExpiryDateTag())
        self.pan_alias_tail = get_tag_value(pan_alias_xml, TagConstants.getPanTailTag())


class Operation:
    def __init__(self, operation_xml):
        self.transaction_id = get_tag_value(operation_xml, TagConstants.getTransactionIDTag())
        self.timestamp_req = get_tag_value(operation_xml, TagConstants.getTimestampReqTag())
        self.timestamp_elab = get_tag_value(operation_xml, TagConstants.getTimestampElabTag())
        self.src_type = get_tag_value(operation_xml, TagConstants.getSrcTypeTag())
        self.amount = get_tag_value(operation_xml, TagConstants.getAmountTag())
        self.result = get_tag_value(operation_xml, TagConstants.getResultTag())
        self.status = get_tag_value(operation_xml, TagConstants.getStatusTag())
        self.op_descr = get_tag_value(operation_xml, TagConstants.getOpDescrTag())
        self.operation = get_tag_value(operation_xml, TagConstants.getOperationTag())
        auth = operation_xml.find(TagConstants.getAuthorizationTag())
        if auth is not None:
            self.authorization = Authorization(auth)
