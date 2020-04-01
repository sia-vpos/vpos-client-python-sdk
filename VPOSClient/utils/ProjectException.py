class VPOSException(Exception):

    def __init__(self, message, stack_trace=None):
        self.message = message
        self.stack_trace = stack_trace
