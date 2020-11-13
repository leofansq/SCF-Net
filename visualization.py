# open3d == 0.10.0.1
import open3d
import argparse
import numpy as np
from helper_ply import read_ply

s3dis_color = [[255,248,220], [220,220,220], [139,71,38], [238,197,145], [70,130,180], [179,238,58], [110,139,61], [105,105,105], [0,0,128], [205,92,92], [244,164,96], [147,112,219], [255,228,225]]
semantic3d_color = [[220,220,220], [154,205,50], [0,100,0], [238,220,130], [139,115,85], [70,130,180], [255,231,186], [255,99,71]]

def draw_pc(pc_xyzrgb):
    """
    Draw Point Cloud
    """
    pc = open3d.geometry.PointCloud()
    pc.points = open3d.utility.Vector3dVector(pc_xyzrgb[:, 0:3])
    if pc_xyzrgb.shape[1] == 3:
        open3d.draw_geometries([pc])
        return 0
    if np.max(pc_xyzrgb[:, 3:6]) > 20:  ## 0-255
        pc.colors = open3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6] / 255.)
    else:
        pc.colors = open3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6])
    open3d.visualization.draw_geometries([pc])
    return 0

def s3dis(origin_file_name, label_file_name):
    """
    Visualization for S3DIS
    """
    origin_data = read_ply(origin_file_name)
    label_data = read_ply(label_file_name)
    
    pred = label_data["pred"]
    label = label_data["label"]

    x = origin_data["x"]
    y = origin_data["y"]
    z = origin_data["z"]

    r = origin_data["red"]
    g = origin_data["green"]
    b = origin_data["blue"]

    label_rgb = np.array([s3dis_color[i] for i in label])

    pred_rgb =  np.array([s3dis_color[i] for i in pred])

    xyzrgb = np.vstack((x,y,z,r,g,b)).T
    draw_pc(xyzrgb)

    pred_xyzrgb = np.vstack(([x,y,z],pred_rgb.T)).T
    draw_pc(pred_xyzrgb)

    label_xyzrgb = np.vstack(([x,y,z],label_rgb.T)).T
    draw_pc(label_xyzrgb)

def semantic3d(origin_file_name, label_file_name):
    """
    Visualization for Semantic3D
    """
    origin_data = read_ply(origin_file_name)

    with open(label_file_name, 'r') as f: pred = f.readlines()

    x = origin_data["x"]
    y = origin_data["y"]
    z = origin_data["z"]

    r = origin_data["red"]
    g = origin_data["green"]
    b = origin_data["blue"]

    pred_rgb =  np.array([semantic3d_color[int(i)-1] for i in pred])

    xyzrgb = np.vstack((x,y,z,r,g,b)).T
    draw_pc(xyzrgb)

    pred_xyzrgb = np.vstack(([x,y,z],pred_rgb.T)).T
    draw_pc(pred_xyzrgb)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='s3dis', help='s3dis or semantic3d [default: s3dis]')
    parser.add_argument('--ply_path', type=str, help='origin ply path')
    parser.add_argument('--label_path', type=str, help='label path')
    args = parser.parse_args()

    if args.dataset == 's3dis':
        s3dis(args.ply_path, args.label_path)
    elif args.dataset == 'semantic3d':
        semantic3d(args.ply_path, args.label_path)
    else:
        print("Wrong dataset. S3DIS or Semantic3D")