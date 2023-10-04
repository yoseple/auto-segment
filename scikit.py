
#Testing Code with just Raw FILE No segmentation.

import nibabel as nib
import nrrd
import numpy as np
from skimage.filters import threshold_otsu
from skimage import measure

def segment_lumbar_spine(file_path, file_type='nii.gz'):
    # Load the image data
    if file_type == 'nii.gz':
        img = nib.load(file_path)
        data = img.get_fdata()
    else:
        raise ValueError("Unsupported file type")

    # Apply thresholding to segment the lumbar spine
    thresh = threshold_otsu(data)
    segmented_data = (data > thresh).astype(int)

    return segmented_data

def volume_to_mesh(data, level=0.5):
    # Use marching cubes to extract surface mesh
    verts, faces, normals, values = measure.marching_cubes(data, level)
    return verts, faces

def save_to_obj(verts, faces, filename):
    with open(filename, 'w') as f:
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

# Usage:
data = segment_lumbar_spine('sub-gl017_raw/sub-gl017_ct.nii.gz')
verts, faces = volume_to_mesh(data)
save_to_obj(verts, faces, 'output_mesh.obj')

