import xml.etree.ElementTree as ET
from collections import OrderedDict

from VPOSClient.utils import Constants, AES
from VPOSClient.utils import Encoder
from VPOSClient.utils import TagConstants
from VPOSClient.utils import Utils


class Request:
    def __init__(self, shop_id, operator_id, options=None):
        self._timestamp = Utils.getTimestamp()
        self._shop_id = shop_id
        self._operator_id = operator_id
        self._options = options
        self._reqRefNum = Utils.genReqRefNum()

    def get_request_base_xml(self, operation, operation_Tag):
        requestDict = OrderedDict()
        requestDict[TagConstants.getReleaseTag()] = Constants.getRelease()
        requestDict[TagConstants.getRequestTag()] = ""
        requestDict[TagConstants.getDataTag()] = ""
        request = Utils.dict_to_xml(TagConstants.getBPWXmlRequestTag(), requestDict)
        # Request <Request>
        Utils.addChild(request.find(TagConstants.getRequestTag()), TagConstants.getOperationTag(), operation)
        Utils.addChild(request.find(TagConstants.getRequestTag()), TagConstants.getTimestampTag(), self._timestamp)
        mac = Utils.addChild(request.find(TagConstants.getRequestTag()), TagConstants.getMACTag(), None)
        # Data <Data>
        operation = Utils.addChild(request.find(TagConstants.getDataTag()), operation_Tag, None)
        # OrderStatus
        header = Utils.addChild(operation, TagConstants.getHeaderTag(), None)
        # Header
        Utils.addChild(header, TagConstants.getShopIDTag(), self._shop_id)
        Utils.addChild(header, TagConstants.getOperatorIDTag(), self._operator_id)
        Utils.addChild(header, TagConstants.getReqRefNumTag(), self._reqRefNum)
        return request


class RefundRequestXml(Request):
    def __init__(self, refundRequestDto, shop_id):
        super().__init__(shop_id, refundRequestDto.operator_id, refundRequestDto.options)
        self._operation = 'REFUND'
        self._transaction_id = refundRequestDto.transaction_id
        self._order_id = refundRequestDto.order_id
        self._amount = refundRequestDto.amount
        self._currency = refundRequestDto.currency
        self._exponent = refundRequestDto.exponent
        self._op_descr = refundRequestDto.op_descr

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getRefundRequestTag())
        refundRequest = request.find(TagConstants.getDataTag()).find(TagConstants.getRefundRequestTag())
        Utils.addChild(refundRequest, TagConstants.getTransactionIDTag(), self._transaction_id)
        Utils.addChild(refundRequest, TagConstants.getOrderIDTag(), self._order_id)
        Utils.addChild(refundRequest, TagConstants.getAmountTag(), self._amount)
        Utils.addChild(refundRequest, TagConstants.getCurrencyTag(), self._currency)
        if self._exponent is not None:
            Utils.addChild(refundRequest, TagConstants.getExponentTag(), self._exponent)
        if self._op_descr is not None:
            Utils.addChild(refundRequest, TagConstants.getOpDescrTag(), self._op_descr)
        if self._options is not None:
            Utils.addChild(refundRequest, TagConstants.getOptionsTag(), self._options)
        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.get_mac(self._string_for_mac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _string_for_mac(self):
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getTransactionIdName(), self._transaction_id)
        macString = Utils.appendField(macString, Constants.getOrderIdName(), self._order_id)
        macString = Utils.appendField(macString, Constants.getAmountName(), self._amount)
        macString = Utils.appendField(macString, Constants.getCurrencyName(), self._currency)
        macString = Utils.appendField(macString, Constants.getExponentName(), self._exponent)
        macString = Utils.appendField(macString, Constants.getOpDescrName(), self._op_descr)
        macString = Utils.appendField(macString, Constants.getOptionsName(), self._options)
        return macString


