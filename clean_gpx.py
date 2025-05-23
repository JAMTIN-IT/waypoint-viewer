#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import re

def clean_gpx_file(input_file, output_file):
    # Parse the GPX file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Define the namespace
    namespaces = {
        '': 'http://www.topografix.com/GPX/1/1',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'wptx1': 'http://www.garmin.com/xmlschemas/WaypointExtension/v1',
        'gpxtrx': 'http://www.garmin.com/xmlschemas/GpxExtensions/v3',
        'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1',
        'gpxx': 'http://www.garmin.com/xmlschemas/GpxExtensions/v3',
    }
    
    # Register all namespaces
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)
    
    # Find all waypoints
    waypoints = root.findall('.//{http://www.topografix.com/GPX/1/1}wpt')
    
    # Text pattern to remove
    pattern = r"Marine Data:\s*notes: Marine data not available - API integration required\s*\n*Processed on:.*"
    
    modified_count = 0
    
    # Process each waypoint
    for wpt in waypoints:
        # Check and clean description tag
        desc = wpt.find('.//{http://www.topografix.com/GPX/1/1}desc')
        if desc is not None and desc.text and re.search(pattern, desc.text):
            desc.text = ''
            modified_count += 1
        
        # Check and clean comment tag
        cmt = wpt.find('.//{http://www.topografix.com/GPX/1/1}cmt')
        if cmt is not None and cmt.text and re.search(pattern, cmt.text):
            cmt.text = ''
            modified_count += 1
    
    # Write the modified XML to the output file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    return modified_count // 2  # Divide by 2 because we modify both cmt and desc for each waypoint

if __name__ == "__main__":
    input_file = "waypoints.gpx"
    output_file = "waypoints_cleaned.gpx"
    
    modified_waypoints = clean_gpx_file(input_file, output_file)
    print(f"Cleaned {modified_waypoints} waypoints. Saved to {output_file}")
    print("To replace the original file, run: move /y waypoints_cleaned.gpx waypoints.gpx")
