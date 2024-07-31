class SSHAuthenticationTimeoutError(Exception):
    pass


class SSHAuthenticationFailedError(Exception):
    pass


class XrdcpNoServersAvailableToReadFileError(Exception):
    pass


class XrdcpTimeoutError(Exception):
    pass


class XrdcpUnknownError(Exception):
    pass


class XrdcpBadRootFileError(Exception):
    pass
