from cairosvg import svg2png

# Complete SVG content
svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">
    <!-- Solid Background -->
    <rect width="800" height="500" fill="#1e40af"/>
    
    <!-- Search Bar Container -->
    <rect x="150" y="80" width="500" height="70" rx="35" fill="#ffffff"/>
    
    <!-- Magnifying Glass -->
    <circle cx="190" cy="115" r="18" fill="none" stroke="#1e40af" stroke-width="4"/>
    <line x1="203" y1="128" x2="215" y2="140" stroke="#1e40af" stroke-width="4" stroke-linecap="round"/>
    
    <!-- Sample Search Text -->
    <text x="230" y="125" font-family="Arial" font-size="16" fill="#64748b">Search resumes by skills, experience...</text>

    <!-- Resume Cards -->
    <g transform="translate(150, 180)">
        <!-- Resume 1 -->
        <g transform="translate(0, 0)">
            <rect x="0" y="0" width="140" height="200" fill="#ffffff" rx="15"/>
            <rect x="20" y="20" width="100" height="15" fill="#bfdbfe"/>
            <rect x="20" y="45" width="80" height="10" fill="#93c5fd"/>
            <rect x="20" y="65" width="90" height="10" fill="#93c5fd"/>
            <text x="20" y="110" font-family="Arial" font-size="14" fill="#1e40af">Software Dev</text>
            <text x="20" y="130" font-family="Arial" font-size="12" fill="#64748b">5 years exp.</text>
        </g>

        <!-- Resume 2 -->
        <g transform="translate(160, 0)">
            <rect x="0" y="0" width="140" height="200" fill="#ffffff" rx="15"/>
            <rect x="20" y="20" width="100" height="15" fill="#bfdbfe"/>
            <rect x="20" y="45" width="80" height="10" fill="#93c5fd"/>
            <rect x="20" y="65" width="90" height="10" fill="#93c5fd"/>
            <text x="20" y="110" font-family="Arial" font-size="14" fill="#1e40af">Data Science</text>
            <text x="20" y="130" font-family="Arial" font-size="12" fill="#64748b">3 years exp.</text>
        </g>

        <!-- Resume 3 -->
        <g transform="translate(320, 0)">
            <rect x="0" y="0" width="140" height="200" fill="#ffffff" rx="15"/>
            <rect x="20" y="20" width="100" height="15" fill="#bfdbfe"/>
            <rect x="20" y="45" width="80" height="10" fill="#93c5fd"/>
            <rect x="20" y="65" width="90" height="10" fill="#93c5fd"/>
            <text x="20" y="110" font-family="Arial" font-size="14" fill="#1e40af">UI Designer</text>
            <text x="20" y="130" font-family="Arial" font-size="12" fill="#64748b">4 years exp.</text>
        </g>
    </g>

    <!-- Connection Lines -->
    <g stroke="#60a5fa" stroke-width="3">
        <path d="M 200 150 Q 250 170 260 180" fill="none"/>
        <path d="M 350 150 Q 400 170 410 180" fill="none"/>
        <path d="M 500 150 Q 550 170 560 180" fill="none"/>
    </g>

    <!-- Feature Keywords -->
    <g font-family="Arial, sans-serif" font-size="16" fill="#ffffff">
        <text x="150" y="450">Experience</text>
        <text x="280" y="450">Skills</text>
        <text x="380" y="450">Education</text>
        <text x="480" y="450">Projects</text>
        <text x="580" y="450">Certificates</text>
    </g>
</svg>'''

# First save the SVG file
with open('resume_search.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

# Then convert to PNG with high quality settings
try:
    svg2png(url='resume_search.svg',
            write_to='resume_search.png',
            output_width=2400,
            output_height=1500,
            dpi=300)
    print("Conversion completed successfully!")
except Exception as e:
    print(f"An error occurred: {str(e)}")