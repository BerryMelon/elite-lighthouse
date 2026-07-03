# Elite Lighthouse

**Elite Lighthouse** is a lightweight, frameless HUD overlay for Elite Dangerous explorers. Designed to automate and streamline the grueling process of long-range neutron star routing, Lighthouse integrates seamlessly with the Spansh API and your ship's telemetry.

![Expanded Mode](screenshots/expanded.png)

## Features

- **Spansh API Integration**: Automatically calculates long-range neutron highways to your destination, perfectly optimized for your ship's jump range.
- **Supercruise Overcharge (SCO) Support**: Fully supports the new SCO FSDs (`supercharge_multiplier = 6x`), ensuring you squeeze every lightyear out of those massive overcharged jumps.
- **Auto-Copy Next System**: Sniffs your Elite Dangerous player journal in real-time. The exact second you drop into a new star system, Lighthouse ticks off your waypoint and **automatically copies the next system name to your clipboard**. Just open your galaxy map and paste!
- **Off-Route Detection**: Jumps to the wrong star? Lighthouse instantly turns orange and warns you that you are off route, helping you correct your trajectory immediately.
- **Deep Space EDSM Fallback**: Stuck in a completely uncharted sector? Lighthouse can triangulate your exact galactic (X, Y, Z) coordinates from your journal logs and use the EDSM API to find the nearest known star, automatically generating a rescue route from the middle of nowhere.
- **Sleek HUD UI**: A gorgeous, glassmorphism design that sits directly over your cockpit. 
- **Ultra-Minimal Mode**: Need to focus on the sights? Collapse the HUD into an ultra-minimal single-line readout (`Waypoint | Jumps | Next`) that takes up almost zero screen space.

![Minimized Mode](screenshots/minimized.png)

## Installation

1. Head over to the [Releases page](https://github.com/BerryMelon/elite-lighthouse/releases).
2. Download the latest `Elite Lighthouse Setup.exe` file.
3. Run the installer. The app will automatically launch and stay on top of your Elite Dangerous window.

*Note: Elite Lighthouse is completely borderless and click-through. You can't accidentally click it and lose control of your ship unless you explicitly hover over its tiny window controls.*

## Development

If you want to build the project from source or contribute to it:

1. Clone the repository
2. Run `npm install`
3. Run `npm run dev` to start both the Vite React server and the Electron shell simultaneously.

To compile a production build executable:
```bash
npm run dist
```
The output `.exe` will be located in the `dist-electron` folder.

## Technologies Used

- **React + Vite**: For a blazingly fast frontend UI
- **Electron**: For native window layering and filesystem (Journal) access
- **Tailwind-style CSS**: Custom styling optimized for transparent HUDs
- **Spansh API & EDSM API**: The backbone of the galaxy's routing network

Enjoy the black, Commander! o7
