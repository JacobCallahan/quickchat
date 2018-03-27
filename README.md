QuickChat
=========

Fast, Disposable, Containerized Chat!
```
docker run -p 1337:5000 jacobcallahan/quickchat
```
QuickChat is a no frills on-demand private chat app.
Run the container image for easily scalable app instances
 as well as easy installation/cleanup.
When you're done, just kill the container and all data is wiped!

You can also run the app manually (see below), but why?
```
python dbinit.py
python app.py
```
