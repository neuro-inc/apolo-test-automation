class BasePage:
    def __init__(self, page):
        self.page = page

        if self.__class__.is_loaded == BasePage.is_loaded:
            raise NotImplementedError("All pages must implement 'is_loaded()' method!")

    def is_loaded(self, **kwargs) -> bool:
        """Returns True if the page is considered loaded (key elements are visible)."""
        raise NotImplementedError