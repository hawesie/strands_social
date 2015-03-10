import web
import os
import roslib

template_dir = roslib.packages.get_pkg_dir('robot_web_view') + '/templates'
render = web.template.render(template_dir)

def create_robot_view_page(full_path, image_topic, other_button=''):		
	""" Generates the tweet me page at the given location. """
	try:
		os.makedirs(os.path.dirname(full_path))
	except OSError, e:
		pass

	page = str(render.robot_view(image_topic, other_button))
	with open(full_path, 'w+') as f:
		f.write(page)

	print('written ', full_path)
