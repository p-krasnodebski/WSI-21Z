from file_read  import WineCsvReader
from random import shuffle
from math import sqrt, pi, exp

class NBC:

    def __init__(self, stream, factor, attr = []):
        """
        Constructs a wine object from csv file.
        """
        self.stream = stream
        self.factor = factor
        self.attr = attr
        self.data = self.read_data()
        shuffle(self.data)
        self.validation_data = []
        self.train_data = []
        self.test_data = []

        self.attr_num = self.data[1].no_attr

        self.mi = {}
        self.sigma = {}

        self.err = 0
        self.mean_error = 0
        self.n = 0

        if self.factor < 1 and self.factor > 0:
            print("Podział na zbiór treningowy i testowy")
            self.train_data, self.test_data = self.two_sets()
            self.n = 1
        elif self.factor > 1 and type(self.factor) == int:
            self.validation_data = self.split_data()
            print("Walidacja danych")
            self.n = self.factor
        else:
            print("Błąd")
            return

        for i in range(self.n):
            if self.n > 1:
                self.train_data = []
                self.test_data = self.validation_data[i]
                
                for j in range(self.n):
                    if j !=i:
                        self.train_data = self.train_data + self.validation_data[j]

            self.separated_data = self.separate_class()

            self.Py = {}
            self.calculate_py()

            self.train_model()
            self.test_model()

    def read_data(self):
        """
        Read file with data
        """
        with open(self.stream, newline='', encoding="utf-8") as file:
        
            raw_data = WineCsvReader(file, self.attr).read_file()

        return raw_data

    def two_sets(self):
        """
        Devide data into two group
        """
        no = int(self.factor*len(self.data))
        train_data = self.data[:no]
        test_data = self.data[no+1:]
        return train_data, test_data

    def split_data(self):
        """
        Devide data for validation
        """
        table = []
        k, m = divmod(len(self.data), self.factor)
        for i in range(self.factor):
            table.append(self.data[i*k+min(i, m):(i+1)*k+min(i+1, m)])
        return table


    def separate_class(self):
        """
        Devide data into class.
        """
        separated = dict()
        for i in range(len(self.train_data)):
            vector = self.train_data[i]
            class_value = vector.get_quality()
            if (class_value not in separated):
                separated[class_value] = list()
            separated[class_value].append(vector)
        return separated


    def calculate_py(self):
        """
        Calculate P(y) probability.
        """
        for i in self.separated_data.keys():
            self.Py[i] = len(self.separated_data[i])/len(self.train_data)

    def train_model(self):

        for i in self.separated_data.keys():
            all_attr = {}
            for j in range(self.attr_num):

                mi = 0
                for x in self.separated_data[i]:
                    mi = mi + float(x.create_train_data()[j])
                    all_attr[j] = mi/len(self.separated_data[i])

            self.mi[i] = all_attr

        self.sigma = {}
        for i in self.separated_data.keys():
        
            all_attr = {}
            for j in range(self.attr_num):

                sigma = 0
                for x in self.separated_data[i]:
                    b = self.mi[i][j]
                    sigma = sigma + (float(x.create_train_data()[j]) - b)**2
                    all_attr[j] = sigma/len(self.separated_data[i])

            self.sigma[i] = all_attr

    def gaus(self, x, mi, sigma):
        if sigma == 0:
            sigma = 10**(-99)
        s = 1/(sqrt(2*pi*sigma))
        e = exp(-((x - mi)**2)/(2*sigma))

        return s*e 

    def test_model(self):
        correct = 0
        for q in self.test_data:

            all_p = {}
            for i in self.separated_data.keys():
                p = 1

                for j in range(self.attr_num):
                    p = p* self.gaus(float(q.create_train_data()[j]), self.mi[i][j], self.sigma[i][j])

                all_p[i] = self.Py[i] * p

            real_p = {}

            for z in all_p:
            
                real_p[z] = all_p[z]

            if max(real_p, key=real_p.get) == q.get_quality():
                correct +=  1


        self.err = 1 - (correct / len(self.test_data))     
        self.mean_error +=  self.err/self.n

















    


if __name__ == "__main__":
    pass
