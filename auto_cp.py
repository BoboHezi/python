import os
import commands

def cherry_pick(path, cmd):
	os.chdir(path)
	print(commands.getstatusoutput(change_name(cmd)))

def change_name(cmd):
	name_start = cmd.find('ssh://') + 6
	name_end = cmd.find('@')
	if 0 < name_start < name_end:
		origin_name = cmd[name_start : name_end]
		if origin_name != git_user:
			return cmd.replace(origin_name, git_user)
	return cmd

def read_cmds_from_file(path):
	file = open(path, 'r')
	str = file.read()
	lines = str.splitlines()
	for line in lines:
		ele = line.split('#')
		if len(ele) == 2:
			path = ele[0]
			cmd = ele[1]
			cherry_pick(os.getcwd() + '/' + path, cmd)

git_user = commands.getstatusoutput('git config user.name')[1];

read_cmds_from_file('cp.txt')