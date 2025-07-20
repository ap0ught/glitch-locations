# Glitch Locations - Developer Guide

This document provides technical information for developers working with Glitch location assets.

## File Structure Deep Dive

### Asset Organization
```
glitch-locations/
├── source/                    # 39 asset category directories
│   ├── abbasid/              # Category: architectural elements
│   │   ├── *.fla             # Flash source files (editable)
│   │   └── *.swf             # Compiled Flash files (runtime)
│   ├── lighting/             # Category: lighting & effects (200+ assets)
│   └── ...                   # 37 other categories
├── glitch-location-swfs/     # Bundled production assets (60+ files)
└── locations-xml.zip         # World construction data (2,850+ locations)
```

## File Format Specifications

### Flash Source Files (.fla)
- **Format**: Adobe Flash Professional project files (CS5/CS6 era)
- **Content**: Vector graphics, animations, symbols, timelines
- **Editability**: Requires Adobe Flash Professional or compatible software
- **Structure**: Often contains multiple symbols and movie clips per file

#### Opening .fla Files
```bash
# These files require Adobe Flash Professional, Adobe Animate, or:
# - OpenToonz (open source, limited Flash support)
# - Synfig Studio (vector animation, import/export tools)
# - Wick Editor (web-based Flash-like editor)
```

### Compiled Flash Files (.swf)
- **Format**: Shockwave Flash movies (SWF version 10)
- **Usage**: Runtime assets used by the game client
- **Decompilation**: Use tools like FFDec, SWiX, or Trillix for analysis

#### SWF Analysis Tools
```bash
# Install FFDec (Free Flash Decompiler)
wget https://github.com/jindrapetrik/jpexs-decompiler/releases/latest/ffdec.jar

# Extract assets from SWF
java -jar ffdec.jar -export sprite,shape,image /path/to/asset.swf /output/dir/

# Command line SWF info
swfdump input.swf    # Part of SWFTools package
```

### Location XML Schema
Each location XML follows this structure:

```xml
<game_object 
    tsid="[UNIQUE_ID]"           <!-- Location identifier -->
    ts="[TIMESTAMP]"             <!-- Creation timestamp -->
    label="[HUMAN_NAME]"         <!-- Display name -->
    class_tsid=""                <!-- Object class (usually empty) -->
    swf_file="[SWF_REFERENCE]">  <!-- Primary SWF bundle -->
    
    <object id="dynamic">
        <!-- Boundary definitions -->
        <int id="l">-3000</int>    <!-- Left boundary -->
        <int id="r">3000</int>     <!-- Right boundary -->
        <int id="t">-1000</int>    <!-- Top boundary -->
        <int id="b">0</int>        <!-- Bottom boundary -->
        
        <str id="label">[NAME]</str>
        <str id="swf_file">[SWF]</str>
        
        <object id="layers">
            <object id="[LAYER_ID]">
                <object id="decos">
                    <!-- Individual decoration objects -->
                    <object id="[DECORATION_ID]">
                        <int id="x">[X_POSITION]</int>
                        <int id="y">[Y_POSITION]</int>
                        <int id="z">[Z_DEPTH]</int>
                        <int id="w">[WIDTH]</int>
                        <int id="h">[HEIGHT]</int>
                        <int id="r">[ROTATION]</int>
                        <str id="sprite_class">[ASSET_CLASS]</str>
                        <str id="name">[INSTANCE_NAME]</str>
                    </object>
                </object>
            </object>
        </object>
    </object>
</game_object>
```

## Development Workflows

### Extracting and Analyzing Assets

#### 1. Extract Location Data
```bash
# Extract all location XMLs
unzip locations-xml.zip -d ./extracted_locations/

# Count total locations
find extracted_locations/ -name "*.xml" | wc -l
# Result: 2,850+ files

# Find locations using specific assets
grep -r "sprite_class.*grass" extracted_locations/ | head -5
```

