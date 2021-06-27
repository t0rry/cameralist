import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    BoolProperty,
)

bl_info = {
    "name": "CameraList",
    "author": "t0rry_",
    "version": (0, 0 , 1),
    "blender": (2, 80, 0),
    "location": "3Dビューポート > Sidebar",
    "description": "BlenderのUIを制御するアドオン",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Tutorial"
}

class SAMPLE27_OT_Nop(bpy.types.Operator):

    bl_idname = "object.sample27_nop"
    bl_label = "NOP"
    bl_description = "何もしない"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "add camera in CAMERALIST")
        return {'FINISHED'}

    def init_props():
        scene = bpy.types.Scene
        scene.test_01 = IntProperty(
        name="Camera List",
        description="登録したカメラのリスト（重複）登録されます",
        items = []
        )
    # プロパティを削除
    def clear_props():
        scene = bpy.types.Scene
        del scene.test_01


class SAMPLE27_MT_NopMenu(bpy.types.Menu):

    bl_idname = "SAMPLE27_MT_NopMenu"
    bl_label = "NOP メニュー"
    bl_description = "何もしないオペレータを複数持つメニュー"

    def draw(self, context):
        layout = self.layout
        # メニュー項目の追加
        for i in range(3):
            layout.operator(SAMPLE27_OT_Nop.bl_idname, text=("項目 %d" % (i)))


# Sidebarのタブ [カスタムタブ] に、パネル [カスタムパネル] を追加
class SAMPLE27_PT_CustomPanel(bpy.types.Panel):

    bl_label = "CameraList"         # パネルのヘッダに表示される文字列
    bl_space_type = 'VIEW_3D'           # パネルを登録するスペース
    bl_region_type = 'UI'               # パネルを登録するリージョン
    bl_category = "CameraList"        # パネルを登録するタブ名
    bl_context = "objectmode"           # パネルを表示するコンテキスト

    # ヘッダーのカスタマイズ
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='VIEW_CAMERA')

    # メニューの描画処理
    def draw(self, context):
        layout = self.layout
        scene = context.scene


        #display active camera
        layout.label(text ="Active Camera")
        layout.prop(scene, "camera")

        #display camera list
        layout.prop(context.scene, "sample27_prop_enum")
        # 一行配置（アライメントあり）
        row = layout.row(align=True)
        # Cameradata_Inputボタンを追加
        layout.label(text="Oparation CameraList:")
        layout.operator(SAMPLE27_OT_Nop.bl_idname, text="LIST IN" , icon="PLAY")

        # Cameradata Daleteボタンを追加
        layout.operator(SAMPLE27_OT_Nop.bl_idname, text="LIST OUT" , icon="CANCEL")
        layout.separator()


        # ドロップダウンメニューを追加
        layout.label(text="Active Camera:")
        layout.menu(SAMPLE27_MT_NopMenu.bl_idname,
                    text= "あとでかく")

        layout.separator()

        

# プロパティの初期化
def init_props():
    scene = bpy.types.Scene
    scene.sample27_prop_int = EnumProperty(
        name="Camera List",
        description="登録したカメラのリスト（重複）登録されます",
        items = []
    )
    scene.sample27_prop_float = FloatProperty(
        name="プロパティ 2",
        description="プロパティ（float）",
        default=0.75,
        min=0.0,
        max=1.0
    )
    scene.sample27_prop_floatv = FloatVectorProperty(
        name="プロパティ 3",
        description="プロパティ（float vector）",
        subtype='COLOR_GAMMA',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0
    )
    scene.sample27_prop_enum = EnumProperty(
        name="プロパティ 4",
        description="プロパティ（enum）",
        items=[
            ('ITEM_1', "項目 1", "項目 1"),
            ('ITEM_2', "項目 2", "項目 2"),
            ('ITEM_3', "項目 3", "項目 3")
        ],
        default='ITEM_1'
    )
    scene.sample27_prop_bool = BoolProperty(
        name="プロパティ 5",
        description="プロパティ（bool）",
        default=False
    )


# プロパティを削除
def clear_props():
    scene = bpy.types.Scene
    del scene.sample27_prop_int
    del scene.sample27_prop_float
    del scene.sample27_prop_floatv
    del scene.sample27_prop_enum
    del scene.sample27_prop_bool


classes = [
    SAMPLE27_OT_Nop,
    SAMPLE27_MT_NopMenu,
    SAMPLE27_PT_CustomPanel,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    init_props()
    print("サンプル 2-7: アドオン『サンプル 2-7』が有効化されました。")




def unregister():
    clear_props()
    for c in classes:
        bpy.utils.unregister_class(c)
    print("サンプル 2-7: アドオン『サンプル 2-7』が無効化されました。")


if __name__ == "__main__":
    register()
