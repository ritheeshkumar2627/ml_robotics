from setuptools import find_packages, setup

package_name = 'custom_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dyaga',
    maintainer_email='dyaga@todo.todo',
    description='Production Hazard Detection Package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 🛠️ ENTRY POINT ENTRY: Map terminal execution string to target python file class
            'joint_pub = custom_perception.joint_publisher_node:main',
        ],
    },
)
