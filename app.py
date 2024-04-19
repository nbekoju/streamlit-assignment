"""streamlit app with employee and department registration features"""
import os
import csv
import time

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

menu_options = ["Employee", "Department", "Joined View"]


def save_to_csv(filename, data):
    """
    save the new data to the given filename
    """
    # Check if the file exists
    file_exists = False
    try:
        with open(filename, "r", encoding="utf-8") as file:
            file_exists = True
    except FileNotFoundError:
        pass

    # If the file exists, append data to it, else create a new file and write data
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        # Write header only if file is newly created
        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


# create the sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="FuseMachines",
        options=menu_options,
        default_index=0,
    )


# select different pages
if selected == menu_options[0]:
    st.title(f"Welcome to the {selected} page")

    # show the employee table
    if os.path.exists("employee.csv"):
        employee_df = pd.read_csv("employee.csv")
        st.table(employee_df)

    # Employee Form
    st.markdown("## Add an employee")
    emp_id = st.text_input("Employee ID:")
    emp_name = st.text_input("Employee Name:")
    emp_job = st.text_input("Job:")
    dept_num = st.number_input("Department Number:", 1, 10)

    if st.button("Add Employee"):
        emp_data = {
            "ID": emp_id,
            "Name": emp_name,
            "Job": emp_job,
            "Department Number": dept_num,
        }

        save_to_csv("employee.csv", emp_data)

        success_message = st.success("Employee added successfully!")
        time.sleep(2)
        success_message.empty()


if selected == menu_options[1]:
    st.title(f"Welcome to the {selected} page")

    # show the departments table
    if os.path.exists("departments.csv"):
        department_df = pd.read_csv("departments.csv")
        st.table(department_df)

    # add department form
    st.markdown("## Add Department")
    dept_num = st.number_input("Department Number:", 1, 10)
    dept_name = st.text_input("Department Name: ")
    location = st.radio("Location", ["Nepal", "USA", "India", "Argentina", "Canada"])

    if st.button("Add Department"):
        dept_data = {
            "Department Number": dept_num,
            "Department Name": dept_name,
            "Location": location,
        }
        save_to_csv("departments.csv", dept_data)

        success_message = st.success("Department added successfully!")
        time.sleep(2)
        success_message.empty()


if selected == menu_options[2]:
    st.title(f"Welcome to the {selected} page")

    # join the tables based on the department number
    department_df = pd.read_csv("departments.csv")
    employee_df = pd.read_csv("employee.csv")

    desired_columns = ["ID", "Name", "Department Number", "Department Name"]

    join_view = pd.merge(
        employee_df, department_df, on="Department Number", how="left"
    )[desired_columns]
    st.table(join_view)
