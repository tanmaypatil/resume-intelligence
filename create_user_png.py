from cairosvg import svg2png

# Complete SVG content
svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">
    <!-- Outer Circle (Background) -->
    <circle cx="120" cy="120" r="120" fill="#F8FAFC"/>
    
    <!-- Inner Circle (Container) -->
    <circle cx="120" cy="120" r="100" fill="#ffffff" stroke="#64748B" stroke-width="2"/>
    
    <!-- Main Chat Bubble -->
    <path d="M75 80 C75 70, 85 60, 95 60 L165 60 C175 60, 185 70, 185 80 L185 130 C185 140, 175 150, 165 150 L135 150 L120 170 L105 150 L95 150 C85 150, 75 140, 75 130 Z" 
          fill="#3B82F6" stroke="#2563EB" stroke-width="2"/>
    
    <!-- Abstract Circuit Lines (representing AI) -->
    <path d="M95 90 L115 90 L125 100 L145 100" 
          stroke="#ffffff" stroke-width="2" stroke-linecap="round" fill="none"/>
    <path d="M95 110 L135 110 L145 120" 
          stroke="#ffffff" stroke-width="2" stroke-linecap="round" fill="none"/>
    <path d="M95 130 L115 130" 
          stroke="#ffffff" stroke-width="2" stroke-linecap="round" fill="none"/>
    
    <!-- Decorative Circles -->
    <circle cx="90" cy="180" r="15" fill="#3B82F6" opacity="0.2"/>
    <circle cx="170" cy="160" r="10" fill="#3B82F6" opacity="0.2"/>
    <circle cx="150" cy="190" r="8" fill="#3B82F6" opacity="0.15"/>
    
    <!-- Connection Points -->
    <circle cx="90" cy="180" r="4" fill="#3B82F6"/>
    <circle cx="170" cy="160" r="4" fill="#3B82F6"/>
    <circle cx="150" cy="190" r="4" fill="#3B82F6"/>
    
    <!-- Connecting Lines -->
    <path d="M90 180 Q120 175 170 160" 
          stroke="#3B82F6" stroke-width="1.5" fill="none" opacity="0.5"/>
    <path d="M90 180 Q120 185 150 190" 
          stroke="#3B82F6" stroke-width="1.5" fill="none" opacity="0.5"/>
</svg>
'''

# First save the SVG file
with open('resume_user.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

# Then convert to PNG with high quality settings
try:
    svg2png(url='resume_user.svg',
            write_to='resume_user.png',
            output_width=2400,
            output_height=1500,
            dpi=300)
    print("Conversion completed successfully!")
except Exception as e:
    print(f"An error occurred: {str(e)}")