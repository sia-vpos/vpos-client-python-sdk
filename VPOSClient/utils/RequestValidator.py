import re

from VPOSClient.impl.VPosConfig import VPosConfig
from VPOSClient.request.Request import *
from VPOSClient.utils import Constants
from VPOSClient.utils.Constants import *
from VPOSClient.utils.FieldsRegEx import *
from VPOSClient.utils.ProjectException import VPOSException


def validate_order_status_request(order_status_request):
    invalid_fields = []
    _validate_common_fields(order_status_request, invalid_fields)

    if order_status_request.product_ref is not None and not re.search(get_product_ref_Reg_Ex(),
                                                                      order_status_request.product_ref):
        invalid_fields.append(Constants.getProductRefName())

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def validate_refund_payment_request(refund_request):
    invalid_fields = []
    if not isinstance(refund_request, RefundRequest):
        raise VPOSException("invalid request type")

    _validate_common_fields(refund_request, invalid_fields)

    if refund_request.transaction_id is None:
        invalid_fields.append(Constants.getTransactionIdName())

    if refund_request.amount is None or not re.search(get_amount_Reg_Ex(), refund_request.amount):
        invalid_fields.append(Constants.getAmountName())

    _validate_currency_and_exponent(refund_request, invalid_fields)

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def validate_capture_request(capture_request):
    invalid_fields = []
    if not isinstance(capture_request, CaptureRequest):
        raise VPOSException("invalid request type")

    _validate_common_fields(capture_request, invalid_fields)
    _validate_currency_and_exponent(capture_request, invalid_fields)

    if capture_request.transaction_id is None:
        invalid_fields.append(Constants.getTransactionIdName())

    if capture_request.amount is None or not re.search(get_amount_Reg_Ex(),
                                                       capture_request.amount):
        invalid_fields.append(Constants.getAmountName())

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def _validate_common_fields(request, invalid_fields):
    if request.order_id is None or not re.search(get_order_id_Reg_Ex(), request.order_id):
        invalid_fields.append(Constants.getOrderIdName())

    if request.operator_id is None or not re.search(get_operator_id_Reg_Ex(),
                                                    request.operator_id):
        invalid_fields.append(Constants.getOperatorIdName())


def _validate_currency_and_exponent(request, invalid_fields):
    if request.currency is None or not re.search(get_currency_Reg_Ex(), request.currency):
        invalid_fields.append(Constants.getCurrencyName())

    if request.currency != getEurCurrencyName() and request.exponent is None:
        invalid_fields.append(Constants.getExponentName())


