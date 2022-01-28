# Personal Home Athan Automation
This was a proof of concept that was never completed due to the successor [Project Bilal](https://github.com/Project-Bilal/bilal-backend). In theory it's a Flask server running along side HASS which is in docker, all of which are on the Raspberry Pi. The Flask server is used as an interface to let users upload different athan files. The HASS is used to communciate with the Google Home Speakers. Although in a better iteration we can skip HASS and just pychromecast to send the audio to the Google device.

A crontab job exists to schedule all the necessary athan calls every morning as other cronjbos. When these cronjobs run they trigger a script which sends the information to Google to play the audio. Additionally the script will randomize which athan sound to play for that day by naming one of the files `play.mp3`. An older version of this did the same thing but the files were on Gooolge Cloud Storage. 

## Issues
- In order to cast locally hosted files to Google either using HASS or Pychromecast we need to have the files sitting on a server. An easy way to do this is using a SimpleHTTPServer. Make sure that runs where it sees the audio files we have uploaded and then update the scripts to point to the URL of those files. Google then should be able to play the file
- For each prayer the setting that determines what kind of audio file is going to play is hard coded in the script that casts the audio. A better way would be to allow the user to choose this setting in the Flask front end.
- The same issue exists for Volume, each athan is hard coded in the script
- Uploading duplicate file name will override each other
- You can't name a file play.mp3 because that will override the existing file logic
- The display name of the file in the Flask front end includes the subdirectory like `takbir/1.mp3`. We can't get rid the the directory part because when we delete it we should know where to put it back
- When I delete a file the URL will take me to `delete` but when I click on `deleted` it takes me to `deleted`. But essentially they are the same place

## How to install
It's best to follow these instructions on the [Goolge Doc](https://docs.google.com/document/d/1VQYipYXDIVEoGv9a8v6bf6R-2Fw9s3umBTerVNrlnF4/edit#)
