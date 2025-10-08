class NotFoundError(Exception):
    """The error message about not found DB record"""

    def __init__(self, not_found_type: type, message: str):
        """
        Args:
            not_found_type: The type of the not found record (e.g. User)
            message: The message about the not found record, e.g. "with id 1"
        """
        super().__init__(f"{not_found_type.__name__} not found {message}")
