from setuptools import setup
import os
from glob import glob

package_name = 'my_swarm_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*')),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'drone_interface = my_swarm_pkg.drone_interface:main',
            'local_fsm = my_swarm_pkg.local_fsm:main',
            'intent_coordinator = my_swarm_pkg.intent_coordinator:main',
            'formation_controller = my_swarm_pkg.formation_controller:main',
            'collision_avoidance = my_swarm_pkg.collision_avoidance:main',
            'safety_monitor = my_swarm_pkg.safety_monitor:main',
            'qr_perception = my_swarm_pkg.qr_perception:main',
            'waypoint_navigator = my_swarm_pkg.waypoint_navigator:main',
            'mission_fsm = my_swarm_pkg.mission_fsm:main',
            'precision_landing = my_swarm_pkg.precision_landing:main',
            'color_zone_detector = my_swarm_pkg.color_zone_detector:main',
        ],
    },
)
