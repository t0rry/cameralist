import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty, PointerProperty , EnumProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel

import os 

#need for Calculation view origin point 
import numpy as np


bl_info = {
    "name": "CameraList",
    "author": "t0rry_",
    "version": (0, 9 , 2),
    "blender": (2, 80, 0),
    "location": "3DViewPort > Sidebar > CameraList",
    "description": "Camera List And Rendering Support(rendering support is 'DEVELOPING')",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "CAMERA"
}

def update_ob(self,context,):
    index = context.scene.list_index
    camera_list = context.scene.camera_list[index]

    #update name

    

    if camera_list.ob.type == "CAMERA":
        #update cam ob
        camera_list.name = camera_list.ob.name
        camera_list.cam = camera_list.ob.data

    # if selected other camera object
    else:
        camera_list.ob= None

    return None
    
class CamProperty(bpy.types.PropertyGroup):
    """Camera List Property Group"""

    name:StringProperty(
        name = "camera_name(name)"  )

    cam:PointerProperty(
        name="camera_data(cam)",
        type = bpy.types.Camera,
        description="camera data")

    ob:PointerProperty(
        name="camera_data(obj)",
        type = bpy.types.Object,
        description = "camera_data(obj)",
        update = update_ob
    )

    frame_start:IntProperty(
         name = "Start Frame" ,default = 0)

    frame_end:IntProperty(
        name = "End Frame" , default = 100)

    render_name:StringProperty(
        name ="rendering image name"
    )

class LIST_OT_NewItem(bpy.types.Operator):
    """Add a new item to the list."""

    bl_idname = "camera_list.new_item"
    bl_label = "Add a new item"


    def execute(self, context):
        
        if context.active_object.type == "CAMERA":
            
            #add item of camera_list 
            context.scene.list_index = -1

            context.scene.camera_list.add()

            #definition cam_list and index 
            index = context.scene.list_index
            camera_list = context.scene.camera_list
            active_ob =context.active_object

            #Add Property of object_data status:
            camera_list[index].ob = active_ob

            #other property is "update_ob"fx (1.update ob 2.update other property)

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
        
        return{'FINISHED'}

class CML_OT_ViewCamera(bpy.types.Operator):
    """"Change to register Camera and View to Camera_List CameraView"""

    bl_idname = "camera_list.view_camera"
    bl_label = "View Camera Object"

    def execute(self, context):

        #00. Mode,camera_list,index
        index = context.scene.list_index
        camera_list = context.scene.camera_list[index]

        #01. Reset to Scene Camera
        context.scene.camera = None

        
        #03. processing "change scene camera" and "view to scene camera"
        #bpy.context.view_layer.objects.active = camera_list[index].ob
        context.view_layer.objects.active = camera_list.ob
        context.scene.camera = camera_list.ob
        bpy.ops.view3d.object_as_camera()
        context.view_layer.objects.active = None
            

        return{'FINISHED'}

class CML_OT_SelectCamera(bpy.types.Operator):
    """"Selected CameraList Item Camera"""

    bl_idname = "camera_list.select_camera"
    bl_label = "Select Camera Object"

    def execute(self, context):

        ##01. camera_list , index 
        index = context.scene.list_index
        camera_list = context.scene.camera_list[index]

        ##02 select camera
        bpy.data.objects[camera_list.name].select_set(True)

        ##03 pop
        self.report({'INFO'},"{Success!!!}Selected List Item (Item Name =" + camera_list.name + ")")

        return{'FINISHED'}

class CML_OT_Debug_Button(bpy.types.Operator):
    """Debug Button Developing """
    bl_idname = "camera_list.debug"
    bl_label = "Debug"

    def execute(self , context):

        #debug to screen data    
        area = context.space_data.region_3d
        print("distance")
        print(area.view_distance)
        print("view_location")
        print(area.view_location)
        print("view_rotation")
        print(area.view_rotation)
        print("view_perspective")
        #area.view_location.x =5
        #area.view_location.y =-4
        #area.view_location.z =5
        print(area.view_perspective)

        #debug to camera_view
        index = context.scene.list_index
        camera_list =context.scene.camera_list[index]

        #call to debug end
        print("DEBUG END")

        return{'FINISHED'}

