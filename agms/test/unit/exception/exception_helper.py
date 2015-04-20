from agms.exception.agms_exception import AgmsException
from agms.exception.authentication_exception import AuthenticationException
from agms.exception.authorization_exception import AuthorizationException
from agms.exception.client_error_exception import ClientErrorException
from agms.exception.configuration_exception import ConfigurationException
from agms.exception.down_for_maintenance_exception import DownForMaintenanceException
from agms.exception.forged_query_string_exception import ForgedQueryStringException
from agms.exception.invalid_parameter_exception import InvalidParameterException
from agms.exception.invalid_request_exception import InvalidRequestException
from agms.exception.invalid_signature_exception import InvalidSignatureException
from agms.exception.not_found_exception import NotFoundException
from agms.exception.request_validation_exception import RequestValidationException
from agms.exception.response_exception import ResponseException
from agms.exception.server_error_exception import ServerErrorException
from agms.exception.ssl_certificate_exception import SSLCertificateException
from agms.exception.unexpected_exception import UnexpectedException
from agms.exception.upgrade_required_exception import UpgradeRequiredException


class ExceptionHelper():
    def agmsException(self):
        raise AgmsException('Agms Exception')

    def authenticationException(self):
        raise AuthenticationException('Authentication Exception')

    def authorizationException(self):
        raise AuthorizationException('Authorization Exception')

    def clientErrorException(self):
        raise ClientErrorException('Client Error Exception')

    def configurationException(self):
        raise ConfigurationException('Configuration Exception')

    def downForMaintenanceException(self):
        raise DownForMaintenanceException('Down For Maintenance Exception')

    def forgedQueryStringException(self):
        raise ForgedQueryStringException('Forged Query String Exception')

    def invalidParameterException(self):
        raise InvalidParameterException('Invalid Parameter Exception')

    def invalidRequestException(self):
        raise InvalidRequestException('Invalid Request Exception')

    def invalidSignatureException(self):
        raise InvalidSignatureException('Invalid Signature Exception')

    def notFoundException(self):
        raise NotFoundException('NotFoundException')

    def requestValidationException(self):
        raise RequestValidationException('Request Validation Exception')

    def responseException(self):
        raise ResponseException('Response Exception')

    def serverErrorException(self):
        raise ServerErrorException('Server Error Exception')

    def sslCertificateException(self):
        raise SSLCertificateException('SSL Certificate Exception')

    def unexpectedException(self):
        raise UnexpectedException('Unexpected Exception')

    def upgradeRequiredException(self):
        raise UpgradeRequiredException('Upgrade Required Exception')