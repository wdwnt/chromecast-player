import pychromecast
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

NTUNES_STREAM_URL = 'https://streaming.live365.com/a31769'
NTUNES_IMAGE_URL = 'https://appcdn.wdwnt.com/roku/images/WDWNTunes_600x334.png'

def start_chromecast(device_name):
  chromecasts = pychromecast.get_chromecasts()

  cast = next(cc for cc in chromecasts if cc.device.friendly_name == device_name)
  cast.wait()
  cast.set_volume(0.3)

  mc = cast.media_controller

  mc.play_media(NTUNES_STREAM_URL, 'audio/mp3', 'WDWNTunes', NTUNES_IMAGE_URL)
  mc.block_until_active()
  mc.play()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/devices')
def get_devices():
  result = []

  chromecasts = pychromecast.get_chromecasts()
  for cc in chromecasts:
    obj = dict()
    obj['name'] = cc.device.friendly_name
    result.append(obj)

  return jsonify(result)

@app.route('/play', methods=['POST'])
def play():
  result = {'success': False}

  req_data = request.get_json()

  if not 'device' in req_data:
    return result

  device_to_cast_to = req_data['device']

  start_chromecast(device_to_cast_to)

  result['success'] = True

  return result

@app.route('/stop')
def stop():
  chromecasts = pychromecast.get_chromecasts()
  for cc in chromecasts:
    cc.media_controller.stop()

  return {'success': True}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
