from typing import DefaultDict
from original import init_props
import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel


bl_info = {
    "name": "CameraList",
    "author": "t0rry_",
    "version": (0, 0 , 3),
    "blender": (2, 80, 0),
    "location": "3Dビューポート > Sidebar",
    "description": "BlenderのUIを制御するアドオン",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Tutorial"
}

class ListItem(bpy.types.PropertyGroup):
    """Group of properties representing an item in the list."""

    

    name:PointerProperty(
        name="camera_name(obj)",
        type = bpy.types.Object,
        description="this property's object data")




class LIST_OT_NewItem(bpy.types.Operator):
    """Add a new item to the list."""

    bl_idname = "camera_list.new_item"
    bl_label = "Add a new item"

    def execute(self, context):
        
        camera_list = context.scene.camera_list.add()
        active_obj = context.active_object
        camera_list.name = active_obj
            


        

        return{'FINISHED'}


class LIST_OT_DeleteItem(bpy.types.Operator):
    """Delete the selected item from the list."""

    bl_idname = "camera_list.delete_item"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.camera_list

    def execute(self, context):
        camera_list = context.scene.camera_list
        index = context.scene.list_index

        camera_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(camera_list) - 1)

        return{'FINISHED'}


class LIST_OT_MoveItem(bpy.types.Operator):
    """Move an item in the list."""

    bl_idname = "camera_list.move_item"
    bl_label = "Move an item in the list"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        return context.scene.camera_list

    def move_index(self):
        """ Move index of an item render queue while clamping it. """

        index = bpy.context.scene.list_index
        list_length = len(bpy.context.scene.camera_list) - 1  # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)

        bpy.context.scene.list_index = max(0, min(new_index, list_length))

    def execute(self, context):
        camera_list = context.scene.camera_list
        index = context.scene.list_index

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        camera_list.move(neighbor, index)
        self.move_index()

        return{'FINISHED'}

class LIST_OT_AddCamera(bpy.types.Operator):
    """Add Camera Object"""
    bl_idname = "camera_list.add_camera"
    bl_label = "Add new camera object"

    def execute(self, context):
        bpy.ops.object.camera_add(rotation = (1.5708 , 0 , 0))
        #x rotation = 90  = 1.5708 ???? wakaran 
        print("add camera")
        
        return{'FINISHED'}


class PT_ListExample(bpy.types.Panel):
    """Demo panel for UI list Tutorial."""

    bl_label = "Camera List"
    bl_idname = "SCENE_PT_LIST_DEMO"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='VIEW_CAMERA')   

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list("MY_UL_List", "The_List", scene,
                          "camera_list", scene, "list_index")

        row = layout.row()
        row.operator('camera_list.new_item', text='NEW')
        row.operator('camera_list.delete_item', text='REMOVE')
        row.operator('camera_list.move_item', text='UP').direction = 'UP'
        row.operator('camera_list.move_item', text='DOWN').direction = 'DOWN'
        row.operator('camera_list.add_camera', text='ADD CAMERA')

        layout.separator()

        layout.label(text="WARNIG :elected camera object, show NEW button")
        #add any Panel t0rry_

        if scene.list_index >= 0 and scene.camera_list:
            item = scene.camera_list[scene.list_index]

            row = layout.row()
            row.prop(item, "name")
            row.prop(item, "random_prop")

class MY_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                active_propname, index):
        ob = data
        psys = item
        # We could write some code to decide which icon to use here...
        custom_icon = 'RENDER_STILL'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)

            row.prop(psys, "name", text="", emboss=True, icon_value=icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

classes = [
    ListItem,
    MY_UL_List,
    LIST_OT_NewItem,
    LIST_OT_DeleteItem,
    LIST_OT_MoveItem,
    PT_ListExample,
    LIST_OT_AddCamera,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    
    init_props()
    print("Register of CameraList Addon")

    bpy.types.Scene.camera_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list",
                                             default = 0)


def unregister():

    del bpy.types.Scene.camera_list
    del bpy.types.Scene.list_index

    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()