"""
SleepyDriver 라이브러리 설치 스크립트
운전자 피로도 분석 시스템 - 영상 기반 눈 감김 분석을 통한 실시간 피로도 판단
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sleepy-driver",
    version="1.2.6",
    author="SleepyDriver Team",
    author_email="junju404@naver.com",
    description="운전자 피로도 분석 시스템 - 영상 기반 눈 감김 분석을 통한 실시간 피로도 판단 라이브러리",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kimhotac/sleepy-driver-detector",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'sleepy_driver': [
            'models/*.pkl',
            'models/*.pth',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Image Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "mediapipe>=0.8.0",
    ],
    extras_require={
        "ml": [
            "joblib>=1.0.0", 
            "scikit-learn>=1.0.0"
        ],
        "dl": [
            "torch>=1.9.0",
            "torchvision>=0.10.0"
        ],
        "all": [
            "joblib>=1.0.0",
            "scikit-learn>=1.0.0", 
            "torch>=1.9.0",
            "torchvision>=0.10.0"
        ],
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sleepy-driver-demo=examples.demo:main",
        ],
    },
    keywords="drowsiness, fatigue, driver, safety, computer-vision, ai, real-time, monitoring, adas, autonomous-driving",
) 