# Stable Diffusion Houdini Toolset

Works with Houdini 19.5 with Python 3.9.

*Tested with Automatic1111 and ControlNet version as of 28.05.2023 (may 2023).*

Developed by Stanislav Demchenko (stassius) for EVR Systems.

https://www.linkedin.com/in/stanislav-demchenko/

https://evr.systems/

Our Discord:
https://discord.gg/bfdzAWQwct

https://user-images.githubusercontent.com/35260274/234114613-43e2b2a9-f4ed-4494-a304-6b9cd92c178e.mp4

Professional set of Houdini digital assets for Stable Diffusion image processing.

### Features:
1. Automatic1111 in Houdini
2. All main A1111 features, including TI, Loras, Hypernetworks, face restoration, tiling, hires fix
4. ControlNet 1.1, whole set of preprocessors and models
5. Animateable Image2Image alternative test
6. Upscale
7. Prompt from file, prompt animation
8. Bulk processing in i2i, mask, i2i alt test, ControlNet
9. Full PDG integration
10. Bulk ControlNet preprocessing
11. Work on a remote server with http authorization
12. Use A1111 scripts like Ultimate SD Upscale right from Houdini

### Installation
1. Install Automatic1111
2. Add --api command line key to the webui-user.bat
3. Run A1111 with webui-user.bat
4. Install asset libraries from /hda/ and use assets inside Houdini
5. Make sure the Python and Presets folders are located next to the top_stable_diffusion.hda file
6. After the first time you created an SD node, /hda/Config/config.ini file will be created. In it you can change the default URL and also turn on http authorization for remote server if you use it. Also, if you work locally, put 0.15 to the Timeout property, it will speed up starting a project when Automatic is not loaded. Restart Houdini for changes to take effect.

If you got problems running Stable Houdini, there is a troubleshooting guide: https://github.com/stassius/StableHoudini/wiki/Troubleshooting-checklist

### Recommended TOP Network settings
In localscheduler node:
- Scheduler/Slot count - Custom slot count=1
- Job params/Single - On

### Houdini Nodes included:
1. SD Switch Model (PDG) - switch to any A1111 checkpoint
2. SD Dream (PDG) - t2i, i2i, control net, all the A1111 features
3. SD Prompt (PDG) - create and animate prompts
4. SD Upscaler (PDG) - upscale an image with various neural networks
5. Image Preview (PDG) - easily switch and save generation batches
6. Image Process (PDG) - process images in COPs
7. Depth map (Obj) - instant depth-map for ControlNet generation
8. SD Preprocessor (PDG) - get preprocessed images (depth, normal and other maps) from ControlNet
9. SD Png Info (PDG) - parses generation parameters stored in PNG-file and stores them in attributes for reuse.
10. SD Set Option (PDG) - lets you set any A1111 option. You can find the internal name of the option and its type in config.json file in A1111 folder.
11. SD Interrogate (PDG) - takes an image and generates a prompt for it. Works like the CLIP Interrogation feature of A1111.
12. SD Script (PDG) - lets you use A1111 scripts in t2i and i2i modes. Add it before the SD Dream node.
13. COP Processor (PDG) - lets you add your own image processing. Dive inside this node and add any COP nodes between Input and Output. Your image will be processed and rendered.

### Documentation
Our wiki is full of valuable information:
https://github.com/stassius/StableHoudini/wiki

### Video tutorials:
* English:
https://www.youtube.com/watch?v=jCE1Dx_Q924
* Russian:
https://www.youtube.com/watch?v=Un_b8cvzxcw

### Additional demo videos:

https://user-images.githubusercontent.com/35260274/234114730-d19e9615-332a-4c5e-89af-30ef44ca3742.mp4

https://user-images.githubusercontent.com/35260274/234129594-1405b0de-df7a-4395-b628-5a5bed728114.mp4

Support me: https://www.donationalerts.com/r/houdinirus
