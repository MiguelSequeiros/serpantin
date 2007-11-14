from setuptools import setup, find_packages
setup(
    name = "Serpantin",
    version = "0.0.1",
    packages = find_packages(),
    include_package_data = True,

    # metadata for upload to PyPI
    author = "Dmitry Sorokin",
    author_email = "ds@dial.com.ru",
    description = "Small ERP application build with django and dojo",
    license = "GNU GPL v2",
    keywords = "python django dojo ERP application",
    url = "http://code.google.com/p/serpantin/", # project home page, if any
)
