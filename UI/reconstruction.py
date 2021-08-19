import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import subprocess

OPENMVG_BIN = "..\\openmvg_bin"
OPENMVS_BIN = "..\\openmvs_bin"


def sparse_reconstruct(image_dir, output_dir):
    print(output_dir)
    sfm_dir = os.path.join(output_dir, 'sfm')
    mvs_dir = os.path.join(output_dir, 'mvs')
    matches_dir = os.path.join(sfm_dir, 'matches')
    mkdir(sfm_dir)
    mkdir(mvs_dir)
    mkdir(matches_dir)
    cmd0_list = [
        os.path.join(OPENMVG_BIN,
                     "openMVG_main_SfMInit_ImageListing"), "-i",
        image_dir, "-o", matches_dir, "-d",
        os.path.join(OPENMVG_BIN, 'sensor_width_camera_database.txt')
    ]
    cmd1_list = [
        os.path.join(OPENMVG_BIN,
                     "openMVG_main_ComputeFeatures"), "-i",
        os.path.join(matches_dir, 'sfm_data.json'), "-o", matches_dir,
        "-m", "SIFT", "-n", "4"
    ]
    cmd2_list = [
        os.path.join(OPENMVG_BIN,
                     "openMVG_main_ComputeMatches"), "-i",
        os.path.join(matches_dir, 'sfm_data.json'), "-o", matches_dir,
        "-n", "HNSWL2", "-r", ".8", "-g", "e"
    ]
    cmd4_list = [
        os.path.join(OPENMVG_BIN, "openMVG_main_GlobalSfM"), "-i",
        os.path.join(matches_dir, 'sfm_data.json'), "-m", matches_dir,
        "-o", sfm_dir
    ]
    cmd9_list = [
        os.path.join(OPENMVG_BIN, "openMVG_main_openMVG2openMVS"),
        "-i",
        os.path.join(sfm_dir, 'sfm_data.bin'), "-o",
        os.path.join(mvs_dir, 'scene.mvs'), "-d",
        os.path.join(mvs_dir, 'images')
    ]

    try:
        p_step = subprocess.Popen(cmd0_list)
        p_step.wait()
        print(cmd0_list)
        p_step = subprocess.Popen(cmd1_list)
        p_step.wait()
        print(cmd1_list)
        p_step = subprocess.Popen(cmd2_list)
        p_step.wait()
        print(cmd2_list)
        p_step = subprocess.Popen(cmd4_list)
        p_step.wait()
        print(cmd4_list)
        p_step = subprocess.Popen(cmd9_list)
        p_step.wait()
        print(cmd9_list)
    except KeyboardInterrupt:
        sys.exit('\r\nProcess canceled by user, all files remains')


def dense_reconstruct(mvs_dir):
    print(mvs_dir)
    cmd10_list = [
        os.path.join(OPENMVS_BIN, "DensifyPointCloud"),
        os.path.join(mvs_dir, "scene.mvs"), "-o",
        os.path.join(mvs_dir, "scene_dense.mvs"),
        "--resolution-level", "2", "-w", mvs_dir
    ]

    cmd11_list = [
        os.path.join(OPENMVS_BIN, "ReconstructMesh"),
        os.path.join(mvs_dir, "scene_dense.mvs"), "-w", mvs_dir
    ]

    try:
        p_step = subprocess.Popen(cmd10_list)
        p_step.wait()
        print(cmd10_list)
        p_step = subprocess.Popen(cmd11_list)
        p_step.wait()
        print(cmd11_list)
    except KeyboardInterrupt:
        sys.exit('\r\nProcess canceled by user, all files remains')


def mesh_reconstruct(self, output_dir):
    print(output_dir)
    ply_path = os.path.join(output_dir, "scene_dense.ply")
    cmd11_list = [
        os.path.join(self.OPENMVS_BIN, "ReconstructMesh"),
        os.path.join(self.mvs_dir, "scene_dense.mvs"), "-w", output_dir
    ]
    try:
        pStep = subprocess.Popen(cmd11_list)
        pStep.wait()
        print(cmd11_list)
    except KeyboardInterrupt:
        sys.exit('\r\nProcess canceled by user, all files remains')
    cmd10_list = [
        os.path.join(self.OPENMVS_BIN, "DensifyPointCloud"),
        os.path.join(self.mvs_dir, "scene.mvs"), "-o",
        os.path.join(self.mvs_dir, "scene_dense.mvs"),
        "--resolution-level", "2", "-w", output_dir
    ]

    try:
        p_step = subprocess.Popen(cmd10_list)
        p_step.wait()
        print(cmd10_list)
    except KeyboardInterrupt:
        sys.exit('\r\nProcess canceled by user, all files remains')


def generate_dem(output_dir):
    pass


def detect_planes(mvs_dir):
    ply_path = os.path.join(mvs_dir, "scene_dense.ply")
    print(ply_path)
    pcd = o3d.io.read_point_cloud(ply_path)
    print(np.shape(pcd.points))

    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(
            pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))

    # max_label = labels.max()
    # print(f"point cloud has {max_label + 1} clusters")
    # colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    # colors[labels < 0] = 0
    # pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    # o3d.visualization.draw_geometries([pcd],
    #                                   zoom=0.455,
    #                                   front=[-0.4999, -0.1659, -0.8499],
    #                                   lookat=[2.1813, 2.0619, 2.0999],
    #                                   up=[0.1204, -0.9852, 0.1215])


def mkdir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
