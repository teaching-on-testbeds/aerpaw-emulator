#! /usr/bin/env python


from datetime import datetime


def current_milli_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


import sys

sys.path.insert(0, "..")

import argparse
import csv
import os
import queue as queue
import re
import time
from collections import OrderedDict

import serial

parser = argparse.ArgumentParser(description="Usage: sudo python at_rm500q.py -p /dev/ttyUSB2 -t <Folder_time_name>")
parser.add_argument("-p", "--usbpath", help="Specify USB port, else /dev/ttyUSB2 or USB3 (if ttyUSB2 fails) will be used, if otherwise specify", default="/dev/ttyUSB2")
parser.add_argument("-t", "--time_dir", help="Specify time string")
args = parser.parse_args()
config = vars(args)


# test Main
if __name__ == "__main__":

    def current_milli_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # Define Main defs
    def sleep_countdown(self, timer_count):
        while timer_count:
            mins, secs = divmod(timer_count, 60)
            timer = f"{mins:02d}:{secs:02d}"
            time.sleep(1)
            timer_count -= 1

    def printTable(myDict, colList=None):
        if not colList:
            colList = list(myDict[0].keys() if myDict else [])
        myList = [colList]  # 1st row = header
        for item in myDict:
            myList.append([str(item[col] if item[col] is not None else "") for col in colList])
        colSize = [max(map(len, col)) for col in zip(*myList)]
        formatStr = " | ".join([f"{{:<{i}}}" for i in colSize])
        myList.insert(1, ["-" * i for i in colSize])  # Seperating line
        for item in myList:
            print(formatStr.format(*item))

    def command_to_serial_read_response(command_with_read):
        ser.close()
        ser.open()
        payload = bytes(command_with_read + "\r\n", "utf-8")
        # payload = bytes("ATI\r\n", 'utf-8')
        ser.write(payload)
        time.sleep(0.1)
        read_val = ser.read_until(expected=b"OK").decode("utf-8")
        # read_val = ser.read_until(expected=b"OK")
        # print(read_val)
        return os.linesep.join([s for s in "".join(read_val.removesuffix("OK")).splitlines() if s])

    ser = serial.Serial("/dev/ttyUSB4", baudrate=115200, bytesize=8, timeout=1)

    ser.reset_input_buffer()
    ser.reset_output_buffer()
    rows, columns = os.popen("stty size", "r").read().split()
    connected_string = "========"
    spaces = "=".join([""] * (int(columns) - len(connected_string) - 10))
    empty_print = spaces
    print(current_milli_time(), connected_string, empty_print, end="\n")
    spaces1 = "-".join([""] * (int(columns) - len(connected_string)))
    spaces2 = "_".join([""] * (int(columns) - len(connected_string)))
    ###################################
    # Serving cell Parameters

    print(current_milli_time(), "Serving cell Params")
    # Line2 Serving cell Params
    Line2_Part_LTE = ["servingcell", "state", "LTE", "is_tdd", "MCC", "MNC", "cellID", "PCID", "earfcn", "freq_band", "UL_bw", "DL_bw", "TAC", "RSRP", "RSRQ", "RSSI", "SINR", "CQI", "tx_power", "srxlev"]
    Line2_Part1 = ["servingcell", "State"]
    Line2_Part2 = ["LTE", "is_TDD", "MCC", "MNC", "cellID", "PCID", "earfcn", "freq_band", "UL_bw", "DL_bw", "TAC", "RSRP", "RSRQ", "RSSI", "SINR", "CQI", "tx_power", "srxlev"]
    Line2_Part3 = ["NR5G-NSA", "MCC", "MNC", "PCID", "RSRP", "SINR", "RSRQ", "ARFCN", "band", "NR_DL_bw", "scs"]

    Var_Serving_cell_string = command_to_serial_read_response('AT+QENG="servingcell"')
    lst_Var_Serving_cell_string = Var_Serving_cell_string.split("\n")
    # print(lst_Var_Serving_cell_string)
    if len(lst_Var_Serving_cell_string) == 1:
        # LTE mode
        Dict_Serving_cell_Line_LTE = OrderedDict(zip(Line2_Part_LTE, lst_Var_Serving_cell_string[0].split(",")))
    else:
        # ENDC mode
        Dict_Serving_cell_Line1 = OrderedDict(zip(Line2_Part1, lst_Var_Serving_cell_string[0].split(",")))
        Dict_Serving_cell_Line2 = OrderedDict(zip(Line2_Part2, lst_Var_Serving_cell_string[1].split(",")))
        Dict_Serving_cell_Line3 = OrderedDict(zip(Line2_Part3, lst_Var_Serving_cell_string[2].split(",")))

        print(spaces2)
        row_format1 = (len(Dict_Serving_cell_Line2.keys())) * "{:>15}"
        print(row_format1.format(*Dict_Serving_cell_Line2.keys()))
        print(spaces1)
        print(row_format1.format(*Dict_Serving_cell_Line2.values()))
        print(spaces2, end="\n")

        row_format2 = (len(Dict_Serving_cell_Line3.keys())) * "{:>20}"
        print(row_format2.format(*Dict_Serving_cell_Line3.keys()))
        print(spaces1)
        print(row_format2.format(*Dict_Serving_cell_Line3.values()))
        print(spaces2, end="\n\n")

    # Write to CSV Serving cell params
    Header_Servingcell_LTE = ["timestamp", "servingcell", "state", "LTE", "is_tdd", "MCC", "MNC", "cellID", "PCID", "earfcn", "freq_band", "UL_bw", "DL_bw", "TAC", "RSRP", "RSRQ", "RSSI", "SINR", "CQI", "tx_power", "srxlev"]
    Header_Servingcell_ENDC_Part1 = ["timestamp", "servingcell", "State"]
    Header_Servingcell_ENDC_Part2 = ["LTE", "is_TDD", "LTE_MCC", "LTE_MNC", "LTE_cellID", "LTE_PCID", "LTE_earfcn", "LTE_freq_band", "LTE_UL_bw", "LTE_DL_bw", "LTE_TAC", "LTE_RSRP", "LTE_RSRQ", "LTE_RSSI", "LTE_SINR", "LTE_CQI", "LTE_tx_power", "LTE_srxlev"]
    Header_Servingcell_ENDC_Part3 = ["NR5G-NSA", "nr_MCC", "nr_MNC", "nr_PCID", "nr_RSRP", "nr_SINR", "nr_RSRQ", "nr_ARFCN", "nr_band", "NR_DL_bw", "nr_scs"]
    Header_Servingcell_ENDC = Header_Servingcell_ENDC_Part1 + Header_Servingcell_ENDC_Part2 + Header_Servingcell_ENDC_Part3

    if len(lst_Var_Serving_cell_string) == 1:
        Servingcell_LTE_params_Write = [current_milli_time()]
        Servingcell_LTE_params_Write = Servingcell_LTE_params_Write + list(Dict_Serving_cell_Line_LTE.values())
        Servingcell_LTE_Params_OrderedDict = OrderedDict(zip(Header_Servingcell_LTE, Servingcell_LTE_params_Write))
        with open(f"/root/Results/logs/{args.time_dir!s}/csv_kpi/Serving_cell_Params_LTE_only.csv", "a") as file_serving_lte:
            writer = csv.DictWriter(file_serving_lte, fieldnames=Servingcell_LTE_Params_OrderedDict.keys(), delimiter=",")
            writer.writerow(Servingcell_LTE_Params_OrderedDict)
            file_serving_lte.close()
    else:
        Servingcell_ENDC_params_Write = [current_milli_time()]
        Servingcell_ENDC_params_Write = Servingcell_ENDC_params_Write + list(Dict_Serving_cell_Line1.values())
        Servingcell_ENDC_params_Write = Servingcell_ENDC_params_Write + list(Dict_Serving_cell_Line2.values())
        Servingcell_ENDC_params_Write = Servingcell_ENDC_params_Write + list(Dict_Serving_cell_Line3.values())
        Servingcell_ENDC_Params_OrderedDict = OrderedDict(zip(Header_Servingcell_ENDC, Servingcell_ENDC_params_Write))
        with open(f"/root/Results/logs/{args.time_dir!s}/csv_kpi/Serving_cell_Params_ENDC.csv", "a") as file_serving_endc:
            writer = csv.DictWriter(file_serving_endc, fieldnames=Servingcell_ENDC_Params_OrderedDict.keys(), delimiter=",")
            writer.writerow(Servingcell_ENDC_Params_OrderedDict)
            file_serving_endc.close()

    #################################
    print(current_milli_time(), "Neighbour cell Params", "\n")
    print(spaces2)
    # Line3 Neighbour cell Params
    Line3_Part1 = ["neighbourcell intra", "LTE", "earfcn", "PCID", "RSRQ", "RSRP", "RSSI", "SINR", "srxlev", "cell_resel_priority", "s_non_intra_search", "thresh_serving_lo", "s_intra_search"]
    Line3_Part2 = ["neighbourcell inter", "LTE", "earfcn", "PCID", "RSRQ", "RSRP", "RSSI", "SINR", "srxlev", "cell_resel_priority", "threshX_low", "threshX_high"]
    Var_Neighbour_cell_string = command_to_serial_read_response('AT+QENG="neighbourcell"')
    # print(Var_Neighbour_cell_string)
    if Var_Neighbour_cell_string != "":
        lst_Var_Neighbour_cell_string = Var_Neighbour_cell_string.split("\n")
        for i in range(len(lst_Var_Neighbour_cell_string)):
            # print(lst_Var_Neighbour_cell_string[i]) ;
            Dict_Neighbour_cell_Line = []
            if re.search(r"(?<=intra).*", lst_Var_Neighbour_cell_string[i]):
                Dict_Neighbour_cell_Line = OrderedDict(zip(Line3_Part1, lst_Var_Neighbour_cell_string[i].split(",")))
            if re.search(r"(?<=inter).*", lst_Var_Neighbour_cell_string[i]):
                Dict_Neighbour_cell_Line = OrderedDict(zip(Line3_Part2, lst_Var_Neighbour_cell_string[i].split(",")))
            row_format3 = (len(Dict_Neighbour_cell_Line.keys())) * "{:>24}"
            row_format4 = (len(Dict_Neighbour_cell_Line.keys())) * "{:>23}"
            print(row_format3.format(*Dict_Neighbour_cell_Line.keys()))
            print(spaces1)
            print(row_format4.format(*Dict_Neighbour_cell_Line.values()))
            print(spaces2, end="\n")
        print("\n")

        # Write to CSV neighbour cell params
        Header_Neighbourcell_intra = ["timestamp", "neighbourcell intra", "LTE", "earfcn", "PCID", "RSRQ", "RSRP", "RSSI", "SINR", "srxlev", "cell_resel_priority", "s_non_intra_search", "thresh_serving_lo", "s_intra_search"]
        Header_Neighbourcell_inter = ["timestamp", "neighbourcell inter", "LTE", "earfcn", "PCID", "RSRQ", "RSRP", "RSSI", "SINR", "srxlev", "cell_resel_priority", "threshX_low", "threshX_high"]
        for i in range(len(lst_Var_Neighbour_cell_string)):
            # print(lst_Var_Neighbour_cell_string[i]) ;
            Dict_Neighbour_cell_Line = []
            if re.search(r"(?<=intra).*", lst_Var_Neighbour_cell_string[i]):
                Neighbour_cell_intra_params_Write = [current_milli_time()]
                Neighbour_cell_intra_params_Write_params_Write = Neighbour_cell_intra_params_Write + lst_Var_Neighbour_cell_string[i].split(",")
                Dict_Neighbour_cell_Line = OrderedDict(zip(Header_Neighbourcell_intra, Neighbour_cell_intra_params_Write_params_Write))
                with open(f"/root/Results/logs/{args.time_dir!s}/csv_kpi/Neighbourcell_Params_intra_.csv", "a") as file_neighbour_intra:
                    writer = csv.DictWriter(file_neighbour_intra, fieldnames=Dict_Neighbour_cell_Line.keys(), delimiter=",")
                    writer.writerow(Dict_Neighbour_cell_Line)
                    file_neighbour_intra.close()
            if re.search(r"(?<=inter).*", lst_Var_Neighbour_cell_string[i]):
                Neighbour_cell_inter_params_Write = [current_milli_time()]
                Neighbour_cell_inter_params_Write_params_Write = Neighbour_cell_inter_params_Write + lst_Var_Neighbour_cell_string[i].split(",")
                Dict_Neighbour_cell_Line = OrderedDict(zip(Header_Neighbourcell_inter, Neighbour_cell_inter_params_Write_params_Write))
                with open(f"/root/Results/logs/{args.time_dir!s}/csv_kpi/Neighbourcell_Params_inter_.csv", "a") as file_neighbour_inter:
                    writer = csv.DictWriter(file_neighbour_inter, fieldnames=Dict_Neighbour_cell_Line.keys(), delimiter=",")
                    writer.writerow(Dict_Neighbour_cell_Line)
                    file_neighbour_inter.close()
    ##############################################
    print(current_milli_time(), "Other Parameters", "\n")
    Line4_Part2 = ["+QNWCFG: lte_csi", "lte_mcs", "lte_ri", "lte_cqi", "lte_pmi"]
    Line4_Part3 = ["+QNWCFG: nr5g_csi", "nr_mcs", "nr_ri", "nr_cqi", "nr_pmi"]

    Dict_QNWCFG_LTE_CSI_Line = OrderedDict(zip(Line4_Part2, command_to_serial_read_response('AT+QNWCFG="lte_csi"').split(",")))
    Dict_QNWCFG_NR_Line = OrderedDict(zip(Line4_Part3, command_to_serial_read_response('AT+QNWCFG="nr5g_csi"').split(",")))
    print(spaces2)
    Dict_QNWCFG_LTE_CSI_Line.update(Dict_QNWCFG_NR_Line)
    row_format5 = (len(Dict_QNWCFG_LTE_CSI_Line.keys())) * "{:>24}"
    print(row_format5.format(*Dict_QNWCFG_LTE_CSI_Line.keys()))
    print(spaces1)
    print(row_format5.format(*Dict_QNWCFG_LTE_CSI_Line.values()))
    print(spaces2, end="\n")
    print("\n")
    # Write to CSV basic & other params
    Basic_Param_and_Other_params_Write = [current_milli_time()]
    Basic_Param_and_Other_params_Write = Basic_Param_and_Other_params_Write + list(Dict_QNWCFG_LTE_CSI_Line.values()) + list(Dict_QNWCFG_NR_Line.values())
    Header_Basic_and_other_params = ["timestamp", "+QNWCFG: lte_csi", "lte_mcs", "lte_ri", "lte_cqi", "lte_pmi", "+QNWCFG: nr5g_csi", "nr_mcs", "nr_ri", "nr_cqi", "nr_pmi"]
    Basic_and_other_Params_OrderedDict = OrderedDict(zip(Header_Basic_and_other_params, Basic_Param_and_Other_params_Write))
    with open(f"/root/Results/logs/{args.time_dir!s}/csv_kpi/Basic_and_Other_Params.csv", "a") as file_basic:
        writer = csv.DictWriter(file_basic, fieldnames=Basic_and_other_Params_OrderedDict.keys(), delimiter=",")
        writer.writerow(Basic_and_other_Params_OrderedDict)
        file_basic.close()

    #######################################################
    disconnected_string = "====="
    spaces = "=".join([""] * (int(columns) - len(disconnected_string) - 7))
    empty_print = spaces
    print(current_milli_time(), "\n", disconnected_string, empty_print)
