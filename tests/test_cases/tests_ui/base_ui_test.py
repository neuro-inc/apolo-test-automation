from __future__ import annotations

from collections.abc import Awaitable
from collections.abc import Callable
import pytest
from typing import Any

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
        self._pm = page_manager
        self._add_pm = add_page_manager
        self._test_config = test_config
        self._data_manager = data_manager
        self._users_manager = users_manager
        self._api_helper = api_helper
        self._primary_taken = False  # tracks first implicit use

    async def _pick_pm(self) -> PageManager:
        """
        Decide which PageManager to hand out:

        * first implicit   → self._pm
        * later implicit   → new from self._add_pm()
        """

        if not self._primary_taken:
            self._primary_taken = True
            return self._pm

        return await self._add_pm()

    async def init_test_steps(
        self,
        steps_class: type[Any],
    ) -> tuple[Any, UICommonSteps]:
        """
        Return a tuple (custom_steps, ui_common_steps) bound to the same PageManager.

        Args:
            steps_class  – class to instantiate, e.g. UISignupSteps

        Example:
            steps1, ui1 = await self.init_test_steps(UISignupSteps)   # uses self._pm
            steps2, ui2 = await self.init_test_steps(UISignupSteps)   # new context

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