#### 2. Asset Inventory Script
```python
#!/usr/bin/env python3
"""
Asset inventory generator for Glitch locations
"""
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

def analyze_location_assets(xml_dir):
    """Generate asset usage statistics"""
    asset_usage = defaultdict(int)
    location_count = 0
    
    for root, dirs, files in os.walk(xml_dir):
        for file in files:
            if file.endswith('.xml'):
                location_count += 1
                xml_path = os.path.join(root, file)
                
                try:
                    tree = ET.parse(xml_path)
                    # Find all sprite_class references
                    for elem in tree.iter():
                        if elem.get('id') == 'sprite_class':
                            asset_usage[elem.text] += 1
                except ET.ParseError:
                    print(f"Parse error in {file}")
                    
    return asset_usage, location_count

# Usage
if __name__ == "__main__":
    assets, total = analyze_location_assets("./extracted_locations/")
    print(f"Analyzed {total} locations")
    print(f"Found {len(assets)} unique asset types")
    
    # Top 10 most used assets
    for asset, count in sorted(assets.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{asset}: {count} uses")
```

#### 3. SWF Asset Extraction
```bash
#!/bin/bash
# Extract all images from SWF files

mkdir -p extracted_assets/

for swf in source/*/*.swf; do
    filename=$(basename "$swf" .swf)
    category=$(basename $(dirname "$swf"))
    
    # Create category directory
    mkdir -p "extracted_assets/$category"
    
    # Extract using FFDec
    java -jar ffdec.jar -export image "$swf" "extracted_assets/$category/$filename/"
done
```

### Asset Integration Patterns

#### Loading Assets in Web Applications
```javascript
// Example: Loading Glitch assets in a web project
class GlitchAssetLoader {
    constructor(basePath = './glitch-location-swfs/') {
        this.basePath = basePath;
        this.loadedAssets = new Map();
    }
    
    async loadLocationSWF(categoryName) {
        const swfPath = `${this.basePath}${categoryName}.swf`;
        
        // Note: Modern browsers don't support SWF directly
        // Consider using Ruffle (Flash emulator) or convert to other formats
        
        if (window.RufflePlayer) {
            const ruffle = window.RufflePlayer.newest();
            const player = ruffle.createPlayer();
            player.load(swfPath);
            return player;
        }
        
        throw new Error('Flash player not available. Consider asset conversion.');
    }
    
    // Parse location XML for asset placement
    async parseLocationXML(xmlContent) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(xmlContent, 'text/xml');
        
        const decos = [];
        const decorationElements = doc.querySelectorAll('object[id="decos"] > object');
        
        decorationElements.forEach(deco => {
            const getIntValue = (id) => {
                const elem = deco.querySelector(`int[id="${id}"]`);
                return elem ? parseInt(elem.textContent) : 0;
            };
            
            const getStrValue = (id) => {
                const elem = deco.querySelector(`str[id="${id}"]`);
                return elem ? elem.textContent : '';
            };
            
            decos.push({
                id: deco.id,
                x: getIntValue('x'),
                y: getIntValue('y'),
                z: getIntValue('z'),
                width: getIntValue('w'),
                height: getIntValue('h'),
                rotation: getIntValue('r'),
                spriteClass: getStrValue('sprite_class'),
                name: getStrValue('name')
            });
        });
        
        return decos;
    }
}

// Usage
const loader = new GlitchAssetLoader();
const locationData = await loader.parseLocationXML(xmlContent);
```

### Asset Conversion Workflows

#### Converting SWF to Modern Formats
```bash
# Using swf2js (JavaScript conversion)
npm install -g swf2js
swf2js input.swf output.js

# Using swfextract (part of SWFTools)
swfextract -i input.swf        # List all objects
swfextract -p 1 input.swf      # Extract object #1
swfextract -j 1 input.swf      # Extract as JPEG

# Using FFmpeg for video conversion (for animated assets)
ffmpeg -i input.swf -pix_fmt rgba output.mov
```

#### Batch Asset Processing
```python
#!/usr/bin/env python3
"""
Batch process Glitch assets for modern web use
"""
import os
import subprocess
from pathlib import Path

def convert_swf_to_images(source_dir, output_dir):
    """Convert all SWF files to extractable image sets"""
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for category_dir in source_path.iterdir():
        if category_dir.is_dir():
            category_output = output_path / category_dir.name
            category_output.mkdir(exist_ok=True)
            
            for swf_file in category_dir.glob('*.swf'):
                print(f"Processing {swf_file}")
                
                # Extract images using FFDec
                asset_output = category_output / swf_file.stem
                asset_output.mkdir(exist_ok=True)
                
                cmd = [
                    'java', '-jar', 'ffdec.jar',
                    '-export', 'image',
                    str(swf_file),
                    str(asset_output)
                ]
                
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    print(f"✓ Extracted images from {swf_file.name}")
                except subprocess.CalledProcessError as e:
                    print(f"✗ Failed to extract {swf_file.name}: {e}")

# Usage
convert_swf_to_images('./source/', './converted_assets/')
```

