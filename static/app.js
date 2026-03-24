/* ══════════════════════════════════════════════
   yt-dlp Web UI — app.js
   ══════════════════════════════════════════════ */

/* ── Theme toggle ───────────────────────────── */
const html       = document.documentElement;
const themeBtn   = document.getElementById('theme-toggle');
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);
themeBtn.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

themeBtn.addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  themeBtn.textContent = next === 'dark' ? '☀️' : '🌙';
});

/* ── Toast system ───────────────────────────── */
const toastContainer = document.getElementById('toast-container');

function showToast(msg, type = 'success', duration = 3500) {
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : '🚫';
  t.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
  toastContainer.appendChild(t);
  setTimeout(() => {
    t.style.animation = 'toast-out .3s ease forwards';
    setTimeout(() => t.remove(), 300);
  }, duration);
}

/* ── Type toggle (Audio / Video) ────────────── */
const typeToggles  = document.querySelectorAll('.tog');
const formatSelect = document.getElementById('format-select');
const aqWrap       = document.getElementById('aq-wrap');
const resWrap      = document.getElementById('res-wrap');

const AUDIO_FORMATS = ['mp3','aac','flac','m4a','opus','wav','alac'];
const VIDEO_FORMATS = ['mp4','mkv','webm','avi','mov'];

function setType(type) {
  typeToggles.forEach(b => b.classList.toggle('active', b.dataset.val === type));
  formatSelect.innerHTML = '';
  (type === 'audio' ? AUDIO_FORMATS : VIDEO_FORMATS).forEach(f => {
    const o = document.createElement('option');
    o.value = f; o.textContent = f.toUpperCase();
    formatSelect.appendChild(o);
  });
  aqWrap.classList.toggle('hidden',  type === 'video');
  resWrap.classList.toggle('hidden', type === 'audio');
}
typeToggles.forEach(b => b.addEventListener('click', () => setType(b.dataset.val)));
setType('audio');

/* ── Hidden checkboxes ──────────────────────── */
function bindCheckHidden(checkId, hiddenId) {
  const chk = document.getElementById(checkId);
  const hid = document.getElementById(hiddenId);
  chk.addEventListener('change', () => { hid.value = chk.checked ? 'true' : 'false'; });
}
bindCheckHidden('sub-check', 'sub-hidden');
bindCheckHidden('sponsorblock-check', 'sponsorblock-hidden');

/* ── File drop zones ────────────────────────── */
function setupFileDrop(dropId, inputId, labelId) {
  const input = document.getElementById(inputId);
  const label = document.getElementById(labelId);
  const drop  = document.getElementById(dropId);
  input.addEventListener('change', () => {
    if (input.files.length > 0) {
      label.textContent = '✅ ' + input.files[0].name;
      drop.classList.add('has-file');
    }
  });
}
setupFileDrop('batch-drop',  'batch_file',  'batch-label');
setupFileDrop('cookie-drop', 'cookie_file', 'cookie-label');

/* ── Form submit ────────────────────────────── */
const form      = document.getElementById('dl-form');
const formCard  = document.getElementById('form-card');
const progCard  = document.getElementById('progress-card');
const progBar   = document.getElementById('progress-bar');
const progMsg   = document.getElementById('progress-msg');
const logBox    = document.getElementById('log-box');
const submitBtn = document.getElementById('submit-btn');
const newDlBtn  = document.getElementById('new-dl-btn');
const cancelBtn = document.getElementById('cancel-btn');

const batchWrap       = document.getElementById('batch-progress-wrap');
const batchLabel      = document.getElementById('batch-progress-label');
const batchOverallBar = document.getElementById('batch-overall-bar');
const batchOverallPct = document.getElementById('batch-overall-pct');

let pollTimer   = null;
let currentJob  = null;

