import os
import re
import time
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, Callable
import yt_dlp

def get_ffmpeg_directory() -> Optional[str]:
    """Finds ffmpeg directory in PyInstaller bundle, project bin, PATH or WinGet."""
    import sys

    # 1. PyInstaller bundled location
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", "")
        for sub in ["", "bin"]:
            cand = os.path.join(meipass, sub)
            if os.path.exists(os.path.join(cand, "ffmpeg.exe")):
                return cand
        # Check beside the executable itself
        exe_dir = os.path.dirname(sys.executable)
        for sub in ["", "bin"]:
            cand = os.path.join(exe_dir, sub)
            if os.path.exists(os.path.join(cand, "ffmpeg.exe")):
                return cand

    # 2. Local project bin directory
    project_bin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    if os.path.exists(os.path.join(project_bin, "ffmpeg.exe")):
        return project_bin

    # 3. System PATH
    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin:
        return str(Path(ffmpeg_bin).parent)
    
    # 4. WinGet packages
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    if local_appdata:
        winget_path = Path(local_appdata) / "Microsoft" / "WinGet" / "Packages"
        if winget_path.exists():
            for p in winget_path.glob("**/bin/ffmpeg.exe"):
                return str(p.parent)
            for p in winget_path.glob("**/ffmpeg.exe"):
                return str(p.parent)

    # 5. Standard fallback paths
    for candidate in [
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
    ]:
        if os.path.exists(os.path.join(candidate, "ffmpeg.exe")):
            return candidate

    return None

def format_duration(seconds: Optional[int]) -> str:
    """Formats seconds into HH:MM:SS or MM:SS."""
    if not seconds:
        return "Bilinmiyor"
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def format_views(views: Optional[int]) -> str:
    """Formats view count into human-readable string (e.g., 1.2M, 450K)."""
    if not views:
        return "0"
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    if views >= 1_000:
        return f"{views / 1_000:.1f}K"
    return str(views)

def format_filesize(size_bytes: Optional[int]) -> str:
    """Formats byte size into KB, MB, GB."""
    if not size_bytes:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_video_info(url: str) -> Dict[str, Any]:
    """Fetches video metadata without downloading."""
    ffmpeg_dir = get_ffmpeg_directory()
    ydl_opts: Dict[str, Any] = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'source_address': '0.0.0.0',
        'nocheckcertificate': True,
        'js_runtimes': {'node': {}, 'deno': {}, 'quickjs': {}},
        'remote_components': ['ejs:github'],
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
    }
    if ffmpeg_dir:
        ydl_opts['ffmpeg_location'] = ffmpeg_dir

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if not info:
            raise ValueError("Video bilgileri alınamadı.")

        title = info.get('title', 'YouTube Medyası')
        channel = info.get('uploader') or info.get('channel', 'Bilinmeyen Kanal')
        duration = info.get('duration', 0)
        thumbnail = info.get('thumbnail')
        view_count = info.get('view_count', 0)
        description = info.get('description', '')
        
        # Check resolutions available
        formats = info.get('formats', [])
        heights = set()
        for f in formats:
            h = f.get('height')
            if h and isinstance(h, int):
                heights.add(h)
        best_resolution = f"{max(heights)}p" if heights else "1080p (En Yüksek)"

        return {
            'id': info.get('id', ''),
            'title': title,
            'channel': channel,
            'duration': duration,
            'duration_formatted': format_duration(duration),
            'views_formatted': format_views(view_count),
            'thumbnail': thumbnail,
            'description': (description[:240] + "...") if len(description) > 240 else description,
            'best_resolution': best_resolution,
            'webpage_url': info.get('webpage_url', url)
        }

def parse_time_to_seconds(time_str: Optional[str]) -> Optional[float]:
    """Parses timestamps ('00:01:15', '01:15', '75') into seconds."""
    if not time_str or not time_str.strip():
        return None
    val = time_str.strip()
    try:
        return float(val)
    except ValueError:
        pass

    parts = val.split(":")
    try:
        if len(parts) == 3:
            h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
            return h * 3600 + m * 60 + s
        elif len(parts) == 2:
            m, s = float(parts[0]), float(parts[1])
            return m * 60 + s
    except (ValueError, TypeError):
        pass
    raise ValueError(f"Geçersiz zaman biçimi: '{time_str}'. Örnek: '00:01:15', '01:15' veya saniye '75'")

def cleanup_old_files(folder: str = "downloads", max_age_hours: float = 3.0) -> None:
    """Removes temporary files older than max_age_hours to prevent cloud server disk bloat."""
    try:
        if not os.path.exists(folder):
            return
        now = time.time()
        max_age_sec = max_age_hours * 3600
        for entry in os.listdir(folder):
            fpath = os.path.join(folder, entry)
            if os.path.isfile(fpath):
                if now - os.path.getmtime(fpath) > max_age_sec:
                    try:
                        os.remove(fpath)
                    except Exception:
                        pass
    except Exception:
        pass

