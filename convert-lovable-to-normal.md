Here's a generic blueprint that applies to any complex Lovable project (not just AceJamb). It focuses on removing server‑side dependencies, converting to a client‑side Vite + React SPA, and making it Termux‑compatible.

---

🧭 Universal Blueprint: Convert Any Lovable Project to Termux-Compatible Vite SPA

This guide works for most apps exported from Lovable that use TanStack Start (or similar full‑stack frameworks). The goal is to strip the server layer, keep all UI components, and produce a static React app that runs in Termux.

🔍 What makes Lovable projects break in Termux

· Full‑stack framework (TanStack Start, Next.js, Remix) – requires Node.js server or Cloudflare Workers.
· Native dependencies (sharp, lightningcss, workerd) – fail to compile on Android/ARM.
· SSR / server‑entry points – not needed for a client‑only app.
· Service Worker / PWA – may cause registration errors but can be kept or ignored.

✅ Generic conversion steps

Phase 1: Remove server‑side packages

1. Open package.json.
2. Delete dependencies like:
   · @tanstack/react-start, @tanstack/router-plugin
   · @cloudflare/vite-plugin, wrangler
   · @tailwindcss/vite (or downgrade to v3)
   · @lovable.dev/vite-tanstack-config
3. Add the client router:
   ```bash
   npm install react-router-dom
   ```

Phase 2: Replace routing

1. Delete framework‑specific router files:
   · src/routeTree.gen.ts, src/router.tsx, src/routes/__root.tsx (TanStack)
   · or pages/, app/ folder for Next.js
2. Convert each route file to a plain React component:
   · Remove createFileRoute (TanStack) or export default function Page() (Next.js).
   · Replace import { Link, useNavigate } from "@tanstack/react-router" with import { Link, useNavigate } from "react-router-dom".
   · Keep all other logic (state, effects, API calls) unchanged.
3. Create src/App.tsx with BrowserRouter, Routes, and your providers:
   ```tsx
   import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
   import Home from './routes/home';
   import About from './routes/about';
   // ... other routes
   
   export default function App() {
     return (
       <BrowserRouter>
         <Routes>
           <Route path="/" element={<Home />} />
           <Route path="/about" element={<About />} />
           {/* add all your routes */}
           <Route path="*" element={<Navigate to="/" replace />} />
         </Routes>
       </BrowserRouter>
     );
   }
   ```

Phase 3: Fix entry point

Create src/main.tsx (if missing):

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

Phase 4: Fix CSS (Tailwind v4 → v3)

If the project uses Tailwind CSS v4 (@tailwindcss/vite), downgrade to v3:

```bash
npm uninstall @tailwindcss/vite tailwindcss
npm install tailwindcss@^3 postcss autoprefixer
```

Create postcss.config.js:

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

Create tailwind.config.js (adjust content paths):

```js
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: { extend: {} },
  plugins: [],
};
```

Update src/styles.css:

· Remove @import "tailwindcss" and @source.
· Add @tailwind base; @tailwind components; @tailwind utilities;
· Keep all your custom CSS.

Phase 5: Update vite.config.ts

Remove any Cloudflare or Tailwind v4 plugins. Use only:

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  server: { host: '0.0.0.0', port: 5173 },
});
```

Phase 6: Delete server‑side files

Remove:

· src/server.ts, src/start.ts
· src/lib/error-capture.ts, src/lib/error-page.ts
· Any *.server.ts or *.server.js files
· wrangler.jsonc (if present)

Phase 7: Fix initial route flash (hydration)

In many apps, data is loaded asynchronously from localStorage or an API. To avoid showing the wrong page on first load:

· In your main data provider, add a hydrated boolean that becomes true after initial data is loaded.
· In App.tsx (or the root component), render a loading screen until hydrated is true.

Generic pattern:

```tsx
// In your data context/provider
const [hydrated, setHydrated] = useState(false);
useEffect(() => {
  loadData().then(() => setHydrated(true));
}, []);

// In App.tsx
if (!hydrated) return <div>Loading...</div>;
// then render routes
```

Phase 8: Update index.html

Ensure it has:

```html
<div id="root"></div>
<script type="module" src="/src/main.tsx"></script>
```

Add any Google Fonts or other <link> tags as needed.

Phase 9: Handle service workers (optional)

If you have public/sw.js and a manifest, the registration may fail in Termux. You can conditionally register only when not in Termux:

```ts
if ('serviceWorker' in navigator && !navigator.userAgent.includes('Android')) {
  navigator.serviceWorker.register('/sw.js');
}
```

Or simply delete sw.js and the manifest – the app will still work.

Phase 10: Build and run in Termux

```bash
npm install
npm run dev
```

Visit http://localhost:5173 in Termux’s browser (or use npm run build and serve the dist/ folder statically).

---

🧪 Common fixes for Termux environment

Issue Solution
lightningcss binary missing Downgrade Tailwind to v3 (pure JS)
sharp compilation error Remove @cloudflare/vite-plugin
ECONNABORTED during install npm config set registry https://registry.npmmirror.com
Port already in use Change port in vite.config.ts (port: 5174)
Blank page with no errors Check browser console – likely missing #root div or CSS import path

---

📌 Key principle

The UI code is fully reusable – only the server layer and native modules are incompatible.

By converting to a Vite SPA, you keep all React components, state logic, styling, and third‑party libraries (like charts, markdown, animations) exactly as they were. The only thing you lose is server‑side rendering and Cloudflare integration – neither of which is needed for a local, static frontend.

This blueprint works for any Lovable project based on React + TanStack Start. For Next.js projects, the steps are similar: remove next, replace with Vite + React Router, and copy over the page components. The same principle applies.

---

✅ Final checklist (generic)

· package.json cleaned of server‑side frameworks and Cloudflare packages.
· Tailwind CSS downgraded to v3 (if v4 was used).
· postcss.config.js and tailwind.config.js created.
· Routing replaced with react-router-dom.
· All route files converted to plain React components.
· src/App.tsx and src/main.tsx created.
· vite.config.ts simplified to react() + tsconfigPaths().
· Server‑entry files deleted.
· index.html includes <div id="root">.
· App loads correctly in Termux after npm run dev.

---

This blueprint is independent of your specific app’s features (e.g., no mention of UserProfile, onboarding, etc.). It gives you a repeatable process for any Lovable export.
