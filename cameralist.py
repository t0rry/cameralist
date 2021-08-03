import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel
bl_info = {
    "name": "CameraList",
    "author": "t0rry_",
    "version": (0, 9 , 0),
    "blender": (2, 80, 0),
    "location": "3DViewPort > Sidebar > CameraList",
    "description": "Camera List And Rendering Support(rendering support is 'DEVELOPING')",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "CAMERA"
}

class CamProperty(bpy.types.PropertyGroup):
    """Group of properties representing an item in the list."""

    name:PointerProperty(
        name="camera_name(cam)",
        type = bpy.types.Camera,
        description="this property's camera data")
        
    frame_start:IntProperty(
         name = "Start Frame" ,default = 0)

    frame_end:IntProperty(
        name = "End Frame" , default = 100)

    render_name:StringProperty(
        name ="rendering image name"
    )

    cam_name:StringProperty(
        name="camera_name(name)"
    )

    exchange_data:PointerProperty(
        name="camera_name(cam)_exchange",
        type = bpy.types.Camera,
        description="this property's exchange camera data")

    object_data:PointerProperty(
        name="camera_data(obj)",
        type = bpy.types.Object,
        description = "this property's camera_data(obj)"
    )

#i'll implement it someday.......... :) exchange cam data
'''class CML_OT_ChangeItem(bpy.types.Operator):
    """Exchange to CameraData."""

    bl_idname = "camera_list.change_item"
    bl_label = "Change Camera Object"

    @classmethod
    def poll(cls, context):
        return context.scene.camera_list[context.scene.list_index].exchange_data


    def execute(self, context):
        camera_list = context.scene.camera_list
        index = context.scene.list_index
        exchange_data = context.scene.camera_list[index].exchange_data.id_data
        exchange_name = context.scene.camera_list[index].exchange_data.name

        camera_list[index].name = None
        camera_list[index].name = exchange_data

        camera_list[index].cam_name = "cam_name(error)"
        camera_list[index].cam_name = exchange_name

        #camera_list[index].cam_name = camera_list[index].exchange_data.id_data
'''     
class CML_OT_ViewCamera(bpy.types.Operator):
    """"Change to register Camera and View to Camera_List CameraView"""

    bl_idname = "camera_list.view_camera"
    bl_label = "View Camera Object"

    def execute(self, context):
        #01. Reset to Scene Camera
        context.scene.camera = None

        #02. camera_list , index 
        camera_list = context.scene.camera_list
        index = context.scene.list_index

        #03. processing "change scene camera" and "view to scene camera"
        bpy.context.view_layer.objects.active = camera_list[index].object_data
        context.scene.camera = camera_list[index].object_data
        bpy.ops.view3d.object_as_camera()
        bpy.context.view_layer.objects.active = None

        return{'FINISHED'}

class LIST_OT_NewItem(bpy.types.Operator):
    """Add a new item to the list."""

    bl_idname = "camera_list.new_item"
    bl_label = "Add a new item"


    def execute(self, context):
        
        if context.active_object.type == "CAMERA":
            
            #add item of camera_list 
            context.scene.camera_list.add()

            #definition cam_list and index 
            index = context.scene.list_index
            camera_list = context.scene.camera_list
            active_ob =context.active_object

            #Add Property of name status:
            camera_list[index].name =  active_ob.data
            
            #Add Property of cam_name status:
            camera_list[index].cam_name = active_ob.name

            #Add Property of object_data status:
            camera_list[index].object_data = active_ob

            #Add Property of render_name status:
            camera_list[index].render_name = active_ob.name

        else:
            self.report({'ERROR'},"{ERROR!}select camera obj")
        

        
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

class CML_OT_AddCamera(bpy.types.Operator):
    """Add Camera Object"""
    bl_idname = "camera_list.add_camera"
    bl_label = "Add new camera object"

    def execute(self, context):
        bpy.ops.object.camera_add(rotation = (1.5708 , 0 , 0))
        #x rotation = 90  = 1.5708 ???? wakaran 
        print("add camera")
        
        return{'FINISHED'}

