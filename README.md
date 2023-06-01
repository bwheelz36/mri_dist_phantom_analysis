# mri_dist_phantom_analysis

This repository demonstrates the anaysis of a distortion phantom using the [mri_distortion_toolkit](https://github.com/ACRF-Image-X-Institute/mri_distortion_toolkit).

The analysed data was acquired on the australian MRI-Linac system, and can be downloaded [here](https://ses.library.usyd.edu.au/handle/2123/31139).


If you execute the scripts in order (_0_, _1_, _2_, etc.), the data will be downloaded for you and the rest of the pipeline will be in correct order. For explanation of what exactly is happening at each step, you can read our [documentation](https://acrf-image-x-institute.github.io/mri_distortion_toolkit/examples.html).

The only dependency you should need is `mri_distortion_toolkit` and `requests`:

```commandline
pip install mri_distortion_toolkit
pip install requests
```


## Code to add DSV in slicer

(I'm putting this here because I don't know where else to put it)
If you want to add a DSV model in slice, use the below code:

```python
# Create some model that will be added to a segmentation node
# credit: https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#create-segmentation-from-a-model-node
sphere = vtk.vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(150)
sphere.SetThetaResolution(50)
sphere.SetPhiResolution(50)
modelNode = slicer.modules.models.logic().AddModel(sphere.GetOutputPort())

# Create segmentation
segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
segmentationNode.CreateDefaultDisplayNodes() # only needed for display

# Import the model into the segmentation node
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelNode, segmentationNode)
```