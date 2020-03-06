import re

from VPOSClient.impl.VPosConfig import VPosConfig
from VPOSClient.request.RequestDto import *
from VPOSClient.utils import Constants
from VPOSClient.utils.Constants import *
from VPOSClient.utils.FieldsRegEx import *
from VPOSClient.utils.ProjectException import COFException


def validate_auth_3DS_request(auth3DSRequestDto):
    if not isinstance(auth3DSRequestDto, Auth3DSRequestDto):
        raise COFException("invalid request type")

    _validate_common_fields(auth3DSRequestDto)

    if auth3DSRequestDto.pan is None or not re.search(get_pan_Reg_Ex(), auth3DSRequestDto.pan):
        raise COFException("invalid pan")

    if auth3DSRequestDto.exp_date is None or not re.search(get_exp_date_Reg_Ex(), auth3DSRequestDto.exp_date):
        raise COFException("invalid exp date")

    if auth3DSRequestDto.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                                  auth3DSRequestDto.accounting_mode):
        raise COFException("invalid accounting mode")

    if auth3DSRequestDto.network is None or not re.search(get_network_Reg_Ex(), auth3DSRequestDto.network):
        raise COFException("invalid network ")

    if auth3DSRequestDto.is_master_pass is None or not isinstance(auth3DSRequestDto.is_master_pass, bool):
        raise COFException("invalid is master pass")

    if auth3DSRequestDto.amount is None or not re.search(get_amount_Reg_Ex(), auth3DSRequestDto.amount):
        raise COFException("invalid amount pass")

    if auth3DSRequestDto.currency is None or not re.search(get_currency_Reg_Ex(), auth3DSRequestDto.currency):
        raise COFException("invalid currency pass")


def validate_order_status_request(order_status_request):
    if order_status_request.order_id is None or not re.search(get_order_id_Reg_Ex(), order_status_request.order_id):
        raise COFException("invalid order Id")

    if order_status_request.operator_id is None or not re.search(get_operator_id_Reg_Ex(),
                                                                 order_status_request.operator_id):
        raise COFException("invalid operator Id")

    if order_status_request.product_ref is not None and not re.search(get_product_ref_Reg_Ex(),
                                                                      order_status_request.product_ref):
        raise COFException("invalid product ref")


def validate_refund_payment_request(refund_request):
    if not isinstance(refund_request, RefundRequest):
        raise COFException("invalid request type")

    _validate_common_fields(refund_request)

    if refund_request.transaction_id is None:
        raise COFException("invalid transaction Id")

    if refund_request.amount is None or not re.search(get_amount_Reg_Ex(), refund_request.amount):
        raise COFException("invalid amount")

    _validate_currency_and_exponent(refund_request)


def validate_verify_payment_request(original_req_ref_num, shop_id, operator_id):
    if shop_id is None or not re.search(get_shop_id_Reg_Ex(), shop_id):
        raise COFException("invalid shop Id")

    if original_req_ref_num is None or not re.search(get_req_ref_num_Reg_EX(), original_req_ref_num):
        raise COFException("invalid original req ref num")

    if operator_id is None or not re.search(get_operator_id_Reg_Ex(), operator_id):
        raise COFException("invalid operator Id")


def validate_capture_request(capture_request):
    if not isinstance(capture_request, CaptureRequest):
        raise COFException("invalid request type")

    _validate_common_fields(capture_request)
    _validate_currency_and_exponent(capture_request)

    if capture_request.transaction_id is None:
        raise COFException("invalid transaction Id")

    if capture_request.amount is None or not re.search(get_amount_Reg_Ex(),
                                                       capture_request.amount):
        raise COFException("invalid amount")


def validate_start_3DS_auth_step2(auth_3DS_step2_request_dto):
    if not isinstance(auth_3DS_step2_request_dto, Auth3DSStep2RequestDto):
        raise COFException("invalid request type")

    _validate_common_fields(auth_3DS_step2_request_dto)

    if auth_3DS_step2_request_dto.original_req_ref_num is None or not re.search(get_req_ref_num_Reg_EX(),
                                                                                auth_3DS_step2_request_dto.original_req_ref_num):
        raise COFException("invalid original req ref num")

    if auth_3DS_step2_request_dto.pares is None or not re.search(get_pares_Reg_Ex(), auth_3DS_step2_request_dto.pares):
        raise COFException("invalid pares")

    if auth_3DS_step2_request_dto.acquirer is not None and not re.search(get_acquirer_Reg_Ex(),
                                                                         auth_3DS_step2_request_dto.acquirer):
        raise COFException("invalid acquirer")


def _validate_common_fields(request):
    if request.order_id is None or not re.search(get_order_id_Reg_Ex(), request.order_id):
        raise COFException("invalid order Id")

    if request.operator_id is None or not re.search(get_operator_id_Reg_Ex(),
                                                    request.operator_id):
        raise COFException("invalid operator Id")


def _validate_currency_and_exponent(request):
    if request.currency is None or not re.search(get_currency_Reg_Ex(), request.currency):
        raise COFException("invalid currency")

    if request.currency != getEurCurrencyName() and request.exponent is None:
        raise COFException("invalid or missing exponent")


def validate_redirect_request(request):
    if not isinstance(request, PaymentInfo):
        raise COFException("invalid request type")

    if request.amount is None or not re.search(get_amount_Reg_Ex(),
                                               request.amount):
        raise COFException("invalid amount")

    if request.currency is None or not re.search(get_currency_Reg_Ex(), request.currency):
        raise COFException("invalid currency")

    if request.order_id is None or not re.search(get_order_id_Reg_Ex(), request.order_id):
        raise COFException("invalid order Id")

    if request.url_back is None:
        raise COFException("missing url back")

    if request.url_done is None:
        raise COFException("missing url done")

    if request.url_ms is None:
        raise COFException("missing url ms")

    if request.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                        request.accounting_mode):
        raise COFException("invalid accounting mode")

    if request.author_mode is None or not re.search(get_author_mode_Reg_Ex(),
                                                    request.author_mode):
        raise COFException("invalid accounting mode")


def validate_config(config):
    invalid_fields = []
    if not isinstance(config, VPosConfig):
        raise COFException("invalid config object")
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
        raise COFException("Invalid or missing config params: " + str(invalid_fields))
