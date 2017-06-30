class Session:

    def __init__(self):
        self.name = str(datetime.datetime.now()) + " " + options["name_method"]
        self.files = {}

    def acumulate(keys, values):
        for key in keys:
            pass

    def append_vals_to_csv(self, name_file, vals):
        keys = sorted(list(vals.keys()))
        name_file_full = "sessions/" + self.name + "/" + name_file
        if name_file_full not in self.files:
            if not os.path.exists(os.path.dirname(name_file_full)):
                os.makedirs(os.path.dirname(name_file_full))
            if not os.path.exists(name_file_full):
                fd = open(name_file_full, 'w')
                self.files[name_file_full] = fd
                writer_csv = csv.writer(
                    fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer_csv.writerow(keys)
        # else:
        writer_csv = csv.writer(
            self.files[name_file_full],
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
        vs = [vals[key] for key in keys]
        writer_csv.writerow(vs)
        #str_row=','.join(map(str, vs))
        # self.files[name_file].write(str_row+"\n")
        # fd.close()

    def __del__(self):
        for key in self.files:
            self.files[key].close()

    def flush(self):
        for key in self.files:
            self.files[key].close()
            self.files[key] = open(key, 'a')
# session=Session()
