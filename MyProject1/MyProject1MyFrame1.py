"""Subclass of MyFrame1, which is generated by wxFormBuilder."""

import wx
import MyProject1


# Implementing MyFrame1
class MyProject1MyFrame1(MyProject1.MyFrame1):
	def __init__(self, parent):
		MyProject1.MyFrame1.__init__(self, parent)

	# Handlers for MyFrame1 events.
	def m_button1OnButtonClick(self, event):
		# TODO: Implement m_button1OnButtonClick
		print('clicked!')
		wx.MessageBox('メッセージ', 'タイトル')
		dialog = wx.FileDialog(self, 'ファイルを選択してください', style=wx.FD_SAVE)
		dialog.ShowModal()
		select_file = dialog.GetPath()
		print('select_file={}'.format(select_file))


app = wx.App()
frame = MyProject1MyFrame1(None)
frame.Show()
app.SetTopWindow(frame)
app.MainLoop()
