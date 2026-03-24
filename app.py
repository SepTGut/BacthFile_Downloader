from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess, os, threading, uuid, re, glob

app = Flask(__name__)

BASE_DIR   = os.path.dirname(__file__)
DL_DIR     = os.path.join(BASE_DIR, "downloads")
COOKIE_DIR = os.path.join(BASE_DIR, "cookies")
os.makedirs(DL_DIR, exist_ok=True)
os.makedirs(COOKIE_DIR, exist_ok=True)

jobs = {}          # job_id -> job dict
_sem_lock = threading.Lock()
_semaphore = threading.Semaphore(3)   # default max 3 simultaneous downloads


# ─── helpers ────────────────────────────────────────────────────────────────

def set_thread_limit(n):
    global _semaphore
    with _sem_lock:
        _semaphore = threading.Semaphore(max(1, int(n)))


def parse_percent(line):
    if "[download]" in line and "%" in line:
        try:
            m = re.search(r'(\d+\.?\d*)%', line)
            if m:
                return float(m.group(1))
        except Exception:
            pass
    return None


def parse_video_index(line):
    """Detect lines like '[download] Downloading video 3 of 10'"""
    m = re.search(r'Downloading video (\d+) of (\d+)', line)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def cleanup_old_cookies():
    files = sorted(
        glob.glob(os.path.join(COOKIE_DIR, "cookies_*.txt")),
        key=os.path.getmtime, reverse=True
    )
    for old in files[5:]:
        try:
            os.remove(old)
        except Exception:
            pass


def build_cmd(url_list, opts):
    fmt         = opts.get("format", "mp3")
    resolution  = opts.get("resolution", "best")
    quality     = opts.get("quality", "0")
    subtitles   = opts.get("subtitles", False)
    cookie_file = opts.get("cookie_file", "")
    sponsorblock = opts.get("sponsorblock", False)
    rate_limit  = opts.get("rate_limit", "").strip()

    is_audio = fmt in ("mp3", "aac", "flac", "m4a", "opus", "wav", "alac")

    cmd = ["yt-dlp", "--newline", "--progress"]

    if cookie_file and os.path.exists(cookie_file):
        cmd += ["--cookies", cookie_file]

    # rate limiter
    if rate_limit:
        cmd += ["--limit-rate", rate_limit]

    # SponsorBlock
    if sponsorblock:
        cmd += ["--sponsorblock-remove", "sponsor,intro,outro,selfpromo,interaction"]

    if is_audio:
        cmd += [
            "-x",
            "--audio-format", fmt,
            "--audio-quality", quality,
            "--embed-thumbnail",
            "--embed-metadata",
        ]
    else:
        if resolution == "best":
            format_sel = "bestvideo+bestaudio/best"
        else:
            format_sel = (
                f"bestvideo[height<={resolution}]+bestaudio/"
                f"bestvideo[height<={resolution}]+bestaudio/best"
            )
        cmd += [
            "-f", format_sel,
            "--merge-output-format", fmt,
            "--embed-thumbnail",
            "--embed-metadata",
        ]

    if subtitles:
        cmd += ["--write-subs", "--write-auto-sub", "--embed-subs", "--sub-lang", "en"]

    cmd += ["-o", os.path.join(DL_DIR, "%(uploader)s - %(title)s.%(ext)s")]
    cmd += url_list
    return cmd


