#!/usr/bin/env python3
"""
Glitch Locations Asset Analyzer

This script demonstrates how to work with Glitch location assets.
It provides examples for:
- Extracting location XML data
- Analyzing asset usage patterns  
- Generating inventory reports
- Finding asset relationships

Usage:
    python3 analyze_assets.py [--extract-xml] [--inventory] [--usage-stats]
"""

import os
import sys
import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
import zipfile
from pathlib import Path

class GlitchAssetAnalyzer:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.locations_zip = self.base_path / "locations-xml.zip"
        self.source_dir = self.base_path / "source"
        self.swf_dir = self.base_path / "glitch-location-swfs"
        
    def extract_locations_xml(self, output_dir="extracted_locations"):
        """Extract locations-xml.zip for analysis"""
        output_path = self.base_path / output_dir
        output_path.mkdir(exist_ok=True)
        
        if not self.locations_zip.exists():
            print(f"Error: {self.locations_zip} not found")
            return False
            
        print(f"Extracting {self.locations_zip} to {output_path}")
        
        with zipfile.ZipFile(self.locations_zip, 'r') as zip_ref:
            zip_ref.extractall(output_path)
            
        xml_files = list(output_path.rglob("*.xml"))
        print(f"Extracted {len(xml_files)} location XML files")
        return True
        
    def get_asset_categories(self):
        """List all asset categories from source directory"""
        if not self.source_dir.exists():
            print(f"Error: {self.source_dir} not found")
            return []
            
        categories = [d.name for d in self.source_dir.iterdir() if d.is_dir()]
        categories.sort()
        return categories
        
    def analyze_asset_usage(self, xml_dir="extracted_locations"):
        """Analyze which assets are used in locations"""
        xml_path = self.base_path / xml_dir
        
        if not xml_path.exists():
            print(f"XML directory {xml_path} not found. Run with --extract-xml first.")
            return None
            
        asset_usage = Counter()
        swf_usage = Counter()
        location_count = 0
        
        print("Analyzing location XML files...")
        
        for xml_file in xml_path.rglob("*.xml"):
            location_count += 1
            
            if location_count % 100 == 0:
                print(f"  Processed {location_count} locations...")
                
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Get SWF file reference
                swf_elem = root.find(".//str[@id='swf_file']")
                if swf_elem is not None:
                    swf_usage[swf_elem.text] += 1
                
                # Find all sprite_class references (individual assets)
                for elem in tree.iter():
                    if elem.get('id') == 'sprite_class' and elem.text:
                        asset_usage[elem.text] += 1
                        
            except ET.ParseError as e:
                print(f"Parse error in {xml_file}: {e}")
                continue
                
        print(f"Analyzed {location_count} locations")
        
        return {
            'assets': asset_usage,
            'swfs': swf_usage,
            'location_count': location_count
        }
        
    def generate_inventory_report(self):
        """Generate comprehensive asset inventory"""
        print("=== GLITCH LOCATIONS ASSET INVENTORY ===\n")
        
        # Asset categories
        categories = self.get_asset_categories()
        print(f"📁 Asset Categories ({len(categories)}):")
        for i, category in enumerate(categories, 1):
            asset_files = list((self.source_dir / category).glob("*.swf"))
            print(f"  {i:2d}. {category:<20} ({len(asset_files)} assets)")
        
        print()
        
        # SWF bundles
        if self.swf_dir.exists():
            swf_files = list(self.swf_dir.glob("*.swf"))
            print(f"🎮 Compiled SWF Bundles: {len(swf_files)} files")
            
            # Show file sizes
            total_size = sum(f.stat().st_size for f in swf_files)
            print(f"📊 Total SWF size: {total_size / (1024*1024):.1f} MB")
            
            # Largest files
            swf_sizes = [(f.name, f.stat().st_size) for f in swf_files]
            swf_sizes.sort(key=lambda x: x[1], reverse=True)
            
            print("\n   Largest SWF files:")
            for name, size in swf_sizes[:5]:
                print(f"     {name:<25} {size/1024:.1f} KB")
        
        print()
        
        # Location data
        if self.locations_zip.exists():
            zip_size = self.locations_zip.stat().st_size
            print(f"🗺️  Location XML Data: {zip_size / (1024*1024):.1f} MB compressed")
            
            with zipfile.ZipFile(self.locations_zip, 'r') as zf:
                xml_count = len([f for f in zf.namelist() if f.endswith('.xml')])
                print(f"📍 Total Locations: {xml_count}")
        
    def show_usage_statistics(self, xml_dir="extracted_locations"):
        """Show asset usage statistics from location analysis"""
        usage_data = self.analyze_asset_usage(xml_dir)
        
        if not usage_data:
            return
            
        assets = usage_data['assets']
        swfs = usage_data['swfs']
        
        print("=== ASSET USAGE STATISTICS ===\n")
        
        print(f"📊 Analysis Summary:")
        print(f"   Locations analyzed: {usage_data['location_count']:,}")
        print(f"   Unique assets used: {len(assets):,}")
        print(f"   Unique SWF bundles: {len(swfs):,}")
        print(f"   Total asset instances: {sum(assets.values()):,}")
        
        print(f"\n🏆 Top 15 Most Used Assets:")
        for i, (asset, count) in enumerate(assets.most_common(15), 1):
            print(f"   {i:2d}. {asset:<30} ({count:,} uses)")
            
        print(f"\n📦 Most Used SWF Bundles:")
        for i, (swf, count) in enumerate(swfs.most_common(10), 1):
            print(f"   {i:2d}. {swf:<25} ({count:,} locations)")
            
        # Find rare assets (used in only 1-2 locations)
        rare_assets = [(asset, count) for asset, count in assets.items() if count <= 2]
        print(f"\n🔍 Rare Assets (≤2 uses): {len(rare_assets)} found")
        
        if rare_assets:
            print("   Examples:")
            for asset, count in sorted(rare_assets)[:10]:
                print(f"     {asset:<30} ({count} use{'s' if count > 1 else ''})")

def main():
    parser = argparse.ArgumentParser(description="Analyze Glitch Locations assets")
    parser.add_argument("--extract-xml", action="store_true", 
                       help="Extract locations-xml.zip file")
    parser.add_argument("--inventory", action="store_true",
                       help="Generate asset inventory report")
    parser.add_argument("--usage-stats", action="store_true",
                       help="Show asset usage statistics")
    parser.add_argument("--xml-dir", default="extracted_locations",
                       help="Directory containing extracted XML files")
    
    args = parser.parse_args()
    
    analyzer = GlitchAssetAnalyzer()
    
    if args.extract_xml:
        analyzer.extract_locations_xml(args.xml_dir)
        
    if args.inventory:
        analyzer.generate_inventory_report()
        
    if args.usage_stats:
        analyzer.show_usage_statistics(args.xml_dir)
        
    # If no specific action requested, show basic inventory
    if not any([args.extract_xml, args.inventory, args.usage_stats]):
        print("Glitch Locations Asset Analyzer")
        print("Run with --help to see available options\n")
        analyzer.generate_inventory_report()

if __name__ == "__main__":
    main()