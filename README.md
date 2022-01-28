# Personal Home Athan Automation
This was a proof of concept that was never completed due to the successor [Project Bilal](https://github.com/Project-Bilal/bilal-backend). In theory it's a Flask server running along side HASS which is in docker, all of which are on the Raspberry Pi. The Flask server is used as an interface to let users upload different athan files. The HASS is used to communciate with the Google Home Speakers. Although in a better iteration we can skip HASS and just pychromecast to send the audio to the Google device.

A crontab job exists to schedule all the necessary athan calls every morning as other cronjbos. When these cronjobs run they trigger a script which sends the information to Google to play the audio.

## Issues
- In order to cast locally hosted files to Google either using HASS or Pychromecast we need to have the files sitting on a server. An easy way to do this is using a SimpleHTTPServer. Make sure that runs where it sees the audio files we have uploaded and then update the scripts to point to the URL of those files. Google then should be able to play the file
- For each prayer the setting that determines what kind of audio file is going to play is hard coded in the script that casts the audio. A better way would be to allow the user to choose this setting in the Flask front end.
- The same issue exists for Volume, each athan is hard coded in the script
