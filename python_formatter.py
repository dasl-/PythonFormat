import sublime, sublime_plugin, python_beautifier, re

s = sublime.load_settings('PythonFormat.sublime-settings')

class PythonFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		selection = []
		nwsOffset = self.prev_non_whitespace()

		# do formatting and replacement
		replaceRegion = None
		formatSelection = False

		replaceRegion = sublime.Region(0, self.view.size())
		res = python_beautifier.beautify(self.view.substr(replaceRegion))
		self.view.replace(edit, replaceRegion, res)

		# re-place cursor
		offset = self.get_nws_offset(nwsOffset, self.view.substr(sublime.Region(
                                     0, self.view.size())))
		rc = self.view.rowcol(offset)
		pt = self.view.text_point(rc[0], rc[1])
		sel = self.view.sel()
		sel.clear()
		self.view.sel().add(sublime.Region(pt))

		self.view.show_at_center(pt)

	def prev_non_whitespace(self):
		pos = self.view.sel()[0].a
		preTxt = self.view.substr(sublime.Region(0, pos));
		return len(re.findall('\S', preTxt))

	def get_nws_offset(self, nonWsChars, buff):
		nonWsSeen = 0
		offset = 0
		for i in range(0, len(buff)):
			offset += 1
			if (not (buff[i].isspace())):
				nonWsSeen += 1

			if (nonWsSeen == nonWsChars):
				break

		return offset