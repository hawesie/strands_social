#include <ros/ros.h>
#include "CDump.h"
#include "CTimer.h"
#include "CCircleDetect.h"
#include <image_transport/image_transport.h>

#define MAX_PATTERNS 1

int misdetections = 0; 
TLogModule module = LOG_MODULE_MAIN;
image_transport::Publisher imdebug;
CCircleDetect *detector;
SSegment currentSegment;
SSegment lastSegment;
CRawImage *image;
ros::Subscriber scan_sub;

int  defaultImageWidth= 640;
int  defaultImageHeight = 480;

ros::Publisher cmd_vel;
 
void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
	if (image->bpp != msg->step/msg->width || image->width != msg->width || image->height != msg->height){
		delete image;
		ROS_DEBUG("Readjusting image format from %ix%i %ibpp, to %ix%i %ibpp.",image->width,image->height,image->bpp,msg->width,msg->height,msg->step/msg->width);
		image = new CRawImage(msg->width,msg->height,msg->step/msg->width);
	}

	memcpy(image->data,(void*)&msg->data[0],msg->step*msg->height);

	lastSegment = currentSegment;
	currentSegment = detector->findSegment(image,lastSegment);
	if (currentSegment.valid) printf("Circle detected!\n");
}

int main(int argc, char** argv)
{
	ros::init(argc, argv, "social_card_reader");
	ros::NodeHandle n;
	image_transport::ImageTransport it(n);
	dump = new CDump(NULL,256,1000000);
	image = new CRawImage(defaultImageWidth,defaultImageHeight,4);
	detector = new CCircleDetect(defaultImageWidth,defaultImageHeight);
	image_transport::Subscriber subim = it.subscribe("/chest_xtion/rgb/image_mono", 1, imageCallback);
	
	while (ros::ok()){
		ros::spinOnce();
		usleep(30000);
	}
}

