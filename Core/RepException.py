
class Error(Exception):
    """Base class for other exceptions"""
    pass


class CommandIsNotValid(Error):
    """Command Is Not Valid"""
    pass


class VariableDoesNotExist(Error):
    """Variable Does Not Exist"""
    def __init__(self, variable):
        self.variable = variable
        super().__init__(self.variable)

    def __str__(self):
        return f"Variable {self.variable} Does Not Exist"


class RepoDoesNotExist(Error):

    def __str__(self):
        return f"Repo Does Not Exist"


class VariableDoesNotExistOnSpecificRepo(Error):
    def __init__(self, variable, repo):
        self.var = variable
        self.repo = repo
        super().__init__(self.var, self.repo)

    def __str__(self):
        return f"Variable {self.var} Does Not Exist on {self.repo}"
