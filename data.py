import h5py
import numpy as np


class Data:

    def __init__(self, name, max_size: int = 10_000):
        self.max_size = max_size
        self.name = f"{name}.h5"
        self.nums_files_name()

    def nums_files_name(self):
        try:
            nums = len(h5py.File(self.name, 'r'))
            self.nums = nums // 3 + nums % 3 - 1
        except FileNotFoundError:
            self.nums = 0
            self.create_new_dataset()

        self.status_data_set()

    def create_new_dataset(self):
        print(f"\n*****\nCreate New DS {self.nums}")
        h5py.File(self.name, 'a').create_dataset(f'graph256_{self.nums}', (1, 256, 256), maxshape=(None, 256, 256), dtype='i8')
        h5py.File(self.name, 'a').create_dataset(f'points16_{self.nums}', (1, 16, 16), maxshape=(None, 16, 16), dtype='i8')
        h5py.File(self.name, 'a').create_dataset(f'result16_{self.nums}', (1, 16, 16), maxshape=(None, 16, 16), dtype='i8')
        print("\tFull Create")

        print(list(h5py.File(self.name, 'r')), "*****\n")

    def status_data_set(self):
        try:
            size = np.array(
                h5py.File(self.name, 'r')[f'result16_{self.nums}']
            ).shape[0]
        except KeyError:
            print(list(h5py.File(self.name, 'r')))
            raise KeyError

        if size > self.max_size:
            self.nums += 1
            self.create_new_dataset()

    def return_datasets(self) -> dict:
        """
        :return:  dict {
                        graph256_{self.nums} : data graph - np.array , shape = (None, 256, 256)
                        points16_{self.nums} : data points - np.array , shape = (None, 16, 16)
                        result16_{self.nums} : data result - np.array , shape = (None, 16, 16)
                    }
        """

        ds = {
            f'{i}_{self.nums}': np.array(h5py.File(self.name, 'r')[f'{i}_{self.nums}'])
            for i in ("graph256", "points16", "result16")
        }

        return ds

    @staticmethod
    def restruct_data(data) -> tuple:

        nums = len(data)
        new_graph = np.zeros((nums, 256, 256), dtype=np.int8)
        new_points = np.zeros((nums, 16, 16), dtype=np.int8)
        new_result = np.zeros((nums, 16, 16), dtype=np.int8)

        i = 0
        for g, sf, r in data:
            new_graph[i] = g
            new_points[i] = sf
            new_result[i] = r
            i += 1

        return new_graph, new_points, new_result

    def write(self, data):
        """
         data = [
            (
                graph.graph,                1 256 256
                graph.start_finish,         1 16 16
                graph.graph_table_result    1 16 16
            )
        ]
        :param data:
        :return:
        """
        try:
            self.nums_files_name()
        except KeyError:
            print(list(h5py.File(self.name, 'r')))
            raise KeyError

        data_sets = self.return_datasets()
        dg, dp, dr = self.restruct_data(data)

        for ds in data_sets:
            res = None

            if "graph256" in ds:
                res = dg

            elif "points16" in ds:
                res = dp
            elif "result16" in ds:
                res = dr

            result = np.append(data_sets[ds], res, axis=0)
            if "graph256" in ds:
                print(f"data = shape {result.shape[0]}")

            h5py.File(self.name, 'a')[ds].resize(result.shape)
            h5py.File(self.name, 'a')[ds][:] = result

    def config_iter(self, batch=64, get=None):

        self.get = get
        if get is None:
            self.get = self.__len__()
        self.batch = batch

    def __gen(self):

        for n in range(self.get):
            x =  np.array(h5py.File(self.name, 'r')[f"graph256_{n}"])
            x2 = np.array(h5py.File(self.name, 'r')[f"graph256_{n}"])
            y = np.array(h5py.File(self.name, 'r')[f"graph256_{n}"])

            if x.shape[0] != x2.shape[0] != y.shape[0]:
                print("Не соответствует длинна")
                continue

            temp = self.batch
            for batch in range(0, x.shape[0], self.batch):
                yield x[batch:temp], x2[batch:temp], y[batch:temp]
                temp = temp + self.batch

    def drop_data_in_file(self, n: int):

        with h5py.File(self.name, 'r') as f:
            x = f[f"graph256_{n}"]
            x2 = f[f"graph256_{n}"]
            y = f[f"graph256_{n}"]

            return x, x2, y

    def __iter__(self):
        if not self.__dict__.get("batch", False):
            self.config_iter()

        self.generator = self.__gen()
        return self.generator

    def __next__(self):
        return next(self.generator)

    def __len__(self):
        nums = len(h5py.File(self.name, 'r'))
        return nums // 3 + nums % 3
