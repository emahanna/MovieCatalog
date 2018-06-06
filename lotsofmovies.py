from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from database_setup import Genre, Base, Movie, User

engine = create_engine('sqlite:///movieswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bing = engine


DBSession = sessionmaker(bind=engine)
# Establishes connection to database in the form of a staging area
session = DBSession()


# Dummy user
User1 = User(name="Koda Bot", email="koda_bot2018@gmail.com")
session.add(User1)
session.commit()

# Movies for Comedy
genre1 = Genre(user_id=1, name="Comedy",
               description="""Comedy's main emphasis is on humor, and are designed
               to make the audience laugh. These movies
               typically have happy endings.""")

session.add(genre1)
session.commit()

movie1 = Movie(user_id=1, genre=genre1, name="Ghost Busters",
               release_date="June 8, 1994",
               description="""A team of four paranormal investigators go after
               ghosts and ghouls in an attempts to save the city.""")

session.add(movie1)
session.commit()

movie2 = Movie(user_id=1, genre=genre1, name="Bridesmaids",
               release_date="April 28, 2011",
               description="""A single women learns her bestfriend is engaged,
               and she has no choice but to serve as the maid of honor.""")

session.add(movie2)
session.commit()

movie3 = Movie(user_id=1, genre=genre1, name="The Hangover",
               release_date="June 2, 2009",
               description="""Two days before his wedding, Doug (Justin Bartha)
               and three friends (Bradley Cooper,
               Ed Helms, Zach Galifianakis) drive to
               Las Vegas for a wild and memorable stag party.""")

session.add(movie3)
session.commit()

movie4 = Movie(user_id=1, genre=genre1, name="Ace Ventura: Pet Detective",
               release_date="February 4, 1994",
               description="""When the dolphin mascot of
               Miami's NFL team is abducted,
               Ace Ventura (Jim Carrey), a zany private
               investigator who specializes in
               finding missing animals, looks into the case.""")

session.add(movie4)
session.commit()


# Movies for Action & Adventure
genre2 = Genre(user_id=1, name="Action & Adventure", description="""Action & Adventure
    movies are designed to bring an exciting,
    energetic experience to the film viewer.""")

session.add(genre2)
session.commit()

movie5 = Movie(user_id=1, genre=genre2, name="Cast Away",
               release_date="December 7, 2000",
               description="""Obsessively punctual FedEx
                executive Chuck Noland (Tom Hanks)
               is en route to an assignment in Malaysia when his plane crashes
               over the Pacific Ocean during a storm.""")

session.add(movie5)
session.commit()

movie6 = Movie(user_id=1, genre=genre2,
               name="The Hobbit: The Desolation of Smaug",
               release_date="December 13, 2013",
               description="""Having survived the first part of their
                            unsettling journey,
                            Bilbo Baggins (Martin Freeman)
                            and his companions (Ian McKellen, Richard Armitage)
                            continue east to the Lonely Mountain,
                            where they face the greatest danger
                            of all: the fearsome
                            dragon Smaug (Benedict Cumberbatch).""")

session.add(movie6)
session.commit()

movie7 = Movie(user_id=1, genre=genre2, name="Star Wars: The Last Jedi",
               release_date="December 15, 2017",
               description="""Luke Skywalker's peaceful and solitary existence
               gets upended when he encounters Rey,
                young woman who shows strong signs of the Force.""")

session.add(movie7)
session.commit()

movie8 = Movie(user_id=1, genre=genre2, name="300",
               release_date="March 9, 2007",
               description=""""At the Battle of Thermopylae, Leonidas (Gerard Butler),
               king of the Greek city state of Sparta, leads his badly
               outnumbered warriors against the massive Persian army.""")

session.add(movie8)
session.commit()

# Movies for Drama
genre3 = Genre(user_id=1, name="Drama",
               description="""Drama is intended to be more serious than humorous,
               and foucus on development of characters who must deal
               with emotional struggles and strife.""")

session.add(genre3)
session.commit()

movie9 = Movie(user_id=1, genre=genre3, name="A Beautiful Mind",
               release_date="Devember 21, 2001",
               description="""A human drama inspired by events in the life of
               John Forbes Nash Jr., and in part based on the biography,
               A Beautiful Mind, by Sylvia Nasar.""")

session.add(movie9)
session.commit()

movie10 = Movie(user_id=1, genre=genre3, name="The Pianist",
                release_date="December 4, 2002",
                description="""The Extraordinary True Story of
                One Man's Survival in Warsaw,
                1939-1945, Wladyslaw Szpilman
                (Adrien Brody), a Polish Jewish radio
                station pianist, sees Warsaw change gradually
                as World War II begins.""")

session.add(movie10)
session.commit()

movie11 = Movie(user_id=1, genre=genre3, name="Million Dollar Baby",
                release_date="December 15, 2004",
                description="""Frankie Dunn (Clint Eastwood) is a veteran Los Angeles
                boxing trainer who keeps almost everyone
                at arm's length, when Maggie
                Fitzgerald (Hilary Swank) arrives in
                Frankie's life seeking his expertise,
                he is reluctant to train the young woman,
                a transplant from working-class Missouri.""")

session.add(movie11)
session.commit()

movie12 = Movie(user_id=1, genre=genre3, name="Goodfellas",
                release_date="September 19, 1990",
                description="""A young man grows up in the mob and works
                very hard to advance himself through the ranks.""")

session.add(movie12)
session.commit()

# Movies for Horror
genre4 = Genre(user_id=1, name="Horror",
               description="""A type of movie that is intended to
               scare of frighten the audience.""")

session.add(genre4)
session.commit()

movie13 = Movie(user_id=1, genre=genre4, name="The Sixth Sense",
                release_date="August 6, 1999",
                description="""Young Cole Sear (Haley Joel Osment) is
                haunted by a dark secret: he is visited by ghosts.""")

session.add(movie13)
session.commit()

movie14 = Movie(user_id=1, genre=genre4, name="Frankenstein",
                release_date="November 21, 1931",
                description=""""This iconic horror film follows the obsessed scientist
                Dr. Henry Frankenstein (Colin Clive) as he attempts to
                create life by assembling a creature
                from body parts of the deceased.""")

session.add(movie14)
session.commit()

movie15 = Movie(user_id=1, genre=genre4, name="The Conjuring",
                release_date="July 19, 2013",
                description="""The Perrons and their five daughters have recently
                moved into a secluded farmhouse, where a supernatural
                presence has made itself known.""")

session.add(movie15)
session.commit()

movie16 = Movie(user_id=1, genre=genre4, name="Jaws",
                release_date="June 20, 1975",
                description="""When a young woman is killed
                by a shark while skinny-dipping
                near the New England tourist town of Amity Island, police chief
                Martin Brody (Roy Scheider) wants to
                close the beaches, but mayor
                Larry Vaughn (Murray Hamilton) overrules him, fearing that the
                loss of tourist revenue will cripple the town.""")

session.add(movie16)
session.commit()

# Movies for Mystery
genre5 = Genre(user_id=1, name="Mystery",
               description="""A mystery follows an investigator as
               he/she attempts to solve a puzzle.""")

session.add(genre5)
session.commit()

# Movies for Thriller
genre6 = Genre(user_id=1, name="Thriller",
               description="""A thriller is a story that is
               typically a mix of fear and excitement.""")

session.add(genre6)
session.commit()

print ("All movies added!")
