# Glitch Locations

<a href="http://www.glitch.com">Glitch</a> was a browser-based MMO created by 
<a href="http://tinyspeck.com">Tiny Speck</a>. This repository contains the
artwork and source code for all of the locations in the game world of Ur.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ap0ught/glitch-locations.git
cd glitch-locations

# Extract location data for analysis
unzip locations-xml.zip

# Browse asset categories
ls source/
```

## Repository Contents

### 🏗️ Source Assets (`source/`)
The `source` directory contains **39 asset categories** with Flash source files (.fla) and compiled SWF files (.swf):

#### **Architectural & Buildings**
- `abbasid/` - Middle Eastern architectural elements
- `apartment_exterior/`, `apartment_interior/` - Housing exteriors and interiors
- `bureaucratic_hall/` - Administrative building components
- `tower_quest/` - Tower and quest location elements

#### **Environmental & Landscapes**
- `alpine_landscape/` - Mountain and alpine scenery
- `enchanted_tree/` - Magical tree environments
- `firebog/` - Volcanic and fire-themed areas
- `groddle/`, `groddle_arid/` - Groddle homeland environments
- `esquibeth/` - Forest and nature elements

#### **Housing Systems**
- `homes_alakol/` - Desert-themed housing
- `homes_forest/` - Forest-themed housing  
- `homes_heights/` - Mountain housing
- `homes_meadow/` - Meadow housing
- `new_homes/` - Updated housing elements

#### **Technical & Effects**
- `lighting/` - Comprehensive lighting effects (200+ assets)
- `animated_fx/` - Particle effects, wind, steam, water caustics
- `machine_rooms/` - Industrial and mechanical elements
- `substrata/` - Underground and foundational elements

#### **Game Systems**
- `quests/` - Quest-related visual elements
- `signs/` - Signage and UI indicators
- `wallpaper/` - Interior decoration patterns
- `subway/` - Transportation system elements
- `newxp/` - New player experience elements

### 🎮 Compiled Game Assets (`glitch-location-swfs/`)
Pre-compiled SWF files used by the game client (60+ bundled assets).

### 🗺️ World Data (`locations-xml.zip`)
Contains **2,850+ XML files** representing the construction data for every street in the world of Ur. Each file describes:
- Decoration placement and layering
- Asset positioning and scaling
- Environmental lighting setup
- Interactive object placement

## Sample Usage

### Working with Location XML
```xml
<!-- Example from a typical location XML -->
<game_object tsid="GA5101HF7F429V5" label="Empty Via 5" class_tsid="" swf_file="groddle1.swf">
  <object id="layers">
    <object id="decos">
      <object id="lens_grass_1_1307999844120">
        <int id="x">3208</int>
        <int id="y">516</int>
        <int id="z">27</int>
        <str id="sprite_class">lens_grass_1</str>
      </object>
    </object>
  </object>
</game_object>
```

### Asset Organization Pattern
```
source/[category]/
├── asset_name.fla          # Flash source file
├── asset_name.swf          # Compiled Flash file
└── variations/             # Asset variants
```

### Common Asset Types
- **Decorative Elements**: Trees, rocks, grass, architectural details
- **Lighting Effects**: Ambient lighting, shadows, glows, particle effects
- **Interactive Objects**: Signs, portals, functional game elements
- **Environmental Systems**: Weather effects, atmospheric elements

## Development Information

For technical development details, build instructions, and advanced usage information, see [README-dev.md](README-dev.md).

## License

All files are provided by Tiny Speck under the 
<a href="http://creativecommons.org/publicdomain/zero/1.0/legalcode">Creative
Commons CC0 1.0 Universal License</a>. This is a broadly permissive "No Rights 
Reserved" license — you may do what you please with what we've provided. Our 
intention is to dedicate these works to the public domain and make them freely 
available to all, without restriction.

All files are provided AS-IS. Tiny Speck cannot provide any support to help you 
bring these assets into your own projects. Many of these files are not 
structured in a standard, straightforward way, and they may take a bit of 
your time and work to understand.

**Note**: the Glitch logo and trademark are *not* among the things we are making 
available under this license. Only items in the files explicitly included 
herein are covered.

## Attribution

There is no obligation to link or credit the works, but if you do, please link 
to <a href="http://glitchthegame.com">glitchthegame.com</a>, our permanent 
"retirement" site for the game and these assets. Of course, links/shoutouts to 
Tiny Speck (<a href="http://tinyspeck.com">tinyspeck.com</a>) and/or Slack 
(<a href="http://slack.com">slack.com</a>) are appreciated.

## What is not included

* The LocoDeco tool used to build streets
* Pictures of streets
* Game logic and server code
* Player data or user-generated content

## Contributing

Documentation contributions are welcome! If you figure something out that you think others could learn from, write up a quick how-to document and submit it as a pull request. Share your knowledge!

### Ways to Contribute
- 📚 Improve documentation and examples
- 🔍 Analyze and document asset relationships
- 🛠️ Create tools for working with the assets
- 🎨 Document artistic techniques and patterns
- 📊 Catalog and organize asset usage patterns
