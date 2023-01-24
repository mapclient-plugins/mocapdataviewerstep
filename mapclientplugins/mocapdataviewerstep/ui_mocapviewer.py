# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mocapviewer.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from mapclientplugins.mocapdataviewerstep.zincwidget import ZincWidget

class Ui_MOCAPViewer(object):
    def setupUi(self, MOCAPViewer):
        if not MOCAPViewer.objectName():
            MOCAPViewer.setObjectName(u"MOCAPViewer")
        MOCAPViewer.resize(907, 596)
        self.gridLayout = QGridLayout(MOCAPViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(MOCAPViewer)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.zincWidget = ZincWidget(self.groupBox_2)
        self.zincWidget.setObjectName(u"zincWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.zincWidget.sizePolicy().hasHeightForWidth())
        self.zincWidget.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.zincWidget)


        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 2)

        self.groupBox = QGroupBox(MOCAPViewer)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.listWidget = QListWidget(self.groupBox)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_2.addWidget(self.listWidget)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.pushButtonDone = QPushButton(MOCAPViewer)
        self.pushButtonDone.setObjectName(u"pushButtonDone")

        self.verticalLayout_3.addWidget(self.pushButtonDone)


        self.gridLayout.addLayout(self.verticalLayout_3, 1, 2, 1, 1)

        self.groupBox_4 = QGroupBox(MOCAPViewer)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(15)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.labelSlider = QLabel(self.groupBox_4)
        self.labelSlider.setObjectName(u"labelSlider")

        self.horizontalLayout.addWidget(self.labelSlider)

        self.horizontalSlider = QSlider(self.groupBox_4)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalSlider)

        self.pushButtonPlay = QPushButton(self.groupBox_4)
        self.pushButtonPlay.setObjectName(u"pushButtonPlay")

        self.horizontalLayout.addWidget(self.pushButtonPlay)


        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 1)

        self.groupBox_3 = QGroupBox(MOCAPViewer)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.spinBox = QSpinBox(self.groupBox_3)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_2.addWidget(self.spinBox)


        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)


        self.retranslateUi(MOCAPViewer)

        QMetaObject.connectSlotsByName(MOCAPViewer)
    # setupUi

    def retranslateUi(self, MOCAPViewer):
        MOCAPViewer.setWindowTitle(QCoreApplication.translate("MOCAPViewer", u"MOCAP Viewer", None))
        self.groupBox_2.setTitle("")
        self.groupBox.setTitle(QCoreApplication.translate("MOCAPViewer", u"Labels", None))
        self.pushButtonDone.setText(QCoreApplication.translate("MOCAPViewer", u"&Done", None))
        self.groupBox_4.setTitle("")
#if QT_CONFIG(tooltip)
        self.labelSlider.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.labelSlider.setText(QCoreApplication.translate("MOCAPViewer", u"Time", None))
        self.pushButtonPlay.setText(QCoreApplication.translate("MOCAPViewer", u"&Play", None))
        self.groupBox_3.setTitle("")
        self.label.setText(QCoreApplication.translate("MOCAPViewer", u"Icon size:", None))
    # retranslateUi

