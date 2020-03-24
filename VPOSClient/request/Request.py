import json


class PaymentInfo:
    def __init__(self, url_back, url_done, url_ms, amount, currency, exponent, order_id, accountingMode,
                 authorMode):
        self.url_back = url_back
        self.url_done = url_done
        self.url_ms = url_ms

        self.amount = amount
        self.currency = currency
        self.exponent = exponent
        self.order_id = order_id
        self.accounting_mode = accountingMode
        self.author_mode = authorMode

        self.data_3DS_json = None
        self.options = None
        self.name = None
        self.surname = None
        self.tax_id = None
        self.lock_card = None
        self.commis = None
        self.ord_descr = None
        self.VSID = None
        self.op_descr = None
        self.remaining_duration = None
        self.user_id = None
        self.bb_poste_pay = None
        self.bp_cards = None
        self.phone_number = None
        self.causation = None
        self.user = None
        self.product_ref = None
        self.anti_fraud = None
        self.lang = None
        self.shop_email = None


class ThreeDSAuthorization0Request:
    def __init__(self, order_id, operator_id, pan, exp_date, network, amount, currency, accounting_mode, three_ds_data,
                 notify_url):
        self.order_id = order_id
        self.operator_id = operator_id
        self.pan = pan
        self.exp_date = exp_date
        self.network = network
        self.amount = amount
        self.currency = currency
        self.exponent = None
        self.accounting_mode = accounting_mode
        self.cvv2 = None
        self.email_ch = None
        self.name_ch = None
        self.user_id = None
        self.acquirer = None
        self.ip_address = None
        self.usr_auth_flag = None
        self.op_descr = None
        self.anti_fraud = None
        self.product_ref = None
        self.name = None
        self.surname = None
        self.tax_id = None
        self.create_pan_alias = None
        self.three_ds_data = three_ds_data
        self.notify_url = notify_url
        self.c_prof = None
        self.three_ds_mtd_notify_url = None
        self.challenge_win_size = None
        self.merchant_key = None
        self.options = None


class ThreeDSAuthorization1Request:
    def __init__(self, operator_id, three_DS_trans_id, three_DS_Mtd_compl_ind):
        self.operator_id = operator_id
        self.three_DS_trans_id = three_DS_trans_id
        self.three_DS_Mtd_compl_ind = three_DS_Mtd_compl_ind


class ThreeDSAuthorization2Request:
    def __init__(self, operator_id, three_DS_trans_id):
        self.operator_id = operator_id
        self.three_DS_trans_id = three_DS_trans_id