def validate_redirect_request(request):
    invalid_fields = []
    if not isinstance(request, PaymentInfo):
        raise VPOSException("invalid request type")

    if request.amount is None or not re.search(get_amount_Reg_Ex(),
                                               request.amount):
        invalid_fields.append(Constants.getAmountName())

    if request.currency is None or not re.search(get_currency_Reg_Ex(), request.currency):
        invalid_fields.append(Constants.getCurrencyName())

    if request.order_id is None or not re.search(get_order_id_Reg_Ex(), request.order_id):
        invalid_fields.append(Constants.getOrderIdName())

    if request.url_back is None:
        invalid_fields.append(Constants.getUrlBackName())

    if request.url_done is None:
        invalid_fields.append(Constants.getUrlDoneName())

    if request.url_ms is None:
        invalid_fields.append(Constants.getUrlMsName())

    if request.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                        request.accounting_mode):
        invalid_fields.append(Constants.getAccountingModeName())

    if request.author_mode is None or not re.search(get_author_mode_Reg_Ex(),
                                                    request.author_mode):
        invalid_fields.append(Constants.getAuthorModeName())

    if request.token is not None and (
            request.email is None or request.surname_ch is None or request.name_ch is None or request.network is None or request.exp_date is None):
        raise VPOSException(
            "Invalid or missing config params: For token payments name_ch, surname_ch, email, exp_date, network are required")

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def validate_config(config):
    invalid_fields = []
    if not isinstance(config, VPosConfig):
        raise VPOSException("invalid config object")
    if config.shop_id is None or not re.search(get_shop_id_Reg_Ex(), config.shop_id):
        invalid_fields.append(Constants.getShopIdName())
    if config.api_key is None:
        invalid_fields.append(Constants.getApiKeyName())
    if config.api_url is None:
        invalid_fields.append(Constants.getApiUrlName())
    if config.redirect_key is None:
        invalid_fields.append(Constants.getRedirectKeyName())
    if config.redirect_url is None:
        invalid_fields.append(Constants.getRedirectUrlName())

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def validate_threeDSAuthorization0_request(request):
    invalid_fields = []
    if not isinstance(request, ThreeDSAuthorization0Request):
        raise VPOSException("invalid request type")

    _validate_common_fields(request, invalid_fields)

    if request.pan is None or not re.search(get_pan_Reg_Ex(), request.pan):
        invalid_fields.append(Constants.getPanName())

    if request.exp_date is None or not re.search(get_exp_date_Reg_Ex(), request.exp_date):
        invalid_fields.append(Constants.getExpDateName())

    if request.cvv2 is not None and not re.search(get_cvv2_Reg_Ex(),
                                                  request.cvv2):
        invalid_fields.append(Constants.getCvv2Name())

    if request.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                        request.accounting_mode):
        invalid_fields.append(Constants.getAccountingModeName())

    if request.amount is None or not re.search(get_amount_Reg_Ex(),
                                               request.amount):
        invalid_fields.append(Constants.getAmountName())

    _validate_currency_and_exponent(request, invalid_fields)

    if request.network is None or not re.search(get_network_Reg_Ex(), request.network):
        invalid_fields.append(Constants.getNetworkName())

    if request.email_ch is not None and not re.search(get_email_ch_Reg_Ex(),
                                                      request.email_ch):
        invalid_fields.append(Constants.getEmailChName())

    if request.user_id is not None and not re.search(get_user_id_Reg_Ex(),
                                                     request.user_id):
        invalid_fields.append(Constants.getUserIdName())

    if request.acquirer is not None and not re.search(get_acquirer_Reg_Ex(),
                                                      request.acquirer):
        invalid_fields.append(Constants.getAcquirerName())

    if request.ip_address is not None and not re.search(get_ip_address_Reg_Ex(),
                                                        request.ip_address):
        invalid_fields.append(Constants.getIpAddressName())

    if request.usr_auth_flag is not None and not re.search(get_usr_auth_flag_Reg_Ex(),
                                                           request.usr_auth_flag):
        invalid_fields.append(Constants.getUsrAuthFlagName())

    if request.op_descr is not None and not re.search(get_op_descr_Reg_Ex(),
                                                      request.op_descr):
        invalid_fields.append(Constants.getOpDescrName())

    if request.anti_fraud is not None and not re.search(get_anti_fraud_Reg_Ex(),
                                                        request.anti_fraud):
        invalid_fields.append(Constants.getAntiFraudName())

    if request.product_ref is not None and not re.search(get_product_ref_Reg_Ex(),
                                                         request.product_ref):
        invalid_fields.append(Constants.getProductRefName())

    if request.name is not None and not re.search(get_name_Reg_Ex(),
                                                  request.name):
        invalid_fields.append(Constants.getNameName())

    if request.surname is not None and not re.search(get_surname_Reg_Ex(),
                                                     request.surname):
        invalid_fields.append(Constants.getSurnameName())

    if request.tax_id is not None and not re.search(get_tax_id_Reg_Ex(),
                                                    request.tax_id):
        invalid_fields.append(Constants.getTaxIdName())

    if request.three_ds_data is None or not isinstance(request.three_ds_data, Data3DSJsonDto):
        invalid_fields.append(Constants.getThreeDSDataName())

    if request.notify_url is None:
        invalid_fields.append(Constants.getNotifUrl())

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def validate_threeDSAuthorization1_request(request):
    invalid_fields = []

    if request.operator_id is None or not re.search(get_operator_id_Reg_Ex(), request.operator_id):
        invalid_fields.append(Constants.getOperatorIdName())

    if request.three_DS_trans_id is None:
        invalid_fields.append(Constants.getThreeDSTransIdName())

    if request.three_DS_Mtd_compl_ind is None:
        invalid_fields.append(Constants.getThreeDSMtdComplIndName())

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def validate_threeDSAuthorization2_request(request):
    invalid_fields = []

    if request.operator_id is None or not re.search(get_operator_id_Reg_Ex(), request.operator_id):
        invalid_fields.append(Constants.getOperatorIdName())

    if request.three_DS_trans_id is None:
        invalid_fields.append(Constants.getThreeDSTransIdName())

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))


