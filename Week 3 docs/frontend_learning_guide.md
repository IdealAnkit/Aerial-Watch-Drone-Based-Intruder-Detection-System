# Frontend Learning Guide - Web Interface Code

This guide explains the frontend code (HTML, CSS, JavaScript) that creates the Aerial Watch web interface.

## Architecture Overview

```
┌─────────────┐      HTTP/JSON      ┌─────────────┐
│   Browser   │ ←─────────────────→ │   Flask     │
│  (Frontend) │                     │  (Backend)  │
│             │      MJPEG          │             │
│  HTML/CSS/JS│ ←─────────────────→ │  Python     │
└─────────────┘                     └─────────────┘
```

---

## Part 1: HTML Structure (index.html)

### Main Container
```html
<div class="container">
    <header>
        <h1>🛡️ Aerial Watch</h1>
        <p class="subtitle">Drone-Based Intruder Detection System</p>
    </header>
```

**Purpose**: Organizes the entire page layout.

### Video Feed Section
```html
<div class="video-container">
    <img id="videoFeed" alt="Video Feed" style="display: none;">
    <div class="placeholder" id="placeholder">
        <p>Select source and click Start to begin monitoring</p>
    </div>
</div>
```

**Key Concept**: 
- Initially, `videoFeed` has **no `src` attribute** and is hidden
- JavaScript sets the `src` dynamically when user clicks Start
- This prevents loading the stream before it's needed

### Control Panel
```html
<select id="sourceSelect">
    <option value="camera">Live Camera</option>
    <option value="video">Video File</option>
</select>

<button id="startBtn" class="btn btn-start">Start Monitoring</button>
<button id="stopBtn" class="btn btn-stop">Stop</button>
```

**Form Elements**:
- `<select>`: Dropdown for source selection
- `<button>`: Triggers actions via JavaScript event listeners

### Snapshot Gallery
```html
<div class="gallery" id="snapshotGallery">
    {% for snapshot in snapshots %}
    <div class="gallery-item">
        <img src="{{ url_for('serve_snapshot', filename=snapshot) }}">
        <p class="timestamp">{{ ... }}</p>
    </div>
    {% endfor %}
</div>
```

