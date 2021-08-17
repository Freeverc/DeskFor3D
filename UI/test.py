import open3d as o3d
import os
import numpy as np

file_name = os.path.join("C://Users//Freeverc//Projects//Fun//Reconstruction//ReconstructionTool//data//out1//mvs",
                         "scene_dense.ply")
point_cloud = o3d.io.read_point_cloud(file_name)

# np_points = o3d.np.asarray(point_cloud.points)
print(np.shape(point_cloud.points))
