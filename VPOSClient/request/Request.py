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
    def __init__(self):
        self.three_DS_requestor_challenge_ind = None
        self.addr_match = None
        self.ch_acc_age_ind = None
        self.ch_acc_change = None
        self.ch_acc_change_ind = None
        self.ch_acc_date = None
        self.ch_acc_pw_change = None
        self.ch_acc_pw_change_ind = None
        self.nb_purchase_account = None
        self.txn_activity_day = None
        self.txn_activity_year = None
        self.ship_address_usage = None
        self.ship_address_usage_ind = None
        self.ship_name_indicator = None
        self.acct_iD = None
        self.bill_addr_city = None
        self.bill_addr_country = None
        self.bill_addr_line1 = None
        self.bill_addr_line2 = None
        self.bill_addr_line3 = None
        self.bill_addr_post_code = None
        self.bill_addr_state = None
        self.home_phone = None
        self.mobile_phone = None
        self.ship_addr_city = None
        self.ship_addr_country = None
        self.ship_addr_line1 = None
        self.ship_addr_line2 = None
        self.ship_addr_line3 = None
        self.ship_addr_postCode = None
        self.ship_addr_state = None
        self.work_phone = None
        self.delivery_email_address = None
        self.delivery_time_frame = None
        self.pre_order_date = None
        self.pre_order_purchase_ind = None

    def toJson(self):
        to_remove = []
        json_Dict = self.__dict__
        for attribute_key in json_Dict.keys():
            if json_Dict.get(attribute_key) is None:
                to_remove.append(attribute_key)
        for attribute_key in to_remove:
            json_Dict.pop(attribute_key)
        return str(json_Dict)


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
