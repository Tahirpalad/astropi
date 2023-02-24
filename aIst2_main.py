from sense_hat import SenseHat
from datetime import datetime, timedelta
from logzero import logger, logfile
from pathlib import Path
from os import mkdir, remove, fsync
from os.path import exists, getsize
from time import sleep
from orbit import ISS
from numpy import ceil
from datetime import timezone

sense = SenseHat()
sense.clear()
CONST_TIME_MINUTES = 177
CONST_SLEEP_TIME = 5



#TODO Change back to 3 hours

def sense_get_data():
  '''Function to get acceleration and magnetic data'''
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
  '''Gets the orientation data(pitch, roll, yaw)
  Displays an image on the LEDs that changes to show that the program is running
  Creates a log file and data file to store data of experiment
  Writes data to the log file as well as data file
  ''' 
  o = sense.get_orientation()

  pitch = round(o["pitch"], 2)
  roll = round(o["roll"], 2)
  yaw = round(o["yaw"], 2)
  
  
  #Display an image to show that the experiment is running  
  b = (255, 0, 0) # red
  p = (255, 0, 0) # red
  c = (0, 0, 0) # Black
  r = (255,255,255) #(rgb.red, rgb.green, rgb.blue)
  

  image2 = [
  	c, b, c, c, c, c, c, c,
  	c, b, b, c, c, c, c, c,
    c, b, b, b, c, c, c, c,
    c, b, b, b, b, c, c, c,
    c, b, b, b, c, c, c, c,
  	c, b, b, c, c, c, c, c,
    c, b, c, c, c, c, c, c,
    c, c, c, c, c, c, c, c] 
    
  image = [
  	c, c, c, c, b, c, c, c,
  	c, c, c, c, b, b, c, c,
    c, c, c, c, b, b, b, c,
    c, c, c, c, b, b, b, b,
    c, c, c, c, b, b, b, c,
  	c, c, c, c, b, b, c, c,
    c, c, c, c, b, c, c, c,
    c, c, c, c, c, c, c, c]

  
    

  
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
  #Finds the time at which the experiment will finish
  endtime = datetime.now(timezone.utc) + timedelta(minutes = CONST_TIME_MINUTES) 
  logger.info('Starting data collection!')
  size_mb = 0.0
  sense.clear(b)
  imageshown = 1

  while datetime.now(timezone.utc) < endtime:
    begin = datetime.now(timezone.utc)
    # Display the image
    if (imageshown % 5 == 1):
        sense.set_pixels(image)
        imageshown = imageshown + 1
        #print(imageshown)
    else:
        sense.set_pixels(image2)
        imageshown = 1
        #print(imageshown)


      
    try:
      
      o = sense.get_orientation()
      time_stamp = datetime.now(timezone.utc)
      pitch2 = round(o["pitch"], 2)
      roll2 = round(o["roll"], 2)
      yaw2 = round(o["yaw"], 2)
    
      #Finds the coordinates of the ISS and writes it to data file
      coords = ISS.coordinates()
      lat = coords.latitude
      longit = coords.longitude
      data_file.write('\nLat: {}\nLong: {}'.format( str(lat),str(longit)))
      data_file.flush()

      #Returns the values from the sense_get_data function and writes it to data file
      sense_mag_data, sense_acc_data = sense_get_data()
      data_file.write('\n{} \n{}'.format(sense_mag_data, sense_acc_data))
      data_file.flush()
      fsync(data_file)
      if pitch2 != pitch or roll2 != roll or yaw2 != yaw:

        pitch = pitch2
        roll = roll2
        yaw = yaw2
        data_file.write('\nP: {} \nR: {}\nY: {}\nT: {}\n'.format(str(pitch2), str(roll2), str(yaw2), str(time_stamp)))
        data_file.flush()


      elif pitch2 == pitch and roll2 == roll and yaw2 == yaw:
        data_file.write('\nNo change\n')
        data_file.flush()
      fsync(data_file)
    #Incase of an error, it will write it to the log with time it happened
    except Exception as e:
      logger.error(f"Error in {e.__class__.__name__}, {e}")
      print('Catching exception')
    seconds = (datetime.now(timezone.utc) - begin).total_seconds()
    sleep_time = CONST_SLEEP_TIME - seconds
    if sleep_time > 0:
        sleep(sleep_time)
    else:
        logger.warning(f"Experiment is taking too long! (+{abs(sleep_time)} seconds!)")
  
    size_mb = getsize(f"{ist2_data_folder}/data.txt") / 1000000.0  
    if size_mb > 2995:
        logger.warning("Max size reached! exiting!")
        break
  data_file.write(f'End of experiment ----> {ceil(size_mb)} MB\n')
  data_file.flush()
  data_file.close()
  sense.clear()  
  logger.info('Experiment finished, end of log.')
