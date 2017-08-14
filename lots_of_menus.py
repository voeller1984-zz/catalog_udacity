from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete Categories if exisitng.
session.query(Category).delete()
# Delete Items if exisitng.
session.query(Item).delete()
# Delete Users if exisitng.
#session.query(User).delete()



# Items for cat Soccer
category1 = Category(name="Soccer")

session.add(category1)
session.commit()

Item2 = Item(name="ShinGuards", category=category1, description="Juicy grilled veggie patty with tomato mayo and lettuce")

session.add(Item2)
session.commit()


Item3 = Item(name="Jersey", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                     category=category1)

session.add(Item3)
session.commit()

Item4 = Item(name="Soccer Cleats", description="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. ",
                     category=category1)

session.add(Item4)
session.commit()




# Items for cat Baseball
category2 = Category(name="Baseball")

session.add(category2)
session.commit()

Item2 = Item(name="Bat", description="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo",
                     category=category2)

session.add(Item2)
session.commit()


Item3 = Item(name="Baseball Jersey", description="Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
                     category=category2)

session.add(Item3)
session.commit()

Item4 = Item(name="helmet", description="At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident",
                     category=category2)

session.add(Item4)
session.commit()



# Items for cat Snowboarding
category3 = Category(name="Snowboarding")

session.add(category3)
session.commit()

Item2 = Item(name="Snowboard", description="Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat",
                     category=category3)

session.add(Item2)
session.commit()


Item3 = Item(name="Jacket", description="so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will",
                     category=category3)

session.add(Item3)
session.commit()

Item4 = Item(name="Googles", description="On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment",
                     category=category3)

session.add(Item4)
session.commit()



# Items for cat Skating
category4 = Category(name="Skating")

session.add(category3)
session.commit()

Item2 = Item(name="Skate", description="description skate",
                     category=category4)

session.add(Item2)
session.commit()


Item3 = Item(name="Shoes", description="description shoes for skating",
                     category=category4)

session.add(Item3)
session.commit()

Item4 = Item(name="Cool shirt", description="description shirt for skating",
                     category=category4)

session.add(Item4)
session.commit()


print "added menu items!"