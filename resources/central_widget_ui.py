# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'central_widget.ui'
#
# Created: Sat Jul 18 11:03:57 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(756, 580)
        Form.setMinimumSize(QtCore.QSize(756, 580))
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gif_player = QtGui.QLabel(Form)
        self.gif_player.setMinimumSize(QtCore.QSize(623, 285))
        self.gif_player.setText(_fromUtf8(""))
        self.gif_player.setObjectName(_fromUtf8("gif_player"))
        self.verticalLayout.addWidget(self.gif_player)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.play_btn = QtGui.QPushButton(Form)
        self.play_btn.setObjectName(_fromUtf8("play_btn"))
        self.horizontalLayout.addWidget(self.play_btn)
        self.pause_btn = QtGui.QPushButton(Form)
        self.pause_btn.setObjectName(_fromUtf8("pause_btn"))
        self.horizontalLayout.addWidget(self.pause_btn)
        self.next_frame_btn = QtGui.QPushButton(Form)
        self.next_frame_btn.setObjectName(_fromUtf8("next_frame_btn"))
        self.horizontalLayout.addWidget(self.next_frame_btn)
        self.stop_btn = QtGui.QPushButton(Form)
        self.stop_btn.setObjectName(_fromUtf8("stop_btn"))
        self.horizontalLayout.addWidget(self.stop_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.width_label = QtGui.QLabel(Form)
        self.width_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.width_label.setObjectName(_fromUtf8("width_label"))
        self.gridLayout.addWidget(self.width_label, 2, 0, 1, 1)
        self.scale_input = QtGui.QLineEdit(Form)
        self.scale_input.setObjectName(_fromUtf8("scale_input"))
        self.gridLayout.addWidget(self.scale_input, 2, 5, 1, 1)
        self.scale_check = QtGui.QCheckBox(Form)
        self.scale_check.setObjectName(_fromUtf8("scale_check"))
        self.gridLayout.addWidget(self.scale_check, 2, 4, 1, 1)
        self.width_input = QtGui.QLineEdit(Form)
        self.width_input.setObjectName(_fromUtf8("width_input"))
        self.gridLayout.addWidget(self.width_input, 2, 1, 1, 1)
        self.fps_label = QtGui.QLabel(Form)
        self.fps_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fps_label.setObjectName(_fromUtf8("fps_label"))
        self.gridLayout.addWidget(self.fps_label, 3, 0, 1, 1)
        self.start_label = QtGui.QLabel(Form)
        self.start_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.start_label.setObjectName(_fromUtf8("start_label"))
        self.gridLayout.addWidget(self.start_label, 1, 0, 1, 1)
        self.height_label = QtGui.QLabel(Form)
        self.height_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.height_label.setObjectName(_fromUtf8("height_label"))
        self.gridLayout.addWidget(self.height_label, 2, 2, 1, 1)
        self.height_input = QtGui.QLineEdit(Form)
        self.height_input.setObjectName(_fromUtf8("height_input"))
        self.gridLayout.addWidget(self.height_input, 2, 3, 1, 1)
        self.end_input = QtGui.QLineEdit(Form)
        self.end_input.setObjectName(_fromUtf8("end_input"))
        self.gridLayout.addWidget(self.end_input, 1, 3, 1, 1)
        self.video_file_label = QtGui.QLabel(Form)
        self.video_file_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.video_file_label.setObjectName(_fromUtf8("video_file_label"))
        self.gridLayout.addWidget(self.video_file_label, 0, 0, 1, 1)
        self.fps_input = QtGui.QLineEdit(Form)
        self.fps_input.setObjectName(_fromUtf8("fps_input"))
        self.gridLayout.addWidget(self.fps_input, 3, 1, 1, 1)
        self.end_label = QtGui.QLabel(Form)
        self.end_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.end_label.setObjectName(_fromUtf8("end_label"))
        self.gridLayout.addWidget(self.end_label, 1, 2, 1, 1)
        self.start_input = QtGui.QLineEdit(Form)
        self.start_input.setObjectName(_fromUtf8("start_input"))
        self.gridLayout.addWidget(self.start_input, 1, 1, 1, 1)
        self.video_file_btn = QtGui.QPushButton(Form)
        self.video_file_btn.setObjectName(_fromUtf8("video_file_btn"))
        self.gridLayout.addWidget(self.video_file_btn, 0, 5, 1, 1)
        self.video_file_input = QtGui.QLineEdit(Form)
        self.video_file_input.setObjectName(_fromUtf8("video_file_input"))
        self.gridLayout.addWidget(self.video_file_input, 0, 1, 1, 3)
        self.mirror_check = QtGui.QCheckBox(Form)
        self.mirror_check.setObjectName(_fromUtf8("mirror_check"))
        self.gridLayout.addWidget(self.mirror_check, 3, 4, 1, 2)
        self.speed_label = QtGui.QLabel(Form)
        self.speed_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.speed_label.setObjectName(_fromUtf8("speed_label"))
        self.gridLayout.addWidget(self.speed_label, 3, 2, 1, 1)
        self.speed_input = QtGui.QLineEdit(Form)
        self.speed_input.setObjectName(_fromUtf8("speed_input"))
        self.gridLayout.addWidget(self.speed_input, 3, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(200)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.reset_btn = QtGui.QPushButton(Form)
        self.reset_btn.setMinimumSize(QtCore.QSize(0, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(241, 98, 95))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(241, 98, 95))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.reset_btn.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.reset_btn.setFont(font)
        self.reset_btn.setObjectName(_fromUtf8("reset_btn"))
        self.horizontalLayout_2.addWidget(self.reset_btn)
        self.generate_btn = QtGui.QPushButton(Form)
        self.generate_btn.setMinimumSize(QtCore.QSize(0, 40))
        self.generate_btn.setObjectName(_fromUtf8("generate_btn"))
        self.horizontalLayout_2.addWidget(self.generate_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.video_file_input, self.video_file_btn)
        Form.setTabOrder(self.video_file_btn, self.start_input)
        Form.setTabOrder(self.start_input, self.end_input)
        Form.setTabOrder(self.end_input, self.width_input)
        Form.setTabOrder(self.width_input, self.height_input)
        Form.setTabOrder(self.height_input, self.scale_check)
        Form.setTabOrder(self.scale_check, self.scale_input)
        Form.setTabOrder(self.scale_input, self.fps_input)
        Form.setTabOrder(self.fps_input, self.speed_input)
        Form.setTabOrder(self.speed_input, self.mirror_check)
        Form.setTabOrder(self.mirror_check, self.reset_btn)
        Form.setTabOrder(self.reset_btn, self.generate_btn)
        Form.setTabOrder(self.generate_btn, self.play_btn)
        Form.setTabOrder(self.play_btn, self.pause_btn)
        Form.setTabOrder(self.pause_btn, self.next_frame_btn)
        Form.setTabOrder(self.next_frame_btn, self.stop_btn)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.play_btn.setText(_translate("Form", "Play", None))
        self.pause_btn.setText(_translate("Form", "Pause", None))
        self.next_frame_btn.setText(_translate("Form", "Next Frame", None))
        self.stop_btn.setText(_translate("Form", "Stop", None))
        self.width_label.setText(_translate("Form", "Width (px)", None))
        self.scale_check.setText(_translate("Form", "Scale", None))
        self.fps_label.setText(_translate("Form", "FPS", None))
        self.start_label.setText(_translate("Form", "Start Time(s)", None))
        self.height_label.setText(_translate("Form", "Height (px)", None))
        self.video_file_label.setText(_translate("Form", "Video File", None))
        self.end_label.setText(_translate("Form", "End Time (s)", None))
        self.video_file_btn.setText(_translate("Form", "Open Video", None))
        self.mirror_check.setText(_translate("Form", "Mirror GIF", None))
        self.speed_label.setText(_translate("Form", "Speed", None))
        self.reset_btn.setText(_translate("Form", "Reset", None))
        self.generate_btn.setText(_translate("Form", "Generate GIF", None))
