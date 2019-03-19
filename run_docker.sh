xhost +SI:localuser:root
docker run --rm -it -e DISPLAY=:0.0 --user 0:0 --ipc=host -v /tmp/.X11-unix:/tmp/.X11-unix:rw --privileged --name pidocker -v "$PWD":/home -w /home andrewssobral/rpi-raspbian:keras_tensorflow /bin/bash
