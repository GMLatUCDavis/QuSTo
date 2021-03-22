
from QuSlicer import QuSlicer
import open3d as o3d
import matplotlib.pyplot as plt


# Sling tailed Agama skin
meshPath = "meshes/lizardSlingTail_067.obj"
mesh = o3d.io.read_triangle_mesh(meshPath)
print(mesh)
slicedVerts = QuSlicer.sliceVerts(mesh.vertices, 'x', .40, .50)
skimmedVerts = QuSlicer.skimSlice(slicedVerts, 'y', .10)
smoothedVerts = QuSlicer.smoothSlice(skimmedVerts, 2, 10)
QuSlicer.writeCSV(smoothedVerts,'documents', "SliceOutput_Lizard.csv")


'''
# Florida Mammoth molar
meshPath = "meshes/uf_uf_86975_M6213-5695.stl"
mesh = o3d.io.read_triangle_mesh(meshPath)
print(mesh)
slicedVerts = QuSlicer.sliceVerts(mesh.vertices, 'z', .40, .50)
skimmedVerts = QuSlicer.skimSlice(slicedVerts, 'y', .20)
skimmedVerts = QuSlicer.skimSlice(skimmedVerts, 'x', .95)
smoothedVerts = QuSlicer.smoothSlice(skimmedVerts, 3, 10)
QuSlicer.writeCSV(smoothedVerts,'documents', "SliceOutput_Mammoth.csv")
'''

'''
# Sea snail shell
meshPath = "meshes/AMNH_FI_101646_M21283-40436_2.stl"
mesh = o3d.io.read_triangle_mesh(meshPath)
print(mesh)
slicedVerts = QuSlicer.sliceVerts(mesh.vertices, 'z', .40, .50)
skimmedVerts = QuSlicer.skimSlice(slicedVerts, 'y', .25)
skimmedVerts = QuSlicer.skimSlice(skimmedVerts, 'x', .95)
smoothedVerts = QuSlicer.smoothSlice(skimmedVerts, 3, 20)
QuSlicer.writeCSV(smoothedVerts,'documents', "SliceOutput_Snail.csv")
'''



