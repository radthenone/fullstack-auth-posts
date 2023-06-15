from pathlib import Path
import environ # noqa

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
APPS_DIR = BASE_DIR / "apps"
