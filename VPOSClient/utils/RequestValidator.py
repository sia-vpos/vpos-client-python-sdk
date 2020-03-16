import re

from VPOSClient.impl.VPosConfig import VPosConfig
from VPOSClient.request.RequestDto import *
from VPOSClient.utils import Constants
from VPOSClient.utils.Constants import *
from VPOSClient.utils.FieldsRegEx import *
from VPOSClient.utils.ProjectException import VPOSException


def validate_auth_3DS_request(auth3DSRequestDto):
    if not isinstance(auth3DSRequestDto, Auth3DSRequestDto):
        raise VPOSException("invalid request type")

    _validate_common_fields(auth3DSRequestDto)

    if auth3DSRequestDto.pan is None or not re.search(get_pan_Reg_Ex(), auth3DSRequestDto.pan):
        raise VPOSException("invalid pan")

    if auth3DSRequestDto.exp_date is None or not re.search(get_exp_date_Reg_Ex(), auth3DSRequestDto.exp_date):
        raise VPOSException("invalid exp date")

    if auth3DSRequestDto.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                                  auth3DSRequestDto.accounting_mode):
        raise VPOSException("invalid accounting mode")

    if auth3DSRequestDto.network is None or not re.search(get_network_Reg_Ex(), auth3DSRequestDto.network):
        raise VPOSException("invalid network ")

    if auth3DSRequestDto.is_master_pass is None or not isinstance(auth3DSRequestDto.is_master_pass, bool):
        raise VPOSException("invalid is master pass")

    if auth3DSRequestDto.amount is None or not re.search(get_amount_Reg_Ex(), auth3DSRequestDto.amount):
        raise VPOSException("invalid amount pass")

    if auth3DSRequestDto.currency is None or not re.search(get_currency_Reg_Ex(), auth3DSRequestDto.currency):
        raise VPOSException("invalid currency pass")


def validate_order_status_request(order_status_request):
    if order_status_request.order_id is None or not re.search(get_order_id_Reg_Ex(), order_status_request.order_id):
        raise VPOSException("invalid order Id")

    if order_status_request.operator_id is None or not re.search(get_operator_id_Reg_Ex(),
                                                                 order_status_request.operator_id):
        raise VPOSException("invalid operator Id")

    if order_status_request.product_ref is not None and not re.search(get_product_ref_Reg_Ex(),
                                                                      order_status_request.product_ref):
        raise VPOSException("invalid product ref")


def validate_refund_payment_request(refund_request):
    if not isinstance(refund_request, RefundRequest):
        raise VPOSException("invalid request type")

    _validate_common_fields(refund_request)

    if refund_request.transaction_id is None:
        raise VPOSException("invalid transaction Id")

    if refund_request.amount is None or not re.search(get_amount_Reg_Ex(), refund_request.amount):
        raise VPOSException("invalid amount")

    _validate_currency_and_exponent(refund_request)


def validate_verify_payment_request(original_req_ref_num, shop_id, operator_id):
    if shop_id is None or not re.search(get_shop_id_Reg_Ex(), shop_id):
        raise VPOSException("invalid shop Id")

    if original_req_ref_num is None or not re.search(get_req_ref_num_Reg_EX(), original_req_ref_num):
        raise VPOSException("invalid original req ref num")

    if operator_id is None or not re.search(get_operator_id_Reg_Ex(), operator_id):
        raise VPOSException("invalid operator Id")


def validate_capture_request(capture_request):
    if not isinstance(capture_request, CaptureRequest):
        raise VPOSException("invalid request type")

    _validate_common_fields(capture_request)
    _validate_currency_and_exponent(capture_request)

    if capture_request.transaction_id is None:
        raise VPOSException("invalid transaction Id")

    if capture_request.amount is None or not re.search(get_amount_Reg_Ex(),
                                                       capture_request.amount):
        raise VPOSException("invalid amount")