class OrderStatusRequestXml(Request):
    def __init__(self, order_status_request, shop_id):
        super().__init__(shop_id, order_status_request.operator_id, order_status_request.options)
        self._operation = 'ORDERSTATUS'
        self._order_id = order_status_request.order_id
        self._product_ref = order_status_request.product_ref

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getOrderStatusTag())
        # set order_id <order_id>
        orderStatus = request.find(TagConstants.getDataTag()).find(TagConstants.getOrderStatusTag())
        Utils.addChild(orderStatus, TagConstants.getOrderIDTag(), self._order_id)
        # set optional field if present
        if self._product_ref is not None:
            Utils.addChild(orderStatus, TagConstants.getProductRefTag(), self._product_ref)
        if self._options is not None:
            Utils.addChild(orderStatus, TagConstants.getOptionsTag(), self._options)

        # Calculate and set Mac
        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.get_mac(self._string_for_mac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _string_for_mac(self):
        macString = str()
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getOrderIdName(), self._order_id)
        macString = Utils.appendField(macString, Constants.getOptionsName(), self._options)
        macString = Utils.appendField(macString, Constants.getProductRefName(), self._product_ref)
        return macString


class CaptureRequestXml(Request):
    def __init__(self, confirmTransactionRequestDto, shop_id):
        super().__init__(shop_id, confirmTransactionRequestDto.operator_id, confirmTransactionRequestDto.options)
        self._transaction_id = confirmTransactionRequestDto.transaction_id
        self._amount = confirmTransactionRequestDto.amount
        self._currency = confirmTransactionRequestDto.currency
        self._exponent = confirmTransactionRequestDto.exponent
        self._order_id = confirmTransactionRequestDto.order_id
        self._op_descr = confirmTransactionRequestDto.op_descr
        self._operation = 'ACCOUNTING'

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getConfirmRequestTag())
        confirmRequest = request.find(TagConstants.getDataTag()).find(TagConstants.getConfirmRequestTag())
        if self._options is not None:
            Utils.addChild(confirmRequest, TagConstants.getOptionsTag(), self._options)
        Utils.addChild(confirmRequest, TagConstants.getTransactionIDTag(), self._transaction_id)
        Utils.addChild(confirmRequest, TagConstants.getOrderIDTag(), self._order_id)
        Utils.addChild(confirmRequest, TagConstants.getAmountTag(), self._amount)
        Utils.addChild(confirmRequest, TagConstants.getCurrencyTag(), self._currency)

        if self._exponent is not None:
            Utils.addChild(confirmRequest, TagConstants.getExponentTag(), self._exponent)
        if self._op_descr is not None:
            Utils.addChild(confirmRequest, TagConstants.getOpDescrTag(), self._op_descr)
        if self._options is not None:
            Utils.addChild(confirmRequest, TagConstants.getOptionsTag(), self._options)

        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.get_mac(self._string_for_mac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _string_for_mac(self):
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getTransactionIdName(), self._transaction_id)
        macString = Utils.appendField(macString, Constants.getOrderIdName(), self._order_id)
        macString = Utils.appendField(macString, Constants.getAmountName(), self._amount)
        macString = Utils.appendField(macString, Constants.getCurrencyName(), self._currency)
        macString = Utils.appendField(macString, Constants.getExponentName(), self._exponent)
        macString = Utils.appendField(macString, Constants.getOpDescrName(), self._op_descr)
        macString = Utils.appendField(macString, Constants.getOptionsName(), self._options)
        return macString


