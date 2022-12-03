from setuptools import setup

setup(
    name="predictor",
    version="0.0.1",
    description="Python library to predict the class of an image using a trained model.",
    author="MISIS ML Team",
    author_email="itatm@misis.ru",
    packages=["predictor"],
    install_requires=["numpy", "pillow", "torch", "torchvision"],
    license="GNU Lesser General Public License v3",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
