"""Helper class to handle filesystem paths as lists"""
# TODO: who would have thought that there is such handler in stdlib, use it instead
import os

# __doc__ = "reStructuredText"  # TODO: check what does this affect


class Path(object):
    """Path handler

    Class to automatically handle various path in the filesystem
    as a list-like object"""
    def __init__(self, *path):
        """Initialize path instance

        :param path: desired path"""
        self._path = (
            os.path.join(*(os.path.normpath(str(part)) for part in path))
            if path
            else os.path.normpath("")
        )

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return repr(self._path)

    def append(self, path_part):
        self._path = os.path.join(
            self._path,
            os.path.normpath(str(path_part))
        )

    def extend(self, path_part):
        self._path = os.path.join(
            self._path,
            *(os.path.normpath(str(part)) for part in path_part)
        )
