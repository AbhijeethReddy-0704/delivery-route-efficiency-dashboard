from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def full_df() -> pd.DataFrame:
    from src.data.data_loader import load_delivery_data

    return load_delivery_data()


@pytest.fixture()
def sample_df(full_df: pd.DataFrame) -> pd.DataFrame:
    # Small fixture for faster unit tests while preserving schema and realistic values.
    return full_df.sample(n=2000, random_state=42).reset_index(drop=True)
