import mysql.connector as connector


class DBHelper:
    def __init__(self):
        self.con = connector.connect(host='database-1.codef6iuo0yk.ap-south-1.rds.amazonaws.com',
                                     port='3306',
                                     user='admin',
                                     password='password',
                                     database='Database_Maiden',
                                     auth_plugin='mysql_native_password')

        query = 'CREATE TABLE IF NOT EXISTS `bins` (`id` INT NOT NULL AUTO_INCREMENT,`angle` INT NOT NULL,' \
                '`battery_alarm` INT NOT NULL,`capacity` INT NOT NULL,`color` VARCHAR(25) NOT NULL,`latitude` ' \
                'DECIMAL(4,2) NOT NULL,`longitude` DECIMAL(4,2) NOT NULL,`place` VARCHAR(45) NOT NULL,`rsrp` INT NOT ' \
                'NULL,`temperature` INT NOT NULL,`sim_number` VARCHAR(45) NOT NULL,`tilt_alarm` INT NOT NULL,' \
                '`volt` DECIMAL(2,1) NOT NULL,`last_updated` VARCHAR(45) NOT NULL,`height` INT NOT NULL,' \
                '`total_height` INT NOT NULL,`bin_id` VARCHAR(25) NOT NULL,`fire_alarm` INT NOT NULL,`full_alarm` INT ' \
                'NOT NULL,`frame_counter` INT NOT NULL,`user_name` VARCHAR(25) NOT NULL,PRIMARY KEY (`id`)) ' \
                'ENGINE=InnoDB DEFAULT CHARSET=utf8; '

        query1 = 'CREATE TABLE IF NOT EXISTS `bins_history` (`id` INT NOT NULL AUTO_INCREMENT,`angle` INT NOT NULL,' \
                 '`battery_alarm` INT NOT NULL,`bin_id` VARCHAR(25) NOT NULL,`fire_alarm` INT NOT NULL,' \
                 '`frame_counter` INT NOT NULL,`full_alarm` INT NOT NULL,`height` INT NOT NULL,`rsrp` INT NOT NULL,' \
                 '`temperature` INT NOT NULL,`tilt_alarm` INT NOT NULL,`last_updated` TIMESTAMP(6) NOT NULL,' \
                 '`volt` DECIMAL(2,1) NOT NULL,`latitude` DECIMAL(4,2) NOT NULL,`longitude` DECIMAL(4,2) NOT NULL,' \
                 'PRIMARY KEY (`id`)) Engine=InnoDB DEFAULT CHARSET=utf8 '

        cur = self.con.cursor()
        cur.execute(query)
        cur.execute(query1)
        print('created tables or updated tables')

    # Create
    def insert(self, bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt,
               last_updated, height, fire_alarm, full_alarm, frame_counter):
        query = "Insert into bins_history(bin_id, angle, battery_alarm, latitude, longitude, rsrp, temperature ," \
                "tilt_alarm, volt, last_updated, height, 'fire_alarm', 'full_alarm', 'frame_counter') Values ('{}'," \
                "'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
            bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt, last_updated, height, fire_alarm, full_alarm, frame_counter)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print('successfully')

    # Update
    def update(self, bin_id, angle, battery_alarm, rsrp, temperature,
               tilt_alarm, volt, last_updated, height, fire_alarm, frame_counter, full_alarm):
        query = "insert into bins(bin_id, angle, battery_alarm, capacity, color, latitude, longitude, place, rsrp, " \
                "temperature, sim_number, tilt_alarm, volt, last_updated, height, total_height, fire_alarm, " \
                "frame_counter, full_alarm, user_name) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                "'{}','{}') where bin_id = '{}' ".format(
            bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt, last_updated, height, fire_alarm, frame_counter, full_alarm, bin_id)

        print(query)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
