#!/usr/bin/python

# Decorator class for Error handling within scripts so that useful error messages are generated when problem sets arise
class ConvertExceptions(object):
    func = None
    def __init__(self, exceptions, replacement=None):
        self.exceptions = exceptions
        self.replacement = replacement
    def __call__(self, *args, **kwargs):
        if self.func is None:
            self.func = args[0]
            return self
        try:
            return self.func(*args, **kwargs)
        except self.exceptions:
            return self.replacement