**Template Syntax**: `{{ }}` is **Jinja2** (Flask's template engine)
- Server-side: Runs before HTML is sent to browser
- Generates initial HTML with existing snapshots

---

## Part 2: CSS Styling (style.css)

### CSS Grid Layout
```css
.main-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
}
```

**Modern Layout**: 
- Video section takes 2/3 width
- Control panel takes 1/3 width
- Automatically responsive

### Gradient Background
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**Visual Design**: Creates professional purple gradient backdrop

### Button States
```css
.btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
```

**Interactive Feedback**:
- Lift effect on hover
- Grayed out when disabled
- Cursor changes to show state

### Animations
```css
@keyframes pulse-alert {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.2); }
}

.status-indicator.alert .dot {
    background: #dc3545;
    animation: pulse-alert 0.5s infinite;
}
```

**Real-time Feedback**: Red dot pulses when intruder detected

---

## Part 3: JavaScript Functionality

### 1. DOM Element References
```javascript
const sourceSelect = document.getElementById('sourceSelect');
const startBtn = document.getElementById('startBtn');
const videoFeed = document.getElementById('videoFeed');
```

**DOM API**: `getElementById()` gets reference to HTML elements for manipulation

### 2. Event Listeners

#### Dynamic UI Based on Selection
```javascript
sourceSelect.addEventListener('change', function() {
    if (this.value === 'video') {
        videoFileGroup.style.display = 'block';
    } else {
        videoFileGroup.style.display = 'none';
    }
});
```

**Conditional Display**: Shows/hides video file selector based on dropdown choice

### 3. Fetch API - Starting Monitoring

```javascript
startBtn.addEventListener('click', async function() {
    const response = await fetch('/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({source: source, video_path: videoPath})
    });

    if (response.ok) {
        // Set video source with cache buster
        videoFeed.src = '/video_feed?t=' + new Date().getTime();
        videoFeed.style.display = 'block';
        placeholder.style.display = 'none';
    }
});
```

**Key Concepts**:

**async/await**: Modern way to handle asynchronous operations
- `async function`: Allows use of `await` inside
- `await fetch()`: Waits for HTTP request to complete

**fetch()**: Modern replacement for XMLHttpRequest
- Returns a Promise
- `method: 'POST'`: Sends data to server
- `headers`: Tells server we're sending JSON
- `JSON.stringify()`: Converts JavaScript object to JSON string

**Cache Busting**: `?t=` + timestamp
- Prevents browser from reusing old cached stream
- Forces fresh connection

### 4. Polling for Real-time Updates

```javascript
function checkStatus() {
    statusInterval = setInterval(async () => {
        const response = await fetch('/status');
        const data = await response.json();
        
        if (data.is_running) {
            if (data.detection_status === 'INTRUDER DETECTED') {
                statusIndicator.classList.add('alert');
                statusText.textContent = '⚠️ INTRUDER DETECTED';
            } else {
                statusIndicator.classList.remove('alert');
                statusText.textContent = '✓ Monitoring Active';
            }
        }
    }, 1000);
}
```

**Polling Pattern**:
- `setInterval()`: Runs function every N milliseconds (1000ms = 1 second)
- Continuously checks server status
- Updates UI based on response

**Why Polling?**: Simple alternative to WebSockets for real-time updates

### 5. Dynamic Gallery Updates

```javascript
async function updateGallery() {
    const response = await fetch('/snapshots');
    const data = await response.json();
    const gallery = document.getElementById('snapshotGallery');
    
    if (data.snapshots && data.snapshots.length > 0) {
        gallery.innerHTML = data.snapshots.map(snapshot => `
            <div class="gallery-item">
                <img src="/snapshot/${snapshot}">
                <p class="timestamp">${snapshot.replace('intruder_', '').replace('.jpg', '').replace(/_/g, ' ')}</p>
            </div>
        `).join('');
    }
}
```

**Advanced JavaScript**:

**Template Literals**: Backticks `` ` `` allow multi-line strings and `${variables}`

**Array.map()**: Transforms array of filenames into array of HTML strings
- `snapshot => ...`: Arrow function (ES6)
- Returns HTML for each snapshot

**.join('')**: Combines array of strings into single string

**.replace()**: String manipulation to format timestamps
- `/g` flag: Global replace (all occurrences)

**innerHTML**: Replaces entire gallery content with new HTML

---

## Part 4: Frontend-Backend Communication

### Request Flow

```
User Click Start
     ↓
JavaScript: fetch('/start', {POST data})
     ↓
Flask: @app.route('/start') receives request
     ↓
Flask: Starts camera, sets is_running = True
     ↓
Flask: Returns JSON: {'status': 'started'}
     ↓
JavaScript: response.ok → Update UI
     ↓
JavaScript: Sets videoFeed.src = '/video_feed'
     ↓
Browser: Requests /video_feed
     ↓
Flask: generate_frames() streams MJPEG
     ↓
Browser: Displays video
```

### Data Formats

**JSON Request**:
```json
{
  "source": "camera",
  "video_path": null
}
```

**JSON Response**:
```json
{
  "status": "started",
  "source": "camera"
}
```

---

## Part 5: Advanced Concepts

### MJPEG Streaming
```html
<img src="/video_feed">
```

**How it works**:
1. Browser makes GET request to `/video_feed`
2. Server sends `Content-Type: multipart/x-mixed-replace`
3. Server sends JPEG frames continuously
4. Browser automatically displays each frame
5. Connection stays open indefinitely

### Error Handling
```javascript
if (response.ok) {
    // Success path
} else {
    // Error path
}
```

**response.ok**: True if HTTP status is 200-299

### Memory Management
```javascript
clearInterval(statusInterval);
```

**Why needed**: Prevents memory leaks by stopping polling when not needed

---

## Summary: Key Web Technologies Used

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure and semantic markup |
| **CSS3** | Styling, animations, responsive layout |
| **JavaScript (ES6)** | Interactivity and logic |
| **Fetch API** | HTTP requests to backend |
| **Promises/async-await** | Asynchronous operations |
| **DOM API** | Manipulating page elements |
| **Jinja2** | Server-side templating |
| **JSON** | Data exchange format |
| **MJPEG** | Video streaming protocol |

---

## Best Practices Demonstrated

✅ **Separation of Concerns**: HTML (structure), CSS (style), JS (behavior)  
✅ **Event-Driven Programming**: User actions trigger functions  
✅ **Asynchronous Operations**: Non-blocking HTTP requests  
✅ **Dynamic Content**: Updates without page refresh  
✅ **Cache Control**: Prevents stale data  
✅ **Error Prevention**: Disabled buttons prevent invalid states  
✅ **Clean Code**: Readable variable names, comments where needed