class ThreeDSAuthorization0RequestXML(Request):
    def __init__(self, threeDS0_request, shop_id):
        super().__init__(shop_id, threeDS0_request.operator_id, threeDS0_request.options)
        self._operation = 'THREEDSAUTHORIZATION0'
        self._order_id = threeDS0_request.order_id
        self._pan = threeDS0_request.pan
        self._exp_date = threeDS0_request.exp_date
        self._network = threeDS0_request.network
        self._amount = threeDS0_request.amount
        self._currency = threeDS0_request.currency
        self._exponent = threeDS0_request.exponent
        self._accounting_mode = threeDS0_request.accounting_mode
        self._cvv2 = threeDS0_request.cvv2
        self._email_ch = threeDS0_request.email_ch
        self._name_ch = threeDS0_request.name_ch
        self._user_id = threeDS0_request.user_id
        self._acquirer = threeDS0_request.acquirer
        self._ip_address = threeDS0_request.ip_address
        self._usr_auth_flag = threeDS0_request.usr_auth_flag
        self._op_descr = threeDS0_request.op_descr
        self._anti_fraud = threeDS0_request.anti_fraud
        self._product_ref = threeDS0_request.product_ref
        self._name = threeDS0_request.name
        self._surname = threeDS0_request.surname
        self._tax_id = threeDS0_request.tax_id
        self._create_pan_alias = threeDS0_request.create_pan_alias
        self._three_ds_data = threeDS0_request.three_ds_data.toJson()
        self._notify_url = threeDS0_request.notify_url
        self._c_prof = threeDS0_request.c_prof
        self._three_ds_mtd_notify_url = threeDS0_request.three_ds_mtd_notify_url
        self._challenge_win_size = threeDS0_request.challenge_win_size
        self._merchant_key = threeDS0_request.merchant_key

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getThreeDSAuthorizationRequest0Tag())
        authorization3DS = request.find(TagConstants.getDataTag()).find(
            TagConstants.getThreeDSAuthorizationRequest0Tag())

        Utils.addChild(authorization3DS, TagConstants.getOrderIDTag(), self._order_id)
        Utils.addChild(authorization3DS, TagConstants.getPanTag(), self._pan)
        Utils.addChild(authorization3DS, TagConstants.getExpDateTag(), self._exp_date)
        Utils.addChild(authorization3DS, TagConstants.getAmountTag(), self._amount)
        Utils.addChild(authorization3DS, TagConstants.getCurrencyTag(), self._currency)
        Utils.addOptionalChild(authorization3DS, TagConstants.getExponentTag(), self._exponent)
        Utils.addChild(authorization3DS, TagConstants.getAccountingModeTag(), self._accounting_mode)
        Utils.addChild(authorization3DS, TagConstants.getNetworkTag(), self._network)

        # OPTIONAL CHILD
        Utils.addOptionalChild(authorization3DS, TagConstants.getCVV2Tag(), self._cvv2)
        Utils.addOptionalChild(authorization3DS, TagConstants.getEmailCHTag(), self._email_ch)
        Utils.addOptionalChild(authorization3DS, TagConstants.getNameCHTag(), self._name_ch)

        Utils.addOptionalChild(authorization3DS, TagConstants.getUseridTag(), self._user_id)
        Utils.addOptionalChild(authorization3DS, TagConstants.getAcquirerTag(), self._acquirer)
        Utils.addOptionalChild(authorization3DS, TagConstants.getIpAddressTag(), self._ip_address)
        Utils.addOptionalChild(authorization3DS, TagConstants.getUserAuthFlagTag(), self._usr_auth_flag)

        Utils.addOptionalChild(authorization3DS, TagConstants.getOpDescrTag(), self._op_descr)
        Utils.addOptionalChild(authorization3DS, TagConstants.getOptionsTag(), self._options)
        Utils.addOptionalChild(authorization3DS, TagConstants.getAntiFraudTag(), self._anti_fraud)
        Utils.addOptionalChild(authorization3DS, TagConstants.getProductRefTag(), self._product_ref)
        Utils.addOptionalChild(authorization3DS, TagConstants.getNameTag(), self._name)
        Utils.addOptionalChild(authorization3DS, TagConstants.getSurnameTag(), self._surname)

        Utils.addOptionalChild(authorization3DS, TagConstants.getTaxIDTag(), self._tax_id)
        Utils.addOptionalChild(authorization3DS, TagConstants.getCreatePanAliasTag(), self._create_pan_alias)
        Utils.addOptionalChild(authorization3DS, TagConstants.getThreeDSDataTag(),
                               Utils.parse_url(AES.AES_encrypt(self._three_ds_data, api_result_key)))
        Utils.addOptionalChild(authorization3DS, TagConstants.getNotifUrLTag(), self._notify_url)
        Utils.addOptionalChild(authorization3DS, TagConstants.getCprofTag(), self._c_prof)
        Utils.addOptionalChild(authorization3DS, TagConstants.getThreeDSMtdNotifUrl(), self._three_ds_mtd_notify_url)
        Utils.addOptionalChild(authorization3DS, TagConstants.getChallengeWinSizeTag(), self._challenge_win_size)

        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.get_mac(self._string_for_mac(api_result_key), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _string_for_mac(self, api_result_key):
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOrderIdName(), self._order_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getPanName(), self._pan)
        macString = Utils.appendField(macString, Constants.getCvv2Name(), self._cvv2)
        macString = Utils.appendField(macString, Constants.getExpDateName(), self._exp_date)

        macString = Utils.appendField(macString, Constants.getAmountName(), self._amount)
        macString = Utils.appendField(macString, Constants.getCurrencyName(), self._currency)
        macString = Utils.appendField(macString, Constants.getExponentName(), self._exponent)
        macString = Utils.appendField(macString, Constants.getAccountingModeName(), self._accounting_mode)

        macString = Utils.appendField(macString, Constants.getNetworkName(), self._network)
        macString = Utils.appendField(macString, Constants.getEmailChName(), self._email_ch)
        macString = Utils.appendField(macString, Constants.getUserIdName(), self._user_id)
        macString = Utils.appendField(macString, Constants.getAcquirerName(), self._acquirer)
        macString = Utils.appendField(macString, Constants.getIpAddressName(), self._ip_address)
        macString = Utils.appendField(macString, Constants.getOpDescrName(), self._op_descr)
        macString = Utils.appendField(macString, Constants.getUsrAuthFlagName(), self._usr_auth_flag)
        macString = Utils.appendField(macString, Constants.getOptionsName(), self._options)
        macString = Utils.appendField(macString, Constants.getAntiFraudName(), self._anti_fraud)

        macString = Utils.appendField(macString, Constants.getProductRefName(), self._product_ref)
        macString = Utils.appendField(macString, Constants.getNameName(), self._name)
        macString = Utils.appendField(macString, Constants.getSurnameName(), self._surname)
        macString = Utils.appendField(macString, Constants.getTaxIdName(), self._tax_id)

        macString = Utils.appendField(macString, Constants.getThreeDSDataName(),
                                      AES.AES_encrypt(self._three_ds_data, api_result_key))
        macString = Utils.appendField(macString, Constants.getNameCHName(), self._name_ch)
        macString = Utils.appendField(macString, Constants.getNotifUrl(), self._notify_url)
        macString = Utils.appendField(macString, Constants.getThreeDSMtdNotifUrlName(), self._three_ds_mtd_notify_url)
        macString = Utils.appendField(macString, Constants.getChallengeWinSizeName(), self._challenge_win_size)
        return macString