def validate_authorize(request):
    invalid_fields = []
    if not isinstance(request, AuthorizationRequest):
        raise VPOSException("invalid request type")

    _validate_common_fields(request, invalid_fields)

    if request.pan is None or not re.search(get_pan_Reg_Ex(), request.pan):
        invalid_fields.append(Constants.getPanName())

    if request.exp_date is None or not re.search(get_exp_date_Reg_Ex(), request.exp_date):
        invalid_fields.append(Constants.getExpDateName())

    if request.cvv2 is not None and not re.search(get_cvv2_Reg_Ex(),
                                                  request.cvv2):
        invalid_fields.append(Constants.getCvv2Name())

    if request.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                        request.accounting_mode):
        invalid_fields.append(Constants.getAccountingModeName())

    if request.amount is None or not re.search(get_amount_Reg_Ex(),
                                               request.amount):
        invalid_fields.append(Constants.getAmountName())

    _validate_currency_and_exponent(request, invalid_fields)

    if request.network is None or not re.search(get_network_Reg_Ex(), request.network):
        invalid_fields.append(Constants.getNetworkName())

    if request.email_ch is not None and not re.search(get_email_ch_Reg_Ex(),
                                                      request.email_ch):
        invalid_fields.append(Constants.getEmailChName())

    if request.user_id is not None and not re.search(get_user_id_Reg_Ex(),
                                                     request.user_id):
        invalid_fields.append(Constants.getUserIdName())

    if request.acquirer is not None and not re.search(get_acquirer_Reg_Ex(),
                                                      request.acquirer):
        invalid_fields.append(Constants.getAcquirerName())

    if request.ip_address is not None and not re.search(get_ip_address_Reg_Ex(),
                                                        request.ip_address):
        invalid_fields.append(Constants.getIpAddressName())

    if request.usr_auth_flag is not None and not re.search(get_usr_auth_flag_Reg_Ex(),
                                                           request.usr_auth_flag):
        invalid_fields.append(Constants.getUsrAuthFlagName())

    if request.op_descr is not None and not re.search(get_op_descr_Reg_Ex(),
                                                      request.op_descr):
        invalid_fields.append(Constants.getOpDescrName())

    if request.anti_fraud is not None and not re.search(get_anti_fraud_Reg_Ex(),
                                                        request.anti_fraud):
        invalid_fields.append(Constants.getAntiFraudName())

    if request.product_ref is not None and not re.search(get_product_ref_Reg_Ex(),
                                                         request.product_ref):
        invalid_fields.append(Constants.getProductRefName())

    if request.name is not None and not re.search(get_name_Reg_Ex(),
                                                  request.name):
        invalid_fields.append(Constants.getNameName())

    if request.surname is not None and not re.search(get_surname_Reg_Ex(),
                                                     request.surname):
        invalid_fields.append(Constants.getSurnameName())

    if request.tax_id is not None and not re.search(get_tax_id_Reg_Ex(),
                                                    request.tax_id):
        invalid_fields.append(Constants.getTaxIdName())

    if len(invalid_fields) > 0:
        raise VPOSException("Invalid or missing config params: " + str(invalid_fields))
