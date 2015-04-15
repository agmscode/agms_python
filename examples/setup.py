import agms
from distutils.core import setup
setup(
    name="agms",
    version=agms.version.Version,
    description="Avant-Garde Gateway Python Library",
    author="AGMS",
    author_email="support@agms.com",
    url="https://www.onlinepaymentprocessing.com/docs/python",
    packages=["agms"],
    install_requires=["requests>=0.11.1,<3.0"],
    zip_safe=False
)
