class Auth3DSRequestDto:
    def __init__(self, shop_id, order_id, operator_id, pan, exp_date, amount, currency, accounting_mode, network,
                 isMasterPass):
        # COMPULSORY PROPERTY
        self.is_master_pass = isMasterPass
        self.shop_id = shop_id
        self.order_id = order_id
        self.operator_id = operator_id
        self.pan = pan
        self.exp_date = exp_date
        self.amount = amount
        self.currency = currency
        self.accounting_mode = accounting_mode
        self.network = network
        # NOT COMPULSORY
        self.cvv2 = None
        self.exponent = None
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
        self.create_pan_alias = None
        self.in_person = None
        self.merchant_url = None
        self.service = None
        self.xId = None
        self.cavv = None
        self.eci = None
        self.pp_authenticate_method = None
        self.card_enroll_method = None
        self.pares_status = None
        self.scen_roll_status = None
        self.signature_verification = None


class Auth3DSStep2RequestDto:
    def __init__(self, shop_id, order_id, operator_id, original_req_ref_num, pares):
        self.shop_id = shop_id
        self.order_id = order_id
        self.operator_id = operator_id
        self.original_req_ref_num = original_req_ref_num
        self.pares = pares
        self.acquirer = None
        self.options = None


class PaymentRequestDto:
    def __init__(self, shop_id, url_back, url_done, url_ms, amount, currency, exponent, order_id, accountingMode,
                 authorMode):
        self.shop_id = shop_id
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


class VerifyPaymentRequestDto:
    def __init__(self, original_req_ref_num, shop_id, operator_id, options=None):
        self.original_req_ref_num = original_req_ref_num
        self.shop_id = shop_id
        self.operator_id = operator_id
        self.options = options


class ConfirmTransactionRequestDto:
    def __init__(self, transaction_id, amount, currency, order_id, shop_id, operator_id, exponent=None, op_descr=None,
                 options=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency
        self.exponent = exponent
        self.order_id = order_id
        self.shop_id = shop_id
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


class RefundRequestDto:
    def __init__(self, transaction_id, order_id, amount, currency, shop_id, operator_id, exponent=None , op_descr=None,
                      options=None):
        self.transaction_id = transaction_id
        self.order_id = order_id
        self.amount = amount
        self.currency = currency
        self.exponent = exponent
        self.shop_id = shop_id
        self.operator_id = operator_id
        self.op_descr = op_descr
        self.options = options