"""Test configuration."""

from __future__ import annotations

import pytest
from jinja2 import Environment

from jinja2_copier_extension import CopierExtension


@pytest.fixture
def env() -> Environment:
    """A pytest fixture for a Jinja2 environment using the Copier extension.

    Returns:
        The Jinja2 environment object.
    """
    return Environment(
        extensions=[CopierExtension],
        variable_start_string="[[",
        variable_end_string="]]",
    )
