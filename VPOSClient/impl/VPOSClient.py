import logging
import traceback
import urllib.parse as urlparse

import requests

from VPOSClient.request.RequestXML import *
from VPOSClient.response.ResponseMapper import map_order_status_response, map_operation_response, \
    map_authorize_response, map_three_ds_authorize0, map_three_ds_authorize1, map_three_ds_authorize2
from VPOSClient.utils.RequestValidator import *
from VPOSClient.utils.Utils import map_for_verify_url_mac


class VPosClient:

    def __init__(self, vpos_config):

        validate_config(vpos_config)

        self._start_key = vpos_config.redirect_key
        self._api_result_key = vpos_config.api_key
        self._digest_mode = vpos_config.algorithm
        # api endpoint
        self._web_api = vpos_config.api_url
        self._url_redirect = vpos_config.redirect_url
        self._shop_id = vpos_config.shop_id
        self._timeout = vpos_config.timeout
        self._proxies = None
        self._cert = None
        if (vpos_config.proxy_host is not None) & (vpos_config.proxy_port is not None):
            self._set_proxy(vpos_config.proxy_host, vpos_config.proxy_port, vpos_config.proxy_username,
                            vpos_config.proxy_password)
        self._set_ssl(vpos_config.cert_path, vpos_config.cert_key)
        logging.getLogger(__name__).info("Client correctly initiated")

    def build_HTML_redirect_fragment(self, paymentInfo):
        """Create an HTML fragment for payment initiation.
        :param paymentInfo: data transfer object containing all the payment parameters
        :return: the HTML fragment for redirect
        """
        validate_redirect_request(paymentInfo)
        paymentRequest = PaymentRequest(paymentInfo, self._shop_id)
        return Utils.getHtml(self._url_redirect,
                             paymentRequest.getParametersMap(self._start_key, self._api_result_key, self._digest_mode))

    def authorize(self, authorization_request):
        """ This operation allows to forward authorization requests to the circuits
        :param authorization_request: authorization request object containing all the parameters to perform the operation
        :return: response object with the operation outcome infos
        """
        validate_authorize(authorization_request)
        authorization = OnlineAuthorizationRequestXml(authorization_request, self._shop_id)
        request_xml = authorization.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self._verify_mac_response(response)
        return map_authorize_response(response)

    def threeDS_authorize0(self, threeDS0_request):
        """
        The 3DS 2.x authorization request message permits to send authorization requests to the circuits.
        :param threeDS0_request: authorization request object containing all the parameters to perform the operation
        :return: response object with the operation outcome infos
        """
        validate_threeDSAuthorization0_request(threeDS0_request)
        three_ds0_auth = ThreeDSAuthorization0RequestXML(threeDS0_request, self._shop_id)
        request_xml = three_ds0_auth.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self._verify_mac_response(response)
        return map_three_ds_authorize0(response)

    def threeDS_authorize1(self, threeDS1_request):
        """
        The 3DS 2.x authorization request message step 1 permits to forward authentication requests to the circuits once a call to the ACS 3DS method has been performed.
        The message THREEDSAUTHORIZATION1 must arrive within 8 minutes from the time the original message THREEDSAUTHORIZATION0 is sent.
        :param threeDS1_request: authorization request object containing all the parameters to perform the operation
        :return: response object with the operation outcome infos
        """
        validate_threeDSAuthorization1_request(threeDS1_request)
        three_ds1_auth = ThreeDSAuthorization1RequestXML(threeDS1_request, self._shop_id)
        request_xml = three_ds1_auth.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self._verify_mac_response(response)
        return map_three_ds_authorize1(response)

    def threeDS_authorize2(self, threeDS2_request):
        """
        The 3DS 2.x authorization request message step 2 permits to forward authentication requests to the circuits once an user authentication challenge has been performed.
        The message THREEDSAUTHORIZATION2 must arrive within 8 minutes from the time the original message THREEDSAUTHORIZATION0 or THREEDSAUTHORIZATION1 are sent.
        :param threeDS2_request: authorization request object containing all the parameters to perform the operation
        :return: response object with the operation outcome infos
        """
        validate_threeDSAuthorization2_request(threeDS2_request)
        three_ds2_auth = ThreeDSAuthorization2RequestXML(threeDS2_request, self._shop_id)
        request_xml = three_ds2_auth.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self._verify_mac_response(response)
        return map_three_ds_authorize2(response)

    def capture(self, capture_request):
        """A booking request transaction permits the SIA VPOS system to forward to the competent acquirer the request for the booking of
        an authorization previously granted with a deferred booking.
        :param capture_request: object containing all the required parameters to perform a payment confirmation
        :return: object with the operation outcome infos
        """
        validate_capture_request(capture_request)
        capture = CaptureRequestXml(capture_request, self._shop_id)
        requestXml = capture.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(requestXml)
        self._verify_mac_response(response)
        return map_operation_response(response)

    def get_order_status(self, order_status_request):
        """
        This request returns the current status of an order, including all the related authorization transactions
        :param order_status_request: object containing all the required parameters to perform an order status request
        :return: object with the operation outcome infos
        """
        validate_order_status_request(order_status_request)
        order_status = OrderStatusRequestXml(order_status_request, self._shop_id)
        request_xml = order_status.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self._verify_mac_response(response)
        return map_order_status_response(response)

    def refund(self, refund_request):
        """ Refund request
        :param refund_request: request object containing all the required parameters to perform a payment refund
        :return: response object with the operation outcome infos
        """
        validate_refund_payment_request(refund_request)
        refund = RefundRequestXml(refund_request, self._shop_id)
        request_xml = refund.build_request(self._api_result_key, self._digest_mode)
        response = self._execute_call(request_xml)
        self._verify_mac_response(response)
        return map_operation_response(response)

    def verify_MAC(self, url):
        """
        Validate the result of a payment initiation verifying the integrity of the data contained in URMLS/URLDONE
        :param url:  url generated from SIA VPOS redirect
        """
        parsed = dict(urlparse.parse_qsl(urlparse.urlparse(url).query))
        receivedMac = parsed.get(Constants.getMacName())
        calculated_mac = Encoder.getMac(map_for_verify_url_mac(parsed), self._api_result_key, self._digest_mode)
        if not Encoder.compareDigest(calculated_mac, receivedMac):
            return False
        else:
            return True

    def _verify_mac_response(self, response):
        """ This method is used to verify the integrity of the VPOS response.
        :param response: The VPOS response
        """
        response = Utils.stringToXML(response)
        receivedMac = response.find(Constants.getMacName())
        calculatedMac = Encoder.getMac(Utils.geResultStringForMac(response), self._api_result_key, self._digest_mode)

        if (not receivedMac.text == "NULL") & (not Encoder.compareDigest(receivedMac.text, calculatedMac)):
            raise VPOSException("Response MAC is not valid")

        data = response.find(TagConstants.getDataTag())
        if (data is not None) & (data.find(TagConstants.getOperationTag()) is not None):
            operation_calculated_mac = Encoder.getMac(
                Utils.getOperationStringForMac(data.find(TagConstants.getOperationTag())), self._api_result_key,
                self._digest_mode)
            operation_received_mac = data.find(TagConstants.getOperationTag()).find(TagConstants.getMACTag())
            if (not operation_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(operation_received_mac.text, operation_calculated_mac)):
                raise VPOSException("Operation MAC is not valid")

        if (data is not None) & (data.find(TagConstants.getAuthorizationTag()) is not None):
            authorization_calculated_mac = Encoder.getMac(
                Utils.getAuthorizationStringForMac(data.find(TagConstants.getAuthorizationTag())), self._api_result_key,
                self._digest_mode)
            authorization_received_mac = data.find(TagConstants.getAuthorizationTag()).find(TagConstants.getMACTag())
            if (not authorization_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(authorization_received_mac.text, authorization_calculated_mac)):
                raise VPOSException("Authorization MAC is not valid")

        if (data is not None) & (data.find(TagConstants.getThreeDSChallengeTag()) is not None):
            challenge_calculated_mac = Encoder.getMac(
                Utils.getChallengeStringForMac(data.find(TagConstants.getThreeDSChallengeTag())), self._api_result_key,
                self._digest_mode)
            challenge_received_mac = data.find(TagConstants.getThreeDSChallengeTag()).find(TagConstants.getMACTag())
            if (not challenge_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(challenge_received_mac.text, challenge_calculated_mac)):
                raise VPOSException("Challenge MAC is not valid")

        if (data is not None) & (data.find(TagConstants.getThreeDSMtdTag()) is not None):
            mtd_calculated_mac = Encoder.getMac(
                Utils.getThreeDSMtdStringForMac(data.find(TagConstants.getThreeDSMtdTag())), self._api_result_key,
                self._digest_mode)
            mtd_received_mac = data.find(TagConstants.getThreeDSMtdTag()).find(TagConstants.getMACTag())
            if (not mtd_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(mtd_received_mac.text, mtd_calculated_mac)):
                raise VPOSException("ThreeDS Method MAC is not valid")

        if (data is not None) & (data.find(TagConstants.getPanAliasDataTag()) is not None):
            panAlias_calculated_mac = Encoder.getMac(
                Utils.getPanAliasDataStringForMac(data.find(TagConstants.getPanAliasDataTag())), self._api_result_key,
                self._digest_mode)
            panAlias_received_mac = data.find(TagConstants.getPanAliasDataTag()).find(TagConstants.getMACTag())
            if (not panAlias_received_mac.text == "NULL") & (
                    not Encoder.compareDigest(panAlias_received_mac.text, panAlias_calculated_mac)):
                raise VPOSException("Pan Alias MAC is not valid")

    def _set_proxy(self, proxy_name, proxy_port, username=None, password=None):
        proxy = "http://" + str(proxy_name) + ":" + str(proxy_port)
        if username is not None and password is not None:
            proxy = proxy + username + ":" + password + "@" + str(proxy_name) + ":" + str(proxy_port)
        self._proxies = {"http": proxy}

    def _set_ssl(self, cert_path, cert_key):
        if cert_key is not None and cert_path is not None:
            self._cert = (cert_path, cert_key)
        elif cert_path is not None and cert_key is None:
            self._cert = cert_path

    def _execute_call(self, request_xml):
        request_xml = 'data=' + str(request_xml, "utf-8")
        logging.getLogger(__name__).info("REQUEST: " + request_xml)
        try:
            response = requests.post(self._web_api, request_xml,
                                     headers={'content-type': 'application/x-www-form-urlencoded'},
                                     proxies=self._proxies,
                                     cert=self._cert, timeout=self._timeout)
        except Exception as e:
            raise VPOSException("Connection Error while contacting VPOS", traceback.format_exc()) from None
        logging.getLogger(__name__).info("RESPONSE: " + response.text)
        return response.text
