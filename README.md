# Elite: Lighthouse (v2.0)

Lighthouse is a sleek, minimalist, and immersive overlay HUD for Elite Dangerous. 

While tools like Exploration Buddy are fantastic and popular for providing comprehensive, full-blown toolkits with every piece of data imaginable, **Lighthouse is built with a different philosophy**. We wanted a HUD that feels like a natural extension of your ship's dashboard. It doesn't overwhelm you with spreadsheets of data; it gives you exactly what you need, right when you need it, and completely gets out of your way.

Designed with a premium glassmorphic aesthetic, it sits seamlessly over your game without breaking immersion.

[Screenshot of Lighthouse overlay here]

## Features

### 🌌 Neutron Route Planner
Seamlessly integrated with the Spansh API to provide instant, in-game neutron routing.
- Automatically copies the next waypoint to your clipboard as soon as you jump.
- Real-time High Value Target (HVT) alerts when entering a system with valuable scans.
- **Smart Tracking**: If you venture off-route, Lighthouse knows. When you re-enter the route later, it instantly picks up where you left off and copies the next destination.
- **Minimize to Status Bar**: Collapse the router into a tiny, unobtrusive status bar that just tells you your next jump and gets out of your view.

[Screenshot of Neutron Router here]

### 🧬 Exo Tracker
A zero-click exobiology companion. No more tabbing out to check what's on the planet you just probed.
- Automatically hydrates your exobiology state from your ship's logs.
- Scan a planet from orbit with your DSS, and Lighthouse instantly displays all biological signals and their scan progress.
- Tracks your samples: 1/3, 2/3, or fully analyzed.
- **Smart Wiping**: Automatically clears your biological tracking data the moment you leave the planet's orbit or jump to another system.

[Screenshot of Exo Tracker here]

### 🚢 POI & Fleet Carrier Radar
Quickly find the nearest services when you're out in the black.
- Search for nearby Drake-Class Fleet Carriers based on your real-time location.
- **Active Services Filter**: Don't waste time docking at a carrier that doesn't have what you need. Lighthouse parses and highlights the crucial active services of nearby carriers (like Vista Genomics, Universal Cartographics, Refuel/Repair, and Shipyards).

[Screenshot of POI Search here]

## Installation & Setup

1. **Prerequisites**: Ensure you have [Node.js](https://nodejs.org/) installed.
2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd commander-hud
   ```
3. **Install Dependencies**:
   ```bash
   npm install
   ```
4. **Run Lighthouse**:
   ```bash
   npm run dev
   ```

*Note: Make sure you run Elite Dangerous in **Borderless Windowed** or **Windowed** mode for the overlay to sit on top of the game!*

## Tech Stack
- **Electron** (for transparent, click-through overlay capabilities and local journal reading)
- **React 19 & Vite** (for ultra-fast rendering and modern UI state)
- **Spansh & EDSM APIs** (for routing and system mapping)

## Philosophy
Lighthouse is not meant to replace your massive third-party tools if you want to see every asteroid in the galaxy. It's meant to make your standard exploration loop (jumping, scanning, landing) feel completely integrated into the cockpit experience. Keep your eyes on the stars, Commander. o7
