import csv
import operator
import math


class User:
    def __init__(self, row):
        self.user = row[0]
        self.age = row[1]
        self.gender = row[2]
        self.occupation = row[3]
        self.zcode = row[4]
        self.ratings = []

    def parse_users(datafile):
        with open(datafile, encoding='latin_1') as f:
            user_lib = {}
            reader = csv.reader(f, delimiter='|')
            print('2222222')
            for row in reader:
                user_lib[int(row[0])] = User(row)
            return user_lib

    def __str__(self):
        return "{}: {}".format(self.user, self.gender)

    def append_ratings(self, rating):
        self.ratings.append(rating)


class Movie:
    def __init__(self, row):
        self.movieid = int(row[0])
        self.title = row[1]
        self.rdate = row[2]
        self.vrdate = row[3]
        self.imdburl = row[4]
        genre_dict = {
            0: 'Unknown', 1: 'Action', 2: 'Adventure', 3: 'Animation',
            4: 'Childrens', 5: 'Comedy', 6: 'Crime', 7: 'Documentary',
            8: 'Drama', 9: 'Fantasy', 10: 'Film-Noir', 11: 'Horror',
            12: 'Musical', 13: 'Mystery', 14: 'Romance', 15: 'Sci-Fi',
            16: 'Thriller', 17: 'War', 18: 'Western'}
        genre_list = [genre_dict[idx] for idx, item in enumerate(row[5:]) if item == '1']
        self.genres = genre_list
        self.ratings = []

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    def append_ratings(self, rating):
        self.ratings.append(rating)
        self.avgrating = sum(self.ratings)/len(self.ratings)

    def avg_rating(self):
        return self.avgrating

    def parse_movies(datafile):
        with open(datafile, encoding='latin_1') as f:
            movie_lib = {}
            reader = csv.reader(f, delimiter='|')
            print('1111111')
            for row in reader:
                movie_lib[int(row[0])] = Movie(row)
            return movie_lib

    def find_movie(idno, mdict):
        return mdict[idno].title

    def get_top_movies(mlist):
        top = int(input("How many top movies do you want to see? "))
        new_list = []
        for movie in mlist.values():
            if len(movie.ratings) >= 10:
                new_list.append(movie)
        return sorted(new_list, key=operator.attrgetter('avgrating'), reverse=True)[:top]

    def get_unseen_top_movies(mlist, ulist):
        user = int(input("Which user? "))
        user_ratings = ulist[user].ratings
        seen_list = [item[0] for item in user_ratings]
        new_list = []
        for movie in mlist.values():
            if len(movie.ratings) >= 10:
                if movie.movieid not in seen_list:
                    new_list.append(movie)
        return sorted(new_list, key=operator.attrgetter('avgrating'), reverse=True)[:10]

    def get_shared_list(user1, user2, mlist, ulist):
        user1_movies = [item for item in ulist[user1].ratings]
        user2_movies = [item for item in ulist[user2].ratings]
        both_seen = [x for x in user1_movies if any(x[0]==y[0] for y in user2_movies)]
        both_seen2 = [x for x in user2_movies if any(x[0]==y[0] for y in user1_movies)]
        both_seen = sorted(both_seen, key=lambda tup: tup[0])
        both_seen2 = sorted(both_seen2, key=lambda tup: tup[0])
        both_seen = [x[1] for x in both_seen]
        both_seen2 = [x[1] for x in both_seen2]
        return both_seen, both_seen2

    def euclid_distance(user_list1, user_list2):
        if len(user_list1) is 0:
            return 0
        differences = [user_list1[idx] - user_list2[idx] for idx in range(len(user_list1))]
        squares = [diff ** 2 for diff in differences]
        sum_of_squares = sum(squares)
        return 1 / (1 + math.sqrt(sum_of_squares))

    def compare_two_users(mlist, ulist):
        u1 = int(input("Please enter user 1: "))
        u2 = int(input("Please enter user 2: "))
        user1, user2 = Movie.get_shared_list(u1, u2, mlist, ulist)

        return Movie.euclid_distance(user1, user2)


class Rating:
    def __init__(self, row):
        self.user = row[0]
        self.movieid = row[1]
        self.rating = row[2]
        self.timestamp = row[3]

    def __str__(self):
        return "{}, {}, {}, {}".format[self.user, self.movieid, self.rating, self.timestamp]

    def parse_ratings(datafile, movie_lib, user_lib):
        with open(datafile) as f:
            reader = csv.reader(f, delimiter='\t')
            print('------')
            for row in reader:
                movie_lib[int(row[1])].append_ratings(int(row[2]))
                user_lib[int(row[0])].append_ratings((int(row[1]), int(row[2])))


def main():
    movie_lib = Movie.parse_movies('ml-100k/u.item')
    user_lib = User.parse_users('ml-100k/u.user')
    Rating.parse_ratings('ml-100k/u.data', movie_lib, user_lib)

    euc = Movie.compare_two_users(movie_lib, user_lib)
    print(euc)

if __name__ == "__main__":
    main()
