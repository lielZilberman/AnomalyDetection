import statistics
import csv
import pandas as pd
import operator
import streamlit as st
from csv import writer

f_path = "conn_attack.csv"
df = pd.read_csv(f_path, names=["record ID", "duration_", "src_bytes", "dst_bytes"], header=None)
record_id = len(df)


def enterCSV(input):
    with open(f_path, 'a') as csv_file:
        writer_obj = writer(csv_file)
        writer_obj.writerow(input)
        csv_file.close()


def generate(src, rcv, dur, col2):
    if src.isnumeric() and dur.isnumeric() and rcv.isnumeric():
        global record_id
        record_id = record_id + 1
        # input_csv = [record_id,dur,src,rcv]
        temp_table = create_table()
        temp_table[record_id] = float(src)
        median_sorted = dict(sorted(temp_table.items(), key=operator.itemgetter(1)))
        anomaly = MAD(median_sorted, record_id)
        if anomaly:
            return col2.warning("ANOMALY 👎")
        else:
            return col2.warning("NOT AN ANOMALY 👍")
        # enterCSV(input_csv)


# Initializing the first dictionary of data.
def create_table() -> dict:
    median_table = {}
    for id in df["record ID"]:
        src = df["src_bytes"][id - 1]
        median_table[id] = src
    return median_table


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://image.shutterstock.com/image-vector/abstract-financial-chart-line-graph-260nw-1240192321.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


def main():
    add_bg_from_url()
    src = st.text_input("SRC BYTES", value=0)
    rcv = st.text_input("RCV BYTES", value=0)
    dur = st.text_input("DUR BYTES", value=0)
    col1, col2, col3 = st.columns([1, 1, 1])
    col2.button("GENERATE A RESULT", on_click=generate, args=(src, rcv, dur, col2))
    # st.title("Streamlit App")
    # st.header("Deploying Streamlit in Docker")


def MAD(median_dict, requested_id) -> dict:
    # Implementation of MAD(Median Absolute Deviation):
    threshold = 3  # Usually 2.5 or 3
    # Getting the first median.
    median_num = statistics.median_high(median_dict.values())
    # Subtracting the median from each value in the dictionary , and then absoluting the values.
    for key in median_dict:
        median_dict[key] = abs(median_dict[key] - median_num)
    # Second sort.
    median_sorted = dict(sorted(median_dict.items(), key=operator.itemgetter(1)))
    # Getting the second median after the second sort.
    median_num2 = statistics.median_high(median_sorted.values())
    k = 1.4826  # Scaling factor in MAD algorithm.
    mad = k * median_num2  # Formula according to the MAD algorithm steps.
    result = {}  # {id:anomaly(0= good, 1 = anomaly)}
    # If value above the threshold , anomaly otherwise good.
    for key in median_sorted:
        median_sorted[key] = median_sorted[key] / mad
        if median_sorted[key] > threshold:
            result[key] = 1
        else:
            result[key] = 0
    # Implementing the alogrithm , following the steps of the alogrithm.

    return result[requested_id]


main()
