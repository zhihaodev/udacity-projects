class InvalidUsageException(Exception):

    """A new handy Exception class with an error message and extra payload."""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        """
        Args:
            message: error message to be carried
            status_code: HTTP status code, e.g. 404
            payload: extra payload to be carried

        """

        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Create a dictionary which inludes the payload and
        the error message."""
        
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv
