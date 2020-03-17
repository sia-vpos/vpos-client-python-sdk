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
        self.pan_alias_data = None


class AuthorizeResponse:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        self.authorization = None
        self.pan_alias_data= None


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
        self.pan_alias_data=None


class ThreeDSAuthorize2Response:
    def __init__(self):
        # Timestamp Result
        self.timestamp = None
        self.result = None
        self.pan_alias_data = None
        self.authorization = None


class Authorization:
    def __init__(self, authorizationXml):
        self.paymentType = get_tag_value(authorizationXml, TagConstants.getPaymentTypeTag())
        self.authorizationType = get_tag_value(authorizationXml, TagConstants.getAuthorizationTypeTag())
        self.transactionID = get_tag_value(authorizationXml, TagConstants.getTransactionIDTag())
        self.network = get_tag_value(authorizationXml, TagConstants.getNetworkTag())
        self.orderID = get_tag_value(authorizationXml, TagConstants.getOrderIDTag())
        self.transactionAmount = get_tag_value(authorizationXml, TagConstants.getTransactionAmountTag())
        self.authorizedAmount = get_tag_value(authorizationXml, TagConstants.getAuthorizedAmountTag())
        self.refundedAmount = get_tag_value(authorizationXml, TagConstants.getRefundedAmountTag())
        self.transactionResult = get_tag_value(authorizationXml, TagConstants.getTransactionResultTag())
        self.timestamp = get_tag_value(authorizationXml, TagConstants.getTimestampTag())
        self.authorizationNumber = get_tag_value(authorizationXml, TagConstants.getAuthorizationNumberTag())
        self.acquireBIN = get_tag_value(authorizationXml, TagConstants.getAcquirerBinTag())
        self.merchantID = get_tag_value(authorizationXml, TagConstants.getMerchantIdTag())
        self.transactionStatus = get_tag_value(authorizationXml, TagConstants.getTransactionStatusTag())
        self.responseCodeISO = get_tag_value(authorizationXml, TagConstants.getResponseCodeIsoTag())
        self.panTail = get_tag_value(authorizationXml, TagConstants.getPanTailTag())
        self.panExpiryDate = get_tag_value(authorizationXml, TagConstants.getPanExpiryDateTag())
        self.paymentTypePP = get_tag_value(authorizationXml, TagConstants.getPaymentTypePPTag())
        self.rRN = get_tag_value(authorizationXml, TagConstants.getRRNTag())
        self.cardType = get_tag_value(authorizationXml, TagConstants.getCardType())


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
        self.panAlias = get_tag_value(pan_alias_xml, TagConstants.getCreatePanAliasTag())
        self.panAliasRev = get_tag_value(pan_alias_xml, TagConstants.getPanAliasRevTag())
        self.panAliasExpDate = get_tag_value(pan_alias_xml, TagConstants.getPanExpiryDateTag())
        self.panAliasTail = get_tag_value(pan_alias_xml, TagConstants.getPanTailTag())


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
