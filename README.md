# Stable Diffusion Houdini Toolset

Works with Houdini 19.5 and 20 with Python 3.9. 

*Tested with Automatic1111 and ControlNet version as of 19.03.2024 (March 2024).*

Developed by Stanislav Demchenko (stassius) for EVR Systems.

https://www.linkedin.com/in/stanislav-demchenko/

https://evr.systems/

Our Discord:
https://discord.gg/bfdzAWQwct

https://user-images.githubusercontent.com/35260274/234114613-43e2b2a9-f4ed-4494-a304-6b9cd92c178e.mp4

Professional set of Houdini digital assets for Stable Diffusion image processing.

### Features:
1. Automatic1111 in Houdini
2. All main A1111 features, including TI, Loras, Hypernetworks, face restoration, tiling, hires fix. Use any checkpoint or LoRA from civitai.com. SD XL included.
4. ControlNet 1.1, whole set of preprocessors and models
5. Animateable Image2Image alternative test
6. Upscale
7. Prompt from file, prompt animation
8. Bulk processing in i2i, mask, i2i alt test, ControlNet
9. Full PDG integration
10. Bulk ControlNet preprocessing
11. Work on a remote server with http authorization
12. Use A1111 scripts like Ultimate SD Upscale right from Houdini
13. Prepare datasets and train your own LoRAs right from Houdini using Kohya_ss connector. SD XL training profile included.

### Installation
1. Install Automatic1111
2. Add --api command line key to the webui-user.bat
3. Run A1111 with webui-user.bat
4. Install asset libraries from /hda/ and use assets inside Houdini
5. Make sure the Python and Presets folders are located next to the top_stable_diffusion.hda file
6. After the first time you created an SD node, /hda/Config/config.ini file will be created. In it you can change the default URL and also turn on http authorization for remote server if you use it. Also, if you work locally, put 0.15 to the Timeout property, it will speed up starting a project when Automatic is not loaded. Restart Houdini for changes to take effect.
7. (Optional) Install Kohya_ss webui for training and add the installation directory to config.ini

If you got problems running Stable Houdini, there is a troubleshooting guide: https://github.com/stassius/StableHoudini/wiki/Troubleshooting-checklist

### Recommended TOP Network settings
In localscheduler node:
- Scheduler/Slot count - Custom slot count=1
- Job params/Single - On

### Houdini Nodes included:
- Generation
  - SD Dream (PDG) - t2i, i2i, control net, all the A1111 features
  - SD Preprocessor (PDG) - get preprocessed images (depth, normal and other maps) from ControlNet
  - SD Upscale (PDG) - upscale an image with various neural networks
  - SD Script (PDG) - lets you use A1111 scripts in t2i and i2i modes. Add it before the SD Dream node.
  - SD Png Info (PDG) - parses generation parameters stored in PNG-file and stores them in attributes for reuse.
  - Depth map (Obj) - instant depth-map for ControlNet generation
- Prompts
  - SD Prompt (PDG) - create and animate prompts
  - SD Interrogate (PDG) - takes an image and generates a prompt for it. Works like the CLIP Interrogation feature of A1111. Can be used for BLIP captioning.
- Settings
  - SD Switch Model (PDG) - switch to any A1111 checkpoint
  - SD Set Option (PDG) - lets you set an A1111 internal option.
- Image processing
  - Image Process (PDG) - process images in COPs
  - COP Processor (PDG) - lets you add your own image processing. Dive inside this node and add any COP nodes between Input and Output. Your image will be processed and rendered.
- Utility
  - Image Preview (PDG) - easily switch and save generation batches
  - Refresh Viewport Textures (PDG) - resets a cache for viewport textures
- Training
  - SD Dataset Preparation (PDG) - prepares a dataset for further training. It copies all the images into a particular folder, crops and resizes them, adds text captions.
  - SD Trainer Kohya (PDG). Lets you train LoRAs right from the Houdini's TOPs. It's a connector for the most powerful set of training scripts for Stable Diffusion called Kohya_ss.
  
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
