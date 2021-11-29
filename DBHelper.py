import mysql.connector as connector


class DBHelper:
    def __init__(self):
        self.con = connector.connect(host='database-1.codef6iuo0yk.ap-south-1.rds.amazonaws.com',
                                     port='3306',
                                     user='admin',
                                     password='password',
                                     database='Database_Maiden',
                                     auth_plugin='mysql_native_password')

    # Create
    def insert(self, bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt,
               last_updated, height, fire_alarm, full_alarm, frame_counter):
        query = "Insert into bins_history( bin_id, angle, battery_alarm, rsrp, temperature , tilt_alarm, volt, " \
                "last_updated, height, fire_alarm, full_alarm, frame_counter) Values ('{}', '{}','{}','{}'," \
                "'{}','{}','{}','{}','{}','{}','{}','{}');".format(
            bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt, last_updated, height, fire_alarm,
            full_alarm, frame_counter)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print('successfully inserted values into bins history')

    # Update
    def update(self, bin_id, angle, battery_alarm, rsrp, temperature,
               tilt_alarm, volt, last_updated, height, fire_alarm, frame_counter, full_alarm):

        query = "select id from bins where bin_id = '{}'".format(bin_id)

        query1 = "update bins set bin_id = '{}', angle = '{}', battery_alarm = '{}', rsrp = '{}', temperature = '{}', " \
                 "tilt_alarm = '{}', volt = '{}', last_updated = '{}', height = '{}', fire_alarm = '{}', frame_counter " \
                 "= '{}', full_alarm = '{}' where bin_id = '{}'".format(
            bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt, last_updated, height, fire_alarm,
            frame_counter, full_alarm, bin_id)

        cur = self.con.cursor()
        cur.execute(query1)
        self.con.commit()
        print('successfully updated values into bins')

# helper = DBHelper()
# helper.insert('86169873223', '0', '0', '987', '27', '0', '3.6', '1970-01-01 00:00:01', '123', '0', '0', '0')
# helper.update('86169873223', '1', '1', '987', '27', '1', '4.5', '1970-01-01 00:00:01', '123', '1', '1', '1')
