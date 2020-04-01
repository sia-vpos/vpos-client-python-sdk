import random
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

from VPOSClient.utils import Constants, TagConstants


def getTimestamp():
    dateTimeObj = datetime.now().isoformat()
    return str(dateTimeObj)[:-3]


def genReqRefNum():
    x = datetime.now()
    x = x.strftime('%Y%m%d')
    for i in range(0, Constants.getReqRefNumLength()):
        x = x + str(random.randint(0, 9))
    return x


def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.Element(key)
        child.text = str(val)
        elem.append(child)
    return elem


def addChild(parent, childName, value):
    child = ET.SubElement(parent, childName)
    child.text = value
    return child


def addOptionalChild(parent, childName, value):
    if value is not None:
        child = ET.SubElement(parent, childName)
        child.text = value


def appendField(stringMac, fieldName, fieldValue):
    if not fieldValue:
        return stringMac
    else:
        stringMac = stringMac + '&' + fieldName + '=' + str(fieldValue)
    return stringMac


def getHtml(url_vpos, parameters_map):
    base_template = "<div><form id=\"myForm\"action=\"[VPOS_URL]\" method=\"POST\"><input name=\"PAGE\" type=\"hidden\" value=\"LAND\">[PARAMETERS]</form><script>document.getElementById('myForm').submit();</script></div>"
    base_template = base_template.replace("[VPOS_URL]", url_vpos)
    if Constants.getTokenName() in parameters_map:
        base_template = base_template.replace("LAND", "TOKEN")
    base_template = base_template.replace("[PARAMETERS]", _generateHtmlParams(parameters_map))
    return base_template


def _generateHtmlParams(parameters_map):
    inputPattern = "<input type=\"hidden\" name=\"KEY\" value=\"VALUE\">"
    stringForHtml = str()
    for key in parameters_map.keys():
        if parameters_map.get(key) is not None:
            stringForHtml = stringForHtml + inputPattern.replace('KEY', key).replace('VALUE', parameters_map.get(key))
    return stringForHtml


def append_field_for_verification(macString, value):
    if value is not None:
        return macString + '&' + value.strip()
    else:
        return macString + '&'


def append_optional_field_for_verification(macString, tag):
    if tag is not None:
        return macString + '&' + tag.text.strip()
    else:
        return macString


def stringToXML(string):
    return ET.fromstring(string)


def geResultStringForMac(responseXml):
    return responseXml.find(TagConstants.getTimestampTag()).text + '&' + responseXml.find(
        TagConstants.getResultTag()).text


def getOperationStringForMac(operationXml):
    stringForMac = operationXml.find(TagConstants.getTransactionIDTag()).text
    stringForMac = append_field_for_verification(stringForMac,
                                                 operationXml.find(TagConstants.getTimestampReqTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 operationXml.find(TagConstants.getTimestampElabTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getSrcTypeTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getResultTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getStatusTag()).text)
    return append_optional_field_for_verification(stringForMac, operationXml.find(TagConstants.getOpDescrTag()))


def getChallengeStringForMac(challengeXml):
    stringForMac = challengeXml.find(TagConstants.getThreeDSTransactionIDTag()).text
    stringForMac = append_field_for_verification(stringForMac,
                                                 challengeXml.find(TagConstants.getCreqTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 challengeXml.find(TagConstants.getACSUrlTag()).text)

    return stringForMac


def getThreeDSMtdStringForMac(three_ds_mtd_xml):
    stringForMac = three_ds_mtd_xml.find(TagConstants.getThreeDSTransactionIDTag()).text
    stringForMac = append_field_for_verification(stringForMac,
                                                 three_ds_mtd_xml.find(TagConstants.getThreeDSMtdDataTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 three_ds_mtd_xml.find(TagConstants.getThreeDSMtdUrlTag()).text)
    return stringForMac


def getPanAliasDataStringForMac(pan_alias_xml):
    tail = pan_alias_xml.find(TagConstants.getPanAliasRevTag())

    if tail is None:
        stringForMac = "&"
    else:
        stringForMac = tail.text
    stringForMac = append_field_for_verification(stringForMac, pan_alias_xml.find(TagConstants.getPanAliasTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 pan_alias_xml.find(TagConstants.getPanExpiryDateTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 pan_alias_xml.find(TagConstants.getPanAliasTailTag()).text)
    return stringForMac


def getAuthorizationStringForMac(authorizationXml):
    stringForMac = authorizationXml.find(TagConstants.getAuthorizationTypeTag()).text
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getTransactionIDTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getNetworkTag()).text)

    if authorizationXml.find(TagConstants.getOrderIDTag()) is not None:
        stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getOrderIDTag()).text)
    else:
        stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getOrderIdTag()).text)

    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getTransactionAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getAuthorizedAmountTag()).text)

    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getCurrencyTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getAccountedAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getRefundedAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getTransactionResultTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getTimestampTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getAuthorizationNumberTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getAcquirerBinTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getMerchantIdTag()).text)
    stringForMac = append_field_for_verification(stringForMac,
                                                 authorizationXml.find(TagConstants.getTransactionStatusTag()).text)
    # OPTIONAL
    stringForMac = append_optional_field_for_verification(stringForMac,
                                                          authorizationXml.find(TagConstants.getResponseCodeIsoTag()))
    stringForMac = append_optional_field_for_verification(stringForMac,
                                                          authorizationXml.find(TagConstants.getPanTailTag()))
    stringForMac = append_optional_field_for_verification(stringForMac,
                                                          authorizationXml.find(TagConstants.getPanExpiryDateTag()))
    stringForMac = append_optional_field_for_verification(stringForMac,
                                                          authorizationXml.find(TagConstants.getPaymentTypePPTag()))
    stringForMac = append_optional_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getRRNTag()))
    stringForMac = append_optional_field_for_verification(stringForMac,
                                                          authorizationXml.find(TagConstants.getCardType()))
    return stringForMac


