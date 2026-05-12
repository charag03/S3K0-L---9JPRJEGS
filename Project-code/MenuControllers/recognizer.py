import pandas as pd


def is_patient(patients_creds, patient_email, patient_password):

    for i in range(patients_creds.shape[0]):
        if patient_email == patients_creds.iloc[i, 0] and patient_password == patients_creds.iloc[i, 1]:
            return 1


def is_doctor(doctors_creds, doctor_email, doctor_password):

    for i in range(doctors_creds.shape[0]):
        if doctor_email == doctors_creds.iloc[i, 0] and doctor_password == doctors_creds.iloc[i, 1]:
            return 1


def is_pharmacist(pharmacists_creds, pharmacist_email, pharmacist_password):
    for i in range(pharmacists_creds.shape[0]):
        if pharmacist_email == pharmacists_creds.iloc[i, 0] and pharmacist_password == pharmacists_creds.iloc[i, 1]:
            return 1


def is_inv_manager(inv_managers_creds, inv_manager_email, inv_manager_password):
    for i in range(inv_managers_creds.shape[0]):
        if inv_manager_email == inv_managers_creds.iloc[i, 0] and inv_manager_password == inv_managers_creds.iloc[i, 1]:
            return 1


def is_hr_manager(hr_managers_creds, hr_manager_email, hr_manager_password):
    for i in range(hr_managers_creds.shape[0]):
        if hr_manager_email == hr_managers_creds.iloc[i, 0] and hr_manager_password == hr_managers_creds.iloc[i, 1]:
            return 1

def is_secretary(secretaries_creds, secretary_email, secretary_password):
    for i in range(secretaries_creds.shape[0]):
        if secretary_email == secretaries_creds.iloc[i, 0] and secretary_password == secretaries_creds.iloc[i, 1]:
            return 1