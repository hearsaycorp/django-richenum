#!/usr/bin/env python3
import os
import sys


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = os.path.join(REPO_ROOT, "src")


def _db_settings():
    db_host = os.environ.get("DJANGO_DB_HOST")
    db_engine = os.environ.get("DJANGO_DB_ENGINE", "sqlite")
    db_user = os.environ.get("DJANGO_DB_USER")
    db_pass = os.environ.get("DJANGO_DB_PASSWORD")

    if db_engine == "mysql":
        return {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "testdb",
            "USER": db_user or "root",
            "HOST": db_host,
            "PASSWORD": db_pass,
        }
    if db_engine == "postgres":
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "testdb",
            "USER": db_user or "postgres",
            "HOST": db_host,
            "PASSWORD": db_pass,
        }
    if db_engine == "sqlite":
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(REPO_ROOT, "database.db"),
        }

    raise ValueError(f"Unknown DB engine: {db_engine}")


def main():
    if REPO_ROOT not in sys.path:
        sys.path.insert(0, REPO_ROOT)
    if SRC_ROOT not in sys.path:
        sys.path.insert(0, SRC_ROOT)

    import django
    import pytest
    from django.conf import settings

    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={"default": _db_settings()},
            SECRET_KEY=os.environ.get("SECRET_KEY", "placeholder"),
            CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
            MIDDLEWARE=["django.middleware.common.CommonMiddleware"],
            INSTALLED_APPS=(
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",
                "tests",
            ),
        )

    django.setup()
    return pytest.main(["tests/"])


if __name__ == "__main__":
    sys.exit(main())
