# Premium VRM Viewer

A lightweight, high-performance VRM model viewer built with Three.js and `@pixiv/three-vrm`.

## Features
- **Upload & Display**: Drag and drop or upload any `.vrm` file.
- **Interactive Camera**: Orbit, zoom, and pan with mouse/touch.
- **Procedural Animation**: Automatic idle sway and eye blinking.
- **Visual Controls**: Toggle wireframe mode and customize background color.
- **Premium Design**: Modern UI with glassmorphism and responsive layout.

---

## 🚀 Quick Start (CDN Version)

This version requires no installation or build tools.

1.  **Open `index.html`** in your browser.
2.  **Upload a VRM model**: Click the "Upload VRM Model" button or use the file input.
3.  **Interact**: Use your mouse to explore the model.

> [!NOTE]
> For the best experience, run this through a local server (e.g., VS Code Live Server) to avoid potential CORS issues with some browsers, although the direct file upload approach usually works fine locally.

---

## 🛠️ Node.js / Vite Version (Optional)

If you want to build a more complex application, use Vite for a modern development experience.

### 1. Setup Project
```bash
# Create a new Vite project
npm create vite@latest vrm-viewer -- --template vanilla
cd vrm-viewer

# Install dependencies
npm install three @pixiv/three-vrm
```

### 2. Implementation (`main.js`)
Replace the contents of `main.js` with the script logic found in the CDN `index.html`. You will need to change the imports to point to node_modules:

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { VRMLoaderPlugin } from '@pixiv/three-vrm';

// ... (Rest of the logic from index.html)
```

### 3. Run Development Server
```bash
npm run dev
```

---

## 📂 Folder Structure
```text
FINAL/
├── index.html        # Main application (CDN version)
├── README.md         # Documentation
└── [your-model].vrm  # Your VRM models
```
