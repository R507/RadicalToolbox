"""Base object related classes"""


# TODO: surely I could just have a constructor which just takes the names
# instead of putting stuff in init args and then self.stuff = stuff
# check pros and cons
class Structure(object):
    """Generic structure to contain data

    Atm with only some repr for debugging"""
    # TODO: check if makes sense to restrict it to not having any methods
    def __repr__(self):
        value = list()
        value.append(
            'Class: {class_name}'.format(class_name=self.__class__.__name__))
        value.append("Parameters:")
        self_attrs = set(dir(self))
        common_attrs = set(dir(object))
        for attr in (self_attrs - common_attrs):
            value.append("\t{name} - {value}".format(
                name=attr, value=getattr(self, attr)
            ))
        return "\n".join(value)
