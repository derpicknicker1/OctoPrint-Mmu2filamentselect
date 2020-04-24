# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from threading import Timer

from octoprint.server import user_permission

import flask
from flask_babel import gettext


class MMU2SelectPlugin(octoprint.plugin.TemplatePlugin, octoprint.plugin.SettingsPlugin, octoprint.plugin.SimpleApiPlugin, octoprint.plugin.AssetPlugin):

	def __init__(self):
		self._active = False
		self._timer = None
		self._timeout = 0
		self._txTriggered = False
		self._selectedTool = None

	def initialize(self):
		self._timeout = self._settings.get([b"timeout"])

	#~ queuing handling

	def gcode_queuing_handler(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
		if not cmd.startswith("Tx") and not cmd.startswith("M109"):
			return

		if "mmu2Plugin:choose_filament_resend" in tags:
			return

		if cmd.startswith("M109"):
			if self._selectedTool is not None and self._txTriggered:
				tool_cmd = self._selectedTool
				self._selectedTool = None
				self._txTriggered = False
				return[(cmd,),
					(tool_cmd,)]
			else:
				return

		if cmd.startswith("Tx"):
			if self._printer.set_job_on_hold(True):
				self._show_prompt()

		return None,

	#~ SettingsPlugin

	def get_settings_defaults(self):
		return dict(timeout=30)

	def on_settings_save(self, data):
		try:
			data[b"timeout"]=int(data[b"timeout"])
		except:
			data[b"timeout"]=30

		if data[b"timeout"] < 0:
			data[b"timeout"]=30

		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self._timeout = self._settings.get([b"timeout"])

	#~ TemplatePlugin

	def get_template_configs(self):
		return [
			dict(type="settings", name=gettext("MMU2 Select Filament"), custom_bindings=False)
		]

	#~ AssetPlugin

	def get_assets(self):
		return dict(
			js=["js/mmu2filamentselect.js"]
		)

	#~ prompt handling

	def _show_prompt(self):
		self._active = True
		self._timer = Timer(float(self._timeout), self._timeout_prompt)
		self._timer.start()
		self._plugin_manager.send_plugin_message(self._identifier, dict(action="show"))

	def _timeout_prompt(self):
		self._printer.commands("Tx", tags={"mmu2Plugin:choose_filament_resend"})
		self._clean_up_prompt()

	def _done_prompt(self, command, tags=set()):
		self._selectedTool = command
		self._txTriggered = True
		self._clean_up_prompt()

	def _clean_up_prompt(self):
		self._timer.cancel()
		self._active = False
		self._plugin_manager.send_plugin_message(self._identifier, dict(action="close"))
		self._printer.set_job_on_hold(False)

	#~ SimpleApiPlugin

	def get_api_commands(self):
		return dict(select=["choice"])

	def on_api_command(self, command, data):
		if command == "select":
			if not user_permission.can():
				return flask.abort(403, "Insufficient permissions")

			if self._active is False:
				return flask.abort(409, "No active prompt")

			choice = data["choice"]
			if not isinstance(choice, int) or not choice < 5 or not choice >= 0:
				return flask.abort(400, "{!r} is not a valid value for filament choice".format(choice+1))

			self._done_prompt("T" + str(choice))

	#~ Update

	def get_update_information(self, *args, **kwargs):
		return dict(
			mmu2filamentselect=dict(
				displayName=self._plugin_name,
				displayVersion=self._plugin_version,

				type="github_release",
				current=self._plugin_version,
				user="derPicknicker1",
				repo="OctoPrint-Mmu2filamentselect",

				pip="https://github.com/derPicknicker1/OctoPrint-Mmu2filamentselect/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "Prusa MMU2 Select Filament"
__plugin_implementation__ = MMU2SelectPlugin()
__plugin_hooks__ = {
	b"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.gcode_queuing_handler,
	b"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