class CaptureRequest:
    def __init__(self, transaction_id, amount, currency, order_id, operator_id, exponent=None, op_descr=None,
                 options=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.exponent = exponent
        self.order_id = order_id
        self.operator_id = operator_id
        self.options = options
        self.op_descr = op_descr


class Data3DSJsonDto:
    def __init__(self, data3ds):
        data3ds_dict = dict(data3ds)
        self.browserAcceptHeader = data3ds_dict.get("browserAcceptHeader")
        self.browserIP = data3ds_dict.get("browserIP")
        self.browserJavaEnabled = data3ds_dict.get("browserJavaEnabled")
        self.browserLanguage = data3ds_dict.get("browserLanguage")
        self.browserColorDepth = data3ds_dict.get("browserColorDepth")
        self.browserScreenHeight = data3ds_dict.get("browserScreenHeight")
        self.browserScreenWidth = data3ds_dict.get("browserScreenWidth")
        self.browserTZ = data3ds_dict.get("browserTZ")
        self.browserUserAgent = data3ds_dict.get("browserUserAgent")
        self.threeDSRequestorChallengeInd = data3ds_dict.get("threeDSRequestorChallengeInd")
        self.addrMatch = data3ds_dict.get("addrMatch")
        self.chAccAgeInd = data3ds_dict.get("chAccAgeInd")
        self.chAccChange = data3ds_dict.get("chAccChange")
        self.chAccChangeInd = data3ds_dict.get("chAccChangeInd")
        self.chAccDate = data3ds_dict.get("chAccDate")
        self.chAccPwChange = data3ds_dict.get("chAccPwChange")
        self.chAccPwChangeInd = data3ds_dict.get("chAccPwChangeInd")
        self.nbPurchaseAccount = data3ds_dict.get("nbPurchaseAccount")
        self.txnActivityDay = data3ds_dict.get("txnActivityDay")
        self.txnActivityYear = data3ds_dict.get("txnActivityYear")
        self.shipAddressUsage = data3ds_dict.get("shipAddressUsage")
        self.shipAddressUsageInd = data3ds_dict.get("shipAddressUsageInd")
        self.shipNameIndicator = data3ds_dict.get("shipNameIndicator")
        self.acctID = data3ds_dict.get("acctID")
        self.billAddrCity = data3ds_dict.get("billAddrCity")
        self.billAddrCountry = data3ds_dict.get("billAddrCountry")
        self.billAddrLine1 = data3ds_dict.get("billAddrLine1")
        self.billAddrLine2 = data3ds_dict.get("billAddrLine2")
        self.billAddrLine3 = data3ds_dict.get("billAddrLine3")
        self.billAddrPostCode = data3ds_dict.get("billAddrPostCode")
        self.billAddrState = data3ds_dict.get("billAddrState")
        self.homePhone = data3ds_dict.get("homePhone")
        self.mobilePhone = data3ds_dict.get("mobilePhone")
        self.shipAddrCity = data3ds_dict.get("shipAddrCity")
        self.shipAddrCountry = data3ds_dict.get("shipAddrCountry")
        self.shipAddrLine1 = data3ds_dict.get("shipAddrLine1")
        self.shipAddrLine2 = data3ds_dict.get("shipAddrLine2")
        self.shipAddrLine3 = data3ds_dict.get("shipAddrLine3")
        self.shipAddrPostCode = data3ds_dict.get("shipAddrPostCode")
        self.shipAddrState = data3ds_dict.get("shipAddrState")
        self.workPhone = data3ds_dict.get("workPhone")
        self.deliveryEmailAddress = data3ds_dict.get("deliveryEmailAddress")
        self.deliveryTimeFrame = data3ds_dict.get("deliveryTimeFrame")
        self.preOrderDate = data3ds_dict.get("preOrderDate")
        self.preOrderPurchaseInd = data3ds_dict.get("preOrderPurchaseInd")
        self.reorderItemsInd = data3ds_dict.get("reorderItemsInd")
        self.shipIndicator = data3ds_dict.get("shipIndicator")

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(json_dict)

    def toJson(self):
        sb = "{"
        json_Dict = self.__dict__
        for attribute_key in json_Dict.keys():
            if json_Dict.get(attribute_key) is not None:
                sb = sb + "\""
                sb = sb + attribute_key
                sb = sb + "\":\""
                sb = sb + json_Dict.get(attribute_key)
                sb = sb + "\","
        sb = sb[:-1]
        sb = sb + "}"
        return sb


class OrderStatusRequest:
    def __init__(self, order_id, operator_id, product_ref=None, options=None):
        self.order_id = order_id
        self.operator_id = operator_id
        self.product_ref = product_ref
        self.options = options


class RefundRequest:
    def __init__(self, transaction_id, order_id, amount, currency, operator_id, exponent=None, op_descr=None,
                 options=None):
        self.transaction_id = transaction_id
        self.order_id = order_id
        self.amount = amount
        self.currency = currency
        self.exponent = exponent
        self.operator_id = operator_id
        self.op_descr = op_descr
        self.options = options


class AuthorizationRequest:
    def __init__(self, order_id, operator_id, pan, exp_date, amount, currency, accounting_mode, network):
        self.order_id = order_id
        self.operator_id = operator_id
        self.pan = pan
        self.cvv2 = None
        self.create_pan_alias = None
        self.exp_date = exp_date
        self.amount = amount
        self.currency = currency
        self.exponent = None
        self.accounting_mode = accounting_mode
        self.network = network
        self.email_ch = None
        self.user_id = None
        self.acquirer = None
        self.ip_address = None
        self.usr_auth_flag = None
        self.op_descr = None
        self.options = None
        self.anti_fraud = None
        self.product_ref = None
        self.name = None
        self.surname = None
        self.tax_id = None
