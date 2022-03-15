# GoPro Low Latency Stream Demo

This demostrates how to decode the GoPro webcam or 16x9 video preview stream using the ffmpeg library.
To use this demo, plug in a hero 9 or hero 10 camera while in a standard video mode and run the app.  The webcam stream at 1080p should be displayed in the window. The display output is not optimized.
To switch to preview stream (720p non processed stream), uncomment the #define in GoProStreamDemo.h
//#define USE_PREVIEW_STREAM
