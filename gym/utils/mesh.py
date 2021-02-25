import mathutils


def get_dimensions(obj):
    mesh = obj.meshes[0]
    collection = [[], [], []]
    for mat_index in range(mesh.numMaterials):
        for vert_index in range(mesh.getVertexArrayLength(mat_index)):
            vert_XYZ = mesh.getVertex(mat_index, vert_index).XYZ
            [collection[i].append(vert_XYZ[i]) for i in range(3)]
    return mathutils.Vector([abs(max(axis)) + abs(min(axis)) for axis in collection])
