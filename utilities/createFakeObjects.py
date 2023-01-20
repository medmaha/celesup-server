# import random
# from faker import Faker
# from faker.providers import BaseProvider

# from users.models import User

# from post.models import Post

# from django.db import transaction


# fake = Faker()


# # User.objects.filter().delete()
# # Post.objects.filter().delete()

# # create new provider class


# class FakePost:
#     def __init__(self) -> None:
#         self.author = random.choice(User.objects.all())
#         self.caption = fake.text()[: random.choice([10, 20, 35, 50, 75, 100])]
#         self.excerpt = fake.text()[
#             : random.choice([15, 100, 150, 200, 500, 250, 350, 175, 400, 300, 600, 700])
#         ]

#         self.hashtag = "#{}, #{}, #{}".format(
#             fake.email().split("@")[0],
#             fake.email().split("@")[0],
#             fake.email().split("@")[0],
#         )


# def createFakePost(count=50):
#     with transaction.atomic():
#         print("started writing fake posts")
#         for _ in range(count):
#             post = FakePost()
#             Post.objects.create(
#                 author=post.author,
#                 caption=post.caption,
#                 excerpt=post.excerpt,
#                 hashtags=post.hashtag,
#             )

#         print("done writing fake posts")


# class FakeUser:
#     def __init__(self) -> None:
#         self.email = fake.unique.email()
#         self.first_name = fake.first_name()
#         self.last_name = fake.last_name()
#         self.username = fake.unique.name().replace(" ", "").replace(".", "").lower()
#         self.password = fake.password()
#         self.city = fake.address()
#         self.gender = random.choice(["Male", "Female"])
#         self.biography = fake.text()[
#             : random.choice([50, 75, 25, 100, 150, 250, 200, 40, 120, 190, 15])
#         ]


# def createFakeUsers(count=50):

#     with transaction.atomic():
#         print("started writing fake users")
#         for _ in range(count):
#             user = FakeUser()

#             _user = User(
#                 email=user.email,
#                 password=user.password,
#                 username=user.username,
#                 first_name=user.first_name,
#                 last_name=user.last_name,
#                 city=user.city,
#                 biography=user.biography,
#             )
#             _user.set_password(user.password)
#             _user.save()
#         print("done writing fake users")
