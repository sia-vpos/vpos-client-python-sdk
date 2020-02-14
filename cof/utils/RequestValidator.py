import re

from cof.dto.RequestDto import *
from cof.utils.Constants import *
from cof.utils.FieldsRegEx import *
from cof.utils.ProjectException import COFException


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


def validate_order_status_request(order_id, product_ref, shop_id, operator_id):
    if order_id is None or not re.search(get_order_id_Reg_Ex(), order_id):
        raise COFException("invalid order Id")

    if shop_id is None or not re.search(get_shop_id_Reg_Ex(), shop_id):
        raise COFException("invalid shop Id")

    if operator_id is None or not re.search(get_operator_id_Reg_Ex(), operator_id):
        raise COFException("invalid operator Id")

    if product_ref is not None and not re.search(get_product_ref_Reg_Ex(), product_ref):
        raise COFException("invalid product ref")


def validate_refund_payment_request(refund_request_dto):
    if not isinstance(refund_request_dto, RefundRequestDto):
        raise COFException("invalid request type")

    _validate_common_fields(refund_request_dto)

    if refund_request_dto.transaction_id is None:
        raise COFException("invalid transaction Id")

    if refund_request_dto.amount is None or not re.search(get_amount_Reg_Ex(), refund_request_dto.amount):
        raise COFException("invalid amount")

    _validate_currency_and_exponent(refund_request_dto)


def validate_verify_payment_request(original_req_ref_num, shop_id, operator_id):
    if shop_id is None or not re.search(get_shop_id_Reg_Ex(), shop_id):
        raise COFException("invalid shop Id")

    if original_req_ref_num is None or not re.search(get_req_ref_num_Reg_EX(), original_req_ref_num):
        raise COFException("invalid original req ref num")

    if operator_id is None or not re.search(get_operator_id_Reg_Ex(), operator_id):
        raise COFException("invalid operator Id")


def validate_confirm_transaction_request(confirmTransactionRequestDto):
    if not isinstance(confirmTransactionRequestDto, ConfirmTransactionRequestDto):
        raise COFException("invalid request type")

    _validate_common_fields(confirmTransactionRequestDto)
    _validate_currency_and_exponent(confirmTransactionRequestDto)

    if confirmTransactionRequestDto.transaction_id is None:
        raise COFException("invalid transaction Id")

    if confirmTransactionRequestDto.amount is None or not re.search(get_amount_Reg_Ex(),
                                                                    confirmTransactionRequestDto.amount):
        raise COFException("invalid amount")


def validate_confirm_payment_request(confirm_payment_request_dto):
    if not isinstance(confirm_payment_request_dto, ConfirmPaymentRequestDto):
        raise COFException("invalid request type")

    _validate_common_fields(confirm_payment_request_dto)
    _validate_currency_and_exponent(confirm_payment_request_dto)
    if confirm_payment_request_dto.transaction_id is None:
        raise COFException("invalid transaction Id")

    if confirm_payment_request_dto.accounting_mode is None or not re.search(get_accounting_mode_Reg_Ex(),
                                                                            confirm_payment_request_dto.accounting_mode):
        raise COFException("invalid accounting mode")

    if confirm_payment_request_dto.close_order is None or not re.search(get_close_order_Reg_Ex(),
                                                                        confirm_payment_request_dto.close_order):
        raise COFException("invalid accounting mode")

    if confirm_payment_request_dto.amount is not None and not re.search(get_amount_Reg_Ex(),
                                                                        confirm_payment_request_dto.amount):
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

    if request.shop_id is None or not re.search(get_shop_id_Reg_Ex(), request.shop_id):
        raise COFException("invalid shop Id")

    if request.operator_id is None or not re.search(get_operator_id_Reg_Ex(),
                                                    request.operator_id):
        raise COFException("invalid operator Id")


def _validate_currency_and_exponent(request):
    if request.currency is None or not re.search(get_currency_Reg_Ex(), request.currency):
        raise COFException("invalid currency")

    if request.currency != getEurCurrencyName() and request.exponent is None:
        raise COFException("invalid or missing exponent")
