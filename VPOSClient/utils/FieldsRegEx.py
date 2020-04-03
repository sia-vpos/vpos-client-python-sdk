def get_Email_Reg_Ex():
    min_len = 7
    max_len = 50
    return ".{" + min_len + "," + max_len + "}"


def get_in_person_Reg_Ex():
    return "([S]|[N]){1}"


def get_service_Reg_Ex():
    return "[SV47]{4}"


def get_merchant_url_Reg_Ex():
    return "[A-Za-z0-9_\\-/:. ]"


def get_req_ref_num_Reg_EX():
    len1 = 8
    len2 = 24
    return "[20[0-9][0-9](0[1-9]|1[0-2])(0[1-9]|2[0-9]|3[0-1])]{" + len1 + "}" + "\\d{" + len2 + "}"


def get_usr_auth_flag_Reg_Ex():
    return "[0-2]{1}"


def get_xid_Reg_Ex():
    return "{40}"


def get_cavv_Reg_Ex():
    return "{40}"


def get_eci_Reg_Ex():
    return "([01]|[02]|[05]|[07]){2}"


def get_amount_Reg_Ex():
    min_len = 2
    max_len = 8
    return "[0-9]{" + str(min_len) + "," + str(max_len) + "}"


def get_acquirer_Reg_Ex():
    return "[A-Za-z0-9]{5}"


def get_ip_address_Reg_Ex():
    return "^(?=.*[^\\.]$)((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.?){4}$"


def get_pp_authenticate_method_Reg_Ex():
    return "([MERCHANT ONLY]|[3DS]|[NO AUTHENTICATION]){3,20}"


def get_pp_card_enroll_method_Reg_Ex():
    return "([Manual]|[Direct Provisioned]|[3DS Manual]|[NFC Tap]){6,20}"


def get_shop_id_Reg_Ex():
    e_len = 15
    return "[0-9]{" + str(e_len) + "}"


def get_order_id_Reg_Ex():
    min_len = 1
    max_len = 50
    return "[a-zA-Z0-9\\\\\\-\\_]{" + str(min_len) + "," + str(max_len) + "}"


def get_pan_Reg_Ex():
    min_len = 10
    max_len = 19
    return "^[0-9]{" + str(min_len) + "," + str(max_len) + "}"


def get_exp_date_Reg_Ex():
    return "^[0-9]{2}(0[0-9]|1[0-2])"


def get_operator_id_Reg_Ex():
    min_len = 8
    max_len = 18
    return "[a-zA-Z0-9]{" + str(min_len) + "," + str(max_len) + "}"


def get_network_Reg_Ex():
    e_len = 2
    return "[0-9]{" + str(e_len) + "}"


def get_user_id_Reg_Ex():
    min_len = 1
    max_len = 255
    return ".{" + str(min_len) + "," + str(max_len) + "}"


def get_op_descr_Reg_Ex():
    min_len = 1
    max_len = 100
    return ".{" + str(min_len) + "," + str(max_len) + "}"


def get_email_ch_Reg_Ex():
    min_len = 7
    max_len = 50
    return ".{" + str(min_len) + "," + str(max_len) + "}"


def get_accounting_mode_Reg_Ex():
    e_len = 1
    return "[DI]{" + str(e_len) + "}"


def get_cvv2_Reg_Ex():
    min_len = 3
    max_len = 4
    return "[0-9]{" + str(min_len) + "," + str(max_len) + "}"


def get_author_mode_Reg_Ex():
    e_len = 1
    return "[DI]{" + str(e_len) + "}"


def get_currency_Reg_Ex():
    e_len = 3
    return "[0-9]{" + str(e_len) + "}"


def get_product_ref_Reg_Ex():
    min_len = 1
    max_len = 15
    return ".{" + str(min_len) + "," + str(max_len) + "}"


def get_exponent_Reg_ex():
    e_len = 1
    return "[0-9]{" + str(e_len) + "}"


def get_close_order_Reg_Ex():
    min_len = 2
    max_len = 8
    return "[0-9]{" + str(min_len) + "," + str(max_len) + "}"


def get_pares_Reg_Ex():
    return "([Y]|[N]|[A]|[U]){1}"


def get_tax_id_Reg_Ex():
    fc_len = 16
    ti_len = 11
    return "^([A-Z0-9]{" + str(fc_len) + "}|[0-9]{" + str(ti_len) + "})"


def get_surname_Reg_Ex():
    min_len = 1
    max_len = 40
    return ".{" + str(min_len) + "," + str(max_len) + "}"


def get_name_Reg_Ex():
    min_len = 1
    max_len = 40
    return ".{" + str(min_len) + "," + str(max_len) + "}"


def get_anti_fraud_Reg_Ex():
    return ".*"
