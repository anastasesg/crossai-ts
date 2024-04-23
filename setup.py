from setuptools import setup

setup(
    name="crossai-ts",
    version="0.0.0.1",
    packages=[
        "caits",
        "caits.ai",
        "caits.ai.nn1d",
        "caits.ai.nn2d",
        "caits.augmentation",
        "caits.dataset",
        "caits.loading",
        "caits.fe",
        "caits.fe.base",
        "caits.transformers",
        "caits.eda",
        "caits.experimental",
        "caits.performance",
        "caits.resources_handling"
    ],
    url="https://github.com/AIoT-Group-UoP/crossai-ts",
    license="Apache License 2.0",
    author="Pantelis Tzamalis, George Kontogiannis",
    author_email="tzamalis@ceid.upatras.gr",
    description="An open-source Python library for developing "
                "end-to-end AI pipelines for Time Series Analysis",
    install_requires=[
        "tensorflow==2.14.0",
        "tensorflow-metal==1.1.0; platform_system=='Darwin'",
        "tensorflow_addons>=0.21.0",
        "pandas==2.2.0",
        "pyarrow==16.0.0",
        "scipy==1.12.0",
        "scikit-learn==1.4.0",
        "seaborn>=0.12.2",
        "pydub==0.25.1",
        "soundfile==0.12.1",
        "tsaug==0.2.1",
        "resampy==0.4.2",
        "samplerate==0.2.1; platform_system=='Darwin'",
        "samplerate==0.1.0; platform_system=='Linux'",
        "soxr==0.3.7",
        "pyyaml==6.0.1",
        "boto3==1.29.2",
        "tqdm==4.66.2"
    ],
    python_requires=">=3.10"
)
