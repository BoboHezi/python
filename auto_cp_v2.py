import os
import commands
import sys
import re

import RepoHandler
from RepoHandler import Remote
from RepoHandler import Project

def cherry_pick(path, cmd):
	os.chdir(path)
	result = commands.getstatusoutput(change_name(cmd))[0]
	if result != 0:
		commands.getstatusoutput('git cherry-pick --abort')
	print("%s result: %d" % (path, result))
	os.chdir(origin_path)

def change_name(cmd):
	name_start = cmd.find('ssh://') + 6
	name_end = cmd.find('@')
	if 0 < name_start < name_end:
		origin_name = cmd[name_start : name_end]
		if origin_name != git_user:
			return cmd.replace(origin_name, git_user)
	return cmd

def reset(path):
	os.chdir(path)
	status = commands.getstatusoutput('git status')
	print(path)
	if status[0] == 0:
		if True :#"Your branch is ahead of" in status[1] :
			# match = re.search('by [0-9] commit', status[1])
			if True:#match != None:
				heads = 1#int(match.group()[2 : match.group().find(' commit')])
				cmd = 'git reset --hard HEAD~%d' % heads
				reset_result = commands.getstatusoutput(cmd)[0]
				print(cmd)
	os.chdir(origin_path)

def read_cmds_from_file(path):
	file = open(path, 'r')
	str = file.read()
	lines = str.splitlines()
	result = []
	for line in lines:
		if not line.lstrip().startswith('#'):
			result.append(line)
	return result

git_user = ''
origin_path = ''
action = ''
projects = None

if (__name__ == '__main__'):
	git_user = commands.getstatusoutput('git config user.name')[1];
	origin_path = os.getcwd()

	projects = RepoHandler.dump_projects().projects

	git_path = {}
	for project in projects:
		git_path[project.name] = project.path

	action = 'cp'
	if len(sys.argv) > 1:
		action = sys.argv[1]

	for cmd in read_cmds_from_file('../cp_v2.txt'):
		match = re.search('[0-9]\/.*"', cmd)
		if match != None:
			git_name = match.group()[2 : -1]
			if git_path.has_key(git_name):
				path = git_path[git_name]
				if action =='cp':
					cherry_pick(origin_path + '/' + path, cmd)
				elif action == 'rst':
					reset(origin_path + '/' + path)