def run_job(job_id, url_list, opts):
    with _semaphore:
        if jobs[job_id]["status"] == "cancelled":
            return

        jobs[job_id]["status"] = "downloading"
        cmd = build_cmd(url_list, opts)
        jobs[job_id]["log"].append("$ " + " ".join(cmd))

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, encoding="utf-8", errors="replace",
            )
            jobs[job_id]["proc"] = proc   # store so we can cancel

            for line in proc.stdout:
                line = line.rstrip()
                jobs[job_id]["log"].append(line)
                if len(jobs[job_id]["log"]) > 200:
                    jobs[job_id]["log"] = jobs[job_id]["log"][-200:]

                pct = parse_percent(line)
                if pct is not None:
                    jobs[job_id]["percent"] = pct

                vi, vt = parse_video_index(line)
                if vi is not None:
                    jobs[job_id]["video_index"] = vi
                    jobs[job_id]["video_total"] = vt
                    jobs[job_id]["percent"] = 0  # reset per-video bar

                # build message
                vi = jobs[job_id].get("video_index")
                vt = jobs[job_id].get("video_total")
                pct_now = jobs[job_id]["percent"]
                if vi and vt:
                    jobs[job_id]["message"] = f"Video {vi}/{vt} — {pct_now:.1f}%"
                elif pct_now > 0:
                    jobs[job_id]["message"] = f"Downloading: {pct_now:.1f}%"

            proc.wait()

            if jobs[job_id]["status"] == "cancelled":
                pass  # already set
            elif proc.returncode == 0:
                jobs[job_id]["status"]  = "done"
                jobs[job_id]["percent"] = 100
                jobs[job_id]["message"] = "✅ Download complete! Check the downloads folder."
            else:
                jobs[job_id]["status"]  = "error"
                jobs[job_id]["message"] = "❌ yt-dlp exited with errors. See log below."

        except FileNotFoundError:
            jobs[job_id]["status"]  = "error"
            jobs[job_id]["message"] = "❌ yt-dlp not found. Run: pip install yt-dlp"
        except Exception as e:
            if jobs[job_id]["status"] != "cancelled":
                jobs[job_id]["status"]  = "error"
                jobs[job_id]["message"] = f"❌ Error: {str(e)}"
        finally:
            jobs[job_id].pop("proc", None)


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
                extra = f.read().decode("utf-8").splitlines()
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
            cleanup_old_cookies()

    # update thread limit if provided
    thread_limit = data.get("thread_limit", "").strip()
    if thread_limit:
        try:
            set_thread_limit(int(thread_limit))
        except ValueError:
            pass

    opts = {
        "format":       data.get("format", "mp3"),
        "resolution":   data.get("resolution", "best"),
        "quality":      data.get("quality", "0"),
        "subtitles":    data.get("subtitles") == "true",
        "sponsorblock": data.get("sponsorblock") == "true",
        "rate_limit":   data.get("rate_limit", ""),
        "cookie_file":  cookie_path,
    }

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status":       "queued",
        "message":      "Queued…",
        "percent":      0,
        "video_index":  None,
        "video_total":  None,
        "log":          [],
        "urls":         url_list,
    }

    t = threading.Thread(target=run_job, args=(job_id, url_list, opts))
    t.daemon = True
    t.start()

    return jsonify({"job_id": job_id})


@app.route("/cancel/<job_id>", methods=["POST"])
def cancel(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    job["status"]  = "cancelled"
    job["message"] = "🚫 Download cancelled."

    proc = job.get("proc")
    if proc:
        try:
            proc.terminate()
        except Exception:
            pass

    return jsonify({"ok": True})


@app.route("/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({
        "status":      job["status"],
        "message":     job["message"],
        "percent":     job["percent"],
        "video_index": job.get("video_index"),
        "video_total": job.get("video_total"),
        "log":         job["log"][-50:],
        "log_total":   len(job["log"]),
    })


@app.route("/downloads")
def list_downloads():
    sort_by = request.args.get("sort", "date")   # date | name | size
    files = []
    try:
        for fn in os.listdir(DL_DIR):
            fp = os.path.join(DL_DIR, fn)
            if os.path.isfile(fp):
                files.append({
                    "name":  fn,
                    "size":  round(os.path.getsize(fp) / (1024 * 1024), 2),
                    "mtime": os.path.getmtime(fp),
                })
        if sort_by == "name":
            files.sort(key=lambda x: x["name"].lower())
        elif sort_by == "size":
            files.sort(key=lambda x: x["size"], reverse=True)
        else:  # date (default)
            files.sort(key=lambda x: x["mtime"], reverse=True)
    except Exception:
        pass
    return jsonify(files)


@app.route("/downloads/<path:filename>", methods=["GET", "DELETE"])
def serve_file(filename):
    fp = os.path.join(DL_DIR, filename)
    if request.method == "DELETE":
        try:
            os.remove(fp)
            return jsonify({"ok": True})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return send_from_directory(DL_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    print("=" * 50)
    print("🎬 yt-dlp Web UI Starting…")
    print("📍 URL  : http://localhost:5000")
    print(f"📁 Save : {DL_DIR}")
    print("=" * 50)
    app.run(debug=False, port=5000)
