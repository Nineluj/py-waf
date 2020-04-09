from waf.templates import TEMPLATES


class FormTemplate:
    def __init__(self, path):
        if path in TEMPLATES:
            self.id = path
            # What FormKeys will be checked, using their respective checks
            self.keys = self.parse_template(TEMPLATES[path])
        else:
            self.id = path
            self.keys = self.parse_template(TEMPLATES[""])

    def parse_template(self, template):
        keys = []
        for form in template:
            keys.append(FormKey(form, template[form]))
        return keys


class FormKey:
    def __init__(self, key, checks=None):
        if checks is None:
            checks = []
        self.id = key
        self.checks = checks

    def add_check(self, check) -> None:
        """
        Adds a check method to the list, these methods are the form of String -> Boolean
        :param check: method(str) -> bool
        :return: None
        """
        if check not in self.checks:
            self.checks.append(check)

    def add_checks(self, checks) -> None:
        """
        Adds a list of check methods to the list, these methods are the form of String -> Boolean
        :param checks: [method(str) -> bool]
        :return: None
        """
        for check in checks:
            self.add_check(check)

    def run_checks(self, form_val):
        for check in self.checks:
            if not check(form_val):
                return False
        return True

