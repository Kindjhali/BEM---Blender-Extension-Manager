bl_info = {
    "name": "Extension Manager",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > Extensions Tab",
    "description": "Toggle, install and reinstall Blender extensions easily from a sidebar panel",
    "category": "Interface",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

# ##### BEGIN METADATA #####
"""
METADATA - MODIFY THIS SECTION WITH YOUR DETAILS

Author Information:
    Author: Kindjhali
    Contact: aphexice@gmail.com
    Website: https://www.youtube.com/@GiveItKibble

Project Information:
    Repository: https://github.com/Kindjhali/BEM---Blender-Extension-Manager
    License: MIT
    Version History:
        1.0.0 - Initial release
        
Credits:
    Contributors:
        - Contributor Name 1
        - Contributor Name 2
    Special Thanks:
        - Person or Organization 1
        - Person or Organization 2
    
Additional Notes:
    Any additional information you'd like to include about the addon.
"""
# ##### END METADATA #####

import bpy
import os
import addon_utils
from bpy.types import Panel, Operator
from bpy.props import BoolProperty, StringProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper

class EXTENSION_OT_toggle(Operator):
    """Toggle an extension on or off"""
    bl_idname = "extension.toggle"
    bl_label = "Toggle Extension"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    module_name: StringProperty()
    
    def execute(self, context):
        is_enabled = addon_utils.check(self.module_name)[0]
        
        if is_enabled:
            addon_utils.disable(self.module_name, default_set=True)
        else:
            try:
                addon_utils.enable(self.module_name, default_set=True)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to enable {self.module_name}: {str(e)}")
                return {'CANCELLED'}
        
        # Force a redraw of the UI
        for area in bpy.context.screen.areas:
            area.tag_redraw()
            
        return {'FINISHED'}

class EXTENSION_OT_install(Operator, ImportHelper):
    """Install an extension from file"""
    bl_idname = "extension.install"
    bl_label = "Install Extension"
    
    filter_glob: StringProperty(
        default="*.zip;*.py",
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        import zipfile
        import shutil
        
        # Get the addon installation path
        addon_path = bpy.utils.user_resource('SCRIPTS', path="addons")
        
        # Process the file based on its extension
        filepath = self.filepath
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext == '.zip':
                # Install from zip
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(addon_path)
                self.report({'INFO'}, f"Installed addon from {filename}")
            elif ext == '.py':
                # Install single file addon
                destination = os.path.join(addon_path, filename)
                shutil.copy2(filepath, destination)
                self.report({'INFO'}, f"Installed addon from {filename}")
            else:
                self.report({'ERROR'}, f"Unsupported file format: {ext}")
                return {'CANCELLED'}
                
            # Refresh the addon list
            bpy.ops.preferences.addon_refresh()
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to install addon: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}

class EXTENSION_OT_reinstall(Operator, ImportHelper):
    """Reinstall an extension from file"""
    bl_idname = "extension.reinstall"
    bl_label = "Reinstall Extension"
    
    filter_glob: StringProperty(
        default="*.zip;*.py",
        options={'HIDDEN'}
    )
    
    module_name: StringProperty()
    
    def execute(self, context):
        import zipfile
        import shutil
        
        # Get the addon installation path
        addon_path = bpy.utils.user_resource('SCRIPTS', path="addons")
        
        # First, try to remove the existing addon
        if self.module_name:
            try:
                # Disable the addon if it's enabled
                if addon_utils.check(self.module_name)[0]:
                    addon_utils.disable(self.module_name)
                    
                # Try to determine the addon's location
                module_path = None
                for mod in addon_utils.modules():
                    if mod.__name__ == self.module_name:
                        module_path = os.path.dirname(mod.__file__)
                        break
                        
                # Remove the existing addon files
                if module_path and os.path.exists(module_path):
                    if os.path.isdir(module_path):
                        shutil.rmtree(module_path)
                    else:
                        os.remove(module_path)
            except Exception as e:
                self.report({'WARNING'}, f"Could not completely remove existing addon: {str(e)}")
        
        # Now install the new version
        filepath = self.filepath
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext == '.zip':
                # Install from zip
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(addon_path)
                self.report({'INFO'}, f"Reinstalled addon from {filename}")
            elif ext == '.py':
                # Install single file addon
                destination = os.path.join(addon_path, filename)
                shutil.copy2(filepath, destination)
                self.report({'INFO'}, f"Reinstalled addon from {filename}")
            else:
                self.report({'ERROR'}, f"Unsupported file format: {ext}")
                return {'CANCELLED'}
                
            # Refresh the addon list
            bpy.ops.preferences.addon_refresh()
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to reinstall addon: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}
        
