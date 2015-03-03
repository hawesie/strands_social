#! /usr/bin/env python

import rospy
import roslib
import os

import strands_webserver.client_utils
# import std_srvs.srv 

if __name__ == '__main__':
    rospy.init_node("tweet_me_screen")

    # The display to publish on, defaulting to all displays
    display_no = rospy.get_param("~display", 0) 

    # set http root to be this package
    http_root = os.path.join(roslib.packages.get_pkg_dir('tweet_me_screen'), 'data')
    strands_webserver.client_utils.set_http_root(http_root)

    # start with a basic page pretending things are going normally
    strands_webserver.client_utils.display_relative_page(display_no, 'tweet_me.html')

    rospy.spin()