class CML_OT_RenderingRequest(bpy.types.Operator):
    """Rendering in order of Camera_list"""
    bl_idname = "camera_list.rendering_request"
    bl_label = "Rendering in order of Camera_list"

    def execute(self, context):
        #01. camera_list , index , number of list
        camera_list = context.scene.camera_list
        count = len(camera_list)

        #02. repetition to rendering

        for num in range(count):
            #1. scene camera = none
            context.scene.camera = None

            #2. cam_list to scene camera
            bpy.context.view_layer.objects.active = camera_list[num].object_data
            context.scene.camera = camera_list[num].object_data

            #3. scene frame 
            cml_f_start = camera_list[num].frame_start
            cml_f_end = camera_list[num].frame_end

            bpy.context.scene.frame_start = cml_f_start
            bpy.context.scene.frame_end = cml_f_end

            #4. rendering

            bpy.ops.render.render(animation = True)
            bpy.data.images['Render Result'].save_render(filepath = os.environ['HOMEPATH'] + '/' + camera_list[num].cam_name + 'png')
        return{'FINISHED'}

class PT_CML_Panel(bpy.types.Panel):
    """Demo panel for UI list Tutorial."""

    bl_label = "Camera List"
    bl_idname = "CML_PT_LIST"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CameraList"
    bl_context = "objectmode"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='VIEW_CAMERA')   

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list("MY_UL_List", "camera_list_id", scene,
                          "camera_list", scene, "list_index")

        row = layout.row()

        row.operator('camera_list.new_item', text='ADD')
        row.operator('camera_list.delete_item', text='DALETE')
        row.operator('camera_list.move_item', text='UP').direction = 'UP'
        row.operator('camera_list.move_item', text='DOWN').direction = 'DOWN'

        row = layout.row()
        row.operator('camera_list.add_camera', text='ADD CAMERA' ,icon='VIEW_CAMERA')
        row.scale_y = 3

        row= layout.row()
        row.scale_y = 5

        layout.separator()
 
        if scene.list_index >= 0 and scene.camera_list:
            item = scene.camera_list[scene.list_index]

            row = layout.row()

            #change item panel
            '''
            row.prop(item,"exchange_data",text = "ExchangeData") 
            row.operator('camera_list.change_item', text='exchange data')
            '''
            row = layout.row()
            row.label(text= "NOTE change to scene camera")
            
            row = layout.row()
            row.operator('camera_list.view_camera', text='View_Camera' ,icon='VIEW_CAMERA')

            layout.separator()
            box = layout.box()

            #file manager + render req
            rd = context.scene.render
            box.label(text = "This ops is development ")
            box.prop(rd, "filepath", text="")
            box.prop(item, "cam_name")
            box.operator("camera_list.rendering_request", text = "renderinig req",icon ="RESTRICT_VIEW_OFF")

class MY_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'RENDER_STILL'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            item = context.scene.camera_list[index]

            row.scale_x = 3
            layout.enabled= False
            row.prop(item, "cam_name")
            #row.label(text = item.cam_name)
            row.scale_x = 1
            layout.enabled= True
            row.prop(item, "frame_start")
            row.prop(item, "frame_end")

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

classes = [
    #CML_OT_ChangeItem,
    CML_OT_RenderingRequest,
    CML_OT_ViewCamera,
    CamProperty,
    MY_UL_List,
    LIST_OT_NewItem,
    LIST_OT_DeleteItem,
    LIST_OT_MoveItem,
    PT_CML_Panel,
    CML_OT_AddCamera,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    
    bpy.types.Scene.camera_list = CollectionProperty(type = CamProperty)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list",
                                             default = 0)

def unregister():

    del bpy.types.Scene.camera_list
    del bpy.types.Scene.list_index

    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()