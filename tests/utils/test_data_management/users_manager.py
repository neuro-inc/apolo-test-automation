from __future__ import annotations

import logging
import random
import string
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("[👤UsersManager]")


@dataclass
class UserData:
    email: str
    username: str
    password: str
    token: str = ""
    authorized: bool = False
    orgs: list[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"UserData(email='{self.email}', username='{self.username}', password='{self.password}')"


class UsersManager:
    def __init__(self) -> None:
        self._users: list[UserData] = []
        self._main_user: Optional[UserData] = None
        self._second_user: Optional[UserData] = None
        self._third_user: Optional[UserData] = None

    def _generate_email(self) -> str:
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"regression-{suffix}@apolo.us"

    def _generate_password(self) -> str:
        specials = "!@#$%^&*"
        lowers = string.ascii_lowercase
        uppers = string.ascii_uppercase
        digits = string.digits

        categories = [lowers, uppers, digits, specials]
        selected_categories = random.sample(categories, k=3)

        password_chars = [random.choice(cat) for cat in selected_categories]

        all_chars = lowers + uppers + digits + specials
        remaining_length = max(8, 12) - len(password_chars)
        password_chars += random.choices(all_chars, k=remaining_length)

        random.shuffle(password_chars)
        return "".join(password_chars)

    def generate_user(self) -> UserData:
        email = self._generate_email()
        username = email.split("@")[0]
        password = self._generate_password()
        user = UserData(email=email, username=username, password=password)
        logger.info(f"Generated new user: {user}")
        self._users.append(user)
        if len(self._users) == 1:
            self.main_user = user
        return user

    @property
    def main_user(self) -> UserData:
        if self._main_user is None:
            raise ValueError("Main user is not set.")
        return self._main_user

    @main_user.setter
    def main_user(self, user: UserData) -> None:
        logger.info(f"Setting main user to {user}")
        self._main_user = user

    @property
    def second_user(self) -> UserData | None:
        return self._second_user

    @second_user.setter
    def second_user(self, user: UserData) -> None:
        logger.info(f"Setting second user to {user}")
        self._second_user = user

    @property
    def third_user(self) -> UserData | None:
        return self._third_user

    @third_user.setter
    def third_user(self, user: UserData) -> None:
        logger.info(f"Setting third user to {user}")
        self._third_user = user
