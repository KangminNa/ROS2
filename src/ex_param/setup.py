from setuptools import setup

package_name = 'ex_param'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='soda',
    maintainer_email='soda@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ex_param = ex_param.ex_param:main',
            'ex_param_get = ex_param.ex_param_get:main',
            'ex_param_set = ex_param.ex_param_set:main'                        
        ],
    },
)