class CML_OT_ViewCoordinate(bpy.types.Operator):
    """Calculation to View Coordinate """
    bl_idname = "camera_list.view_coordinate"
    bl_label = "view coordinate"

    def execute(self,context):
        #00 camera_list,index
        index = context.scene.list_index
        camera_list =context.scene.camera_list[index]

        #01 get camera's locations(x,y,z)
        original_location = camera_list.ob.location 
        

        #02 get camera's rotations(euler)
        original_angle_x  = camera_list.ob.rotation_euler.x
        original_angle_z  = camera_list.ob.rotation_euler.z
        
        #03 calculate theta (180° = π = np.pi )
        #03 -1 when the angle is 360 over
        if original_angle_x > (2 * np.pi) :
            while original_angle_x > (2 * np.pi):
                original_angle_x = original_angle_x - (2 * np.pi)
            
            if original_angle_x < np.pi:
                theta = np.pi - original_angle_x
                print("A :x > 2pi , x < pi")

            else:
                
                theta = 3 * np.pi - original_angle_x
                print("B :x > 2pi , x > pi")

        #03 -2 when the angle is 360 under
        else:

            if original_angle_x < np.pi:
                theta = np.pi - original_angle_x
                print("C :x < 2pi , x < pi")

            else:
                theta =  3 * np.pi -original_angle_x
                print("D :x< 2pi , x > pi")
            

        print(np.rad2deg(theta))
 
        #04 calculate phi
        #04 - 1 when the angle is 270 over
        if original_angle_z > (3 * np.pi / 2) :
            while original_angle_z > (3 * np.pi / 2):
                original_angle_z = original_angle_z - (3 * np.pi / 2)
            
            if original_angle_z < np.pi:
                phi = original_angle_z + (np.pi / 2 )
                print("A :z > 2pi , z < pi")

            else:
                
                phi = original_angle_z + (np.pi / 2 )
                print("B :z > 2pi , z > pi")

        #03 -2 when the angle is 360 under
        else:

            if original_angle_z < np.pi:
                phi = original_angle_z + (np.pi / 2 )
                print("C :z < 2pi , z < pi")

            else:
                phi =  original_angle_z + (np.pi / 2 )
                print("D :z < 2pi , z > pi")
            
        print(np.rad2deg(phi))
        
        #05 get camera's focus distance
        original_view_distance = camera_list.ob.data.dof.focus_distance
        
        
        newPosition = np.empty([1,3], dtype=np.float64)
        newPosition[:,0] = original_view_distance * np.sin(theta) * np.cos(phi)
        newPosition[:,1] = original_view_distance * np.sin(theta) * np.sin(phi)
        newPosition[:,2] = original_view_distance * np.cos(theta)
        print("xyz は" + str(newPosition))
        
        x = newPosition[:,0]
        y = newPosition[:,1]
        z= newPosition[:,2]
              
        #calculate view location
        context.space_data.region_3d.view_location.x = x + original_location.x
        context.space_data.region_3d.view_location.y = y + original_location.y
        context.space_data.region_3d.view_location.z = z + original_location.z
        
        context.space_data.region_3d.view_distance = original_view_distance
        
        print(newPosition[:,0] + original_location.x)
        print(original_location.x)
        
        
        print("---------------DEBUG END---------------")
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
            bpy.context.view_layer.objects.active = camera_list[num].ob
            context.scene.camera = camera_list[num].ob

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
    #bl_context = "objectmode"

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

        row.operator('camera_list.debug', text='Debug' ,icon='VIEW_CAMERA')
        row= layout.row()
        row.scale_y = 5
        
        row.operator('camera_list.view_coordinate', text='Debug_2' ,icon='FUND')
        row= layout.row()

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

            row.operator('camera_list.select_camera', text='Selected Item' ,icon='RESTRICT_SELECT_OFF')
            

            layout.separator()
            box = layout.box()

            #file manager + render req
            rd = context.scene.render
            box.label(text = "This ops is development ")
            box.prop(rd, "filepath", text="")
            box.prop(item, "name")
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

            row.scale_x = 0.2
            row.label(text = str(index))

            row.scale_x = 3
            row.prop(item, "ob",icon_only = True)
            #row.label(text = item.cam_name)

            row.scale_x = 1
            layout.enabled= True
            row.prop(item, "frame_start")
            row.prop(item, "frame_end")

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

classes = [
    CML_OT_ViewCoordinate,
    CML_OT_RenderingRequest,
    CML_OT_ViewCamera,
    CML_OT_SelectCamera,
    CML_OT_Debug_Button,
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