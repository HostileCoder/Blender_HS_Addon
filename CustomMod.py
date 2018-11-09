bl_info = {
    'name':'HS_Addon',
    'category':'3D View',
    'author' : 'Tsai',
    'version': (1.0)
}



import bpy
from bpy.props import *
from bpy.types import Panel, Operator, Menu
import random
import bmesh
import math


# assign radnom color id
class RndColorID ( Operator ) :
    bl_idname = 'my.rndcolor'
    bl_label = 'Assign Color ID'


    @staticmethod
    def AssignColor():  
        selected = bpy.context.selected_objects
        
        i=0
        for obj in selected:
            
            mesh = obj.data
        
            if mesh.vertex_colors.active is None:
                mesh.vertex_colors.new()
                            
            rgb = [random.random() for i in range(3)]  
            rgb.append(1)            
                 
            i+=1           
            for poly in mesh.polygons :
                for poly in poly.loop_indices:
                    mesh.vertex_colors.active.data[poly].color = rgb
                    
            mesh.update()

    def execute ( self, context) :
        RndColorID.AssignColor()
        return {'FINISHED'}


#operator for auto apply smooth/sharp
class AutoSmoothGroup ( Operator ) :
    bl_idname = 'my.autoss'
    bl_label = 'ASG'

    @staticmethod
    def ASG():
            
        selected = bpy.context.selected_objects    
        scene = bpy.context.scene

        for obj in selected:
            scene.objects.active = obj            
            bpy.ops.object.mode_set(mode='EDIT')        
            bpy.ops.mesh.select_mode(type='EDGE')
            
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            
            bpy.ops.mesh.select_all(action='DESELECT')
                          
            bpy.ops.mesh.edges_select_sharp(sharpness = AutoSmoothGroup.degreeToRad(obj.my_prop_grp))
            bpy.ops.mesh.mark_sharp()                            
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = 3.14159
            bpy.ops.object.shade_smooth()
    
    def execute (self, context) :        
        AutoSmoothGroup.ASG()
        return {'FINISHED'}

    def degreeToRad(degree):
        rad = degree * math.pi / 180 
        return rad

#panel for the two operators
class View3dPanel(Panel):
     
    bl_idname = 'myPanel'
    bl_space_type = 'VIEW_3D'    
    bl_region_type = 'TOOLS'
    bl_label = 'Assign Color ID'
    bl_category = 'RndColor'
    
    

    def draw (self ,context):
        layout = self.layout
        obj = bpy.context.object
    
        row = layout.row()
        row.operator('my.rndcolor', text='Assign random color',icon='MOD_MESHDEFORM')

        row = layout.row()
        row.operator('my.autoss', text='Auto Smooth',icon='MOD_MESHDEFORM')
        
        if obj is not None:
            row = layout.row()
            row.prop(obj, 'my_prop_grp', text = 'Smooth Angle')
            
#pie menu for the two operators  
class MyPie(Menu):
    
    bl_idname = 'my.PieAutoss'
    bl_label = 'PASG'
    
    def draw (self ,context):   
        layout = self.layout  
        obj = bpy.context.object
                    
        pie = layout.menu_pie()  
        pie.operator('my.rndcolor', text='Assign random color',icon='MOD_MESHDEFORM')
        
    
        pie = layout.menu_pie()  
        pie.operator('my.autoss', text='Auto Smooth',icon='MOD_MESHDEFORM')


# custom property for the smooth operator
class MyPropertyGroup(bpy.types.PropertyGroup):
    
    bpy.types.Object.my_prop_grp = bpy.props.FloatProperty(name = "",
        description = "",
        default = 45,
        min = 0,
        max = 180)


def register():
    bpy.utils.register_class(RndColorID)
    bpy.utils.register_class(View3dPanel)
    bpy.utils.register_class(MyPie)
    bpy.utils.register_class(AutoSmoothGroup )
    
    bpy.utils.register_class(MyPropertyGroup)
    
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name = "Object Mode")
    kmi = km.keymap_items.new("wm.call_menu_pie", "Q", "PRESS", alt = True).properties.name = "my.PieAutoss"

    
def unregister():
    bpy.utils.register_class(RndColorID)
    bpy.utils.register_class(View3dPanel)
    bpy.utils.register_class(MyPie)
    bpy.utils.register_class(AutoSmoothGroup )
    bpy.utils.register_class(MyPropertyGroup)
    
if __name__== "__main__":
    register()