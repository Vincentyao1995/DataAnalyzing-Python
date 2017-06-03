
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}
import math
class solution:
    def __init__(self,critics):
        self.critics = critics
    def get_sim_distance(self,person1,person2):
        res = 0
        for i in self.critics[person1]:
            if i in self.critics[person2]:
                res += pow((self.critics[person1][i]-self.critics[person2][i]),2)
        res = 1/(1+math.sqrt(res))
        return res
    def get_sim_pearson(self,person1,person2):
        sum1, sum2, sum1Sq,sum2Sq,sumPlus= 0,0,0,0,0
        sameItems = 0
        for i in self.critics[person1]:
            if i in self.critics[person2]:
                sameItems += 1
                sum1 += self.critics[person1][i]
                sum2 += self.critics[person2][i]
                sum1Sq += self.critics[person1][i]**2
                sum2Sq += self.critics[person2][i]**2
                sumPlus += self.critics[person1][i]*self.critics[person2][i]
        if sameItems == 0:
            return 0
        num = sumPlus-(sum1*sum2/sameItems)
        den = math.sqrt((sum1Sq-sum1**2/sameItems)*(sum2Sq-sum2**2/sameItems))
        if den ==0:
            return 0
        return num/den
    #this method input a person and return the most similar persons/items using comparing method sim,sim could be pearson and distance(default), return a list like [(Forrest Gump,0.5),(Speech of the King,0.7)] or [(James, 0.7), (Mike,0.1)]
    def get_most_similar(self,person, n= 5,sim = 'distance',result = 'similarities'):#result could be similarities(default) between persons or items; or 'name', name return the top match person's name; n is the number of return similarities.
        similarities = {}
        sim_distance = 0
        foundName = []
        for another_person in self.critics:
            if another_person == person:
                continue
            if sim == "distance":
                sim_distance = self.get_sim_distance(person,another_person)
            elif sim == 'pearson':
                sim_distance = self.get_sim_pearson(person,another_person)
            similarities.setdefault(another_person)
            similarities[another_person] = sim_distance
            sim_distance = 0
        
        #find the most similar one.
        max_similarity = max(similarities.values())
        #transfer dictionary to list.
        similarities_list  = similarities.items()
        if result == 'similarities':
            return list(similarities_list)[0:n]
        elif result =='name':
            for i in similarities:
                if similarities[i] == max_similarity:
                    foundName.append(i)
            return foundName
    # input a person's name, similarity comparing way, return a recomming movies list for this person according to similarities of other users.
    def get_recommendation(self,person,sim = 'pearson'):
        rankingList = {}
        total_weight = {}
        for another_person in self.critics:
            # ignore user himself
            if another_person == person:
                continue
            #cal similarity between user(person) and another one. 
            if sim =='pearson':
                sim_person = self.get_sim_pearson(person,another_person)
            elif sim == 'distance':
                sim_person = self.get_sim_distance(person,another_person)
            else:
                return ValueError
            if sim_person <=0 :
                continue
            for another_movie in self.critics[another_person]:
                if another_movie not in self.critics[person]:
                    #cal another movie's ranking score, and return the sorted ranking movies list.
                    rankingList.setdefault(another_movie,0)
                    total_weight.setdefault(another_movie,0)
                    weighted_sum = sim_person * self.critics[another_person][another_movie]
                    rankingList[another_movie] += weighted_sum
                    total_weight[another_movie] += sim_person
        rankings = [(rankingList[movie]/total_weight[movie],movie) for movie in rankingList]
        rankings.sort(reverse = True)
        return rankings
    # this method would transfer {List:{Rose:3.5}} to {Rose:{Lisa:3.5}}
    def transfer_prefs(self,changePrefs = False):
        newPrefs = {}
        for person in self.critics:
            for movie in self.critics[person]:
                newPrefs.setdefault(movie,{})
                newPrefs[movie].setdefault(person,0)
                newPrefs[movie][person] = self.critics[person][movie]
        if changePrefs:
            self.critics = newPrefs
        return newPrefs
	#calculate the similarities between items, return a chart that contains all similarities; you should save return list outside the class, and input this chart into get_recommendation_item, only do this could you save efficiency. not like now, using cal_sim_items method.
    def cal_sim_items(self,n = 10):
        result = {}
        prefsItem = self.transfer_prefs(changePrefs = True)
        self.prefsItem = prefsItem
        for item in prefsItem:
            sim_item = self.get_most_similar(item,sim = 'pearson',n = n)
            result[item] = sim_item
        #restore the critics to person:movie,score;person2:movie,socre
        self.transfer_prefs(changePrefs = True)
        return result
    # this method returns a list containing recommended items sorted by score. input a person.
    def get_recommendation_item(self,person):
        if person not in self.critics:
            raise ValueError('the person doesn\'t exist!')
        sim_items_list = {}
        sim_items_list = self.cal_sim_items()
        score_res = []
        for movie_new in self.prefsItem:
            sim_total = 0
            numerator_total = 0
            if not movie_new in self.critics[person]:
                for movie_seen in self.critics[person]:
                    sim_temp = 0
                    #search the similarities between movie_new and movie_seen. This is neccessary cuz sim_item_list is {movieA: (movie1, 0.1),(movie2,0.2); movieb:....} rather than {movieA:{movie1:0.1, movie2:0.2};movieB:....}
                    for i in sim_items_list[movie_new]:
                        if i[0] == movie_seen:
                            sim_temp = i[1]
                    # record score.
                    score_movie_seen = self.critics[person][movie_seen]
                    sim_total += sim_temp
                    numerator_total += sim_temp * score_movie_seen
                score_res.append((movie_new,numerator_total/sim_total))
                score_res.sort(key = lambda x : x[1], reverse = True) 
        return score_res
    def loadData(self,path = 'data/movieLens'):
        movies = {}
        file_item = open(path+'/u.item',encoding = 'utf-8')
        for line in file_item:
            (movieID,movieName) = line.split('|')[0:2]
            movies[movieID] = movieName
        file_item.close()
        dataset = {}
        file_data = open(path+'/u.data',encoding = 'utf-8')
        for line in file_data:
            (userID, movieID, movieScore,ts) = line.split('\t')
            dataset.setdefault(userID,{})
            dataset[userID][movies[movieID]] = movieScore
        return dataset
if __name__ == '__main__':
	s = solution(critics)
	res = s.get_recommendation_item('Toby')
	print(res)
