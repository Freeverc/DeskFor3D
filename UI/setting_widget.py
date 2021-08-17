from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit
from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget


class Setting_widget(QWidget):
    def __init__(self, parent):
        super().__init__()
        # settings self.themes
        self.parent_widget = parent
        # self.themes = ['浅色', '深色']
        self.themes = ['浅色', '深色', '白色']
        self.theme = self.themes[1]
        self.theme_cb = QComboBox()
        self.theme_cb.setStatusTip("选择主题")
        self.theme_cb.addItems(self.themes)

        self.sfm_types = ['Global', 'Incremental', 'Hybrid']
        self.sfm_type = self.sfm_types[0]
        self.sfm_type_cb = QComboBox()
        self.sfm_type_cb.addItems(self.sfm_types)
        self.sfm_type_cb.setToolTip("SFM方法选择")

        self.depth_resolution_le = QLineEdit("1")
        self.depth_resolution_le.setToolTip("深度图生成分辨率参数，范围1-4, 默认为1，数字越大分辨率越低")

        self.fusion_neibor_num_le = QLineEdit("1")
        self.fusion_neibor_num_le.setToolTip("点云语义融合的最大的有效视角数量参数，范围1-5, 默认为3")

        self.dem_resolution_le = QLineEdit("1")
        self.dem_resolution_le.setToolTip(
            "正射投影图分辨率，1-5, 默认为1，数字越大分辨率越低")

        self.plane_thresh = QLineEdit("1")
        self.plane_thresh.setToolTip("平面检测的阈值范围，1-5, 默认为3")

        self.confirm_btn = QPushButton("确认")
        self.confirm_btn.clicked.connect(self.parent_widget.change_setting)
        self.cancel_btn = QPushButton("取消")
        self.confirm_btn.clicked.connect(self.parent_widget.change_setting)
        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.clicked.connect(self.parent_widget.reset_setting)

        self.theme_label = QLabel("主题")
        self.sfm_label = QLabel("SFM方法")
        self.depth_label = QLabel("深度图分辨率")
        self.fusion_neibor_num_label = QLabel("有效视角数量")
        self.dem_resolution_label = QLabel("正射投影图分辨率")
        self.plane_thresh_lable = QLabel("平面检测阈值")

        self.setting_layout = QGridLayout()
        self.setting_layout.addWidget(self.theme_label, 1, 1)
        self.setting_layout.addWidget(self.sfm_label, 3, 1)
        self.setting_layout.addWidget(self.depth_label, 4, 1)
        self.setting_layout.addWidget(self.fusion_neibor_num_label, 5, 1)
        self.setting_layout.addWidget(self.dem_resolution_label, 6, 1)
        self.setting_layout.addWidget(self.plane_thresh_lable, 7, 1)

        self.setting_layout.addWidget(self.confirm_btn, 9, 1)
        self.setting_layout.addWidget(self.reset_btn, 9, 2)

        self.setting_layout.addWidget(self.theme_cb, 1, 2)
        self.setting_layout.addWidget(self.sfm_type_cb, 3, 2)
        self.setting_layout.addWidget(self.depth_resolution_le, 4, 2)
        self.setting_layout.addWidget(self.fusion_neibor_num_le, 5, 2)
        self.setting_layout.addWidget(self.dem_resolution_le, 6, 2)
        self.setting_layout.addWidget(self.plane_thresh, 7, 2)

        self.setting_layout.setRowStretch(0, 1)
        self.setting_layout.setRowStretch(1, 1)
        self.setting_layout.setRowStretch(2, 1)
        self.setting_layout.setRowStretch(3, 1)
        self.setting_layout.setRowStretch(4, 1)
        self.setting_layout.setRowStretch(5, 1)
        self.setting_layout.setRowStretch(6, 1)
        self.setting_layout.setRowStretch(7, 1)
        self.setting_layout.setRowStretch(8, 1)
        self.setting_layout.setRowStretch(9, 1)
        self.setting_layout.setRowStretch(10, 1)
        self.setting_layout.setColumnStretch(0, 3)
        self.setting_layout.setColumnStretch(1, 3)
        self.setting_layout.setColumnStretch(2, 3)
        self.setLayout(self.setting_layout)
