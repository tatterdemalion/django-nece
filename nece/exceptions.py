class NonTranslatableFieldError(Exception):
    def __init__(self, fieldname):
        self.fieldname = fieldname
        message = "{} is not in translatable fields".format(fieldname)
        super(NonTranslatableFieldError, self).__init__(message)
