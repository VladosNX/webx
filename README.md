# WebX
### A simple web-server
***
WebX is a lightweight web-server which can be configured easily.
**NOTE** WebX works on Linux only!
## Installing
**Step 1** Install XLPM:
> wget https://vladosnx.github.io/xlpm/xlpm-1.2.deb
> sudo dpkg -i xlpm-1.2.deb

**Step 2** Install WebX
> sudo xlpm -g vladosnx/webx

**Ready!**
## Configuring WebX
**Step 1** Create config folder
> sudo mkdir -p /etc/webx/configs

**Step 2** Create config
> sudo nano /etc/webx/configs/<config-name>.yml

Write:
> host: <ip>
> port: 80
> workdir: /var/www
> mainfile: index.php
> max_requests: 1000

**host** - server ip **(127.0.0.1 will not work!)**
**port** - server port (default: 80)
**workdir** - directory with site files
**mainfile** - file which will be sent if file is not specified by user
**max_request** - max requests count


## Starting server
To start server, run this command: **webx -s <config-name>**
To stop server press Ctrl+C
