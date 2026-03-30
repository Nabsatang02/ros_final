from setuptools import find_packages, setup

package_name = 'patrol_bot'

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
    maintainer='puree',
    maintainer_email='puree@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'sensor_node = patrol_bot.sensor_node:main',
            'controller_node = patrol_bot.controller_node:main',
            'pose_monitor_node = patrol_bot.pose_monitor_node:main',
        ],
    },
)