def validate_start_3DS_auth_step2(auth_3DS_step2_request_dto):
    if not isinstance(auth_3DS_step2_request_dto, Auth3DSStep2RequestDto):
        raise VPOSException("invalid request type")

    _validate_common_fields(auth_3DS_step2_request_dto)

    if auth_3DS_step2_request_dto.original_req_ref_num is None or not re.search(get_req_ref_num_Reg_EX(),
                                                                                auth_3DS_step2_request_dto.original_req_ref_num):
        raise VPOSException("invalid original req ref num")

    if auth_3DS_step2_request_dto.pares is None or not re.search(get_pares_Reg_Ex(), auth_3DS_step2_request_dto.pares):
        raise VPOSException("invalid pares")

    if auth_3DS_step2_request_dto.acquirer is not None and not re.search(get_acquirer_Reg_Ex(),
                                                                         auth_3DS_step2_request_dto.acquirer):
        raise VPOSException("invalid acquirer")


def _validate_common_fields(request):
    if request.order_id is None or not re.search(get_order_id_Reg_Ex(), request.order_id):
        raise VPOSException("invalid order Id")

    if request.operator_id is None or not re.search(get_operator_id_Reg_Ex(),
                                                    request.operator_id):
        raise VPOSException("invalid operator Id")


def _validate_currency_and_exponent(request):
    if request.currency is None or not re.search(get_currency_Reg_Ex(), request.currency):
        raise VPOSException("invalid currency")

    if request.currency != getEurCurrencyName() and request.exponent is None:
        raise VPOSException("invalid or missing exponent")


def validate_redirect_request(request):
    if not isinstance(request, PaymentInfo):
        raise VPOSException("invalid request type")

    if request.amount is None or not re.search(get_amount_Reg_Ex(),
                                               request.amount):
        raise VPOSException("invalid amount")

    if request.currency is None or not re.search(get_currency_Reg_Ex(), request.currency):
        raise VPOSException("invalid currency")

    if request.order_id is None or not re.search(get_order_id_Reg_Ex(), request.order_id):
        raise VPOSException("invalid order Id")

    if request.url_back is None:
        raise VPOSException("missing url back")

    if request.url_done is None:
        raise VPOSException("missing url done")

    if request.url_ms is None:
        raise VPOSException("missing url ms")

    if request.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                        request.accounting_mode):
        raise VPOSException("invalid accounting mode")

    if request.author_mode is None or not re.search(get_author_mode_Reg_Ex(),
                                                    request.author_mode):
        raise VPOSException("invalid accounting mode")


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
    if not isinstance(request, ThreeDSAuthorization0Request):
        raise VPOSException("invalid request type")

    _validate_common_fields(request)

    if request.pan is None or not re.search(get_pan_Reg_Ex(), request.pan):
        raise VPOSException("invalid pan")

    if request.exp_date is None or not re.search(get_exp_date_Reg_Ex(), request.exp_date):
        raise VPOSException("invalid exp date")

    if request.cvv2 is not None and not re.search(get_cvv2_Reg_Ex(),
                                             request.cvv2):
        raise VPOSException("invalid cvv2")

    if request.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                        request.accounting_mode):
        raise VPOSException("invalid accounting mode")

    if request.amount is None or not re.search(get_amount_Reg_Ex(),
                                                        request.amount):
        raise VPOSException("invalid amount")

    _validate_currency_and_exponent(request)

    if request.network is None or not re.search(get_network_Reg_Ex(), request.network):
        raise VPOSException("invalid network ")

    if request.email_ch is not None and not re.search(get_email_ch_Reg_Ex(),
                                             request.email_ch):
        raise VPOSException("invalid email")

    if request.user_id is not None and not re.search(get_user_id_Reg_Ex(),
                                             request.user_id):
        raise VPOSException("invalid user id")

    if request.acquirer is not None and not re.search(get_acquirer_Reg_Ex(),
                                             request.acquirer):
        raise VPOSException("invalid acquirer")

    if request.ip_address is not None and not re.search(get_ip_address_Reg_Ex(),
                                             request.ip_address):
        raise VPOSException("invalid ip address")

    if request.usr_auth_flag is not None and not re.search(get_usr_auth_flag_Reg_Ex(),
                                             request.usr_auth_flag):
        raise VPOSException("invalid usr auth flag")

    if request.op_descr is not None and not re.search(get_op_descr_Reg_Ex(),
                                             request.op_descr):
        raise VPOSException("invalid op descr")

    if request.anti_fraud is not None and not re.search(get_anti_fraud_Reg_Ex(),
                                             request.anti_fraud):
        raise VPOSException("invalid anti_fraud")

    if request.product_ref is not None and not re.search(get_product_ref_Reg_Ex(),
                                             request.product_ref):
        raise VPOSException("invalid product Ref")

    if request.name is not None and not re.search(get_name_Reg_Ex(),
                                             request.name):
        raise VPOSException("invalid name")

    if request.surname is not None and not re.search(get_surname_Reg_Ex(),
                                             request.surname):
        raise VPOSException("invalid surname")

    if request.tax_id is not None and not re.search(get_tax_id_Reg_Ex(),
                                             request.tax_id):
        raise VPOSException("invalid tax id")

    if request.three_ds_data is None or not isinstance(request.three_ds_data, Data3DSJsonDto):
        raise VPOSException("invalid three_ds_data")

    if request.notify_url is None :
        raise VPOSException("invalid notify url")


