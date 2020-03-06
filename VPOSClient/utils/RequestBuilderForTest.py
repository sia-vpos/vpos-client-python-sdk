from VPOSClient.request.RequestDto import *


def build_start_3DS_Auth_Request(shop_id, orderId, operatorId, expDate, amount, currency, accountingMode):
    step1 = Auth3DSRequestDto(shop_id, orderId, operatorId, "0000409500729966732", expDate, amount, currency, accountingMode, "98",
                              False)
    step1.in_person = "S"
    step1.cvv2 = "111"
    step1.merchant_url = "https://stackoverflow.com/questions/7948494/whats-the-difference-between-a-python-module-and-a-python-package"
    return step1


def build_get_html_payment_Request(shop_id, url_back, url_done, url_ms, amount, currency, exponent, order_id, accountingMode,
                 authorMode):
    request = PaymentInfo(shop_id, url_back, url_done, url_ms, amount, currency, exponent, order_id, accountingMode,
                          authorMode)
    request.options = "GM"
    return request


def build_confirm_transaction(transaction_id, amount, currency, order_id, shop_id, operator_id):
    return CaptureRequest(transaction_id, amount, currency, order_id, shop_id, operator_id)


def build_refund_request(transaction_id, order_id, amount, currency, shop_id, operator_id):
    return RefundRequest(transaction_id, order_id, amount, currency, shop_id, operator_id)


def get_separator(name):
    print(
        "###################################################################################################################\n"
        + "\t\t\t\tTEST  "+name+"\n"
          "###################################################################################################################\n")