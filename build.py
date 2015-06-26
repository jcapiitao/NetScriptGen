from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.pycharm")
use_plugin("python.install_dependencies")


name = "NetScriptGen"
default_task = "publish"


@init
def set_properties(project):
	project.build_depends_on('coverage')
	project.set_property('coverage_break_build', True)
	project.set_property('coverage_threshold_warn', 70)

	project.set_property('flake8_break_build', False)
	project.set_property('flake8_verbose_output', True)
	project.set_property('flake8_include_test_sources', True)
	project.set_property('flake8_max_line_length', 120)


