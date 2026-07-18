from setuptools import find_packages, setup
import os

package_name = 'custom_perception'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),['launch/perception_frames_launch.py'])
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
            'joint_pub = custom_perception.joint_publisher_node:main',
            'image_sub = custom_perception.image_subscriber_node:main',
            'motion_ctrl = custom_perception.motion_controller_node:main',
            'safety_intercept = custom_perception.safety_interceptor_node:main',
        ],
    },

)