class ThreeDSAuthorization1RequestXML(Request):
    def __init__(self, threeDS1_request, shop_id):
        super().__init__(shop_id, threeDS1_request.operator_id, None)
        self._operation = 'THREEDSAUTHORIZATION1'
        self._three_DS_trans_id = threeDS1_request.three_DS_trans_id
        self._three_DS_Mtd_compl_ind = threeDS1_request.three_DS_Mtd_compl_ind

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getThreeDSAuthorizationRequest1Tag())
        authorization3DS = request.find(TagConstants.getDataTag()).find(
            TagConstants.getThreeDSAuthorizationRequest1Tag())

        Utils.addChild(authorization3DS, TagConstants.getThreeDSTransactionIDTag(), self._three_DS_trans_id)
        Utils.addChild(authorization3DS, TagConstants.getThreeDSMtdComplIndTag(), self._three_DS_Mtd_compl_ind)
        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.get_mac(self._string_for_mac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _string_for_mac(self):
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getThreeDSTransIdName(), self._three_DS_trans_id)
        macString = Utils.appendField(macString, Constants.getThreeDSMtdComplIndName(), self._three_DS_Mtd_compl_ind)
        return macString


class ThreeDSAuthorization2RequestXML(Request):
    def __init__(self, threeDS2_request, shop_id):
        super().__init__(shop_id, threeDS2_request.operator_id, None)
        self._operation = 'THREEDSAUTHORIZATION2'
        self._order_id = threeDS2_request.order_id
        self._three_DS_trans_id = threeDS2_request.three_DS_trans_id

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getThreeDSAuthorizationRequest2Tag())
        authorization3DS = request.find(TagConstants.getDataTag()).find(
            TagConstants.getThreeDSAuthorizationRequest2Tag())

        Utils.addChild(authorization3DS, TagConstants.getThreeDSTransactionIDTag(), self._three_DS_trans_id)
        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.get_mac(self._string_for_mac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _string_for_mac(self):
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getThreeDSTransIdName(), self._three_DS_trans_id)
        return macString


