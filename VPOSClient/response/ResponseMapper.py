from VPOSClient.response.Response import OrderStatusResponse, Authorization, PanAliasData, OperationResponse, Operation, \
    AuthorizeResponse, ThreeDSAuthorize0Response, ThreeDSMethod, ThreeDSChallenge, ThreeDSAuthorize1Response, \
    ThreeDSAuthorize2Response
from VPOSClient.utils import Utils, TagConstants
from VPOSClient.utils.Utils import get_tag_value


def map_order_status_response(response):
    response_xml = Utils.stringToXML(response)
    response_status = OrderStatusResponse()
    response_status.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())

    response_status.result = get_tag_value(response_xml, TagConstants.getResultTag())

    data = response_xml.find(TagConstants.getDataTag())
    if (data is not None) and (data.find(TagConstants.getAuthorizationTag()) is not None):
        for auth_xml in data.findall(TagConstants.getAuthorizationTag()):
            auth_dto = Authorization(auth_xml)
            response_status.auth_list.append(auth_dto)

    if (data is not None) and (data.find(TagConstants.getPanAliasDataTag()) is not None):
        pan_alias_xml = PanAliasData(data.find(TagConstants.getPanAliasDataTag()))
        response_status.pan_alias_data = pan_alias_xml

    return response_status


def map_operation_response(response_operation):
    response_xml = Utils.stringToXML(response_operation)
    response_operation = OperationResponse()
    response_operation.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())
    response_operation.result = get_tag_value(response_xml, TagConstants.getResultTag())
    data = response_xml.find(TagConstants.getDataTag())

    if (data is not None) and (data.find(TagConstants.getOperationTag()) is not None):
        operation_xml = data.find(TagConstants.getOperationTag())
        operation = Operation(operation_xml)
        response_operation.operation = operation

    return response_operation


def map_three_ds_authorize0(response_threeDS):
    response_xml = Utils.stringToXML(response_threeDS)
    response_threeDS = ThreeDSAuthorize0Response()
    response_threeDS.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())
    response_threeDS.result = get_tag_value(response_xml, TagConstants.getResultTag())
    data = response_xml.find(TagConstants.getDataTag())

    if (data is not None) and (data.find(TagConstants.getAuthorizationTag()) is not None):
        authorization_xml = data.find(TagConstants.getAuthorizationTag())
        authorization = Authorization(authorization_xml)
        response_threeDS.authorization = authorization

    if (data is not None) and (data.find(TagConstants.getPanAliasDataTag()) is not None):
        pan_alias_xml = PanAliasData(data.find(TagConstants.getPanAliasDataTag()))
        response_threeDS.pan_alias_data = pan_alias_xml

    if (data is not None) and (data.find(TagConstants.getThreeDSMtdTag()) is not None):
        three_ds_mtd_xml = ThreeDSMethod(data.find(TagConstants.getThreeDSMtdTag()))
        response_threeDS.three_DS_Method = three_ds_mtd_xml

    if (data is not None) and (data.find(TagConstants.getThreeDSChallengeTag()) is not None):
        three_ds_challenge_xml = ThreeDSChallenge(data.find(TagConstants.getThreeDSChallengeTag()))
        response_threeDS.three_DS_Challenge = three_ds_challenge_xml

    return response_threeDS


def map_three_ds_authorize1(response):
    response_xml = Utils.stringToXML(response)
    response = ThreeDSAuthorize1Response()
    response.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())
    response.result = get_tag_value(response_xml, TagConstants.getResultTag())
    data = response_xml.find(TagConstants.getDataTag())

    if (data is not None) and (data.find(TagConstants.getAuthorizationTag()) is not None):
        operation_xml = data.find(TagConstants.getAuthorizationTag())
        operation = Authorization(operation_xml)
        response.operation = operation

    if (data is not None) and (data.find(TagConstants.getPanAliasDataTag()) is not None):
        pan_alias_xml = PanAliasData(data.find(TagConstants.getPanAliasDataTag()))
        response.pan_alias_data = pan_alias_xml

    if (data is not None) and (data.find(TagConstants.getThreeDSChallengeTag()) is not None):
        three_ds_challenge_xml = ThreeDSChallenge(data.find(TagConstants.getThreeDSChallengeTag()))
        response.three_DS_Challenge = three_ds_challenge_xml

    return response


def map_three_ds_authorize2(response_ThreeDS):
    response_xml = Utils.stringToXML(response_ThreeDS)
    response_ThreeDS = ThreeDSAuthorize2Response()
    response_ThreeDS.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())
    response_ThreeDS.result = get_tag_value(response_xml, TagConstants.getResultTag())
    data = response_xml.find(TagConstants.getDataTag())

    if (data is not None) and (data.find(TagConstants.getAuthorizationTag()) is not None):
        operation_xml = data.find(TagConstants.getAuthorizationTag())
        operation = Authorization(operation_xml)
        response_ThreeDS.operation = operation

    if (data is not None) and (data.find(TagConstants.getPanAliasDataTag()) is not None):
        pan_alias_xml = PanAliasData(data.find(TagConstants.getPanAliasDataTag()))
        response_ThreeDS.pan_alias_data = pan_alias_xml

    return response_ThreeDS


def map_authorize_response(response):
    response_xml = Utils.stringToXML(response)
    response_authorize = AuthorizeResponse()
    response_authorize.timestamp = get_tag_value(response_xml, TagConstants.getTimestampTag())
    response_authorize.result = get_tag_value(response_xml, TagConstants.getResultTag())
    data = response_xml.find(TagConstants.getDataTag())
    if (data is not None) and (data.find(TagConstants.getAuthorizationTag()) is not None):
        auth_dto = Authorization(data.find(TagConstants.getAuthorizationTag()))
        response_authorize.authorization = auth_dto

    if (data is not None) and (data.find(TagConstants.getPanAliasDataTag()) is not None):
        pan_alias_xml = PanAliasData(data.find(TagConstants.getPanAliasDataTag()))
        response_authorize.pan_alias_data = pan_alias_xml

    return response_authorize
