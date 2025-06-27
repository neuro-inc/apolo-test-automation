from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

import pytest

from tests.components.ui.page_manager import PageManager
from tests.test_cases.steps.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager
from tests.utils.api_helper import APIHelper


class BaseUITest:
    @pytest.fixture(autouse=True)
    async def _inject_fixtures(
        self,
        page_manager: PageManager,
        add_page_manager: Callable[[], Awaitable[PageManager]],
        test_config: ConfigManager,
        data_manager: DataManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        """
        Inject test dependencies into the base test class.

        This autouse fixture sets up:
        - PageManager
        - PageManager factory (`add_page_manager`)
        - Test configuration
        - Data/user/API helpers
        """
        self._pm = page_manager
        self._add_pm = add_page_manager
        self._test_config = test_config
        self._data_manager = data_manager
        self._users_manager = users_manager
        self._api_helper = api_helper

        self._user_counter = 1
        self._primary_taken = False

        self.logger: logging.Logger = logging.getLogger("[📄 TestCaseInfo]")

    async def _pick_pm(self) -> PageManager:
        """
        Decide which PageManager to hand out:

        - First implicit call → `self._pm`
        - Later calls         → new PageManager from `self._add_pm()`
        - Each gets a unique `user_label`: "User1", "User2", ...
        """
        if not self._primary_taken:
            self._primary_taken = True
            pm = self._pm
        else:
            self._user_counter += 1
            pm = await self._add_pm()
            pm.user_label = f"User{self._user_counter}"

        return pm

    def log(self, message: str, level: int = logging.INFO) -> None:
        """
        Log a formatted message with a consistent prefix.

        Parameters
        ----------
        message : str
            The message to log.
        level : int
            Logging level (default: INFO).
        """
        formatted_message = f"{':' * 15} {message}"
        self.logger.log(level, formatted_message)

    async def init_test_steps(
        self,
        steps_class: type[Any],
    ) -> tuple[Any, UICommonSteps]:
        """
        Return a tuple (custom_steps, ui_common_steps) bound to the same PageManager.

        Parameters
        ----------
        steps_class : type
            A class to instantiate test steps, e.g. UISignupSteps.

        Returns
        -------
        tuple
            A tuple: (instance of steps_class, instance of UICommonSteps).

        Example
        -------
        steps1, ui1 = await self.init_test_steps(UISignupSteps)  # uses self._pm
        steps2, ui2 = await self.init_test_steps(UISignupSteps)  # uses a new context
        """
        pm = await self._pick_pm()

        steps_obj = steps_class(
            pm,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )

        ui_common = UICommonSteps(
            pm,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )

        return steps_obj, ui_common
