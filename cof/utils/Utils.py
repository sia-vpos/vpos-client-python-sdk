import random
import time
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib.parse
from cof.utils import Constants, TagConstants
from cof.utils import Encoder


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


def getHtml(fileName, urlApos, parametersMap):
    HtmlFile = open(fileName, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    source_code = source_code.replace("[APOS_URL]", urlApos)
    source_code = source_code.replace("[PARAMETERS]", _generateHtmlParams(parametersMap))
    return Encoder.stringToBase64(source_code)


def _generateHtmlParams(parametersMap):
    inputPattern = 'PGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iS0VZIiB2YWx1ZT0iVkFMVUUiPg=='
    decodedInput = Encoder.base64ToString(inputPattern)
    parametersMap = dict(parametersMap)
    stringForHtml = str()
    for key in parametersMap.keys():
        if parametersMap.get(key) is not None:
            stringForHtml = stringForHtml + decodedInput.replace('KEY', key).replace('VALUE', parametersMap.get(key))
    return stringForHtml


def saveTemplate(base64Html, delay, basePath):
    html = Encoder.base64ToString(base64Html)
    formPattern = Encoder.base64ToString(
        "PGZvcm0gYWN0aW9uPSJbQVBPU19VUkxdIiBtZXRob2Q9IlBPU1QiPjxpbnB1dCBuYW1lPSJQQUdFIiB0eXBlPSJoaWRkZW4iIHZhbHVlPSJMQU5EIj5bUEFSQU1FVEVSU108aW5wdXQgaWQ9InN1Ym1pdCIgc3R5bGU9ImRpc3BsYXk6IG5vbmU7IiB0eXBlPXN1Ym1pdCAgdmFsdWU9Ii4iPjwvZm9ybT4=")
    scriptPattern = Encoder.base64ToString(
        "PHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiPndpbmRvdy5vbmxvYWQgPSBmdW5jdGlvbigpe3NldFRpbWVvdXQoZnVuY3Rpb24oKXtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc3VibWl0JykuY2xpY2soKTt9LCBbREVMQVldKTt9PC9zY3JpcHQ+")
    html = html.replace('</body>', formPattern + '</body>')
    html = html.replace('</html>', scriptPattern + '</html>')
    html = html.replace('[DELAY]', str(delay))
    f = open(basePath + "\customTemplate.html", "w")
    f.write(html)
    f.close()
    return True


def append_field_for_verification(macString, value):
    return macString + '&' + value.strip()


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
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getTimestampReqTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getTimestampElabTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getSrcTypeTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getResultTag()).text)
    stringForMac = append_field_for_verification(stringForMac, operationXml.find(TagConstants.getStatusTag()).text)
    return append_optional_field_for_verification(stringForMac, operationXml.find(TagConstants.getOpDescrTag()))


def getAuthorizationStringForMac(authorizationXml):
    stringForMac = authorizationXml.find(TagConstants.getAuthorizationTypeTag()).text
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getTransactionIDTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getNetworkTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getOrderIDTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getTransactionAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getAuthorizedAmountTag()).text)

    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getCurrencyTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getAccountedAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getRefundedAmountTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getTransactionResultTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getTimestampTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getAuthorizationNumberTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getAcquirerBinTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getMerchantIdTag()).text)
    stringForMac = append_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getTransactionStatusTag()).text)
    # OPTIONAL
    stringForMac = append_optional_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getResponseCodeIsoTag()))
    stringForMac = append_optional_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getPanTailTag()))
    stringForMac = append_optional_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getPanExpiryDateTag()))
    stringForMac = append_optional_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getPaymentTypePPTag()))
    stringForMac = append_optional_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getRRNTag()))
    stringForMac = append_optional_field_for_verification(stringForMac, authorizationXml.find(TagConstants.getCardType()))
    return stringForMac


def get_millis():
    return int(round(time.time() * 1000))


def gen_order_id():
    x = str(get_millis())
    print(len(x))
    for i in range(0, 37):
        x = x + str(random.randint(0, 9))
    return x


def parse_url(url):
    return urllib.parse.quote(url);


