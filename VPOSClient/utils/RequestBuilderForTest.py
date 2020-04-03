from VPOSClient.request.Request import *

data_redirect = """{"addrMatch":"N","chAccAgeInd":"04","chAccChange":"20190211","chAccChangeInd":"03","chAccDate":"20190210","chAccPwChange":"20190214","chAccPwChangeInd":"04","nbPurchaseAccount":"1000","txnActivityDay":"100","txnActivityYear":"100","shipAddressUsage":"20181220","shipAddressUsageInd":"03","shipNameIndicator":"01","billAddrCity":"billAddrCity","billAddrCountry":"004","billAddrLine1":"billAddrLine1","billAddrLine2":"billAddrLine2","billAddrLine3":"billAddrLine3","billAddrPostCode":"billAddrPostCode","billAddrState":"MI","homePhone":"39-321818198","mobilePhone":"33-312","shipAddrCity":"zio","shipAddrCountry":"008","shipAddrLine1":"shipAddrLine1","shipAddrLine2":"shipAddrLine2","shipAddrLine3":"shipAddrLine3","shipAddrPostCode\":\"shipAddrPostCode","shipAddrState":"222","workPhone":"39-0321818198","deliveryEmailAddress":"a-b@example.com","deliveryTimeframe":"02","preOrderDate":"20181220","preOrderPurchaseInd":"01","reorderItemsInd":"02","shipIndicator":"01"}"""

data = """{
"addrMatch":"N",
"chAccAgeInd":"04",
"chAccChange":"20190211",
"chAccChangeInd":"03",
"chAccDate":"20190210",
"chAccPwChange":"20190214",
"chAccPwChangeInd":"04",
"nbPurchaseAccount":"1000",
"txnActivityDay":"100",
"txnActivityYear":"100",
"shipAddressUsage":"20181220",
"shipAddressUsageInd":"03",
"shipNameIndicator":"01",
"billAddrCity":"billAddrCity",
"billAddrCountry":"004",
"billAddrLine1":"billAddrLine1",
"billAddrLine2":"billAddrLine2",
"billAddrLine3":"billAddrLine3",
"billAddrPostCode":"billAddrPostCode",
"billAddrState":"11",
"homePhone":"039-321818198111",
"mobilePhone":"33-312",
"shipAddrCity":"zio",
"shipAddrCountry":"008",
"shipAddrLine1":"shipAddrLine1",
"shipAddrLine2":"shipAddrLine2",
"shipAddrLine3":"shipAddrLine3",
"shipAddrPostCode":"shipAddrPostCode",
"shipAddrState":"222",
"workPhone":"39-0321818198",
"deliveryEmailAddress":"a-b@example.com",
"deliveryTimeframe":"02",
"preOrderDate":"20181220",
"preOrderPurchaseInd":"01",
"reorderItemsInd":"02",
"shipIndicator":"01",
"browserAcceptHeader":"text/html,application/xhtml+xml,application/xml;",
"browserIP":"10.42.195.152",
"browserJavaEnabled":"true",
"browserLanguage":"it-IT",
"browserColorDepth":"16",
"browserScreenHeight":"1024",
"browserScreenWidth":"1920",
"browserTZ":"-120",
"browserUserAgent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
}
"""


def build_threeDS_authorize0(order_id, operator_id, pan, exp_date, network, amount, currency, accounting_mode,
                             notify_url):
    data3ds = Data3DSJsonDto.from_json(data)
    step1 = ThreeDSAuthorization0Request(order_id, operator_id, pan, exp_date, "01", amount, currency, "I", data3ds,
                                         notify_url)
    step1.cvv2 = "111"
    step1.exponent = "2"
    step1.email_ch = "email@gmail.com"
    step1.name_ch = "Mario"
    step1.name = "Mario"

    step1.three_ds_mtd_notify_url = "https://atpostest.ssb.it/atpos/apibo/en/3ds-notification.html"
    return step1


def build_threeDS_authorize1(operator_id, three_ds_transId):
    step2 = ThreeDSAuthorization1Request(operator_id, three_ds_transId, 'N')
    return step2


def build_get_html_payment_Request(url_back, url_done, url_ms, amount, currency, exponent, order_id, accountingMode,
                                   authorMode):
    request = PaymentInfo(url_back, url_done, url_ms, amount, currency, exponent, order_id, accountingMode,
                          authorMode)
    request.data_3DS_json = Data3DSJsonDto.from_json(data_redirect)
    request.options = "M"
    request.t_recurr = "U"

    return request


def build_get_html_payment_token_Request(url_back, url_done, url_ms, amount, currency, exponent, order_id,
                                         accountingMode,
                                         authorMode):
    request = PaymentInfo(url_back, url_done, url_ms, amount, currency, exponent, order_id, accountingMode,
                          authorMode)
    request.data_3DS_json = Data3DSJsonDto.from_json(data_redirect)
    request.token = "0000500550493297466"
    request.exp_date = "2112"
    request.t_recurr = "U"
    request.c_recurr = "899107067200401"
    request.name_ch = "Mario"
    request.surname_ch = "Rossi"
    request.network = "98"
    request.email = "test@tes.it"
    request.shop_email = "test@tes.it"
    return request


def build_confirm_transaction(transaction_id, amount, currency, order_id, operator_id):
    return CaptureRequest(transaction_id, amount, currency, order_id, operator_id)


def build_refund_request(transaction_id, order_id, amount, currency, operator_id):
    return RefundRequest(transaction_id, order_id, amount, currency, operator_id)


def build_authorize(order_id):
    auth = AuthorizationRequest(order_id, "OPERATOR", "4598250000000027", "2112", "6000", "978", "I", "93")
    auth.cvv2 = "111"
    auth.email_ch = "dsdsd@gmail.it"
    return auth


def get_separator(name):
    print(
        "###################################################################################################################\n"
        + "\t\t\t\tTEST  " + name + "\n"
                                    "###################################################################################################################\n")


def build_threeDS_authorize2(order_id, operator_id, three_DS_trans_id):
    return ThreeDSAuthorization2Request(order_id, operator_id, three_DS_trans_id);
