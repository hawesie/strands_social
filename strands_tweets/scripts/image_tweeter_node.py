#! /usr/bin/env python

import rospy
import actionlib
from strands_tweets.msg import SendTweetAction, SendTweetGoal, GrabImageThenTweetAction
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageTweeter(object):
    
    def __init__(self) :
        
        rospy.on_shutdown(self._on_node_shutdown)

        rospy.loginfo('Waiting for strands_tweets')
        self.tweet_client = actionlib.SimpleActionClient('strands_tweets', SendTweetAction)        
        self.tweet_client.wait_for_server()
        rospy.loginfo(" ... Init done")
    

        self.server = actionlib.SimpleActionServer('strands_image_tweets', GrabImageThenTweetAction, self.execute, False) 
        self.server.start()



    def execute(self, goal):

        self.image = None
        self.sub = rospy.Subscriber(goal.topic, Image, self.image_callback, queue_size=1)

        # the polling is ugly, but it's hard do do things in a ros-time friendly way otherwise
        while self.image == None and not rospy.is_shutdown() and not self.server.is_preempt_requested():
            rospy.sleep(0.5)

        result = GrabImageThenTweetResult(success = False)

        if rospy.is_shutdown() or self.server.is_preempt_requested():
            self.server.set_preempted(result)
            return

        # if we got this far we have an image
        tweet = SendTweetGoal(text = goal.text, force = goal.force, with_photo = True, photo = self.image )

        self.tweet_client.send_goal(tweet)
        
        while not self.tweet_client.wait_for_goal(rospy.Duration(0.5)) and not rospy.is_shutdown() and not self.server.is_preempt_requested():
            pass

        if rospy.is_shutdown() or self.server.is_preempt_requested():
            self.server.set_preempted(result)
        else:
            result.success = True
            self.server.set_succeeded(result)

    def image_callback(self, message):
        self.image = message
        self.sub.unregister()

if __name__ == '__main__':
    rospy.init_node('image_tweeter_node')
    it = ImageTweeter()
    rospy.spin()