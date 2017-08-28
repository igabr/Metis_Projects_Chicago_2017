#Created by Ibrahim Gabr
#This script should be run on the local version of your shell - not on AWS itself.
import boto3
import botocore
import os

ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]

SECRET_KEY = os.environ['AWS_SECRET_KEY']

ec2 = boto3.resource('ec2', region_name="us-east-1",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

def view_all_instances():
	instance_lst = []

	for instance in ec2.instances.all():
		instance_lst.append(instance)

	return instance_lst

def update_bash_profile(instance_obj):

	current_directory = os.getcwd()

	os.chdir('/Users/igabr')
	
	with open('.bash_profile', 'r') as file:
		data = file.readlines()

	data[5] = 'export metis_chi17_url="{}"\n'.format(instance_obj.public_dns_name)

	with open('.bash_profile', 'w') as file:
		file.writelines( data )

	os.system("source .bash_profile")

	os.chdir(current_directory)

	print(".bash_profile has been updated for the instance with id: {}. Be sure to open a new shell for changes to take effect".format(instance_obj.id))

def instance_state(instance_obj):

	return instance_obj.state['Name']

def start_instance(instance_obj, safety=True):

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
	Note: The instance ID remains the same for a resize! Be sure to update your .bash_profile IP
	"""
	ec2_resize = boto3.client('ec2', region_name="us-east-1",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

	instance_id = instance_obj.id
	instance_size = instance_obj.instance_type

	if big:
		value_to_switch = "m4.16xlarge"
	elif small:
		value_to_switch = "m4.2xlarge"

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

	if len(instance_obj.tags) == 1:
		print("The tag associated with EC2 instance {} is:".format(instance_obj.id),instance_obj.tags[0]['Key'])
	else:
		tag_list = []
		for dict_ in instance_obj.tags:
			tag_val = dict_['Key']
			tag_list.append(tag_val)

		print("Here are the associated tags with EC2 instance {} is:".format(instance_obj.id), tag_list)