def map_for_verify_url_mac(values):
    mac_string = Constants.getOrderIdName()+"="+values.get(Constants.getOrderIdName())
    mac_string = appendField(mac_string, Constants.getShopIdName(), values.get(Constants.getShopIdName()))
    if values.get(Constants.getAuthNumberName()) is None:
        mac_string = appendField(mac_string, Constants.getAuthNumberName(), None)
    else:
        mac_string = appendField(mac_string, Constants.getAuthNumberName(), values.get(Constants.getAuthNumberName()))
    mac_string = appendField(mac_string, Constants.getAmountName(), values.get(Constants.getAmountName()))
    mac_string = appendField(mac_string, Constants.getCurrencyName(), values.get(Constants.getCurrencyName()))
    mac_string = appendField(mac_string, Constants.getExponentName(), values.get(Constants.getExponentName()))

    mac_string = appendField(mac_string, Constants.getTransactionIdName(), values.get(Constants.getTransactionIdName()))
    mac_string = appendField(mac_string, Constants.getAccountingModeName(), values.get(Constants.getAccountingModeName()))
    mac_string = appendField(mac_string, Constants.getAuthorModeName(), values.get(Constants.getAuthorModeName()))
    mac_string = appendField(mac_string, Constants.getResultName(), values.get(Constants.getResultName()))

    mac_string = appendField(mac_string, Constants.getTransactionTypeName(), values.get(Constants.getTransactionTypeName()))
    mac_string = appendField(mac_string, Constants.getIssuerCountryName(), values.get(Constants.getIssuerCountryName()))
    mac_string = appendField(mac_string, Constants.getAuthCodeName(), values.get(Constants.getAuthCodeName()))
    mac_string = appendField(mac_string, Constants.getPayerIdName(), values.get(Constants.getPayerIdName()))

    mac_string = appendField(mac_string, Constants.getPayerName(),values.get(Constants.getPayerName()))
    mac_string = appendField(mac_string, Constants.getPayerStatusName(), values.get(Constants.getPayerStatusName()))
    mac_string = appendField(mac_string, Constants.getHashPanName(), values.get(Constants.getHashPanName()))
    mac_string = appendField(mac_string, Constants.getPanAliasRevName(), values.get(Constants.getPanAliasRevName()))

    mac_string = appendField(mac_string, Constants.getPanAliasName(), values.get(Constants.getPanAliasName()))
    mac_string = appendField(mac_string, Constants.getPanAliasExpDateName(), values.get(Constants.getPanAliasExpDateName()))
    mac_string = appendField(mac_string, Constants.getPanAliasTailName(), values.get(Constants.getPanAliasTailName()))
    mac_string = appendField(mac_string, Constants.getMaskedPanName(), values.get(Constants.getMaskedPanName()))

    mac_string = appendField(mac_string, Constants.getPanAliasName(), values.get(Constants.getPanAliasName()))
    mac_string = appendField(mac_string, Constants.getPanAliasExpDateName(), values.get(Constants.getPanAliasExpDateName()))
    mac_string = appendField(mac_string, Constants.getPanAliasTailName(), values.get(Constants.getPanAliasTailName()))

    mac_string = appendField(mac_string, Constants.getMaskedPanName(), values.get(Constants.getMaskedPanName()))
    mac_string = appendField(mac_string, Constants.getPanExpDateName(),values.get(Constants.getPanExpDateName()))
    mac_string = appendField(mac_string, Constants.getPanTailName(), values.get(Constants.getPanTailName()))

    mac_string = appendField(mac_string, Constants.getAccountHolderName(), values.get(Constants.getAccountHolderName()))
    mac_string = appendField(mac_string, Constants.getIBANName(), values.get(Constants.getIBANName()))
    mac_string = appendField(mac_string, Constants.getAliasStrName(), values.get(Constants.getAliasStrName()))

    mac_string = appendField(mac_string, Constants.getAcquirerBinName(), values.get(Constants.getAcquirerBinName()))
    mac_string = appendField(mac_string, Constants.getMerchantIdName(), values.get(Constants.getMerchantIdName()))
    mac_string = appendField(mac_string, Constants.getCardTypeName(), values.get(Constants.getCardTypeName()))
    return mac_string