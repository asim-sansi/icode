# iCode 
# 1.Introduction & Project Vision
iCode is a project that focuses on the development of a web based tool that processes GUI screenshots provided by a user, and translates them into HTML code for a browser webpage.
The project primarily focuses on developing coherent and accurate assistive structures for web development purposes, rather than producing full fledged end user solutions.
# 1.1.Objectives
The Objective of this project is to attain partial automation of custom front-end web development. This is done through automated code generation via processing of GUI screenshots that are to be replicated by the user.
# 1.2.Project Scope
The iCode project focuses on developing a web based application that accepts GUI screenshots, processes them (identifying components and classifying unique HTML elements), and returns HTML markup. GUI screenshots provided are required to be clear and sharp images, consisting of explicit design that can be translated into a markup language. Overlays, non-uniform backgrounds, non-uniform components/elements shall not be handled by the tool as per current development domain. Recognizable and translatable designs shall be processed; components will be identified, extracted and classified as a corresponding HTML element; and will then be organized and styled by the tool in HTML.
# 1.3.Constraints
- GUI Screenshots should only consist of the web page itself. Screenshot should not include parts of browser or OS.
- GUI Screenshots provided should be pixel perfect images and not pixelated, blurred, scaled versions. Camera captured images are not handled by the tool.
- GUI Screenshots provided shall have plain, uniform colored backgrounds
- Gradients, patterns, and shades are not handled in this project’s domain
- Only components consisting of basic shapes, i.e rectangles, circles, and squares are handled or recognized in this project’s domain. Any other shapes provided are not taken into consideration.

# 2.List of Features
- Boundary Detection
- Component Extraction
- Dimension and Position Extraction- 
- Text Recognition
- Style Extraction
- Element Classification
- HTML DOM Tree Organisation and Construction
- HTML Code Generation
- Web Portal (GUI)
