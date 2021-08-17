# for saving scores in file
import shelve


class Scores:
    # numbers of best scores to save
    x_saves = 5
    file = 'score.dat'
    scores = []

    def __init__(self):
        # print(" init run ")
        try:
            with shelve.open(self.file, 'c') as shelf:
                # print("ok")
                try:
                    temp = shelf['scores']
                except:
                    shelf['scores'] = [[0, '...']]
                    shelf.sync()
                    # print('')
                    return
        except:
            print("init error")

    def get_scores(self):

        with shelve.open(self.file, 'c') as shelf:
            self.scores = shelf['scores']
        return self.scores

    def set_score(self, score, name='Name ...'):
        data = [[]]
        data = self.get_scores()

        # open files with score saves
        with shelve.open(self.file, 'c', writeback=True) as shelf:
            shelf['scores'] = [[score, name]]
            data = data + shelf['scores']
            data = sorted(data, key=lambda x: x[0], reverse=True)
            data = data[:self.x_saves]
            shelf['scores'] = data
            shelf.sync()
