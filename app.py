from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess, os, threading, uuid, json, re

app = Flask(__name__)

BASE_DIR   = os.path.dirname(__file__)
DL_DIR     = os.path.join(BASE_DIR, "downloads")
COOKIE_DIR = os.path.join(BASE_DIR, "cookies")
os.makedirs(DL_DIR, exist_ok=True)
os.makedirs(COOKIE_DIR, exist_ok=True)

jobs = {}   # job_id -> { status, message, log, percent }


# ─── helpers ────────────────────────────────────────────────────────────────

def parse_percent(line):
    """Extract % from yt-dlp progress lines."""
    if "[download]" in line and "%" in line:
        try:
            match = re.search(r'(\d+\.?\d*)%', line)
            if match:
                return float(match.group(1))
        except Exception:
            pass
    return None


def build_cmd(url_list, opts):
    """Build the yt-dlp command from options dict."""
    fmt        = opts.get("format", "mp3")
    resolution = opts.get("resolution", "best")
    quality    = opts.get("quality", "0")
    subtitles  = opts.get("subtitles", False)
    cookie_file = opts.get("cookie_file", "")

    is_audio = fmt in ("mp3", "aac", "flac", "m4a", "opus", "wav", "alac")

    cmd = ["yt-dlp", "--newline", "--progress"]

    if cookie_file and os.path.exists(cookie_file):
        cmd += ["--cookies", cookie_file]

    if is_audio:
        cmd += [
            "-x",
            "--audio-format", fmt,
            "--audio-quality", quality,
            "--embed-thumbnail",
            "--embed-metadata",
        ]
    else:
        # Video: pick best video+audio without container restrictions,
        # then merge to the desired format.
        if resolution == "best":
            format_sel = "bestvideo+bestaudio/best"
        else:
            format_sel = f"bestvideo[height<={resolution}]+bestaudio/bestvideo[height<={resolution}]+bestaudio/best"

        cmd += [
            "-f", format_sel,
            "--merge-output-format", fmt,
            "--embed-thumbnail",
            "--embed-metadata",
        ]

    if subtitles:
        cmd += ["--write-subs", "--embed-subs", "--sub-lang", "en"]

    cmd += ["-o", os.path.join(DL_DIR, "%(uploader)s - %(title)s.%(ext)s")]

    cmd += url_list
    return cmd


def run_job(job_id, url_list, opts):
    jobs[job_id]["status"] = "downloading"
    cmd = build_cmd(url_list, opts)
    jobs[job_id]["log"].append("$ " + " ".join(cmd))

    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, encoding='utf-8', errors='replace'
        )
        for line in proc.stdout:
            line = line.rstrip()
            jobs[job_id]["log"].append(line)
            if len(jobs[job_id]["log"]) > 200:
                jobs[job_id]["log"] = jobs[job_id]["log"][-200:]
            
            pct = parse_percent(line)
            if pct is not None:
                jobs[job_id]["percent"] = pct
                if pct < 100:
                    jobs[job_id]["message"] = f"Downloading: {pct:.1f}%"
                else:
                    jobs[job_id]["message"] = "Processing..."
        
        proc.wait()

        if proc.returncode == 0:
            jobs[job_id]["status"]  = "done"
            jobs[job_id]["percent"] = 100
            jobs[job_id]["message"] = "✅ Download complete! Check the downloads folder."
        else:
            jobs[job_id]["status"]  = "error"
            jobs[job_id]["message"] = "❌ yt-dlp exited with errors. See log below."
    except FileNotFoundError:
        jobs[job_id]["status"]  = "error"
        jobs[job_id]["message"] = "❌ yt-dlp not found. Install it first: pip install yt-dlp"
    except Exception as e:
        jobs[job_id]["status"]  = "error"
        jobs[job_id]["message"] = f"❌ Error: {str(e)}"


# ─── routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    data = request.form

    raw_urls = data.get("urls", "")
    url_list = [u.strip() for u in raw_urls.splitlines() if u.strip()]

    if "batch_file" in request.files:
        f = request.files["batch_file"]
        if f and f.filename and f.filename.endswith(".txt"):
            try:
                extra = f.read().decode('utf-8').splitlines()
                url_list += [u.strip() for u in extra if u.strip()]
            except Exception as e:
                return jsonify({"error": f"Failed to read batch file: {str(e)}"}), 400

    if not url_list:
        return jsonify({"error": "No URLs provided."}), 400

    cookie_path = ""
    if "cookie_file" in request.files:
        cf = request.files["cookie_file"]
        if cf and cf.filename:
            cookie_path = os.path.join(COOKIE_DIR, f"cookies_{uuid.uuid4().hex[:8]}.txt")
            cf.save(cookie_path)

    opts = {
        "format":      data.get("format", "mp3"),
        "resolution":  data.get("resolution", "best"),
        "quality":     data.get("quality", "0"),
        "subtitles":   data.get("subtitles") == "true",
        "cookie_file": cookie_path,
    }

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status":  "queued",
        "message": "Queued...",
        "percent": 0,
        "log":     [],
        "urls":    url_list,
    }

    t = threading.Thread(target=run_job, args=(job_id, url_list, opts))
    t.daemon = True
    t.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({
        "status":  job["status"],
        "message": job["message"],
        "percent": job["percent"],
        "log":     job["log"][-50:],
    })


@app.route("/downloads")
def list_downloads():
    files = []
    try:
        for fn in sorted(os.listdir(DL_DIR), reverse=True):
            fp = os.path.join(DL_DIR, fn)
            if os.path.isfile(fp):
                files.append({
                    "name": fn,
                    "size": round(os.path.getsize(fp) / (1024*1024), 2),
                })
    except Exception:
        pass
    return jsonify(files)


@app.route("/downloads/<path:filename>")
def serve_file(filename):
    return send_from_directory(DL_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    print("=" * 50)
    print("🎬 yt-dlp Web UI Starting...")
    print(f"📍 URL: http://localhost:5000")
    print(f"📁 Downloads folder: {DL_DIR}")
    print("=" * 50)
    app.run(debug=False, port=5000)