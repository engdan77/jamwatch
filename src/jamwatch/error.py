class AppError(Exception):
    pass


class MountError(AppError):
    pass


class FileWriteError(AppError):
    pass
