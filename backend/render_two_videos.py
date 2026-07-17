import os
import glob
from backend.services.behavior.behavior_renderer import BehaviorRenderer

def render_sample_videos():
    renderer = BehaviorRenderer()
    
    # Get JSON files
    json_files = glob.glob("outputs/behavior/json/*_behavior.json")
    if len(json_files) < 2:
        print("Not enough json files found.")
        return
        
    targets = json_files[:2]
    
    for b_json in targets:
        base_name = os.path.basename(b_json).replace("_behavior.json", "")
        print(f"Rendering {base_name}...")
        
        # Paths
        det_json = f"outputs/detection/json/{base_name}.json"
        if not os.path.exists(det_json):
            det_json = f"outputs/detection/json/{base_name}_tracks.json"
            
        out_vid = f"outputs/behavior/videos/{base_name}_behavior.mp4"
        
        # Find original video
        video_matches = glob.glob(f"datasets/*/{base_name}.mp4") + glob.glob(f"datasets/{base_name}.mp4")
        if not video_matches:
            video_matches = glob.glob(f"datasets/*/*/{base_name}.mp4")
            
        video_src = None
        for root, dirs, files in os.walk("datasets"):
            if f"{base_name}.mp4" in files:
                video_src = os.path.join(root, f"{base_name}.mp4")
                break
                
        if video_src and os.path.exists(det_json):
            print(f"Starting render for {video_src}")
            renderer.render(video_src, det_json, b_json, out_vid)
            print(f"Finished render for {out_vid}")
        else:
            print(f"Could not find video or detection json for {base_name}")

if __name__ == "__main__":
    render_sample_videos()
