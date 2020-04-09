class Verifier:
    def __init__(self, form_temp, form):
        self.form_template = form_temp
        self.form = form

    def verify(self) -> bool:
        """
        Verifies the content of a form against any checks implemented in this verifier.
        If any check fails, the verifier exits and the form is considered invalid
        :param content:
        :return:
        """
        for formKey in self.form_template.keys:
            if formKey.id in self.form:
                if not formKey.run_checks(self.form[formKey.id]):
                    return False
            # Case of no options being set, go with default (Safest option)
            if formKey.id == "":
                for key in self.form:
                    if not formKey.run_checks(self.form[key]):
                        return False
                return True
        return True