class PaymentRequest(Request):
    def __init__(self, payment_info_request, shop_id):
        super().__init__(shop_id, None,
                         payment_info_request.options)
        self._amount = payment_info_request.amount
        self._currency = payment_info_request.currency
        self._order_id = payment_info_request.order_id
        self._url_back = payment_info_request.url_back
        self._url_done = payment_info_request.url_done
        self._url_ms = payment_info_request.url_ms
        self._accounting_mode = payment_info_request.accounting_mode
        self._author_mode = payment_info_request.author_mode
        self._exponent = payment_info_request.exponent
        self._name = payment_info_request.name
        self._surname = payment_info_request.surname
        self._tax_id = payment_info_request.tax_id
        self._lock_card = payment_info_request.lock_card
        self._commis = payment_info_request.commis
        self._ord_descr = payment_info_request.ord_descr
        self._VSID = payment_info_request.VSID
        self._op_descr = payment_info_request.op_descr
        self._remaining_duration = payment_info_request.remaining_duration
        self._userId = payment_info_request.user_id
        self._bb_poste_pay = payment_info_request.bb_poste_pay
        self._bp_cards = payment_info_request.bp_cards
        self._phone_number = payment_info_request.phone_number
        self._causation = payment_info_request.causation
        self._user = payment_info_request.user
        self._product_ref = payment_info_request.product_ref
        self._anti_fraud = payment_info_request.anti_fraud
        self._url_back = payment_info_request.url_back
        self._lang = payment_info_request.lang
        self._shop_email = payment_info_request.shop_email
        self._data_3DS_json = payment_info_request.data_3DS_json.toJson()
        self._network = payment_info_request.network
        self._exp_date = payment_info_request.exp_date
        self._token = payment_info_request.token
        self._t_recurr = payment_info_request.t_recurr
        self._c_recurr = payment_info_request.c_recurr
        self._iban = payment_info_request.iban

        self._email = payment_info_request.email
        self._name_ch = payment_info_request.name_ch
        self._surname_ch = payment_info_request.surname_ch

    def getParametersMap(self, redirect_key, api_result_key, digest_mode):
        map = OrderedDict()
        map[Constants.getUrlMsName()] = self._url_ms
        map[Constants.getUrlDoneName()] = self._url_done
        map[Constants.getOrderIdName()] = self._order_id
        map[Constants.getShopIdName()] = self._shop_id
        map[Constants.getAmountName()] = self._amount
        map[Constants.getCurrencyName()] = self._currency
        map[Constants.getExponentName()] = self._exponent
        map[Constants.getAccountingModeName()] = self._accounting_mode
        map[Constants.getAuthorModeName()] = self._author_mode

        # NOT COMPULSORY FIELDS
        map[Constants.getOptionsName()] = self._options
        map[Constants.getNameName()] = self._name
        map[Constants.getSurnameName()] = self._surname
        map[Constants.getTaxIdName()] = self._tax_id
        map[Constants.getLockCardName()] = self._lock_card
        map[Constants.getCommisName()] = self._commis
        map[Constants.getOrdDescrName()] = self._ord_descr
        map[Constants.getVSIDName()] = self._VSID

        map[Constants.getOpDescrName()] = self._op_descr
        map[Constants.getRemainingDurationName()] = self._remaining_duration
        map[Constants.getUserIdName()] = self._userId
        map[Constants.getBBPostepayName()] = self._bb_poste_pay
        map[Constants.getBPCardsName()] = self._bp_cards

        map[Constants.getPhoneNumberName()] = self._phone_number
        map[Constants.getCausationName()] = self._causation
        map[Constants.getUserName()] = self._user
        map[Constants.getProductRefName()] = self._product_ref
        map[Constants.getAntiFraudName()] = self._anti_fraud

        if self._data_3DS_json is not None:
            map[Constants.get3DSJsonDataName()] = AES.AES_encrypt(self._data_3DS_json, api_result_key)

        map[Constants.getTrecurrName()] = self._t_recurr
        map[Constants.getCrecurrName()] = self._c_recurr
        map[Constants.getTokenName()] = self._token
        map[Constants.getExpDateName()] = self._exp_date
        map[Constants.getNetworkName()] = self._network
        map[Constants.getIBANName()] = self._iban

        map[Constants.getMacName()] = Encoder.get_mac(self._string_for_mac(api_result_key), redirect_key, digest_mode)

        map[Constants.getUrlBackName()] = self._url_back
        map[Constants.getLangName()] = self._lang
        map[Constants.getShopEmailName()] = self._shop_email
        map[Constants.getEmailName()] = self._email
        map[Constants.getNameCHName()] = self._name_ch
        map[Constants.getSurnameCHName()] = self._surname_ch
        return map

    def _string_for_mac(self, apiKey):
        macString = Constants.getUrlMsName() + "=" + self._url_ms
        macString = Utils.appendField(macString, Constants.getUrlDoneName(), self._url_done)
        macString = Utils.appendField(macString, Constants.getOrderIdName(), self._order_id)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getAmountName(), self._amount)
        macString = Utils.appendField(macString, Constants.getCurrencyName(), self._currency)
        macString = Utils.appendField(macString, Constants.getExponentName(), self._exponent)
        macString = Utils.appendField(macString, Constants.getAccountingModeName(), self._accounting_mode)
        macString = Utils.appendField(macString, Constants.getAuthorModeName(), self._author_mode)
        macString = Utils.appendField(macString, Constants.getOptionsName(), self._options)

        if self._options is not None and "B" in self._options:
            macString = Utils.appendField(macString, Constants.getNameName(), self._name)
            macString = Utils.appendField(macString, Constants.getSurnameName(), self._surname)

        macString = Utils.appendField(macString, Constants.getTaxIdName(), self._tax_id)
        macString = Utils.appendField(macString, Constants.getLockCardName(), self._lock_card)

        if self._options is not None and "F" in self._options:
            macString = Utils.appendField(macString, Constants.getCommisName(), self._commis)

        if self._options is not None and ("O" in self._options or "V" in self._options):
            macString = Utils.appendField(macString, Constants.getOrdDescrName(), self._ord_descr)

        macString = Utils.appendField(macString, Constants.getVSIDName(), self._VSID)
        macString = Utils.appendField(macString, Constants.getOpDescrName(), self._op_descr)

        if self._options is not None and "D" in self._options:
            macString = Utils.appendField(macString, Constants.getRemainingDurationName(), self._remaining_duration)

        macString = Utils.appendField(macString, Constants.getUserIdName(), self._userId)
        macString = Utils.appendField(macString, Constants.getBBPostepayName(), self._bb_poste_pay)
        macString = Utils.appendField(macString, Constants.getBPCardsName(), self._bp_cards)

        if self._network is not None and "91" in self._network:
            macString = Utils.appendField(macString, Constants.getPhoneNumberName(), self._phone_number)
            macString = Utils.appendField(macString, Constants.getCausationName(), self._causation)
            macString = Utils.appendField(macString, Constants.getUserName(), self._user)

        macString = Utils.appendField(macString, Constants.getProductRefName(), self._product_ref)
        macString = Utils.appendField(macString, Constants.getAntiFraudName(), self._anti_fraud)

        if self._data_3DS_json is not None:
            macString = Utils.appendField(macString, Constants.get3DSJsonDataName(),
                                          AES.AES_encrypt(self._data_3DS_json, apiKey))

        macString = Utils.appendField(macString, Constants.getTrecurrName(), self._t_recurr)
        macString = Utils.appendField(macString, Constants.getCrecurrName(), self._c_recurr)
        macString = Utils.appendField(macString, Constants.getTokenName(), self._token)
        macString = Utils.appendField(macString, Constants.getExpDateName(), self._exp_date)
        macString = Utils.appendField(macString, Constants.getNetworkName(), self._network)
        macString = Utils.appendField(macString, Constants.getIBANName(), self._iban)
        return macString


