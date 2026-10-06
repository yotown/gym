"""The package list: everything under src/, and vendors/ installed as yotown.gym.vendors, one package
per maker. Found by walking the folders, so a new maker's folder needs no entry here."""

from setuptools import find_namespace_packages, find_packages, setup

VENDORS = "yotown.gym.vendors"

setup(
    packages=find_namespace_packages("src", include=["yotown*"]) + [VENDORS]
    + ["%s.%s" % (VENDORS, p) for p in find_packages("vendors")],
    package_dir={"": "src", VENDORS: "vendors"},
)
