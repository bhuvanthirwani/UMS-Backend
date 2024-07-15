"""ums models."""
import pkgutil
from pathlib import Path

MODEL_PREFIX = "ums.db.models."


def get_model_list() -> pkgutil.ModuleInfo:
    package_dir = Path(__file__).resolve().parent
    return pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix=MODEL_PREFIX,
    )


def load_all_models():
    """Load all models from this folder."""
    modules = get_model_list()
    for module in modules:
        __import__(module.name)  # noqa: WPS421
        yield module
