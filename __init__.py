# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Bone Animation Copy Tool",
    "author" : "Kumopult <kumopult@qq.com>",
    "description" : "Copy animation between different armature by bone constrain",
    "blender" : (2, 80, 3),
    "version" : (0, 0, 1),
    "location" : "View 3D > Toolshelf",
    "warning" : "",
    "category" : "Armature",
    "doc_url": "https://github.com/kumopult/blender_BoneAnimCopy",
    "tracker_url": "https://github.com/kumopult/blender_BoneAnimCopy/issues",
}

import bpy
from . import data
from . import mapping
from .utilfuncs import *

class BAC_PT_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BoneAnimCopy"
    bl_label = "Bone Animation Copy Tool"
    
    def draw(self, context):
        layout = self.layout
        
        if context.object != None and context.object.type == 'ARMATURE':
            s = get_state()
            
            split = layout.row().split(factor=0.244)
            split.column().label(text='Target:')
            split.column().label(text=context.object.name, icon='ARMATURE_DATA')
            layout.prop(s, 'selected_source', text='Source', icon='ARMATURE_DATA')
            layout.separator()
            
            if s.source == None:
                layout.label(text='Choose a source armature to continue', icon='INFO')
            else:
                layout.label(text='Bone Mappings')
                mapping.draw_panel(layout.box())
        else:
            layout.label(text='No armature selected', icon='ERROR')

class BAC_State(bpy.types.PropertyGroup):
    selected_source: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE' and obj != bpy.context.object,
        update=lambda self, ctx: get_state().update_source()
    )
    source: bpy.props.PointerProperty(type=bpy.types.Object)
    target: bpy.props.PointerProperty(type=bpy.types.Object)
    
    mappings: bpy.props.CollectionProperty(type=data.BAC_BoneMapping)
    active_mapping: bpy.props.IntProperty()
    
    editing_mappings: bpy.props.BoolProperty(default=False)
    
    def update_source(self):
        self.target = bpy.context.object

        if self.selected_source == None:
            return
        
        self.source = self.selected_source
    
    def get_source_armature(self):
        return self.source.data

    def get_target_armature(self):
        return self.target.data
    
    def add_mapping(self, target, source):
        m = self.mappings.add()
        m.target = target
        m.source = source
        # self.active_mapping = len(self.mappings) - 1
        return m
    
    def remove_mapping(self, index):
        self.mappings[index].clear()
        self.mappings.remove(index)

classes = (
	BAC_PT_Panel, 
	*data.classes,
	*mapping.classes,
	BAC_State,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.kumopult_bac = bpy.props.PointerProperty(type=BAC_State)
    print("hello kumopult!")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.kumopult_bac
    print("goodbye kumopult!")