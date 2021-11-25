import socket
import Logger
import threading
import time

import df703
from DBHelper import DBHelper

port_number = 9000
max_clients = 10
attr_result = ""
token_id = ""
log = Logger.Logger("all.log", level="debug")


def upload_data(attr, token):
    try:

        data = attr
        print(data)

        bin_id = token
        angle = data["angle"]
        battery_alarm = data["battery_alarm"]
        rsrp = data["rsrp"]
        temperature = data["temperature"]
        tilt_alarm = data["tilt_alarm"]
        volt = data["volt"]
        last_updated = data["time_stamp"]
        height = data["height"]
        full_alarm = data["full_alarm"]
        fire_alarm = data["fire_alarm"]
        frame_counter = data["frame_counter"]

        db = DBHelper()
        db.insert(bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt,
                  last_updated, height, fire_alarm, full_alarm, frame_counter)

        db.update(bin_id, angle, battery_alarm, rsrp, temperature, tilt_alarm, volt, last_updated, height, fire_alarm, frame_counter, full_alarm, bin_id)

        print("try to upload data ")
        log.logger.debug("upload_data: close socket in upload_data")
        # return 1
    except Exception as ex:
        print(ex)
        log.logger.exception("upload_data", ex)
    finally:
        return 1


def response_sensor(client, data):
    try:
        client.send(bytes(data, "utf-8"))
    except Exception as ex:
        # print(e)
        log.logger.exception(ex)


def handle_client(client, address):
    try:
        client.settimeout(10)
        # overtime time
        request_bytes = b""
        global attr_result
        request_str = ""
        global token_id
        find_result1 = -1
        while True:
            if not client._closed:
                request_bytes = request_bytes + (client.recv(1024))
                # TODO problem 1
            if not request_bytes:
                # print("Connection closed")
                break
                # client.close()
            request_str = request_bytes.hex()
            find_result1 = str(request_str).find("8000")
            if find_result1 != -1:
                print(request_str)
                break
            # print(request_data)
        str_subreq = str(request_str[find_result1:])
        data_type = str_subreq[4:6]
        log.logger.debug("packet is %s, data_type is DF%s0", str_subreq, data_type)

        # parse and upload
        attr_result, token_id = df703.DF703.parse_data_DF703(
            str_subreq.strip().upper()
        )

        # for other data_type, there are several module sensors, use different listening port to recognize them.
        print("attr is" + attr_result + ".token_id is " + token_id)
        log.logger.debug("attr is" + attr_result + ".token_id is " + token_id)
        if attr_result != "" and token_id != "":
            upload_data(attr_result, token_id)
            log.logger.debug("after upload data ")
        else:
            log.logger.debug("invalid data ")
        time.sleep(1)
        client.close()
        time.sleep(1)
        log.logger.debug("close device connection ")
    except socket.timeout:
        print("time out")
        client.close()


if __name__ == "__main__":

    try:
        attr_result = ""
        token_deviceid = ""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", port_number))
        server_socket.listen(max_clients)
        while True:
            client_socket, client_address = server_socket.accept()
            log.logger.debug(str(client_address) + "user connected!")
            thread = threading.Thread(
                target=handle_client, args=(client_socket, client_address)
            )
            thread.start()
            log.logger.debug("after handle_client_process close!")
    except Exception as e:
        print(e)
        log.logger.error(e)
