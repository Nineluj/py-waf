
class Verifier:
    def __init__(self, checks=[]):
        self.checks = checks

    def add_check(self, check) -> None:
        """
        Adds a check method to the list, these methods are the form of String -> Boolean
        :param check: method(str) -> bool
        :return: bool
        """
        self.checks.append(check)

    def add_checks(self, checks) -> None:
        """
        Adds a list of check methods to the list, these methods are the form of String -> Boolean
        :param checks: [method(str) -> bool]
        :return: bool
        """
        self.checks += checks

    def verify(self, content) -> bool:
        """
        Verifies the content of a form against any checks implemented in this verifier.
        If any check fails, the verifier exits and the form is considered invalid
        :param content:
        :return:
        """
        for check in self.checks:
            if not check(content):
                return False
        return True

    def parse_form(self, form) -> bool:
        """
        Verifies if a form is properly formatted, otherwise returns false if an suspicious activity is shown.
        :param form:
        :return:
        """
        for key in form:
            form_content = form[key]
            if not self.verify(form_content):
                return False
        return True


