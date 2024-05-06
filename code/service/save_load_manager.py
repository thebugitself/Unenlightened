import pickle
import os

class SaveLoadManager:
    def __init__(self,file_extension,save_folder):
        self.file_extension = file_extension
        self.save_folder = save_folder

    def save_data(self,data,name):
        data_file = open(self.save_folder + "/" + name + self.file_extension,'wb')
        pickle.dump(data,data_file)

    def load_data(self,name):
        try:
            data_file = open(self.save_folder + "/" + name + self.file_extension, 'rb')
            data = pickle.load(data_file)
            return data
        except:
            return None
    
    def del_file(self, name):
        file_path = self.save_folder + "/" + name + self.file_extension
        if os.path.exists(file_path):
            os.remove(file_path)

    def check_for_file(self,name):
        return os.path.exists(self.save_folder + "/" + name + self.file_extension)