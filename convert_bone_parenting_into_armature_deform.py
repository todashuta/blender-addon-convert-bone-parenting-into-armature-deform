# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Convert Bone Parenting into Armature Deform",
    "author": "todashuta",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "Menu bar > Object > Parent > Convert Bone Parenting into Armature Deform",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Armature"
}


import bpy


def main(context):
    selected_objects = context.selected_objects[:]
    objects = [ob for ob in selected_objects if
            ob.parent is not None and
            ob.parent_bone != "" and
            ob.parent_type == "BONE" and
            ob.type == "MESH"]

    bpy.ops.object.select_all(action="DESELECT")

    for ob in objects:
        armature, bone = ob.parent, ob.parent_bone
        #print(armature, bone)

        ob.select_set(True)
        context.view_layer.objects.active = ob # May not be needed?
        bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")

        armature.select_set(True)
        context.view_layer.objects.active = armature
        bpy.ops.object.parent_set(type="ARMATURE")

        vg = ob.vertex_groups.get(bone)
        if vg is None:
            vg = ob.vertex_groups.new(name=bone)
        for v in ob.data.vertices:
            vg.add([v.index], 1.0, "REPLACE")

        bpy.ops.object.select_all(action="DESELECT")


class ConvertBoneParentingIntoArmatureDeform(bpy.types.Operator):
    """Convert Bone Parenting into Armature Deform"""
    bl_idname = "object.convert_bone_parenting_into_armature_deform"
    bl_label = "Convert Bone Parenting into Armature Deform"

    @classmethod
    def poll(cls, context):
        selected_objects = context.selected_objects
        active_object = context.active_object
        return len(selected_objects) > 0 and active_object and active_object.mode == "OBJECT"

    def execute(self, context):
        main(context)
        return {"FINISHED"}


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(ConvertBoneParentingIntoArmatureDeform.bl_idname)


def register():
    bpy.utils.register_class(ConvertBoneParentingIntoArmatureDeform)
    bpy.types.VIEW3D_MT_object_parent.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ConvertBoneParentingIntoArmatureDeform)
    bpy.types.VIEW3D_MT_object_parent.remove(menu_func)


if __name__ == "__main__":
    register()
