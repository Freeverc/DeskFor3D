#!/usr/bin/python3
# -*- encoding: utf-8 -*-
#

import sys
import os
import vtk
import open3d as o3d
import numpy as np
import vtk_visualizer as vv
import reconstruction
import setting_widget

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.pyplot import figure
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QLabel, QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class PointCanvas(FigureCanvas):  # Class for 3D window
    def __init__(self):
        # self.plot_figure = figure(figsize=(100, 100))
        self.figure = figure()
        FigureCanvas.__init__(self, self.figure)  # creating FigureCanvas
        self.axes = self.figure.gca(
            projection='3d')  # generates 3D Axes object
        self.setWindowTitle("sfm")  # sets Window title

    def draw_points(self, x, y, z):  # Function for graph plotting
        self.axes.scatter(x, y, z)
        self.draw()


class ReconstructionTool(QWidget):
    def __init__(self):
        super().__init__()
        self.image_dir = ''
        self.depth_dir = ''
        self.output_dir = ''
        self.mvs_dir = ''

        self.themes = ['浅色', '深色', '白色']
        self.setStyleSheet(
            "QWidget{color: black; background-color:#d0dadf;}QPushButton, QComboBox, QLineEdit{background-color: #d0dadf}"
        )
        # self.setStyleSheet("QWidget{color: black; background-color:white;}QPushButton, QComboBox, QLineEdit{ background-color: white}")
        # self.setStyleSheet("QWidget{color: #b0b0b0; background-color:#203040;}QPushButton, QComboBox, QLineEdit{ background-color: #304050}")
        self.sfm_types = ['Global', 'Incremental', 'Hybrid']
        self.seg_types = ['MPFA-Net', 'SegNet', 'DeepLab v3+', 'PSPNet']
        self.options = {'theme': '浅色', 'sfm_type': 'Global', 'depth_resolution': 1,
                        'fusion_neibor_num': 1, 'dem_resolution': 1, 'plane_thresh': 1}

        self.button_widget = QWidget()
        self.setting_widget = setting_widget.Setting_widget(self)
        self.sfm_widget = PointCanvas()
        self.mvs_widget = QVTKRenderWindowInteractor()
        self.dem_widget = QWidget()
        self.message_box = QMessageBox()
        self.figure_able = 0

        self.init_ui()

    def init_ui(self):
        self.init_button_widget()
        self.init_sfm_widget()
        self.init_mvs_widget()
        # show
        self.layout = QGridLayout()
        self.layout.addWidget(self.button_widget, 1, 1, 1, 2)
        self.layout.addWidget(self.sfm_widget, 2, 1)
        self.layout.addWidget(self.mvs_widget, 2, 2)
        self.layout.addWidget(self.dem_widget, 3, 1)
        self.layout.addWidget(self.setting_widget, 3, 3)

        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 6)
        self.layout.setRowStretch(3, 6)
        self.layout.setColumnStretch(1, 6)
        self.layout.setColumnStretch(2, 6)
        self.layout.setColumnStretch(3, 6)
        self.setLayout(self.layout)
        # calc_hwnd = win32gui.FindWindow(None, r"C:\WINDOWS\system32\cmd.exe")
        # win32gui.SetParent(calc_hwnd, int(self.winId()))

        # self.button_widget.setFixedHeight(60)
        self.setWindowTitle('三维重建')
        self.setWindowIcon(QIcon(r'themes\wine.ico'))
        # desktop = QApplication.desktop()
        # self.resize(desktop.width(), desktop.height()-80)
        self.resize(1200, 800)
        self.move(80, 80)
        self.show()

    def init_button_widget(self):
        # Buttons
        import_btn = QPushButton('导入图像')
        import_btn.setToolTip('选择图像文件夹')
        import_btn.clicked.connect(self.import_image_func)

        sparse_btn = QPushButton('稀疏重建')
        sparse_btn.setToolTip('重建稀疏点云')
        sparse_btn.clicked.connect(self.sparse_func)

        dense_btn = QPushButton('稠密重建')
        dense_btn.setToolTip('重建稠密点云')
        dense_btn.clicked.connect(self.dense_func)

        dem_btn = QPushButton('计算DEM')
        dem_btn.setToolTip('生成DEM')
        dem_btn.clicked.connect(self.dem_func)

        plane_btn = QPushButton('计算结构面')
        plane_btn.setToolTip('计算结构面')
        plane_btn.clicked.connect(self.dem_func)

        save_btn = QPushButton('保存')
        save_btn.setToolTip('保存图像或数据')
        save_btn.clicked.connect(self.save_func)

        settint_btn = QPushButton('设置')
        settint_btn.setToolTip('设置显示的图像和数据格式')
        settint_btn.clicked.connect(self.setting_func)

        clear_btn = QPushButton('清空')
        clear_btn.setToolTip('清空图像和数据')
        clear_btn.clicked.connect(self.clear_func)

        exit_btn = QPushButton('退出')
        exit_btn.setToolTip('退出程序')
        exit_btn.clicked.connect(self.exit_func)

        # button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(import_btn)
        button_layout.addWidget(sparse_btn)
        button_layout.addWidget(dense_btn)
        button_layout.addWidget(dem_btn)
        button_layout.addWidget(plane_btn)
        button_layout.addWidget(settint_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(exit_btn)

        self.button_widget.setLayout(button_layout)

    def init_sfm_widget(self):
        pass

    def init_mvs_widget(self):
        self.ren = vtk.vtkRenderer()
        self.mvs_widget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.mvs_widget.GetRenderWindow().GetInteractor()

    def import_image_func(self):
        self.image_dir = QFileDialog.getExistingDirectory(self, '选择输入图像文件夹')
        print(self.image_dir)

    def sparse_func(self):
        # self.output_dir = QFileDialog.getExistingDirectory(self, '选择输出文件夹')
        # reconstruction.sparse_reconstruct(self.image_dir, self.output_dir)
        # self.show_message("稀疏重建完成")
        self.sfm_show()

    def dense_func(self):
        # if len(self.mvs_dir) < 2:
        #     self.mvs_dir = QFileDialog.getExistingDirectory(self, '选择mvs文件夹')
        # reconstruction.dense_reconstruct(self.mvs_dir)
        # self.show_message("稠密重建完成")
        self.mvs_show()

    def sfm_show(self):
        file_name = os.path.join(
            "C://Users//Freeverc//Projects//Fun//Reconstruction//ReconstructionTool//data//out2//sfm",
            "cloud_and_poses.ply")

        point_cloud = o3d.io.read_point_cloud(file_name)
        data = np.asarray(point_cloud.points)
        print(np.shape(data))
        self.sfm_widget.draw_points(data[:, 0], data[:, 1], data[:, 2])

    def mvs_show(self):
        file_name = os.path.join(
            "C://Users//Freeverc//Projects//Fun//Reconstruction//ReconstructionTool//data//out2//mvs",
            "scene_dense_mesh.ply")
        path, extension = os.path.splitext(file_name)
        extension = extension.lower()
        if extension == '.ply':
            reader = vtk.vtkPLYReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly_data)
        mapper.SetColorModeToDefault()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        colors = vtk.vtkNamedColors()
        actor.GetProperty().SetColor(colors.GetColor3d('Tomato'))
        actor.GetProperty().SetPointSize(4)

        self.ren.AddActor(actor)
        self.ren.ResetCamera()
        self.ren.SetBackground(colors.GetColor3d('DarkGreen'))

        self.iren.Initialize()
        self.mvs_widget.GetRenderWindow().AddRenderer(self.ren)
        self.mvs_widget.GetRenderWindow().Render()
        self.iren.Start()

    def dem_func(self):
        if len(self.mvs_dir) < 2:
            self.mvs_dir = QFileDialog.getExistingDirectory(self, '选择mvs文件夹')
        reconstruction.generate_dem(self.mvs_dir)
        self.show_message("计算DEM完成")

    def detect_planes_func(self):
        if len(self.mvs_dir) < 2:
            self.mvs_dir = QFileDialog.getExistingDirectory(self, '选择mvs文件夹')
        reconstruction.detect_planes(self.mvs_dir)
        self.show_message("检测平面完成")

    def setting_func(self):
        self.setting_widget.setVisible(True)
        # self.figure_layout.removeWidget(self.table)
        # self.figure_layout.removeWidget(self.canvas)
        # self.figure_layout.addWidget(self.setting_widget)
        # self.setting_widget.show()
        pass

    def save_func(self):
        pass

    def clear_func(self):
        sender = self.sender()
        if sender == self.clear_btn:
            self.show_message("清理成功")
        print("clearing data")
        self.main_state = 0
        self.table.setVisible(False)
        self.canvas.setVisible(False)
        self.setting_widget.setVisible(False)
        plt.cla()

    def exit_func(self):
        print("exited")
        self.close()
        # sys.exit(app.exec_())

    def show_message(self, text):
        self.message_box.setText(text)
        self.message_box.show()

    # 改变设置
    def change_setting(self):
        print("changing settings")
        try:
            self.options['theme'] = self.setting_widget.theme_cb.currentText()
            self.options['sfm_type'] = self.setting_widget.sfm_type_cb.currentText()
            self.options['depth_resolution'] = int(
                self.setting_widget.depth_resolution_le.text())
            self.options['fusion_neibor_num'] = int(
                self.setting_widget.fusion_neibor_num_le.text())
            self.options['dem_resolution']= int(
                self.setting_widget.dem_resolution_le.text())
            self.options['plane_thresh'] = int(
                self.setting_widget.plane_thresh.text())
        except:
            self.reset_setting()
        # print(self.theme, self.pca_top, self.knn_top, self.svm_type, self.bp_lr, self.bp_epoch)
        if self.options['theme'] == self.themes[0]:
            self.setStyleSheet(
                "QWidget{color: black; background-color:#d0dadf;}QPushButton, QComboBox, QLineEdit{background-color: #d0dadf}"
            )
        elif self.options['theme'] == self.themes[1]:
            self.setStyleSheet(
                "QWidget{color: #b0b0b0; background-color:#203040;}QPushButton, QComboBox, QLineEdit{ background-color: #304050}"
            )
        elif self.options['theme'] == self.themes[2]:
            self.setStyleSheet(
                "QWidget{color: black; background-color:white;}QPushButton, QComboBox, QLineEdit{ background-color: white}"
            )

    # 重置设置
    def reset_setting(self):
        print("reseting settings")
        self.options = {'theme': '浅色', 'sfm_type': 'Global', 'depth_resolution': 1,
                        'fusion_neibor_num': 1, 'dem_resolution': 1, 'plane_thresh': 1}
        self.setStyleSheet(
            "QWidget{color: black; background-color:#d0dadf;}QPushButton, QComboBox, QLineEdit{background-color: #d0dadf}"
        )

        self.setting_widget.theme_cb.setCurrentText(self.theme)
        self.setting_widget.sfm_type_cb.setCurrentText(self.sfm_type)
        self.setting_widget.depth_resolution_le.setText(
            str(self.options['depth_resolution']))
        self.setting_widget.fusion_neibor_num_le.setText(
            str(self.options['fusion_neibor_num']))
        self.setting_widget.dem_resolution_le.setText(
            str(self.options['dem_resolution']))
        self.setting_widget.plane_thresh.setText(
            str(self.options['plane_thresh']))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    WC = ReconstructionTool()
    print("running")
    sys.exit(app.exec_())
