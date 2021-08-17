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
            # function checking if file exist, and create new if not exists
            with shelve.open(self.file, 'c') as shelf:
                # print("ok")
                try:
                    # try get data from 'scores' field, if not exist create new field
                    temp = shelf['scores']
                except:
                    shelf['scores'] = [[0, '...']]
                    
                    # update file with saved scores
                    shelf.sync()
                    # print('')
                    return
        except:
            print("init error")

    def get_scores(self):
        # get saved data with best scores
        with shelve.open(self.file, 'c') as shelf:
            self.scores = shelf['scores']
            
        # return list with saved best scores
        return self.scores

    def set_score(self, score, name='Name ...'):
        data = [[]]
        data = self.get_scores()

        # open files with score saves
        with shelve.open(self.file, 'c', writeback=True) as shelf:
            
            # add information about new score to varialbe
            shelf['scores'] = [[score, name]]
            
            # add new information to all previously saved best scores
            data = data + shelf['scores']
            
            # sorted data, from higest scores to lowest scores
            data = sorted(data, key=lambda x: x[0], reverse=True)
            
            # get first (n) rows from data
            data = data[:self.x_saves]
            
            
            shelf['scores'] = data
            
            # update information about best scores and save to file
            shelf.sync()
