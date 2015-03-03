#! /usr/bin/env python

import rospy

# import strands_webserver.page_utils
# import strands_webserver.client_utils
# import std_srvs.srv 

if __name__ == '__main__':
	rospy.init_node("tweet_me_screen")

	# The display to publish on, defaulting to all displays
	display_no = rospy.get_param("~display", 0)	

	rospy.spin()