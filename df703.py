# DF703 gprs support

from Utility import utility
import json


# req_data = "8000010222270F001900000000016800803BC40001612674E6186655705560745381"
# req_data = "800001022A270F0100000000000000001A000000000168008054C40001612792F2186655705560745381"


class DF703(object):
    # Func: parse data to attr DF703 TCP
    # Param: req_data: input data string in upper format
    #        attr_result: output attr
    #       token_id: token for thingsboard, imei
    # "80 00 01 02 22 270F 00 1A 00 00 0 0 0 0 0168 00804AC4 0001 00000038 1866557055607453 81"
    # "80 00 01 02 1E 0649 00 1B 0000 0101015F 0080 54440000 1868821043038876 81“ heart beat/alarm without gps
    # "8000010126064901CD03E942EF2720421B00000101015F008054440000186882104303887681" event packet with gps
    # "" Param
    def parse_data_DF703(req_data):
        try:
            data_type = req_data[6:8]
            data_len = int(req_data[8:10], 16)
            attr_result = ""
            token_id = ""

            if (data_len == len(req_data) / 2):
                if (data_type == "01" or data_type == "02"):
                    if (data_len == 34):
                        token_id = req_data[50:66]
                        data_height = int(req_data[10:14], 16)
                        data_temperature = int(req_data[16:18], 16)
                        data_angle = int(req_data[20:22], 16) if (int(req_data[18:20], 16) == 0) else (
                                0 - int(req_data[20:22], 16))
                        data_full_alarm = int(req_data[22:23], 16)
                        data_fire_alarm = int(req_data[23:24], 16)
                        data_tilt_alarm = int(req_data[24:25], 16)
                        data_battery_alarm = int(req_data[25:26], 16)
                        data_volt = int(req_data[26:30], 16) / 100
                        data_rsrp_origin = req_data[30:38]
                        data_rsrp = int(utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                        data_frame_counter = int(req_data[38:42], 16)
                        time_stamp = int(req_data[42:50], 16)
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "height": data_height,
                            "temperature": data_temperature,
                            "full_alarm": data_full_alarm,
                            "fire_alarm": data_fire_alarm,
                            "tilt_alarm": data_tilt_alarm,
                            "battery_alarm": data_battery_alarm,
                            "volt": data_volt,
                            "angle": data_angle,
                            "rsrp": data_rsrp,
                            "frame_counter": data_frame_counter,
                            "time_stamp": time_stamp
                        }
                    # 80 00 01 02 2A 270F 01 00000000 00000000 1A 00 00 0 0 0 0 0168 008054C4 0001 612792F2 1866557055607453 81
                    # 01 23 45 67 89 10   14 16       24       32 34 36 3839404142   46       54   58       66               82
                    else:
                        token_id = req_data[66:82]
                        data_height = int(req_data[10:14], 16)
                        data_longitude_origin = req_data[16:24]
                        data_longitude = utility.IEEE754_Hex_To_Float(data_longitude_origin)
                        data_longitude = ("%.6f" % data_longitude)
                        data_latitude_origin = req_data[24:32]
                        data_latitude = utility.IEEE754_Hex_To_Float(data_latitude_origin)
                        data_latitude = ("%.6f" % data_latitude)
                        data_temperature = int(req_data[32:34], 16)
                        data_angle = int(req_data[36:38], 16) if (int(req_data[34:36], 16) == 0) else (
                                0 - int(req_data[36:38], 16))
                        data_full_alarm = int(req_data[38:39], 16)
                        data_fire_alarm = int(req_data[39:40], 16)
                        data_tilt_alarm = int(req_data[40:41], 16)
                        data_battery_alarm = int(req_data[41:42], 16)
                        data_volt = int(req_data[42:46], 16) / 100
                        data_rsrp_origin = req_data[46:54]
                        data_rsrp = int(utility.IEEE754_Hex_To_Float(data_rsrp_origin))
                        data_frame_counter = int(req_data[54:58], 16)
                        time_stamp = int(req_data[58:66], 16)
                        # print("rsrp is "+str(data_rsrp))
                        attribute = {
                            "height": data_height,
                            "longitude": data_longitude,
                            "latitude": data_latitude,
                            "temperature": data_temperature,
                            "full_alarm": data_full_alarm,
                            "fire_alarm": data_fire_alarm,
                            "tilt_alarm": data_tilt_alarm,
                            "battery_alarm": data_battery_alarm,
                            "volt": data_volt,
                            "angle": data_angle,
                            "rsrp": data_rsrp,
                            "frame_counter": data_frame_counter,
                            "time_stamp": time_stamp
                        }
                attr_result = json.dumps(attribute)
                print(attribute)
            else:
                attr_result = json.dumps("")
                token_id = ""
            # time.sleep(1)
        except Exception as e:
            print(e)
            # log.logger.exception(e)
        finally:
            return attr_result, token_id
