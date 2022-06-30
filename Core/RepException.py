
class Error(Exception):
    """Base class for other exceptions"""
    pass


class CommandIsNotValid(Error):
    """Command Is Not Valid"""
    pass
