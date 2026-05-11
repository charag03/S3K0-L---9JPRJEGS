from .file_reader import File_reader
import pandas as pd

class DocReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getDoctorId(self) -> pd.Series:
        return self.read_file().iloc[:,0]
    
    def getDoctorFirstName(self) ->pd.Series:
        return self.read_file().iloc[:,1]
    
    def getDoctorLastName(self) ->pd.Series:
        return self.read_file().iloc[:,2]
    
    def getDoctorSpecialization(self) ->pd.Series:
        return self.read_file().iloc[:,3]
    
    def getDoctorPhoneNuber(self) ->pd.Series:
        return self.read_file().iloc[:,4]
    
    def getDoctorExperience(self) ->pd.Series:
        return self.read_file().iloc[:,5]
    
    def getDoctorBrach(self) ->pd.Series:
        return self.read_file().iloc[:,6]
    
    def getDoctorEmail(self) ->pd.Series:
        return self.read_file().iloc[:,7]
    
    def getDoctorPassword(self) ->pd.Series:
        return self.read_file().iloc[:,8]

class AppointmentReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getAppointmentId(self) ->pd.Series:
        return self.read_file().iloc[:,0]
        
    def getPatientId(self) ->pd.Series:
        return self.read_file().iloc[:,1]
    
    def getDoctorId(self)->pd.Series:
        return self.read_file().iloc[:,2]
    
    def getAppointmentDate(self)->pd.Series:
        return self.read_file().iloc[:,3]
    
    def getAppointmentTime(self)->pd.Series:
        return self.read_file().iloc[:,4]
    
    def getAppointmentReasor(self)->pd.Series:
        return self.read_file().iloc[:,5]
    
    def getAppointmentStatus(self)->pd.Series:
        return self.read_file().iloc[:,6]
    

class BillingReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getBillId(self)->pd.Series:
        return self.read_file().iloc[:,0]
    
    def getPatientId(self)->pd.Series:
        return self.read_file().iloc[:,1]
    
    def getTreatmentID(self)->pd.Series:
        return self.read_file().iloc[:,2]
    
    def getBillDate(self)->pd.Series:
        return self.read_file().iloc[:,3]
    
    def getBillAmount(self)->pd.Series:
        return self.read_file().iloc[:,4]
    
    def getBillPaymentMethod(self)->pd.Series:
        return self.read_file().iloc[:,5]
    
    def getBillPaymentStatus(self)->pd.Series:
        return self.read_file().iloc[:,6]
    
    
class HrManagerReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getHrManagerId(self)->pd.Series:
        return self.read_file().iloc[:,0]
    
    def getHrManagerFirstName(self)->pd.Series:
        return self.read_file().iloc[:,1]
    
    def getHrManagerLastName(self)->pd.Series:
        return self.read_file().iloc[:,2]
    
    def getHrManagerPhone(self)->pd.Series:
        return self.read_file().iloc[:,3]
    
    def getHrManagerExperience(self)->pd.Series:
        return self.read_file().iloc[:,4]
    
    def getHrManagerBranch(self)->pd.Series:
        return self.read_file().iloc[:,5]
    
    def getHrManagerEmail(self)->pd.Series:
        return self.read_file().iloc[:,6]
    
    def getHrManagerPassword(self)->pd.Series:
        return self.read_file().iloc[:,7]
    
class InvManagerReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getInvManagerId(self)->pd.Series:
        return self.read_file().iloc[:,0]


    def getInvManagerFirstName(self)->pd.Series:
        return self.read_file().iloc[:,1]

    def getInvManagerLastName(self)->pd.Series:
        return self.read_file().iloc[:,2]

    def getInvManagerPhone(self)->pd.Series:
        return self.read_file().iloc[:,3]

    def getInvManagerExperience(self)->pd.Series:
        return self.read_file().iloc[:,4]

    def getInvManagerBranch(self)->pd.Series:
        return self.read_file().iloc[:,5]

    def getInvManagerEmail(self)->pd.Series:
        return self.read_file().iloc[:,6]

    def getInvManagerPassword(self)->pd.Series:
        return self.read_file().iloc[:,7]


class PatientReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getPatientId(self)->pd.Series:
        return self.read_file().iloc[:,0]

    def getPatientFirstName(self)->pd.Series:
        return self.read_file().iloc[:,1]

    def getPatientLastName(self)->pd.Series:
        return self.read_file().iloc[:,2]
    
    def getPatientGender(self)->pd.Series:
        return self.read_file().iloc[:,3]

    def getPatientBirth(self)->pd.Series:
        return self.read_file().iloc[:,4]

    def getPatientNumber(self)->pd.Series:
        return self.read_file().iloc[:,5]

    def getPatientAddress(self)->pd.Series:
        return self.read_file().iloc[:,6]

    def getPatientRegistrationDate(self)->pd.Series:
        return self.read_file().iloc[:,7]

    def getPatientInsuranceProvider(self)->pd.Series:
        return self.read_file().iloc[:,8]

    def getPatientInsuranceNumber(self)->pd.Series:
        return self.read_file().iloc[:,9]

    def getPatientEmail(self)->pd.Series:
        return self.read_file().iloc[:,10]
    
    def getPatientPassword(self)->pd.Series:
        return self.read_file().iloc[:,11]

class PharmacistReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getPharmacistId(self)->pd.Series:
        return self.read_file().iloc[:,0]

    def getPharmacistFirstName(self)->pd.Series:
        return self.read_file().iloc[:,1]

    def getPharmacistLastName(self)->pd.Series:
        return self.read_file().iloc[:,2]

    def getPharmacistSpecialization(self)->pd.Series:
        return self.read_file().iloc[:,3]

    def getPharmacistBranch(self)->pd.Series:
        return self.read_file().iloc[:,4]

    def getPharmacistEmail(self)->pd.Series:
        return self.read_file().iloc[:,5]

    def getPharmacistPassword(self)->pd.Series:
        return self.read_file().iloc[:,6]
    

class TreatmentReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getTreatmentId(self)->pd.Series:
        return self.read_file().iloc[:,0]

    def getAppointmentId(self)->pd.Series:
        return self.read_file().iloc[:,1]

    def getTreatmentType(self)->pd.Series:
        return self.read_file().iloc[:,2]

    def getTreatmentDescription(self)->pd.Series:
        return self.read_file().iloc[:,3]

    def getTreatmentCost(self)->pd.Series:
        return self.read_file().iloc[:,4]

    def getTreatmentDate(self)->pd.Series:
        return self.read_file().iloc[:,5]