def get_millis():
    return int(round(time.time() * 1000))


def gen_order_id():
    x = str(get_millis())
    for i in range(0, 30):
        x = x + str(random.randint(0, 9))
    return x


def parse_url(url):
    return urllib.parse.quote(url);


def map_for_verify_url_mac(values):
    mac_string = Constants.getOrderIdName() + "=" + values.get(Constants.getOrderIdName())
    mac_string = appendField(mac_string, Constants.getShopIdName(), values.get(Constants.getShopIdName()))
    if values.get(Constants.getAuthNumberName()) is None:
        mac_string = appendField(mac_string, Constants.getAuthNumberName(), None)
    else:
        mac_string = appendField(mac_string, Constants.getAuthNumberName(), values.get(Constants.getAuthNumberName()))
    mac_string = appendField(mac_string, Constants.getAmountName(), values.get(Constants.getAmountName()))
    mac_string = appendField(mac_string, Constants.getCurrencyName(), values.get(Constants.getCurrencyName()))
    #mac_string = appendField(mac_string, Constants.getExponentName(), values.get(Constants.getExponentName()))

    mac_string = appendField(mac_string, Constants.getTransactionIdName(), values.get(Constants.getTransactionIdName()))
    mac_string = appendField(mac_string, Constants.getAccountingModeName(),
                             values.get(Constants.getAccountingModeName()))
    mac_string = appendField(mac_string, Constants.getAuthorModeName(), values.get(Constants.getAuthorModeName()))
    mac_string = appendField(mac_string, Constants.getResultName(), values.get(Constants.getResultName()))

    mac_string = appendField(mac_string, Constants.getTransactionTypeName(),
                             values.get(Constants.getTransactionTypeName()))
    mac_string = appendField(mac_string, Constants.getIssuerCountryName(), values.get(Constants.getIssuerCountryName()))
    mac_string = appendField(mac_string, Constants.getAuthCodeName(), values.get(Constants.getAuthCodeName()))
    mac_string = appendField(mac_string, Constants.getPayerIdName(), values.get(Constants.getPayerIdName()))

    mac_string = appendField(mac_string, Constants.getPayerName(), values.get(Constants.getPayerName()))
    mac_string = appendField(mac_string, Constants.getPayerStatusName(), values.get(Constants.getPayerStatusName()))
    mac_string = appendField(mac_string, Constants.getHashPanName(), values.get(Constants.getHashPanName()))
    mac_string = appendField(mac_string, Constants.getPanAliasRevName(), values.get(Constants.getPanAliasRevName()))

    mac_string = appendField(mac_string, Constants.getPanAliasName(), values.get(Constants.getPanAliasName()))
    mac_string = appendField(mac_string, Constants.getPanAliasExpDateName(),
                             values.get(Constants.getPanAliasExpDateName()))
    mac_string = appendField(mac_string, Constants.getPanAliasTailName(), values.get(Constants.getPanAliasTailName()))
    mac_string = appendField(mac_string, Constants.getMaskedPanName(), values.get(Constants.getMaskedPanName()))

    mac_string = appendField(mac_string, Constants.getPanTailName(), values.get(Constants.getPanTailName()))
    mac_string = appendField(mac_string, Constants.getPanExpDateName(), values.get(Constants.getPanExpDateName()))

    mac_string = appendField(mac_string, Constants.getAccountHolderName(), values.get(Constants.getAccountHolderName()))
    mac_string = appendField(mac_string, Constants.getIBANName(), values.get(Constants.getIBANName()))
    mac_string = appendField(mac_string, Constants.getAliasStrName(), values.get(Constants.getAliasStrName()))

    mac_string = appendField(mac_string, Constants.getAcquirerBinName(), values.get(Constants.getAcquirerBinName()))
    mac_string = appendField(mac_string, Constants.getMerchantIdName(), values.get(Constants.getMerchantIdName()))
    mac_string = appendField(mac_string, Constants.getCardTypeName(), values.get(Constants.getCardTypeName()))
    mac_string = appendField(mac_string, Constants.getCHInfoName(), values.get(Constants.getCHInfoName()))

    return mac_string


def get_tag_value(xml, tag):
    value = xml.find(tag)
    if value is not None:
        return value.text
    return None
