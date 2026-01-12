"""Command-line interface for Anymate."""

import sys
import argparse
from pathlib import Path
from anymatelib.config import get_config
from anymatelib.extract_scene import get_scene_class, list_scenes, render_scene


def main():
    """Main entry point for the anymate command."""
    parser = argparse.ArgumentParser(
        description="Anymate - A powerful animation engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  anymate example_scenes.py OpeningExample
  anymate example_scenes.py SquareToCircle -w
  anymate example_scenes.py -l  # List scenes
        """
    )
    
    parser.add_argument(
        'file',
        help='Python file containing the scene'
    )
    
    parser.add_argument(
        'scene',
        nargs='?',
        help='Name of the scene class to render'
    )
    
    # List scenes
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all scenes in the file'
    )
    
    # Output options
    parser.add_argument(
        '-w', '--write_file',
        action='store_true',
        help='Write the scene to a video file'
    )
    
    parser.add_argument(
        '-o', '--open',
        action='store_true',
        help='Write the file and open it'
    )
    
    parser.add_argument(
        '-s', '--skip_animations',
        action='store_true',
        help='Skip animations and show final frame'
    )
    
    parser.add_argument(
        '--save_last_frame',
        action='store_true',
        help='Save the last frame as an image'
    )
    
    parser.add_argument(
        '--save_pngs',
        action='store_true',
        help='Save all frames as PNG images'
    )
    
    parser.add_argument(
        '--save_as_gif',
        action='store_true',
        help='Save the scene as a GIF'
    )
    
    parser.add_argument(
        '--transparent',
        action='store_true',
        help='Render with transparent background'
    )
    
    # Quality presets
    quality_group = parser.add_mutually_exclusive_group()
    quality_group.add_argument(
        '-ql', '--quality_low',
        action='store_true',
        help='Low quality (480p15)'
    )
    
    quality_group.add_argument(
        '-qm', '--quality_medium',
        action='store_true',
        help='Medium quality (720p30)'
    )
    
    quality_group.add_argument(
        '-qh', '--quality_high',
        action='store_true',
        help='High quality (1080p60)'
    )
    
    quality_group.add_argument(
        '-qk', '--quality_ultra',
        action='store_true',
        help='Ultra quality (4K60)'
    )
    
    # Resolution
    parser.add_argument(
        '-r', '--resolution',
        help='Resolution (e.g., "1920x1080")'
    )
    
    # Frame rate
    parser.add_argument(
        '--fps', '--frame_rate',
        type=int,
        help='Frame rate'
    )
    
    # Window options
    parser.add_argument(
        '-f', '--full_screen',
        action='store_true',
        help='Show in fullscreen'
    )
    
    parser.add_argument(
        '-p', '--presenter_mode',
        action='store_true',
        help='Enable presenter mode (interactive)'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        default=True,
        help='Show preview window (default: True)'
    )
    
    parser.add_argument(
        '--no_preview',
        action='store_true',
        help='Disable preview window'
    )
    
    # Animation control
    parser.add_argument(
        '-n', '--from_animation_number',
        type=int,
        help='Start from animation number N'
    )
    
    # Verbosity
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    # List scenes if requested
    if args.list:
        list_scenes(str(file_path))
        sys.exit(0)
    
    # Check if scene name provided
    if not args.scene:
        print("Error: Scene name required (or use -l to list scenes)")
        parser.print_help()
        sys.exit(1)
    
    # Get config
    config = get_config()
    
    # Apply quality preset
    if args.quality_low:
        config.apply_quality_preset('low')
    elif args.quality_medium:
        config.apply_quality_preset('medium')
    elif args.quality_high:
        config.apply_quality_preset('high')
    elif args.quality_ultra:
        config.apply_quality_preset('ultra')
    
    # Apply resolution
    if args.resolution:
        try:
            width, height = map(int, args.resolution.split('x'))
            config.set('pixel_width', width)
            config.set('pixel_height', height)
        except ValueError:
            print(f"Error: Invalid resolution format: {args.resolution}")
            sys.exit(1)
    
    # Apply frame rate
    if args.fps:
        config.set('frame_rate', args.fps)
    
    # Apply other options
    config.set('write_to_movie', args.write_file or args.open)
    config.set('save_last_frame', args.save_last_frame)
    config.set('save_pngs', args.save_pngs)
    config.set('save_as_gif', args.save_as_gif)
    config.set('transparent', args.transparent)
    config.set('skip_animations', args.skip_animations)
    config.set('fullscreen', args.full_screen)
    config.set('presenter_mode', args.presenter_mode)
    
    if args.no_preview:
        config.set('preview', False)
    
    # Get scene class
    try:
        scene_class = get_scene_class(str(file_path), args.scene)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Render scene
    print(f"Rendering {scene_class.__name__}...")
    
    render_options = config.to_dict()
    scene = render_scene(scene_class, **render_options)
    
    print("Done!")
    
    # Open file if requested
    if args.open and scene.file_writer:
        movie_path = scene.file_writer.get_movie_file_path()
        if movie_path:
            import os
            os.startfile(str(movie_path))


if __name__ == "__main__":
    main()
