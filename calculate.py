class FileFormatError(Exception):
    pass

class Month:
    def __init__(self, file, name = None):
        '''
        '''
        self.file = file # should be an opened file, such as file = open("ex.txt", "r")
        if name is None:
            self.name = file.name[:-4]
        else:
            self.name = name
        self.necessary = 0
        self.personal = 0
        self.categories = {"grocery": 0,
        "food": 0,
        "treat": 0,
        "personal": 0,
        "school": 0,
        "cash": 0,
        "clothes": 0} # keywords used in file
        #self.load_keys()
        self.calculate()
        '''def load_keys(self):
        ''fills in dictionary with the categories for that month
        should only run once (during init)''
        for line in self.file:
            if line == "Keys:":
                break
        
        for line in self.file:
            if line.split() == ['']:
                break
            self.categories[line] = 0'''
    def calculate(self): # fills in values with data from file
        try:
            next(self.file) # skips first line
        except StopIteration or ValueError:
            temp = self.file.name
            self.file.close()
            self.file = open(temp, "r")
        
        for line in self.file:
            a = line.split()
            try:
                val = float(a[0])
            except ValueError:
                raise FileFormatError("\nattempted to convert non-number " + a[0] + " to a float. check file and try again")
                return
            try:
                self.categories[a[1]] += val
            except KeyError:
                raise FileFormatError("\ncheck your keys! could not process '" + str(a[1]) + "' " + str(a[-1]))
            if a[2] == 'n':
                self.necessary += val
            elif a[2] == 'sp':
                self.necessary += val/2
                self.personal += val/2
            else:
                self.personal += val
        self.file.seek(0) # go back to start of file
        
    def compare(self, other):
        '''
        gives the values of self relative to other
        ex. 2x spend on school in self
        ex. 10 dollars (more) spent on school in self
        '''
        if type(other) != Month:
            raise TypeError(str(type(other)) + ' is not a month')
        if self.personal + self.necessary == 0:
            raise ValueError('nothing has been spent so far in ' + self.name)
        if other.personal + other.necessary == 0:
            raise ValueError('nothing has been spent so far in ' + other.name)
        
        lines = ['values of ' + self.name + ' relative to ' + other.name, 'ex. $10 more spent in ' + self.name + ' than '  + other.name]
        if other.necessary: # if value isnt equal to zero
            times = self.necessary / other.necessary
            diff = self.necessary - other.necessary
            lines.append(f'necessary: {times:0.3f}x\t{diff:0.2f}')
        else:
            lines.append('nothing spent on necessary items in ' + other.name)
        if other.personal: # if value isnt equal to zero
            times = self.personal / other.personal
            diff = self.personal - other.personal
            lines.append(f'personal : {times:0.3f}x\t{diff:0.2f}')
        else:
            lines.append('nothing spent on personal items in ' + other.name)
        for it in self.categories:
            if other.categories[it]: # if value isnt equal to zero
                times = self.categories[it] / other.categories[it]
                diff = self.categories[it] - other.categories[it]
                lines.append(f'{it:9s}: {times:0.3f}x\t{diff:0.2f}')
            else:
                lines.append('nothing spent on ' + it + ' in ' + other.name)
        return '\n'.join(lines)
        
    def get_necessary(self):
        return self.necessary
    
    def get_personal(self):
        return self.personal
        
    def get_categories(self):
        return self.categories
        
    def close(self):
        self.file.close()
                
    def __str__(self):
        lines = []
        lines.append(f"necessary: {self.necessary:0.2f}")
        lines.append(f"personal : {self.personal:0.2f}")
        for it in self.categories:
            try:
                percent = self.categories[it]*100/(self.necessary + self.personal)
            except ZeroDivisionError:
                return "no money has been spent so far!"
            lines.append(f"{it:9s}: {percent:0.3f}%\t{self.categories[it]:0.2f}")
        return "\n".join(lines)
        
    def __repr__(self):
        lines = []
        lines.append(f"necessary = {self.necessary}")
        lines.append(f'personal = {self.personal}')
        for it in self.categories:
            lines.append(f'{it}: {self.categories[it]}')
        return ', '.join(lines)
        
    def __lt__(self, other):
        # compares total amount of money spent each month
        if type(other) != Month:
            raise TypeError(str(type(other)) + ' is not a month')
        return (self.necessary + self.personal) < (other.necessary + other.personal)
        
    def __gt__(self, other):
        # compares total amount of money spent each month
        if type(other) != Month:
            raise TypeError(str(type(other)) + ' is not a month')
        return (self.necessary + self.personal) > (other.necessary + other.personal)
        
    def __eq__(self, other):
        # compares total amount of money spent each month
        if type(other) != Month:
            raise TypeError(str(type(other)) + ' is not a month')
        return (self.necessary + self.personal) == (other.necessary + other.personal)
        
def comp():
    second = input('enter the baseline month\n')
    secondObj = get_month(second)
    if secondObj is None:
        return
    first = input('enter the other month\n')
    firstObj = get_month(first)
    if firstObj is None:
        return
    print(firstObj.compare(secondObj))
    
def get_month(name):
    # returns month object and creates it if it doesn't already exist
    if name.lower() in months:
        return months[name.lower()]
    try:
        m = Month(open(name.lower() + ".txt", "r"), name)
        months[name.lower()] = m
        return m
    except FileNotFoundError:
        print(name + '.txt was not found')
    
if __name__ == "__main__":
    months = {}
    while True:
        name = input("enter month name, 'compare', or 'close'\n")
        if name == 'close':
            for m in months:
                months[m].close()
            break
        elif name == 'compare':
            comp()
        else:
            m = get_month(name)
            if m is not None:
                print(m)