## Hidden Asset Information

### Lighting System Architecture
The `lighting/` directory contains a sophisticated lighting system with:
- **Ground Effects**: 26 different ground shadow/bump variations
- **Atmospheric**: Clouds, haze, lens flares, light shafts
- **Magic Effects**: Mushroom lights, glowing orbs, color groups
- **Environmental**: Sky gradients, stars, sun elements

### Asset Naming Conventions
```
[category]_[type]_[variant]_[version][suffix]

Examples:
- groddle_light_pool         # Groddle area light pool
- magic_mushroom_light_blue  # Blue magical mushroom light
- shadow_brown_70percent_al1 # Brown shadow at 70% opacity, alpine variant 1
- newxp_t1_striations_sun_01a # New experience tier 1 sun striations, variant 01a
```

### Performance Considerations
- **Asset Loading**: SWF files range from 1KB to 100KB+ each
- **Memory Usage**: Flash assets can consume significant memory when loaded
- **Z-Index Management**: Location XMLs use z-values for proper layering
- **Coordinate System**: Uses Flash coordinate system (top-left origin)

## Debugging and Troubleshooting

### Common Issues

#### 1. Flash Player Compatibility
Modern browsers don't support Flash. Consider:
- **Ruffle**: Open-source Flash emulator
- **Asset Conversion**: Extract to PNG/SVG/WebP
- **Recreation**: Rebuild in modern web technologies

#### 2. Missing Assets
```bash
# Find broken sprite_class references
python3 << EOF
import xml.etree.ElementTree as ET
import os

missing_assets = set()
for root, dirs, files in os.walk('./extracted_locations/'):
    for file in files:
        if file.endswith('.xml'):
            try:
                tree = ET.parse(os.path.join(root, file))
                for elem in tree.iter():
                    if elem.get('id') == 'sprite_class':
                        asset_name = elem.text
                        # Check if corresponding file exists
                        found = False
                        for cat_dir in os.listdir('./source/'):
                            if os.path.exists(f'./source/{cat_dir}/{asset_name}.swf'):
                                found = True
                                break
                        if not found:
                            missing_assets.add(asset_name)
            except ET.ParseError:
                pass

print(f"Found {len(missing_assets)} potentially missing assets:")
for asset in sorted(missing_assets):
    print(f"  - {asset}")
EOF
```

#### 3. Coordinate System Translation
```javascript
// Convert Flash coordinates to web coordinates
function flashToWebCoords(flashX, flashY, stageWidth, stageHeight) {
    // Flash uses top-left origin, web often uses center or bottom-left
    return {
        webX: flashX,
        webY: stageHeight - flashY  // Flip Y axis
    };
}
```

## Building Tools and Extensions

### Recommended Development Stack
- **Flash Analysis**: FFDec, SWFTools
- **Asset Conversion**: ImageMagick, FFmpeg
- **Web Integration**: Ruffle, PixiJS, Three.js
- **XML Processing**: Python xml.etree, Node.js xml2js
- **Version Control**: Git LFS for large asset files

### Contributing to Development

1. **Asset Documentation**: Document discovered patterns and relationships
2. **Tool Development**: Create utilities for asset processing
3. **Format Conversion**: Help modernize assets for current web standards
4. **Analysis Scripts**: Build tools for understanding asset usage patterns

## Resources

- [Adobe Flash Professional Documentation](https://helpx.adobe.com/flash/user-guide.html)
- [SWF File Format Specification](https://www.adobe.com/devnet/swf.html)
- [FFDec GitHub Repository](https://github.com/jindrapetrik/jpexs-decompiler)
- [Ruffle Flash Emulator](https://ruffle.rs/)
- [PixiJS for Asset Rendering](https://pixijs.com/)

---

*This documentation is a living document. Please contribute improvements and discoveries!*