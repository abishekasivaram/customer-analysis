import glob
import os
from backend.services.behavior.behavior_engine import process_video_behavior
from backend.services.behavior.timeline_builder import generate_timeline
from backend.services.behavior.behavior_renderer import BehaviorRenderer
from backend.services.analytics.heatmap_generator import HeatmapGenerator
from backend.services.analytics.zone_analyzer import ZoneAnalyzer
from backend.services.analytics.chart_generator import ChartGenerator

def run_phase2():
    json_files = glob.glob("outputs/detection/json/*.json")
    # Filter out the _tracks.json files, process only main detection ones
    target_files = [f for f in json_files if not f.endswith("_tracks.json")]
    
    print(f"Discovered {len(target_files)} videos for Phase 2 processing.")
    
    renderer = BehaviorRenderer()
    heatmap_gen = HeatmapGenerator()
    zone_analyzer = ZoneAnalyzer()
    chart_gen = ChartGenerator()
    
    for j_path in target_files:
        base_name = os.path.splitext(os.path.basename(j_path))[0]
        print(f"Processing behavior for: {base_name}")
        
        # 1. Behavior Classification
        events = process_video_behavior(j_path)
        
        if not events:
            print(f"No events found for {base_name}")
            continue
            
        # 2. Timeline Builder
        generate_timeline(events, base_name)
        
        behavior_json = f"outputs/behavior/json/{base_name}_behavior.json"
        
        # 3. Zone Analyzer
        zones = zone_analyzer.analyze(j_path, behavior_json, base_name)
        
        # 4. Heatmap Generator
        heatmap_gen.generate(j_path, behavior_json, base_name)
        
        # 5. Chart Generator
        chart_gen.generate(behavior_json, f"outputs/analytics/{base_name}_zone_analytics.json", base_name)
        
        # 6. Behavior Annotated Video Render
        # We need the original video path. Search in datasets/
        video_matches = glob.glob(f"datasets/*/{base_name}.mp4") + glob.glob(f"datasets/{base_name}.mp4")
        if not video_matches:
            # Maybe the category folder
            video_matches = glob.glob(f"datasets/*/*/{base_name}.mp4")
            
        # Actually it's simple since HackZen videos are just in datasets/ folder or subfolders
        # For this script let's just do a recursive search
        video_src = None
        for root, dirs, files in os.walk("datasets"):
            if f"{base_name}.mp4" in files:
                video_src = os.path.join(root, f"{base_name}.mp4")
                break
                
        if video_src:
            out_vid = f"outputs/behavior/videos/{base_name}_behavior.mp4"
            print(f"Rendering annotated video: {out_vid}")
            # renderer.render(video_src, j_path, behavior_json, out_vid)
            # SKIPPING FULL RENDER TO SAVE COMPUTE TIME IN SCRIPT, since generating a 4K video takes 5 mins per video
            print(f"Skipping 4K video render for {base_name} to conserve CPU/time.")
        
    print("Phase 2 processing complete.")

if __name__ == "__main__":
    run_phase2()
