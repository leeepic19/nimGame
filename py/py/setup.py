from setuptools import setup

setup(
    name="nim_hamburger",
    version="1.0",
    py_modules=["nim_gui", "nim", "nimplay"],
    install_requires=[
        "pillow",
        "pygame"
    ],
    package_data={
        "": ["music/*.MP3", "picture/*.png", "picture/*.jpg", "picture/*.jpeg"]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            # 如有 main 函数可写 "nim_hamburger = nim_gui:main"
        ]
    }
)
