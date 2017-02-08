# TODO: this feels wrong to basically dulicate jinja and db stuff in DO for
# better readability

from rt.base.objects import Structure

# < th > {{entry.url}} < / th >
# < th > {{entry.mechanism_name}} < / th >
# < th > {{entry.interval}} < / th >
# < th > {{entry.enabled}} < / th >


# TODO: are such structures is overkill?
class Monitor(Structure):
    def __init__(
            self,
            url,
            display_name,
            mechanism_name,
            interval,
            enabled,

    ):
        self.url = url
        self.display_name = display_name
        self.mechanism_name = mechanism_name
        self.interval = interval
        self.enabled = enabled
