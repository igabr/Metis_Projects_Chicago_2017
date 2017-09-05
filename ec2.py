#Created by Ibrahim Gabr
#This script should be run on the local version of your shell - not on an AWS shell itself.
import boto3
import botocore
import os

ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]

SECRET_KEY = os.environ['AWS_SECRET_KEY']

ec2 = boto3.resource('ec2', region_name="us-east-1",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

def view_all_instances():
	"""
	This function takes not arguments.

	It simply returns a list of all instances that have been set up on AWS EC2.

	Returns:
		list of instance_objs
	"""
	instance_lst = []

	for instance in ec2.instances.all():
		instance_lst.append(instance)

	return instance_lst

def update_bash_profile(instance_obj):
	"""
	This function updates your .bash_profile with the public DNS address for your AWS EC2 instance.

	This function is needed when you wish to connect to a Jupyter Notebook on EC2 via a web browser.

	Inputs:
		instance_obj
	"""

	current_directory = os.getcwd()

	os.chdir('/Users/ibrahimgabr') #change to match the path to your home directory
	
	with open('.bash_profile', 'r') as file:
		data = file.readlines()

	data[5] = 'export metis_chi17_url="{}"\n'.format(instance_obj.public_dns_name) #change to match the appropriate line in your .bash_profile

	with open('.bash_profile', 'w') as file:
		file.writelines(data)

	os.system("source .bash_profile")

	os.chdir(current_directory)

	print(".bash_profile has been updated for the instance with id: {}. Be sure to open a new terminal window for changes to take effect".format(instance_obj.id))

def instance_state(instance_obj):
	"""
	Returns the state of the instance. I.e. Stopped, running, rebooting etc.
	"""

	return instance_obj.state['Name']

def start_instance(instance_obj, safety=True):
	"""
	This function takes an instance_obj and starts it up.

	The safety parameters default value is True - this means the function will ask for confirmation before starting the instance.

	If the safety parameter is set to False, it will automatically launch the instance.

	Inputs:
		instance_obj
	Returns:
		None
	"""

	if safety:
		question = input("Are you sure you want to start instance {}. [y/n]: ".format(instance_obj.id))
		
		if question == 'y':
			instance_obj.start()
			print("EC2 Instance with id {} has has been started".format(instance_obj.id))
		else:
			print("Operation aborted")
	else:
		instance_obj.start()
		print("EC2 Instance with id {} has has been started".format(instance_obj.id))

def stop_instance(instance_obj, safety=True):
	"""
	This function takes an instance_obj and stops it.

	The safety parameters default value is True - this means the function will ask for confirmation before stopping the instance.

	If the safety parameter is set to False, it will automatically stop the instance.

	NOTE: When stopping in the instance, you will lose all data stored in memory!

	Inputs:
		instance_obj
	Returns:
		None
	"""

	if safety:
		question = input("Are you sure you want to stop instance {}. [y/n]: ".format(instance_obj.id))

		if question == "y":
			instance_obj.stop()
			print("EC2 Instance with id {} has has been stopped".format(instance_obj.id))
		else:
			print("Operation aborted")
	else:
		instance_obj.stop()
		print("EC2 Instance with id {} has has been stopped".format(instance_obj.id))

def resize_instance(instance_obj, safety=True, big=False, small=False):
	"""
	This function takes an instance obj and resizes it to a higher or smaller instance.

	You can customize this function to suit your needs of big/small. Simply enter the appropriate tag in the value_to_switch variables below.

	The safety parameters default value is True - this means the function will ask for confirmation before resizing the instance.

	If the safety parameter is set to False, it will automatically resize the instance.

	Note: The instance ID remains the same for a resize! Be sure to update your .bash_profile IP with the update bash profile function.

	Inputs:
		instance_obj
	Returns:
		None
	"""
	ec2_resize = boto3.client('ec2', region_name="us-east-1",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

	instance_id = instance_obj.id
	instance_size = instance_obj.instance_type

	if not big and not small:
		print("You have not selected a size to alter. Operation aborted")

	if big:
		value_to_switch = "m4.16xlarge" #you can change this to match a big instance size that you use.
	elif small:
		value_to_switch = "m4.2xlarge" #you can change this to match a small instance size that you use.

	if safety:
		question = input("Are you sure you want to change the size of instance {} to an {}. [y/n]".format(instance_obj.id, value_to_switch))

		if question == "y":
			ec2_resize.stop_instances(InstanceIds=[instance_id])
			waiter = ec2_resize.get_waiter("instance_stopped")
			waiter.wait(InstanceIds=[instance_id])

			ec2_resize.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value=value_to_switch)

			print("The EC2 with id {} has been resized from {} to {}".format(instance_id, instance_size, value_to_switch))
			print()

		else:
			print("Operation Aborted")
	else:
		ec2_resize.stop_instances(InstanceIds=[instance_id])
		waiter = ec2_resize.get_waiter("instance_stopped")
		waiter.wait(InstanceIds=[instance_id])
		ec2_resize.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value=value_to_switch)

		print("The EC2 with id {} has been  resized from {} to {}".format(instance_id, instance_size, value_to_switch))
		print()
		print("Be sure to start this new instance and update your bash profile.")
		print()

def reboot_instance(instance_obj, safety=True):
	"""
	This function reboots a particular AWS EC2 instance.

	The safety parameters default value is True - this means the function will ask for confirmation before rebooting the instance.

	If the safety parameter is set to False, it will automatically reboot the instance.

	Inputs:
		instance_obj
	Returns:
		None
	"""

	if safety:
		question = input("Are you sure you want to reboot instance {}. [y/n]: ".format(instance_obj.id))
		
		if question == 'y':
			instance_obj.reboot()
			print("EC2 Instance with id {} is rebooting".format(instance_obj.id))
		else:
			print("Operation aborted")
	else:
		instance_obj.reboot()
		print("EC2 Instance with id {} is rebooting".format(instance_obj.id))

def view_tags(instance_obj):
	"""
	This function allows you to view the tags associated with a particular instance.

	Inputs:
		instance_obj
	Returns:
		None
	"""

	if len(instance_obj.tags) == 1:
		print("The tag associated with EC2 instance {} is:".format(instance_obj.id),instance_obj.tags[0]['Key'])
	else:
		tag_list = []
		for dict_ in instance_obj.tags:
			tag_val = dict_['Key']
			tag_list.append(tag_val)

		print("Here are the associated tags with EC2 instance {} is:".format(instance_obj.id), tag_list)
