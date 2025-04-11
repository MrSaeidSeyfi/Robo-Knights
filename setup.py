from setuptools import setup, find_packages

setup(
    name="robo-knights",
    version="0.1.0",
    package_dir={"": "src"},  
    packages=find_packages(where="src"),  
    install_requires=[
        "pygame>=2.5.2",
        "chess>=1.11.2",
        "numpy>=1.26.0",
        "torch>=2.1.0",
    ],
    author="Robo-Knights Team",
    description="A chess reinforcement learning project with actor-critic neural networks",
    python_requires=">=3.8",
    package_data={
        "": ["*.pth"],  
    },
) 