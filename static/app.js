/* ── Type toggle (Audio / Video) ───────────────────────────── */
const typeToggles = document.querySelectorAll('.tog');
const formatSelect = document.getElementById('format-select');
const aqWrap  = document.getElementById('aq-wrap');
const resWrap = document.getElementById('res-wrap');

const AUDIO_FORMATS = ['mp3','aac','flac','m4a','opus','wav','alac'];
const VIDEO_FORMATS = ['mp4','mkv','webm','avi','mov'];

function setType(type) {
  typeToggles.forEach(b => b.classList.toggle('active', b.dataset.val === type));
  formatSelect.innerHTML = '';
  const opts = type === 'audio' ? AUDIO_FORMATS : VIDEO_FORMATS;
  opts.forEach(f => {
    const o = document.createElement('option');
    o.value = f; o.textContent = f.toUpperCase();
    formatSelect.appendChild(o);
  });
  aqWrap.classList.toggle('hidden',  type === 'video');
  resWrap.classList.toggle('hidden', type === 'audio');
}

typeToggles.forEach(b => b.addEventListener('click', () => setType(b.dataset.val)));
setType('audio');

/* ── Subtitle checkbox ──────────────────────────────────────── */
const subCheck  = document.getElementById('sub-check');
const subHidden = document.getElementById('sub-hidden');
subCheck.addEventListener('change', () => {
  subHidden.value = subCheck.checked ? 'true' : 'false';
});

/* ── File drop zones ────────────────────────────────────────── */
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

/* ── Form submit ────────────────────────────────────────────── */
const form      = document.getElementById('dl-form');
const formCard  = document.getElementById('form-card');
const progCard  = document.getElementById('progress-card');
const progBar   = document.getElementById('progress-bar');
const progMsg   = document.getElementById('progress-msg');
const logBox    = document.getElementById('log-box');
const submitBtn = document.getElementById('submit-btn');
const newDlBtn  = document.getElementById('new-dl-btn');

let pollTimer   = null;

form.addEventListener('submit', async e => {
  e.preventDefault();
  submitBtn.disabled = true;
  submitBtn.textContent = 'Starting…';

  const fd = new FormData(form);

  try {
    const res  = await fetch('/download', { method: 'POST', body: fd });
    const data = await res.json();

    if (data.error) {
      alert('Error: ' + data.error);
      submitBtn.disabled = false;
      submitBtn.textContent = 'Download';
      return;
    }

    formCard.classList.add('hidden');
    progCard.classList.remove('hidden');
    logBox.innerHTML = '';
    progBar.style.width = '0%';
    progBar.style.background = '';
    progMsg.textContent = 'Queued…';

    startPolling(data.job_id);
  } catch (err) {
    alert('Network error: ' + err.message);
    submitBtn.disabled = false;
    submitBtn.textContent = 'Download';
  }
});

function startPolling(jobId) {
  if (pollTimer) clearInterval(pollTimer);
  // FIX #5: track by log_total (absolute count), not local slice length
  let knownLogTotal = 0;
  pollTimer = setInterval(() => pollStatus(jobId, (newTotal) => {
    knownLogTotal = newTotal;
  }, () => knownLogTotal), 800);
}

async function pollStatus(jobId, setTotal, getTotal) {
  try {
    const res  = await fetch('/status/' + jobId);
    const data = await res.json();

    progBar.style.width = (data.percent || 0) + '%';
    if (data.percent >= 100) progBar.style.background = 'var(--green)';

    if (data.message) progMsg.textContent = data.message;

    // FIX #5: use log_total to figure out which lines are new
    const serverTotal = data.log_total || 0;
    const lines       = data.log || [];
    const knownTotal  = getTotal();

    if (serverTotal > knownTotal) {
      // lines[] contains the last 50 lines from server; figure out which are new
      const alreadySeen = Math.max(0, knownTotal - (serverTotal - lines.length));
      const newLines    = lines.slice(alreadySeen);

      newLines.forEach(line => {
        const div = document.createElement('div');
        div.textContent = line;
        if (line.includes('[download]'))                              div.className = 'log-line-dl';
        if (line.includes('[ExtractAudio]') || line.includes('Merging')) div.className = 'log-line-done';
        if (line.includes('ERROR'))                                   div.className = 'log-line-error';
        logBox.appendChild(div);
      });
      setTotal(serverTotal);
      logBox.scrollTop = logBox.scrollHeight;
    }

    if (data.status === 'done' || data.status === 'error') {
      clearInterval(pollTimer);
      if (data.status === 'done') loadFiles();
    }
  } catch (err) {
    console.error('Poll error', err);
  }
}

/* ── New download button ────────────────────────────────────── */
newDlBtn.addEventListener('click', () => {
  progCard.classList.add('hidden');
  formCard.classList.remove('hidden');
  submitBtn.disabled = false;
  submitBtn.textContent = 'Download';
  form.reset();
  setType('audio');

  document.getElementById('batch-label').textContent  = 'Drop .txt file or click to browse';
  document.getElementById('cookie-label').textContent = 'Drop cookies.txt or click to browse';
  document.getElementById('batch-drop').classList.remove('has-file');
  document.getElementById('cookie-drop').classList.remove('has-file');
});

/* ── Files list ─────────────────────────────────────────────── */
const fileList   = document.getElementById('file-list');
const refreshBtn = document.getElementById('refresh-btn');

async function loadFiles() {
  try {
    const res   = await fetch('/downloads');
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
        <span class="file-name" title="${escapeHtml(f.name)}">${escapeHtml(f.name)}</span>
        <span class="file-meta">
          <span class="file-size">${f.size} MB</span>
          <a class="file-dl" href="/downloads/${encodeURIComponent(f.name)}" download>↓ Save</a>
        </span>`;
      fileList.appendChild(li);
    });
  } catch (err) {
    console.error('loadFiles error', err);
  }
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

refreshBtn.addEventListener('click', loadFiles);
loadFiles();
