# Extension Manager for Blender

A simple Blender addon that provides an easy-to-use interface for toggling Blender extensions on and off from a sidebar panel.

## Features

- Access all your Blender extensions from a convenient sidebar panel
- Toggle extensions on/off with dedicated buttons
- Install new extensions directly from the panel
- Reinstall/update existing extensions with a single click
- Uninstall extensions completely with confirmation dialog
- Search functionality to quickly find specific extensions
- Alphabetically sorted extension list for easy navigation
- Version information displayed for each extension

## Installation

### Method 1: Direct Installation (Recommended)
1. Download the `extension_manager.zip` file
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Click "Install..." and select the downloaded zip file
5. Enable the "Interface: Extension Manager" addon in the list

### Method 2: Manual Installation
1. Unzip the `extension_manager.zip` file
2. Copy the `extension_manager` folder to your Blender addons directory:
   - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - Linux: `~/.config/blender/[version]/scripts/addons/`
3. Open Blender
4. Go to Edit > Preferences > Add-ons
5. Enable the "Interface: Extension Manager" addon in the list

## Usage

1. Open the 3D View in Blender
2. Look for the sidebar on the right (press N if it's not visible)
3. Click on the "Extensions" tab
4. Use the search box to filter extensions by name
5. Use the "Enable"/"Disable" buttons to toggle extensions on/off
6. Use the "Install New Extension" button to add new extensions
7. Use the "Reinstall" button to update or fix existing extensions
8. Use the "Uninstall" button to completely remove an extension (with confirmation)

## Troubleshooting

If you encounter any issues:

1. Make sure the addon is properly installed and enabled
2. Try restarting Blender after installation
3. Check the Blender System Console for any error messages
4. Ensure you're using a compatible Blender version (3.5+)

## Compatibility

This addon is compatible with Blender 3.5 and newer.

## Customization

You can modify the addon to:
- Change the tab name (modify the `bl_category` property)
- Add additional filtering options
- Customize the display of extension information

See the comments in the source code for guidance.

## License

This addon is released under the [MIT License](LICENSE).

## Author Information

```
Author: Kindjhali
Contact: aphexice@gmail.com
Website: https://www.youtube.com/@GiveItKibble

```

## Project Information

```
Repository: https://github.com/Kindjhali/BEM---Blender-Extension-Manager
License: MIT
Version History:
    1.0.0 - Initial release
```

## Credits

```

Special Thanks:
    - Ziggy
    - Doc
```

