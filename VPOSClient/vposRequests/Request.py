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
        Utils.addChild(refundRequest,TagConstants.getCurrencyTag(), self._currency)
        if self._exponent is not None:
            Utils.addChild(refundRequest, TagConstants.getExponentTag(), self._exponent)
        if self._op_descr is not None:
            Utils.addChild(refundRequest, TagConstants.getOpDescrTag(), self._op_descr)
        if self._options is not None:
            Utils.addChild(refundRequest, TagConstants.getOptionsTag(), self._options)
        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.getMac(self._string_for_mac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')


    def _string_for_mac(self):
        macString = Constants.getOperationName()+"="+str(self._operation)
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


class VerifyPaymentRequest(Request):
    def __init__(self, original_req_ref_num, shop_id, operator_id, options=None):
        super().__init__(shop_id, operator_id, options)
        self._original_req_ref_num = original_req_ref_num
        self._operation = 'VERIFY'

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getVerifyRequestTag())
        verifyRequest = request.find(TagConstants.getDataTag()).find(TagConstants.getVerifyRequestTag())
        if self._options is not None:
            Utils.addChild(verifyRequest, TagConstants.getOptionsTag(), self._options)
        Utils.addChild(verifyRequest, TagConstants.getOriginalReqRefNumTag(), self._original_req_ref_num)
        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.getMac(self._stringForMac(), api_result_key, digest_mode)

    def _stringForMac(self):
        macString = Constants.getOperationName()+"="+str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getOriginalReqRefNumName(), self._original_req_ref_num)
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
        mac.text = Encoder.getMac(self._stringForMac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _stringForMac(self):
        macString = str()
        macString = Constants.getOperationName()+"="+str(self._operation)
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
        mac.text = Encoder.getMac(self._stringForMac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _stringForMac(self):
        macString = Constants.getOperationName()+"="+str(self._operation)
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


class Auth3DSRequest(Request):
    def __init__(self, auth3DSRequestDto):
        super().__init__(auth3DSRequestDto.shop_id, auth3DSRequestDto.operator_id, auth3DSRequestDto.options)
        # COMPULSORY PROPERTY
        self._operation = 'AUTHORIZATION3DSSTEP1'
        self._is_master_pass = auth3DSRequestDto.is_master_pass
        self._order_id = auth3DSRequestDto.order_id
        self._pan = auth3DSRequestDto.pan
        self._exp_date = auth3DSRequestDto.exp_date
        self._amount = auth3DSRequestDto.amount
        self._currency = auth3DSRequestDto.currency
        self._accounting_mode = auth3DSRequestDto.accounting_mode
        self._network = auth3DSRequestDto.network
        # NOT COMPULSORY
        self._cvv2 = auth3DSRequestDto.cvv2
        self._exponent = auth3DSRequestDto.exponent
        self._email_ch = auth3DSRequestDto.email_ch
        self._userId = auth3DSRequestDto.user_id
        self._acquirer = auth3DSRequestDto.acquirer
        self._ip_address = auth3DSRequestDto.ip_address
        self._usr_auth_flag = auth3DSRequestDto.usr_auth_flag
        self._op_descr = auth3DSRequestDto.op_descr
        self._options = auth3DSRequestDto.options
        self._anti_fraud = auth3DSRequestDto.anti_fraud
        self._product_ref = auth3DSRequestDto.product_ref
        self._name = auth3DSRequestDto.name
        self._surname = auth3DSRequestDto.surname
        self._tax_id = auth3DSRequestDto.tax_id
        self._create_pan_alias = auth3DSRequestDto.create_pan_alias
        self._inPerson = auth3DSRequestDto.in_person
        self._merchant_url = auth3DSRequestDto.merchant_url
        self._service = auth3DSRequestDto.service
        self._xId = auth3DSRequestDto.xId
        self._cavv = auth3DSRequestDto.cavv
        self._eci = auth3DSRequestDto.eci
        self._pp_authenticate_method = auth3DSRequestDto.pp_authenticate_method
        self._card_enroll_method = auth3DSRequestDto.card_enroll_method
        self._pares_status = auth3DSRequestDto.pares_status
        self._scen_roll_status = auth3DSRequestDto.scen_roll_status
        self._signature_verification = auth3DSRequestDto.signature_verification

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getAuthorization3DSRequestTag())
        authorization3DS = request.find(TagConstants.getDataTag()).find(TagConstants.getAuthorization3DSRequestTag())

        if self._is_master_pass:
            # 3DS DATA
            data3Ds = Utils.addChild(authorization3DS, TagConstants.getData3DSTag(), None)
            Utils.addChild(data3Ds, TagConstants.getServiceTag(), self._service)
            Utils.addChild(data3Ds, TagConstants.getEciTag(), self._eci)
            Utils.addChild(data3Ds, TagConstants.getXidTag(), self._xId)
            Utils.addChild(data3Ds, TagConstants.getCAVVTag(), self._cavv)
            Utils.addChild(data3Ds, TagConstants.getParesStatusTag(), self._pares_status)
            Utils.addChild(data3Ds, TagConstants.getScEnrollStatusTag(), self._scen_roll_status)
            Utils.addChild(data3Ds, TagConstants.getSignatureVerifytionTag(), self._signature_verification)
            # MASTERPASS DATA
            masterPass = Utils.addChild(authorization3DS, TagConstants.getMasterpassDataTag(), None)
            Utils.addChild(masterPass, TagConstants.getPP_AuthenticateMethodTag(), self._pp_authenticate_method)
            Utils.addChild(masterPass, TagConstants.getPP_CardEnrollMethodTag(), self._card_enroll_method)

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
        Utils.addOptionalChild(authorization3DS, TagConstants.getUseridTag(), self._userId)
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
        Utils.addOptionalChild(authorization3DS, TagConstants.getInPersonTag(), self._inPerson)
        Utils.addOptionalChild(authorization3DS, TagConstants.getMerchantURLTag(), self._merchant_url)
        Utils.addOptionalChild(authorization3DS, TagConstants.getXidTag(), self._xId)
        Utils.addOptionalChild(authorization3DS, TagConstants.getServiceTag(), self._service)

        Utils.addOptionalChild(authorization3DS, TagConstants.getCAVVTag(), self._cavv)
        Utils.addOptionalChild(authorization3DS, TagConstants.getEciTag(), self._eci)
        Utils.addOptionalChild(authorization3DS, TagConstants.getPP_AuthenticateMethodTag(), self._pp_authenticate_method)
        Utils.addOptionalChild(authorization3DS, TagConstants.getPP_CardEnrollMethodTag(), self._card_enroll_method)
        Utils.addOptionalChild(authorization3DS, TagConstants.getParesStatusTag(), self._pares_status)
        Utils.addOptionalChild(authorization3DS, TagConstants.getScEnrollStatusTag(), self._scen_roll_status)
        Utils.addOptionalChild(authorization3DS, TagConstants.getSignatureVerifytionTag(), self._signature_verification)

        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.getMac(self._stringForMac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _stringForMac(self):
        macString = Constants.getOperationName()+"="+str(self._operation)
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
        macString = Utils.appendField(macString, Constants.getUserIdName(), self._userId)
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
        macString = Utils.appendField(macString, Constants.getInPersonName(), self._inPerson)
        macString = Utils.appendField(macString, Constants.getMerchantUrlName(), self._merchant_url)
        macString = Utils.appendField(macString, Constants.getServiceName(), self._service)
        macString = Utils.appendField(macString, Constants.getXIdName(), self._xId)
        macString = Utils.appendField(macString, Constants.getCAVVName(), self._cavv)

        macString = Utils.appendField(macString, Constants.getEciName(), self._eci)
        macString = Utils.appendField(macString, Constants.getPPAuthenticateMethodName(), self._pp_authenticate_method)
        macString = Utils.appendField(macString, Constants.getPPCardEnrollMethodName(), self._card_enroll_method)
        macString = Utils.appendField(macString, Constants.gerParesStatusName(), self._pares_status)
        macString = Utils.appendField(macString, Constants.getScenRollStatusName(), self._scen_roll_status)
        macString = Utils.appendField(macString, Constants.getSignatureVerificationName(), self._signature_verification)

        return macString


class Start3DSAuthStep2Request(Request):
    def __init__(self, start3DSAuthStep2RequestDto):
        super().__init__(start3DSAuthStep2RequestDto.shop_id, start3DSAuthStep2RequestDto.operator_id,
                         start3DSAuthStep2RequestDto.options)
        self._operation = 'AUTHORIZATION3DSSTEP2'
        self._original_req_ref_num = start3DSAuthStep2RequestDto.original_req_ref_num
        self._pares = start3DSAuthStep2RequestDto.pares
        self._acquirer = start3DSAuthStep2RequestDto.acquirer

    def build_request(self, api_result_key, digest_mode):
        request = self.get_request_base_xml(self._operation, TagConstants.getAuthorization3DSStep2RequestTag())
        authorization3DS = request.find(TagConstants.getDataTag()).find(
            TagConstants.getAuthorization3DSStep2RequestTag())

        Utils.addChild(authorization3DS, TagConstants.getReqRefNumTag(), self._reqRefNum)
        Utils.addChild(authorization3DS, TagConstants.getOriginalReqRefNumTag(), self._original_req_ref_num)
        Utils.addChild(authorization3DS, TagConstants.getParesTag(), Utils.parse_url(self._pares))
        Utils.addOptionalChild(authorization3DS, TagConstants.getAcquirerTag(), self._acquirer)
        Utils.addChild(authorization3DS, TagConstants.getOptionsTag(), self._options)

        mac = request.find(TagConstants.getRequestTag()).find(TagConstants.getMACTag())
        mac.text = Encoder.getMac(self._stringForMac(), api_result_key, digest_mode)
        return ET.tostring(request, "utf-8", method='xml')

    def _stringForMac(self):
        macString = Constants.getOperationName() + "=" + str(self._operation)
        macString = Utils.appendField(macString, Constants.getTimestampName(), self._timestamp)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getOperatorIdName(), self._operator_id)
        macString = Utils.appendField(macString, Constants.getReqRefNumName(), self._reqRefNum)
        macString = Utils.appendField(macString, Constants.getOriginalReqRefNumName(), self._original_req_ref_num)
        macString = Utils.appendField(macString, Constants.getPaResName(), self._pares)
        macString = Utils.appendField(macString, Constants.getAcquirerName(), self._acquirer)

        return macString


class PaymentRequest:
    def __init__(self, payment_info_request, shop_id):
        self._shop_id = shop_id
        self._options = payment_info_request.options
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
        self._data_3DS_json = payment_info_request.data_3DS_json

    def getParametersMap(self, api_result_key, digest_mode):
        map = {}
        map[Constants.getUrlMsName()] = self._url_ms
        map[Constants.getUrlDoneName()] = self._url_done
        map[Constants.getUrlBackName()] = self._url_back
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

        # map 3ds Json Data TO DO
        if self._data_3DS_json is not None:
            map[Constants.get3DSJsonDataName()] = AES.AES_encrypt(self._data_3DS_json.toJson(), api_result_key)


        map[Constants.getUrlBackName()] = self._url_back
        map[Constants.getLangName()] = self._lang
        map[Constants.getShopEmailName()] = self._shop_email
        map[Constants.getMacName()] = Encoder.getMac(self._stringForMac(api_result_key), api_result_key, digest_mode)
        return map

    def _stringForMac(self, apiKey):
        macString = Constants.getUrlMsName()+"="+self._url_ms
        macString = Utils.appendField(macString, Constants.getUrlDoneName(), self._url_done)
        macString = Utils.appendField(macString, Constants.getOrderIdName(), self._order_id)
        macString = Utils.appendField(macString, Constants.getShopIdName(), self._shop_id)
        macString = Utils.appendField(macString, Constants.getAmountName(), self._amount)
        macString = Utils.appendField(macString, Constants.getCurrencyName(), self._currency)
        macString = Utils.appendField(macString, Constants.getExponentName(), self._exponent)
        macString = Utils.appendField(macString, Constants.getAccountingModeName(), self._accounting_mode)
        macString = Utils.appendField(macString, Constants.getAuthorModeName(), self._author_mode)
        macString = Utils.appendField(macString, Constants.getOptionsName(), self._options)
        macString = Utils.appendField(macString, Constants.getNameName(), self._name)
        macString = Utils.appendField(macString, Constants.getSurnameName(), self._surname)
        macString = Utils.appendField(macString, Constants.getTaxIdName(), self._tax_id)

        macString = Utils.appendField(macString, Constants.getLockCardName(), self._lock_card)
        macString = Utils.appendField(macString, Constants.getCommisName(), self._commis)
        macString = Utils.appendField(macString, Constants.getOrdDescrName(), self._ord_descr)
        macString = Utils.appendField(macString, Constants.getVSIDName(), self._VSID)
        macString = Utils.appendField(macString, Constants.getOpDescrName(), self._op_descr)

        macString = Utils.appendField(macString, Constants.getRemainingDurationName(), self._remaining_duration)
        macString = Utils.appendField(macString, Constants.getUserIdName(), self._userId)
        macString = Utils.appendField(macString, Constants.getBBPostepayName(), self._bb_poste_pay)
        macString = Utils.appendField(macString, Constants.getBPCardsName(), self._bp_cards)
        macString = Utils.appendField(macString, Constants.getPhoneNumberName(), self._phone_number)

        macString = Utils.appendField(macString, Constants.getCausationName(), self._causation)
        macString = Utils.appendField(macString, Constants.getUserName(), self._user)
        macString = Utils.appendField(macString, Constants.getProductRefName(), self._product_ref)
        macString = Utils.appendField(macString, Constants.getAntiFraudName(), self._anti_fraud)
        # TO DO
        if self._data_3DS_json is not None:
            macString = Utils.appendField(macString, Constants.get3DSJsonDataName(), AES.AES_encrypt(self._data_3DS_json.toJson(), apiKey))
        return macString
