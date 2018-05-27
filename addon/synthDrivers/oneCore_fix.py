# coding: utf-8

import os

import globalPluginHandler

from synthDrivers import oneCore

import _winreg
from synthDriverHandler import SynthDriver, VoiceInfo
from logHandler import log

class SynthDriver(oneCore.SynthDriver):
	name="oneCore_fix"
	# Translators: Description for a speech synthesizer.
	description = _("Windows OneCore voices (fix)")

	def _isVoiceValid(self, id):
		idParts = id.split('\\')
		rootKey = getattr(_winreg, idParts[0])
		subkey = "\\".join(idParts[1:])
		try:
			hkey = _winreg.OpenKey(rootKey, subkey)
		except WindowsError as e:
			log.debugWarning("Could not open registry key %s, %s" % (id, ''))
			return False
		try:
			langDataPath = _winreg.QueryValueEx(hkey, 'langDataPath')
		except WindowsError as e:
			log.debugWarning("Could not open registry value 'langDataPath', %s" % '')
			return False
		if not langDataPath or not isinstance(langDataPath[0], basestring):
			log.debugWarning("Invalid langDataPath value")
			return False
		if not os.path.isfile(os.path.expandvars(langDataPath[0])):
			log.debugWarning("Missing language data file: %s" % langDataPath[0])
			return False
		try:
			voicePath = _winreg.QueryValueEx(hkey, 'voicePath')
		except WindowsError as e:
			log.debugWarning("Could not open registry value 'langDataPath', %s" % '')
			return False
		if not voicePath or not isinstance(voicePath[0],basestring):
			log.debugWarning("Invalid voicePath value")
			return False
		if not os.path.isfile(os.path.expandvars(voicePath[0] + '.apm')):
			log.debugWarning("Missing voice file: %s" % voicePath[0] + ".apm")
			return False
		return True