def validate_authorize(request):
    if not isinstance(request, AuthorizationRequest):
        raise VPOSException("invalid request type")

    _validate_common_fields(request)

    if request.pan is None or not re.search(get_pan_Reg_Ex(), request.pan):
        raise VPOSException("invalid pan")

    if request.exp_date is None or not re.search(get_exp_date_Reg_Ex(), request.exp_date):
        raise VPOSException("invalid exp date")

    if request.cvv2 is not None and not re.search(get_cvv2_Reg_Ex(),
                                                  request.cvv2):
        raise VPOSException("invalid cvv2")

    if request.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                        request.accounting_mode):
        raise VPOSException("invalid accounting mode")

    if request.amount is None or not re.search(get_amount_Reg_Ex(),
                                                        request.amount):
        raise VPOSException("invalid amount")

    _validate_currency_and_exponent(request)

    if request.network is None or not re.search(get_network_Reg_Ex(), request.network):
        raise VPOSException("invalid network ")

    if request.email_ch is not None and not re.search(get_email_ch_Reg_Ex(),
                                             request.email_ch):
        raise VPOSException("invalid email")

    if request.user_id is not None and not re.search(get_user_id_Reg_Ex(),
                                             request.user_id):
        raise VPOSException("invalid user id")

    if request.acquirer is not None and not re.search(get_acquirer_Reg_Ex(),
                                             request.acquirer):
        raise VPOSException("invalid acquirer")

    if request.ip_address is not None and not re.search(get_ip_address_Reg_Ex(),
                                             request.ip_address):
        raise VPOSException("invalid ip address")

    if request.usr_auth_flag is not None and not re.search(get_usr_auth_flag_Reg_Ex(),
                                             request.usr_auth_flag):
        raise VPOSException("invalid usr auth flag")

    if request.op_descr is not None and not re.search(get_op_descr_Reg_Ex(),
                                             request.op_descr):
        raise VPOSException("invalid op descr")

    if request.anti_fraud is not None and not re.search(get_anti_fraud_Reg_Ex(),
                                             request.anti_fraud):
        raise VPOSException("invalid anti_fraud")

    if request.product_ref is not None and not re.search(get_product_ref_Reg_Ex(),
                                             request.product_ref):
        raise VPOSException("invalid product Ref")

    if request.name is not None and not re.search(get_name_Reg_Ex(),
                                             request.name):
        raise VPOSException("invalid name")

    if request.surname is not None and not re.search(get_surname_Reg_Ex(),
                                             request.surname):
        raise VPOSException("invalid surname")

    if request.tax_id is not None and not re.search(get_tax_id_Reg_Ex(),
                                             request.tax_id):
        raise VPOSException("invalid tax id")