form.addEventListener('submit', async e => {
  e.preventDefault();
  submitBtn.disabled = true;
  submitBtn.textContent = 'Starting…';

  const fd = new FormData(form);

  try {
    const res  = await fetch('/download', { method: 'POST', body: fd });
    const data = await res.json();

    if (data.error) {
      showToast(data.error, 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Download';
      return;
    }

    currentJob = data.job_id;
    formCard.classList.add('hidden');
    progCard.classList.remove('hidden');
    batchWrap.classList.add('hidden');
    logBox.innerHTML = '';
    progBar.style.width = '0%';
    progBar.style.background = '';
    progMsg.textContent = 'Queued…';
    cancelBtn.disabled = false;

    startPolling(data.job_id);
  } catch (err) {
    showToast('Network error: ' + err.message, 'error');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Download';
  }
});

/* ── Cancel ─────────────────────────────────── */
cancelBtn.addEventListener('click', async () => {
  if (!currentJob) return;
  cancelBtn.disabled = true;
  try {
    await fetch('/cancel/' + currentJob, { method: 'POST' });
    showToast('Download cancelled.', 'cancel');
  } catch (err) {
    showToast('Could not cancel.', 'error');
  }
});

/* ── Polling ────────────────────────────────── */
function startPolling(jobId) {
  if (pollTimer) clearInterval(pollTimer);
  let knownLogTotal = 0;
  pollTimer = setInterval(async () => {
    try {
      const res  = await fetch('/status/' + jobId);
      const data = await res.json();

      // per-file progress bar
      progBar.style.width = (data.percent || 0) + '%';
      if (data.percent >= 100) progBar.style.background = 'var(--green)';

      if (data.message) progMsg.textContent = data.message;

      // batch overall bar
      if (data.video_index && data.video_total) {
        batchWrap.classList.remove('hidden');
        const overallPct = Math.round(((data.video_index - 1) / data.video_total) * 100);
        batchOverallBar.style.width = overallPct + '%';
        batchOverallPct.textContent  = overallPct + '%';
        batchLabel.textContent = `Video ${data.video_index} / ${data.video_total}`;
      }

      // log — use log_total to avoid de-sync
      const serverTotal = data.log_total || 0;
      const lines       = data.log || [];
      if (serverTotal > knownLogTotal) {
        const alreadySeen = Math.max(0, knownLogTotal - (serverTotal - lines.length));
        lines.slice(alreadySeen).forEach(line => {
          const div = document.createElement('div');
          div.textContent = line;
          if (line.includes('[download]'))                               div.className = 'log-line-dl';
          if (line.includes('[ExtractAudio]') || line.includes('Merging')) div.className = 'log-line-done';
          if (line.includes('ERROR'))                                    div.className = 'log-line-error';
          logBox.appendChild(div);
        });
        knownLogTotal = serverTotal;
        logBox.scrollTop = logBox.scrollHeight;
      }

      if (data.status === 'done') {
        clearInterval(pollTimer);
        showToast('Download complete! 🎉');
        loadFiles();
      } else if (data.status === 'error') {
        clearInterval(pollTimer);
        showToast('Download failed. Check the log.', 'error');
      } else if (data.status === 'cancelled') {
        clearInterval(pollTimer);
      }

    } catch (err) { console.error('Poll error', err); }
  }, 800);
}

/* ── New download ───────────────────────────── */
newDlBtn.addEventListener('click', () => {
  progCard.classList.add('hidden');
  formCard.classList.remove('hidden');
  submitBtn.disabled = false;
  submitBtn.textContent = 'Download';
  form.reset();
  setType('audio');
  currentJob = null;

  document.getElementById('batch-label').textContent  = 'Drop .txt file or click to browse';
  document.getElementById('cookie-label').textContent = 'Drop cookies.txt or click to browse';
  document.getElementById('batch-drop').classList.remove('has-file');
  document.getElementById('cookie-drop').classList.remove('has-file');
});

/* ── File type icon ─────────────────────────── */
function fileIcon(name) {
  const ext = name.split('.').pop().toLowerCase();
  const audio = ['mp3','aac','flac','m4a','opus','wav','alac','ogg'];
  const video = ['mp4','mkv','webm','avi','mov','flv'];
  if (audio.includes(ext)) return '🎵';
  if (video.includes(ext)) return '🎬';
  return '📄';
}

/* ── Files list ─────────────────────────────── */
const fileList   = document.getElementById('file-list');
const refreshBtn = document.getElementById('refresh-btn');
const sortSelect = document.getElementById('sort-select');

async function loadFiles() {
  const sort = sortSelect.value;
  try {
    const res   = await fetch('/downloads?sort=' + sort);
    const files = await res.json();
    fileList.innerHTML = '';
    if (!files.length) {
      fileList.innerHTML = '<li class="empty">No files yet.</li>';
      return;
    }
    files.forEach(f => {
      const li = document.createElement('li');
      li.className = 'file-item';
      li.innerHTML = `
        <div class="file-left">
          <span class="file-icon">${fileIcon(f.name)}</span>
          <span class="file-name" title="${escapeHtml(f.name)}">${escapeHtml(f.name)}</span>
        </div>
        <span class="file-meta">
          <span class="file-size">${f.size} MB</span>
          <a class="file-dl" href="/downloads/${encodeURIComponent(f.name)}" download>↓ Save</a>
          <button class="file-del" data-name="${escapeHtml(f.name)}">✕</button>
        </span>`;
      // delete handler
      li.querySelector('.file-del').addEventListener('click', async () => {
        if (!confirm(`Delete "${f.name}"?`)) return;
        try {
          await fetch('/downloads/' + encodeURIComponent(f.name), { method: 'DELETE' });
          showToast(`Deleted: ${f.name}`);
          loadFiles();
        } catch (err) {
          showToast('Delete failed.', 'error');
        }
      });
      fileList.appendChild(li);
    });
  } catch (err) { console.error('loadFiles error', err); }
}

function escapeHtml(text) {
  const d = document.createElement('div');
  d.textContent = text;
  return d.innerHTML;
}

sortSelect.addEventListener('change', loadFiles);
refreshBtn.addEventListener('click', loadFiles);
loadFiles();
