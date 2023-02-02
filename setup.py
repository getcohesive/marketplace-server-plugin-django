from setuptools import setup


setup(
    name="cohesive-marketplace-server-plugin-django",
    version="1.0.2",
    description="Django plugin for the Cohesive Marketplace",
    author="Cohesive",
    author_email="contact@cohesive.so",
    url="https://github.com/getcohesive/marketplace-server-plugin-django",
    license="MIT",
    keywords="cohesive api marketplace saas django",
    packages=['cohesive_django'],
    install_requires=[
        'Django',
        'cohesive-marketplace-server-sdk-python==1.0.0',
    ],
    python_requires=">=3.7",
    project_urls={
        "Source Code": "https://github.com/getcohesive/marketplace-server-plugin-django",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["wheel"],
)