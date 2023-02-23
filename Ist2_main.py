from sense_hat import SenseHat
from datetime import datetime, timedelta
from logzero import logger, logfile
from pathlib import Path
from os import mkdir, remove
from os.path import exists, getsize
from time import sleep
from orbit import ISS
from numpy import ceil

sense = SenseHat()
CONST_TIME_HOURS = 3
CONST_SLEEP_TIME = 5
#TODO Change back to 3 hours

def sense_get_data():
  sense_mag_data = []
  sense_acc_data = []

  mag = sense.get_compass_raw()
  mag_x = round(mag['x'], 2)
  mag_y = round(mag['y'], 2)
  mag_z = round(mag['z'], 2)
  sense_mag_data.append('Mx: {}'.format(mag_x))
  sense_mag_data.append('My: {}'.format(mag_y))
  sense_mag_data.append('Mz: {}'.format(mag_z))


  acc = sense.get_accelerometer_raw()
  acc_x = round(acc['x'], 2)
  acc_y = round(acc['y'], 2)
  acc_z = round(acc['z'], 2)
  sense_acc_data.append('Ax: {}'.format(acc_x))
  sense_acc_data.append('Ay: {}'.format(acc_y))
  sense_acc_data.append('Az: {}'.format(acc_z))
  return(sense_mag_data, sense_acc_data)

if __name__ == '__main__':

  o = sense.get_orientation()

  pitch = round(o["pitch"], 2)
  roll = round(o["roll"], 2)
  yaw = round(o["yaw"], 2)

  #File logging here
  ist2_base_folder = str(Path(__file__).parent.resolve())
  # Init logger
  logfile(filename=f"{ist2_base_folder}/logfile.txt")
  logger.info("New log")
  # Creating the file structure, default data folder is (base_folder)/data
  ist2_data_folder = f"{ist2_base_folder}/data"
  if not exists(path=ist2_data_folder):
      mkdir(path=ist2_data_folder)
      logger.info("Made data folder")
  data_file = open(file=f"{ist2_data_folder}/data.txt", mode='a')
  logger.info("Opened data file")
  endtime = datetime.now() + timedelta(hours = CONST_TIME_HOURS) #TODO Change back to 3 hours
  logger.info('Starting data collection!')
  size_mb = 0.0
  while datetime.now() < endtime:
    begin = datetime.now()
    try:
      o = sense.get_orientation()
      time_stamp = datetime.now()
      pitch2 = round(o["pitch"], 2)
      roll2 = round(o["roll"], 2)
      yaw2 = round(o["yaw"], 2)

      coords = ISS.coordinates()
      lat = coords.latitude
      longit = coords.longitude
      #print('\nLat:{}\nLon:{}\n'.format(lat, longit))
      data_file.write('\nLat: {}\nLong: {}'.format( str(lat),str(longit)))
      data_file.flush()

      sense_mag_data, sense_acc_data = sense_get_data()
      #TODO write it to file
      data_file.write('\n{} \n{}'.format(sense_mag_data, sense_acc_data))
      data_file.flush()

      if pitch2 != pitch or roll2 != roll or yaw2 != yaw:

        pitch = pitch2
        roll = roll2
        yaw = yaw2
        #print('\nP: {} \nR: {}\nY: {} \nT: {}'.format(pitch2, roll2, yaw2, time_stamp))
        data_file.write('\nP: {} \nR: {}\nY: {}\nT: {}\n'.format(str(pitch2), str(roll2), str(yaw2), str(time_stamp)))
        data_file.flush()


      elif pitch2 == pitch and roll2 == roll and yaw2 == yaw:
        data_file.write('\nNo change\n')
        data_file.flush
      
    except Exception as e:
      logger.error(f"Error in {e.__class__.__name__}, {e}")
    seconds = (datetime.now() - begin).total_seconds()
    sleep_time = CONST_SLEEP_TIME - seconds
    if sleep_time > 0:
        sleep(sleep_time)
    else:
        logger.warning(f"Experiment is taking too long! (+{abs(sleep_time)} seconds!)")
    size_mb += getsize(ist2_data_folder) / 1000000.0  
  data_file.write(f'Ended experiment ----> {ceil(size_mb)} MB\n')
  data_file.flush()
  data_file.close()
  logger.info('Experiment finished, end of log.')
        #TODO comments