class EXTENSION_OT_uninstall(Operator):
    """Uninstall an extension"""
    bl_idname = "extension.uninstall"
    bl_label = "Uninstall Extension"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    module_name: StringProperty()
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):
        import shutil
        
        if not self.module_name:
            self.report({'ERROR'}, "No extension specified")
            return {'CANCELLED'}
        
        try:
            # Disable the addon if it's enabled
            if addon_utils.check(self.module_name)[0]:
                addon_utils.disable(self.module_name)
                
            # Try to determine the addon's location
            module_path = None
            mod_to_remove = None
            
            for mod in addon_utils.modules():
                if mod.__name__ == self.module_name:
                    module_path = mod.__file__
                    mod_to_remove = mod
                    break
                    
            if not module_path or not os.path.exists(module_path):
                self.report({'ERROR'}, f"Could not find {self.module_name} files")
                return {'CANCELLED'}
                
            # If it's a single file addon
            if module_path.endswith('.py'):
                os.remove(module_path)
                self.report({'INFO'}, f"Removed addon file: {os.path.basename(module_path)}")
            # If it's a directory addon
            else:
                addon_dir = os.path.dirname(module_path)
                if os.path.isdir(addon_dir):
                    addon_name = os.path.basename(addon_dir)
                    shutil.rmtree(addon_dir)
                    self.report({'INFO'}, f"Removed addon directory: {addon_name}")
            
            # Refresh the addon list
            bpy.ops.preferences.addon_refresh()
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to uninstall {self.module_name}: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}

class EXTENSION_PT_manager_panel(Panel):
    """Extension Manager Panel"""
    bl_label = "Extension Manager"
    bl_idname = "EXTENSION_PT_manager_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Extensions'  # This creates a new tab in the sidebar
    
    def draw(self, context):
        layout = self.layout
        
        # Installation buttons
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Extension Installation:")
        row = col.row(align=True)
        row.operator("extension.install", text="Install New Extension", icon='IMPORT')
        
        # Add search bar
        layout.separator()
        layout.prop(context.window_manager, "extension_search", text="", icon='VIEWZOOM')
        search_term = context.window_manager.extension_search.lower()
        
        # Get all addons
        addons = [(mod, *addon_utils.check(mod.__name__)) for mod in addon_utils.modules()]
        
        # Sort addons by name
        addons.sort(key=lambda x: x[0].bl_info.get('name', x[0].__name__))
        
        # Filter addons based on search term
        filtered_addons = []
        for mod, is_enabled, is_loaded in addons:
            # Skip internal addons
            if mod.__name__.startswith('_'):
                continue
                
            # Get addon name and apply search filter
            mod_name = mod.bl_info.get('name', mod.__name__)
            if search_term and search_term not in mod_name.lower() and search_term not in mod.__name__.lower():
                continue
                
            filtered_addons.append((mod, is_enabled, is_loaded))
        
        # Show count of matching addons
        layout.label(text=f"Found {len(filtered_addons)} extensions")
        layout.separator()
        
        # Display addons in the panel with a scrollable box
        box = layout.box()
        col = box.column()
        
        # Display addons with toggle buttons
        for mod, is_enabled, is_loaded in filtered_addons:
            mod_name = mod.bl_info.get('name', mod.__name__)
            module_name = mod.__name__
            
            # Create a box for each addon
            addon_box = col.box()
            addon_col = addon_box.column()
            
            # First row: Name and version
            header_row = addon_col.row()
            header_row.label(text=mod_name)
            
            # Show version if available
            if 'version' in mod.bl_info:
                version = '.'.join(str(v) for v in mod.bl_info['version'])
                header_row.label(text=f"v{version}")
            
            # Second row: Buttons
            button_row = addon_col.row(align=True)
            
            # Toggle button
            toggle_icon = 'CHECKBOX_HLT' if is_enabled else 'CHECKBOX_DEHLT'
            toggle_text = "Disable" if is_enabled else "Enable"
            button_row.operator("extension.toggle", text=toggle_text, icon=toggle_icon).module_name = module_name
            
            # Reinstall button
            op = button_row.operator("extension.reinstall", text="Reinstall", icon='FILE_REFRESH')
            op.module_name = module_name
            
            # Uninstall button
            op = button_row.operator("extension.uninstall", text="Uninstall", icon='TRASH')
            op.module_name = module_name

def register():
    bpy.utils.register_class(EXTENSION_OT_toggle)
    bpy.utils.register_class(EXTENSION_OT_install)
    bpy.utils.register_class(EXTENSION_OT_reinstall)
    bpy.utils.register_class(EXTENSION_OT_uninstall)
    bpy.utils.register_class(EXTENSION_PT_manager_panel)
    
    # Add search property
    bpy.types.WindowManager.extension_search = bpy.props.StringProperty(
        name="Search Extensions",
        description="Filter extensions by name",
        default=""
    )

def unregister():
    del bpy.types.WindowManager.extension_search
    
    bpy.utils.unregister_class(EXTENSION_PT_manager_panel)
    bpy.utils.unregister_class(EXTENSION_OT_uninstall)
    bpy.utils.unregister_class(EXTENSION_OT_reinstall)
    bpy.utils.unregister_class(EXTENSION_OT_install)
    bpy.utils.unregister_class(EXTENSION_OT_toggle)

if __name__ == "__main__":
    register()
