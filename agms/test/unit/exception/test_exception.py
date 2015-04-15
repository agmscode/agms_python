import unittest
from exception_helper import ExceptionHelper

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

class TestAgmsException(unittest.TestCase):

	def setUp(self):
		self.helper = ExceptionHelper()

	def testAgmsException(self):
		self.assertRaises(AgmsException, self.helper.agmsException)

	def testAuthenticationException(self):
		self.assertRaises(AuthenticationException, self.helper.authenticationException)

	def testAuthorizationException(self):
		self.assertRaises(AuthorizationException, self.helper.authorizationException)

	def testClientErrorException(self):
		self.assertRaises(ClientErrorException, self.helper.clientErrorException)

	def testConfigurationException(self):
		self.assertRaises(ConfigurationException, self.helper.configurationException)

	def testDownForMaintenanceException(self):
		self.assertRaises(DownForMaintenanceException, self.helper.downForMaintenanceException)

	def testForgedQueryStringException(self):
		self.assertRaises(ForgedQueryStringException, self.helper.forgedQueryStringException)

	def testInvalidParameterException(self):
		self.assertRaises(InvalidParameterException, self.helper.invalidParameterException)

	def testInvalidRequestException(self):
		self.assertRaises(InvalidRequestException, self.helper.invalidRequestException)

	def testInvalidSignatureException(self):
		self.assertRaises(InvalidSignatureException, self.helper.invalidSignatureException)

	def testNotFoundException(self):
		self.assertRaises(NotFoundException, self.helper.notFoundException)

	def testRequestValidationException(self):
		self.assertRaises(RequestValidationException, self.helper.requestValidationException)

	def testResponseException(self):
		self.assertRaises(ResponseException, self.helper.responseException)

	def testServerErrorException(self):
		self.assertRaises(ServerErrorException, self.helper.serverErrorException)

	def testSSLCertificateException(self):
		self.assertRaises(SSLCertificateException, self.helper.sslCertificateException)

	def testUnexpectedException(self):
		self.assertRaises(UnexpectedException, self.helper.unexpectedException)

	def testUpgradeRequiredException(self):
		self.assertRaises(UpgradeRequiredException, self.helper.upgradeRequiredException)
