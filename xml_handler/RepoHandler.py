#!/usr/bin/python
import io
import xml.sax

class RepoHandler(xml.sax.ContentHandler):
	"""parse repo xml"""
	def __init__(self):
		self.default = Project()
		self.projects = []
		self.remotes = []
		self.includes = []

	def decodeProject(self, tag, attributes):
		project = Project()
		project.CurrentData = tag

		if 'name' in attributes:
			project.name = attributes['name']
		if 'path' in attributes:
			project.path = attributes['path']
		if 'revision' in attributes:
			project.revision = attributes['revision']
		if 'remote' in attributes:
			project.remote = attributes['remote']
		if 'sync-c' in attributes:
			project.sync_c = attributes['sync-c']
		if 'sync-j' in attributes:
			project.sync_j = attributes['sync-j']

		return project

	def startElement(self, tag, attributes):
		if tag == 'project':
			self.projects.append(self.decodeProject(tag, attributes))
		elif tag == 'remote':
			remote = Remote()
			remote.CurrentData = tag
			remote.name = attributes['name']
			remote.fetch = attributes['fetch']
			remote.review = attributes['review']
			self.remotes.append(remote)
		elif tag == 'default':
			self.default = self.decodeProject(tag, attributes)
		elif tag == 'include':
			self.includes.append(attributes['name'])

	def endElement(self, tag):
		pass

	def characters(self, content):
		pass

	def endDocument(self):
		self.sinkDefault()

	def sinkDefault(self):
		if self.default != None:
			for project in self.projects:
				if project.name == None or len(project.name) == 0:
					project.name = self.default.name
				if project.path == None or len(project.path) == 0:
					project.path = self.default.path
				if project.revision == None or len(project.revision) == 0:
					project.revision = self.default.revision
				if project.remote == None:
					project.remote = self.default.remote
				if project.sync_c == None or len(project.sync_c) == 0:
					project.sync_c = self.default.sync_c
				if project.sync_j == -1:
					project.sync_j = self.default.sync_j

	def __str__(self):
		msg = 'RepoHandler, default: '
		msg += str(self.default)
		msg += ', projects: '
		for project in self.projects:
			msg += str(project)
			msg += ', '
		msg += ', remotes: '
		for remote in self.remotes:
			msg += str(remote)
			msg += ', '

		return msg

class Remote():
	"""holder of Remote"""
	def __init__(self):
		self.CurrentData = ''
		self.name = ''
		self.fetch = ''
		self.review = ''

	def __str__(self):
		return '[Remote, name: %s, fetch: %s, review: %s]' % (self.name, self.fetch, self.review)

class Project():
	"""docstring for Project"""
	def __init__(self):
		self.CurrentData = ''
		self.name = ''
		self.path = ''
		self.revision = ''
		self.remote = None
		self.sync_c = ''
		self.sync_j = -1

	def __str__(self):
		return '[Project, path: %s, name: %s, revision: %s, remote: %s, sync_c: %s, sync_j: %s]' \
			% (self.path, self.name, self.revision, str(self.remote), self.sync_c, str(self.sync_j))

if ( __name__ == "__main__"):

    parser = xml.sax.make_parser()

    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = RepoHandler()
    parser.setContentHandler( Handler )

    parser.parse('repo/manifest.xml')

    if len(Handler.includes) != 0:
    	for include in Handler.includes:
    		parser.parse('repo/' + include)

    # print(Handler.default)

    # for remote in Handler.remotes:
    # 	print(remote)

    for project in Handler.projects:
    	print(project)