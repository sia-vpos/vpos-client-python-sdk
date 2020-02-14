import hashlib
import os

import requests

from cof.utils.RequestValidator import *
from cof.apos.Request import *
from cof.dto.RequestDto import PaymentRequestDto

from cof.utils.ProjectException import COFException
from cof.utils.Utils import map_for_verify_url_mac


class VposClient:

    def __init__(self, start_key, api_result_key, digest_mode=hashlib.sha256):
        """
        :param start_key:  used to perform MAC calculation of the outcoming requests
        :param api_result_key:  used to perform MAC calculation of the incoming VPOS responses
        :param digest_mode: used to perform MAC calculation (HMAC_SHA_256 used by default)
        """
        self._defaultHtmlPath = 'default.html'
        self._start_key = start_key
        self._api_result_key = api_result_key
        self._digest_mode = digest_mode
        # api endpoint
        self._web_api = "https://atpostest.ssb.it/atpos/apibo/apiBOXML.app"
        self._url_redirect = "https://atpostest.ssb.it/atpos/pagamenti/main"
        self._custom_template = False
        self._custom_template_name = '\customTemplate.html'
        self._default_template_name = '\default.html'
        self._proxies = None

    def injectTemplate(self, base64Html, delay):
        """Perform the injection of a custom HTML redirect template
        :param base64Html: base64 of the HTML template to inject
        :param delay: milliseconds to wait before redirecting to SIA VPOS page
        :return: void
        """

        if Utils.saveTemplate(base64Html, delay,os.path.dirname(__file__)):
            self._custom_template = True

    def getHtmlPaymentDocument(self, paymentRequestDto):
        """Create an HTML document ready to use for payment initiation. The method returns the custom template with an
        hidden form containing all the payment parameters in case of precedent HTML injection. Default template is
        returned otherwise.
        :param paymentRequestDto: data transfer object containing all the payment parameters
        :return: the base64 format of the HTML document
        """
        paymentRequest = PaymentRequest(paymentRequestDto)
        dirname = os.path.dirname(__file__)
        print(dirname)
        path = dirname + "/" + self._custom_template_name if self._custom_template else dirname + "/"+self._default_template_name
        return Utils.getHtml(path, self._url_redirect,
                             paymentRequest.getParametersMap(self._start_key, self._digest_mode))

    def tokenize(self, shop_id, URL_BACK, URL_DONE, URL_MS):
        """Tokenize a credit card

        :param shop_id: identifier of the merchant
        :param URL_BACK: redirect url in case of payment failure
        :param URL_DONE: redirect url in case of success
        :param URL_MS: endpoint of merchant backend
        :return: the base64 format of the HTML document
        """
        paymentInfo = PaymentRequestDto(shop_id, URL_BACK, URL_DONE, URL_MS, "10", "978", "02", Utils.gen_order_id(), "D", "I")
        paymentInfo.options = 'GM'
        return self.getHtmlPaymentDocument(paymentInfo)

    def start3DSAuth(self, auth_3DS_request_dto):
        """
        :param auth_3DS_request_dto: data transfer object containing all the required parameters to perform the first
        step of a 3DS authorization
        :return: the outcome of the operation with the relative additional infos
        """
        validate_auth_3DS_request(auth_3DS_request_dto)
        auth_3DS_request = Auth3DSRequest(auth_3DS_request_dto)
        request_xml = auth_3DS_request.build_request(self._api_result_key, self._digest_mode)
        self.verifyMacResponse(self._execute_call(request_xml))

    def start3DSAuthStep2(self, auth_3DS_step2_request_dto):
        """
        :param auth_3DS_step2_request_dto: data transfer object containing all the required parameters to perform the second step of a 3DS authorization
        :return: the outcome of the operation with the relative additional infos
        """
        auth_3DS_step2_request = Start3DSAuthStep2Request(auth_3DS_step2_request_dto)
        request_xml = auth_3DS_step2_request.build_request(self._api_result_key, self._digest_mode)
        self.verifyMacResponse(self._execute_call(request_xml))

    def confirmTransaction(self, confirm_transaction_request_dto):
        """

        :param confirm_transaction_request_dto: data transfer object containing all the required parameters to perform a
        payment confirmation
        :return:
        """
        validate_confirm_transaction_request(confirm_transaction_request_dto)
        confirmTransaction = ConfirmTransactionRequest(confirm_transaction_request_dto)
        requestXml = confirmTransaction.build_request(self._api_result_key, self._digest_mode)
        self.verifyMacResponse(self._execute_call(requestXml))

    def verifyPayment(self, original_req_ref_num, shop_id, operator_id, options=None):
        """

        :param original_req_ref_num:
        :param shop_id:
        :param operator_id:
        :param options:
        :return:
        """
        validate_verify_payment_request(original_req_ref_num, shop_id, operator_id)
        verifyPayment = VerifyPaymentRequest(original_req_ref_num, shop_id, operator_id, options)
        requestXml = verifyPayment.build_request(self._api_result_key, self._digest_mode)
        self.verifyMacResponse(self._execute_call(requestXml))

    def getOrderStatus(self, order_id, product_ref, shop_id, operator_id, options=None):
        """

        :param order_id: the order id of the transaction to control
        :param product_ref: product_ref code of the transaction
        :param shop_id: shop id
        :param operator_id: operator id
        :param options: options
        :return:
        """
        validate_order_status_request(order_id, product_ref, shop_id, operator_id)
        order_status = OrderStatusRequest(order_id, shop_id, operator_id, product_ref, options)
        request_xml = order_status.build_request(self._api_result_key, self._digest_mode)
        self.verifyMacResponse(self._execute_call(request_xml))

    def refundPayment(self, refund_request_dto):
        """

        :param refund_request_dto: data transfer object containing all the required parameters to perform a payment refund
        :return:
        """
        validate_refund_payment_request(refund_request_dto)
        refund = RefundRequest(refund_request_dto)
        request_xml = refund.build_request(self._api_result_key, self._digest_mode)
        self.verifyMacResponse(self._execute_call(request_xml))

    def verifyMacResponse(self, response):
        response = Utils.stringToXML(response)
        receivedMac = response.find(Constants.getMacName())
        calculatedMac = Encoder.getMac(Utils.geResultStringForMac(response), self._api_result_key, self._digest_mode)

        if (not receivedMac.text == "NULL") & (not Encoder.compareDigest(receivedMac.text, calculatedMac)):
            raise COFException("Response MAC is not valid")

        data = response.find(TagConstants.getDataTag())
        if (data is not None) & (data.find(TagConstants.getOperationTag()) is not None):
            operation_calculated_mac = Encoder.getMac(
                Utils.getOperationStringForMac(data.find(TagConstants.getOperationTag())),self._api_result_key, self._digest_mode)
            operation_received_mac = data.find(TagConstants.getOperationTag()).find(TagConstants.getMACTag())
            if (not operation_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(operation_received_mac.text, operation_calculated_mac)):
                raise COFException("Operation MAC is not valid")

        if (data is not None) & (data.find(TagConstants.getAuthorizationTag()) is not None):
            authorization_calculated_mac = Encoder.getMac(Utils.getAuthorizationStringForMac(data.find(TagConstants.getAuthorizationTag())), self._api_result_key, self._digest_mode)
            authorization_received_mac = data.find(TagConstants.getAuthorizationTag()).find(TagConstants.getMACTag())
            if (not authorization_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(authorization_received_mac.text, authorization_calculated_mac)):
                raise COFException("Authorization MAC is not valid")

    def verifyUrl(self, values, receivedMac):
        """
        Validate the result of a payment initiation verifying the integrity of the data contained in URMLS/URLDONE
        :param values:  parameters received from SIA VPOS
        :param receivedMac: to compare with the calculated one
        """
        calculated_mac = Encoder.getMac(map_for_verify_url_mac(values), self._api_result_key, self._digest_mode)
        if not Encoder.compareDigest(calculated_mac,receivedMac):
            raise COFException("Authorization MAC is not valid")

    def set_proxy(self, proxy_name, username=None, password=None):
        proxy = "https://"
        if username is not None and password is not None:
            proxy = proxy + username + ":" + password + "@" + proxy_name
        self._proxies = {"https": proxy}

    def _execute_call(self, requestXml):
        requestXml = 'data=' + str(requestXml, "utf-8")
        print("REQUEST: " + requestXml)
        response = requests.post(self._web_api, requestXml,
                                 headers={'content-type': 'application/x-www-form-urlencoded'}, proxies=self._proxies)
        print("RESPONSE: " + response.text)
        return response.text
