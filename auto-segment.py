import slicer
#https://slicer.readthedocs.io/en/5.2/developer_guide/script_repository/segmentations.html#use-segmentation-files-in-python-outside-slicer

def automate_model_creation(ct_scan_path, segmentation_path):
    # 1. Load the CT scan (raw data) into Slicer.
    ct_scan_node = slicer.util.loadVolume(ct_scan_path)
    if not ct_scan_node:  # If the CT scan did not load successfully, print an error.
        print(f"Error loading CT scan from {ct_scan_path}")
        return

    # 2. Load the segmentation (from the .gz file) into Slicer.
    segmentation_node = slicer.util.loadSegmentation(segmentation_path)  # Use loadSegmentation here
    if not segmentation_node:  # If the segmentation did not load successfully, print an error.
        print(f"Error loading segmentation from {segmentation_path}")
        return

    # 3. Select the Model Maker module in Slicer.
    slicer.util.selectModule('ModelMaker')
    
    #Issue with the Name./
    # 4. Set the parameters for the Model Maker module.
    parameters = {}
    parameters['Name'] = 'SegmentationModel'
    parameters['InputVolume'] = segmentation_node.Name()  # This ensures the input is the segmentation
    parameters['FilterType'] = 'Sinc'
    parameters['GenerateAll'] = True
    parameters['StartLabel'] = -1
    parameters['EndLabel'] = -1

    # 5. Create a new model hierarchy in Slicer to store the generated models.
    model_hierarchy_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLModelHierarchyNode')
    parameters['ModelSceneFile'] = model_hierarchy_node.GetID()

    # 6. Execute the Model Maker module with the set parameters to generate the 3D model.
    slicer.cli.runSync(slicer.modules.modelmaker, None, parameters)

# testing
segmentation_path = '/Users/yoseple/Documents/BWH1/auto-segment/sub-gl017/sub-gl017_seg-vert_msk.nii.gz'
ct_scan_path = '/Users/yoseple/Documents/BWH1/auto-segment/sub-gl017_raw/sub-gl017_ct.nii.gz'
automate_model_creation(ct_scan_path, segmentation_path)
