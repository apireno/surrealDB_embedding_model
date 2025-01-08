from setuptools import setup, find_packages


setup(
    name="surrealdb_embedding_model",
    version="0.1.0",
    packages=find_packages(),  # Use find_packages() to automatically find packages
    install_requires=[
        "surrealdb",
        "torch",
    ],
    entry_points={
        'console_scripts': [
            'step_0_process_input_embedding_model = surrealdb_embedding_model.scripts.step_0_process_input_embedding_model:main', 
            # Assuming you have a 'main' function in your script
        ],
    }
)