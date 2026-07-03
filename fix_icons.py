import sys
with open('src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update RouteIcon to a Star
old_route_icon = """const RouteIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"></circle>
      <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>
      <path d="M2 12h20"></path>
    </svg>
  );"""
new_route_icon = """const RouteIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
    </svg>
  );"""
code = code.replace(old_route_icon, new_route_icon)

# 2. Update HVT Icon to the old RouteIcon (Globe/Target)
old_hvt_icon = """const HvtIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3"></circle>
      <circle cx="12" cy="12" r="8" strokeDasharray="4 4"></circle>
    </svg>
  );"""
new_hvt_icon = """const HvtIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"></circle>
      <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>
      <path d="M2 12h20"></path>
    </svg>
  );"""
code = code.replace(old_hvt_icon, new_hvt_icon)

# 3. Update Exo Tracker icon to DNA helix
old_exo_icon = """const ExoIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 22v-3c0-4 3-7 7-7 2.2 0 4.2.9 5.7 2.4L22 22"></path>
      <path d="M15.7 15.7L22 7.5"></path>
      <path d="M11 2a7 7 0 0 0-7 7"></path>
    </svg>
  );"""
new_exo_icon = """const ExoIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 2v2M9 2v2M12 12v.01M15 22v-2M9 22v-2M18.9 4a12.5 12.5 0 0 0-13.8 16M5.1 4a12.5 12.5 0 0 1 13.8 16"></path>
      <path d="M7 6h10M6 18h12M11 9l2 6"></path>
    </svg>
  );"""
code = code.replace(old_exo_icon, new_exo_icon)

# Write back
with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
print("Icons replaced.")
