import numpy as np
import nibabel as nib
from skimage import measure
import vtk
from vtk.util import numpy_support

# Define a function to convert a volumetric representation to a 3D mesh.
def create_mesh_from_volume(volume, step_size=1):
    # Extract surface mesh from a 3D volume using the marching cubes algorithm.
    verts, faces, _, _ = measure.marching_cubes(volume, step_size=step_size)

    # Create VTK points from the vertices.
    points = vtk.vtkPoints()
    for v in verts:
        points.InsertNextPoint(v)

    # Create VTK polygons from the faces.
    polygons = vtk.vtkCellArray()
    for f in faces:
        polygons.InsertNextCell(len(f))
        for i in f:
            polygons.InsertCellPoint(i)

    # Generate a VTK mesh from the points and polygons.
    mesh = vtk.vtkPolyData()
    mesh.SetPoints(points)
    mesh.SetPolys(polygons)
    
    return mesh

# 1. LOAD THE DATA
# Load the CT scan and the segmentation data using nibabel.
ct_scan = nib.load('sub-gl017_raw/sub-gl017_ct.nii.gz').get_fdata()
segmentation = nib.load('sub-gl017/sub-gl017_seg-vert_msk.nii.gz').get_fdata()

# 2. EXTRACT THE MESH FROM THE SEGMENTATION
# Convert the entire segmentation (all non-zero values) to a 3D mesh.
spine_mesh = create_mesh_from_volume(segmentation > 0)

# 3. SMOOTH THE MESH
# Used vtkSmoothPolyDataFilter to smooth the mesh. This helps in reducing the roughness and artifacts.
smoother = vtk.vtkSmoothPolyDataFilter()
smoother.SetInputData(spine_mesh)
smoother.SetNumberOfIterations(30)  # Number of smoothing iterations; adjust based on desired smoothness.
smoother.Update()
smoothed_mesh = smoother.GetOutput()

# 4. DECIMATE (REDUCE) THE MESH
# Use vtkDecimatePro to reduce the number of polygons in the mesh without significantly altering its appearance.
decimator = vtk.vtkDecimatePro()
decimator.SetInputData(smoothed_mesh)
decimator.SetTargetReduction(0.2)  # Aim to reduce the mesh size to 80% of the original.
decimator.PreserveTopologyOn()  # Ensure the decimation does not introduce holes in the mesh.
decimator.Update()
decimated_mesh = decimator.GetOutput()

# 5. EXPORT THE OPTIMIZED MESH
# Export the final optimized (smoothed and decimated) mesh to an .obj file for further use.
writer = vtk.vtkOBJWriter()
writer.SetFileName('optimized_spine.obj')
writer.SetInputData(decimated_mesh)
writer.Write()