class OnlineAuthorizationRequestXml(Request):
    def __init__(self, authorization_request, shop_id):
        super().__init__(shop_id, authorization_request.operator_id,
                         authorization_request.options)
        self._operation = 'AUTHORIZATION'

        self._order_id = authorization_request.order_id
        self._pan = authorization_request.pan
        self._cvv2 = authorization_request.cvv2
        self._create_pan_alias = authorization_request.create_pan_alias
        self._exp_date = authorization_request.exp_date
        self._amount = authorization_request.amount
        self._currency = authorization_request.currency
        self._accounting_mode = authorization_request.accounting_mode
        self._exponent = authorization_request.exponent
        self._network = authorization_request.network
        self._email_ch = authorization_request.email_ch
        self._user_id = authorization_request.user_id
        self._acquirer = authorization_request.acquirer
        self._ip_address = authorization_request.ip_address
        self._usr_auth_flag = authorization_request.usr_auth_flag
        self._op_descr = authorization_request.op_descr
        self._anti_fraud = authorization_request.anti_fraud
        self._product_ref = authorization_request.product_ref

        self._name = authorization_request.name
        self._surname = authorization_request.surname
        self._tax_id = authorization_request.tax_id

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getAuthorizationRequestTag())
        authorization = request.find(TagConstants.getDataTag()).find(
            TagConstants.getAuthorizationRequestTag())

        Utils.addChild(authorization, TagConstants.getOrderIDTag(), self._order_id)
        Utils.addChild(authorization, TagConstants.getPanTag(), self._pan)
        Utils.addChild(authorization, TagConstants.getExpDateTag(), self._exp_date)
        Utils.addChild(authorization, TagConstants.getAmountTag(), self._amount)
        Utils.addChild(authorization, TagConstants.getCurrencyTag(), self._currency)
        Utils.addOptionalChild(authorization, TagConstants.getExponentTag(), self._exponent)
        Utils.addChild(authorization, TagConstants.getAccountingModeTag(), self._accounting_mode)
        Utils.addChild(authorization, TagConstants.getNetworkTag(), self._network)

        # OPTIONAL CHILD
        Utils.addOptionalChild(authorization, TagConstants.getCVV2Tag(), self._cvv2)
        Utils.addOptionalChild(authorization, TagConstants.getEmailCHTag(), self._email_ch)
        Utils.addOptionalChild(authorization, TagConstants.getUseridTag(), self._user_id)
        Utils.addOptionalChild(authorization, TagConstants.getAcquirerTag(), self._acquirer)
        Utils.addOptionalChild(authorization, TagConstants.getIpAddressTag(), self._ip_address)
        Utils.addOptionalChild(authorization, TagConstants.getUserAuthFlagTag(), self._usr_auth_flag)

        Utils.addOptionalChild(authorization, TagConstants.getOpDescrTag(), self._op_descr)
        Utils.addOptionalChild(authorization, TagConstants.getOptionsTag(), self._options)
        Utils.addOptionalChild(authorization, TagConstants.getAntiFraudTag(), self._anti_fraud)
        Utils.addOptionalChild(authorization, TagConstants.getProductRefTag(), self._product_ref)
        Utils.addOptionalChild(authorization, TagConstants.getNameTag(), self._name)
        Utils.addOptionalChild(authorization, TagConstants.getSurnameTag(), self._surname)

        Utils.addOptionalChild(authorization, TagConstants.getTaxIDTag(), self._tax_id)
        Utils.addOptionalChild(authorization, TagConstants.getCreatePanAliasTag(), self._create_pan_alias)

        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.get_mac(self._string_for_mac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _string_for_mac(self):
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOrderIdName(), self._order_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getPanName(), self._pan)
        macString = Utils.appendField(macString, Constants.getCvv2Name(), self._cvv2)
        macString = Utils.appendField(macString, Constants.getExpDateName(), self._exp_date)
        macString = Utils.appendField(macString, Constants.getAmountName(), self._amount)
        macString = Utils.appendField(macString, Constants.getCurrencyName(), self._currency)
        macString = Utils.appendField(macString, Constants.getExponentName(), self._exponent)
        macString = Utils.appendField(macString, Constants.getAccountingModeName(), self._accounting_mode)

        macString = Utils.appendField(macString, Constants.getNetworkName(), self._network)
        macString = Utils.appendField(macString, Constants.getEmailChName(), self._email_ch)
        macString = Utils.appendField(macString, Constants.getUserIdName(), self._user_id)
        macString = Utils.appendField(macString, Constants.getAcquirerName(), self._acquirer)
        macString = Utils.appendField(macString, Constants.getIpAddressName(), self._ip_address)
        macString = Utils.appendField(macString, Constants.getOpDescrName(), self._op_descr)
        macString = Utils.appendField(macString, Constants.getUsrAuthFlagName(), self._usr_auth_flag)
        macString = Utils.appendField(macString, Constants.getOptionsName(), self._options)
        macString = Utils.appendField(macString, Constants.getAntiFraudName(), self._anti_fraud)

        macString = Utils.appendField(macString, Constants.getProductRefName(), self._product_ref)
        macString = Utils.appendField(macString, Constants.getNameName(), self._name)
        macString = Utils.appendField(macString, Constants.getSurnameName(), self._surname)
        macString = Utils.appendField(macString, Constants.getTaxIdName(), self._tax_id)
        return macString