def download_media(
    url: str,
    download_mode: str,
    output_folder: str = "downloads",
    progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Downloads the YouTube media as MP3 or MP4 with highest quality.
    Supports partial section cutting using FFmpeg.
    
    download_mode: 'audio' or 'video'
    """
    os.makedirs(output_folder, exist_ok=True)
    cleanup_old_files(output_folder)
    ffmpeg_dir = get_ffmpeg_directory()

    # Ensure FFmpeg directory is in process PATH for frame-accurate section cutting
    if ffmpeg_dir and ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    final_filepath_holder = {'path': None}

    def hook(d: Dict[str, Any]):
        status = d.get('status')
        if status == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total > 0 else 0
            speed = d.get('speed') or 0
            eta = d.get('eta') or 0

            if progress_callback:
                progress_callback({
                    'status': 'downloading',
                    'percent': min(max(percent, 0), 100),
                    'downloaded_bytes': downloaded,
                    'total_bytes': total,
                    'speed_str': f"{format_filesize(speed)}/s" if speed else "Hesaplanıyor...",
                    'eta_str': f"{eta} sn" if eta else "Hesaplanıyor..."
                })
        elif status == 'finished':
            final_filepath_holder['path'] = d.get('filename')
            if progress_callback:
                progress_callback({
                    'status': 'processing',
                    'percent': 100,
                    'message': 'İndirme tamamlandı! Ses/Video dönüştürülüyor...'
                })

    outtmpl = os.path.join(output_folder, "%(title).80s [%(id)s].%(ext)s")

    if download_mode == 'audio':
        # Highest quality audio converted to MP3 (320kbps)
        ydl_opts: Dict[str, Any] = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                },
                {
                    'key': 'FFmpegMetadata',
                    'add_metadata': True,
                }
            ],
            'progress_hooks': [hook],
            'quiet': True,
            'no_warnings': True,
            'windowsfilenames': True,
        }
        target_ext = "mp3"
    else:
        # Highest quality video + best audio merged to MP4
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'outtmpl': outtmpl,
            'merge_output_format': 'mp4',
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }
            ],
            'progress_hooks': [hook],
            'quiet': True,
            'no_warnings': True,
            'windowsfilenames': True,
        }
        target_ext = "mp4"

    if ffmpeg_dir:
        ydl_opts['ffmpeg_location'] = ffmpeg_dir

    ydl_opts['source_address'] = '0.0.0.0'
    ydl_opts['js_runtimes'] = {'node': {}, 'deno': {}, 'quickjs': {}}
    ydl_opts['remote_components'] = ['ejs:github']
    ydl_opts['nocheckcertificate'] = True
    ydl_opts['extractor_args'] = {
        'youtube': {
            'player_client': ['android'],
        }
    }

    # Section / Range Download Handling
    has_cut = False
    section_display = None
    if start_time or end_time:
        start_sec = parse_time_to_seconds(start_time) if start_time else 0.0
        end_sec = parse_time_to_seconds(end_time) if end_time else float('inf')

        if start_sec is not None and end_sec is not None and start_sec >= end_sec:
            raise ValueError(f"Başlangıç zamanı ({start_time}), bitiş zamanından ({end_time}) küçük olmalıdır.")

        from yt_dlp.utils import download_range_func
        ydl_opts['download_ranges'] = download_range_func([], [[start_sec or 0.0, end_sec or float('inf')]])
        # Enable precise cut with FFmpeg keyframe generation
        ydl_opts['force_keyframes_at_cuts'] = True
        has_cut = True
        section_display = f"{start_time or '00:00'} - {end_time or 'Son'}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info.get('id', '')
        title = info.get('title', 'İndirilen Dosya')

        # Locate the newest output file in output_folder matching video_id and target_ext
        candidates = []
        for filename in os.listdir(output_folder):
            if video_id in filename and filename.lower().endswith(f".{target_ext}"):
                full_path = os.path.join(output_folder, filename)
                candidates.append((os.path.getmtime(full_path), full_path))

        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            final_file = candidates[0][1]
        elif final_filepath_holder['path']:
            cand = final_filepath_holder['path']
            cand_target = str(Path(cand).with_suffix(f".{target_ext}"))
            if os.path.exists(cand_target):
                final_file = cand_target
            elif os.path.exists(cand):
                final_file = cand
            else:
                final_file = None
        else:
            final_file = None

        if not final_file or not os.path.exists(final_file):
            raise FileNotFoundError("İndirilen medya dosyası diskte bulunamadı.")

        file_size = os.path.getsize(final_file)

        return {
            'file_path': final_file,
            'file_name': os.path.basename(final_file),
            'file_size': file_size,
            'file_size_formatted': format_filesize(file_size),
            'title': title,
            'format': target_ext.upper(),
            'channel': info.get('uploader') or info.get('channel', ''),
            'is_cut': has_cut,
            'section': section_display
        }
