from __future__ import annotations

import logging
import random
import string
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("[👤UsersManager]")


@dataclass
class UserData:
    email: str
    username: str
    password: str


class UsersManager:
    def __init__(self) -> None:
        self._users: list[UserData] = []
        self._default_user: Optional[UserData] = None

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
            self.default_user = user
        return user

    @property
    def default_user(self) -> UserData:
        if self._default_user is None:
            raise ValueError("Default user is not set.")
        return self._default_user

    @default_user.setter
    def default_user(self, user: UserData) -> None:
        logger.info(f"Setting default user to {user}")
        self._default_user = user
