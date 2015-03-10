#! /usr/bin/env python

import rospy
import roslib
import os

import strands_webserver.client_utils
from robot_web_view import create_robot_view_page

if __name__ == '__main__':
    rospy.init_node("robot_web_view_example")

    # The display to publish on, defaulting to all displays
    display_no = rospy.get_param("~display", 0) 

    image_topic = rospy.get_param('~image_topic') 

    # set http root to be this package
    http_root = os.path.join(roslib.packages.get_pkg_dir('robot_web_view'), 'data')
    strands_webserver.client_utils.set_http_root(http_root)

    # generate the page 
    file_name = 'tweet_me.html'
    create_robot_view_page(os.path.join(http_root, file_name), image_topic)

    # show the page
    strands_webserver.client_utils.display_relative_page(display_no, file_name)