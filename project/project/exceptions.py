# -*- coding: utf-8 -*-


class ProjectBaseException(Exception):
    pass


class ProjectBaseDirectoryVariableException(ProjectBaseException):
    pass


class ProjectLocalSettingsDoesNotExist(ProjectBaseException):
    pass