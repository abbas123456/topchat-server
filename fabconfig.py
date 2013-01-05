from fabric.api import env
from fabric.operations import prompt

def live():
	"Development Settings"

	env.hosts = ['178.79.174.162']
	env.Environment = 'prod'

	"Git Repository Settings"
	env.tag = prompt('Release version to deploy? [e.g: 1.1] ')
	env.branch = '%s' % env.tag
	env.repo = 'origin'

	"Application Paths"
	env.AppRoot = '/var/www/topchat-server'

	"Build Settings"
	env.BuildName = 'prod'
	env.BuildRoot = '%(AppRoot)s/builds/%(tag)s' % env
