from VPOSClient.response.Response import OrderStatusResponse, Authorization, PanAliasData, OperationResponse, Operation, \
    AuthorizeResponse
from VPOSClient.utils import Utils, TagConstants
from VPOSClient.utils.Utils import get_tag_value


def map_order_status_response(response):
    response_xml = Utils.stringToXML(response)
    response_dto = OrderStatusResponse()
    response_dto.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())

    response_dto.result = get_tag_value(response_xml, TagConstants.getResultTag())

    data = response_xml.find(TagConstants.getDataTag())
    if (data is not None) & (data.find(TagConstants.getAuthorizationTag()) is not None):
        for auth_xml in data.findall(TagConstants.getAuthorizationTag()):
            auth_dto = Authorization(auth_xml)
            response_dto.auth_list.append(auth_dto)

    if (data is not None) & (data.find(TagConstants.getPanAliasDataTag()) is not None):
        pan_alias_xml = PanAliasData(data.find(TagConstants.getPanAliasDataTag()))
        response_dto.pan_alias_data = pan_alias_xml

    return response_dto


def map_operation_response(response):
    response_xml = Utils.stringToXML(response)
    response_dto = OperationResponse()
    response_dto.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())
    response_dto.result = get_tag_value(response_xml, TagConstants.getResultTag())
    data = response_xml.find(TagConstants.getDataTag())

    if (data is not None) & (data.find(TagConstants.getOperationTag()) is not None):
        operation_xml = data.find(TagConstants.getOperationTag())
        operation = Operation(operation_xml)
        response_dto.operation = operation

    return response_dto


def map_authorize_response(response):
    response_xml = Utils.stringToXML(response)
    response_dto = AuthorizeResponse()
    response_dto.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())
    response_dto.result = get_tag_value(response_xml, TagConstants.getResultTag())
    data = response_xml.find(TagConstants.getDataTag())
    if (data is not None) & (data.find(TagConstants.getAuthorizationTag()) is not None):
            auth_dto = Authorization(data.find(TagConstants.getAuthorizationTag()))
            response_dto.authorization= auth_dto

    if (data is not None) & (data.find(TagConstants.getPanAliasDataTag()) is not None):
        pan_alias_xml = PanAliasData(data.find(TagConstants.getPanAliasDataTag()))
        response_dto.pan_alias_data = pan_alias_xml

    return response_dto




