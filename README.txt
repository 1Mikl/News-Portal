py manage.py shell
from news.models import * 	
	
	
	СОЗДАТЬ ДВУХ ПОЛЬЗОВАТЕЛЕЙ (С ПОМОЩЬЮ МЕТОДА USER.OBJECTS.CREATE_USER('USERNAME')).


u1 = User.objects.create_user(username='Andrey.K.')   #создал пользователя
u2 = User.objects.create_user(username='Vladimir.V.')   #создал пользователя


	СОЗДАТЬ ДВА ОБЪЕКТА МОДЕЛИ AUTHOR, СВЯЗАННЫЕ С ПОЛЬЗОВАТЕЛЯМИ.


Author.objects.create(authorUser=u1)   #создал автора
Author.objects.create(authorUser=u2)    #создал автора


	ДОБАВИТЬ 4 КАТЕГОРИИ В МОДЕЛЬ CATEGORY.


Category.objects.create(name='IT')
Category.objects.create(name='Internet')
Category.objects.create(name='Science and technology‎')
Category.objects.create(name='Ratings')


	ДОБАВИТЬ 2 СТАТЬИ И 1 НОВОСТЬ.
	
	
author = Author.objects.get(id=1) #переходим к автору 1

Post.objects.create(author=author, categoryType='NW', title='games for everyone', text='Many children start playing computer games at the age of 4 or 5.')

author = Author.objects.get(id=2) #переходим к автору 2

Post.objects.create(author=author, categoryType='AR', title='COMPUTER GAMES', text='Some years ago computer games were quite simple and rare and the scientific research concluded that they stimulated good results at school and at work. ')

Post.objects.create(author=author, categoryType='AR', title='FAST FOOD', text='We all love hamburgers, fried fries, and various sauces. But everyone knows that fast food is bad for health. At the same time, people do not want to give up such tasty, but very harmful food. ')


	ПРИСВОИТЬ ИМ КАТЕГОРИИ (КАК МИНИМУМ В ОДНОЙ СТАТЬЕ/НОВОСТИ ДОЛЖНО БЫТЬ НЕ МЕНЬШЕ 2 КАТЕГОРИЙ).
	
	
Post.objects.get(id=1).postCategory.add(Category.objects.get(id=1))
Post.objects.get(id=2).postCategory.add(Category.objects.get(name='IT'))
Post.objects.get(id=3).postCategory.add(Category.objects.get(id=4))
Post.objects.get(id=3).postCategory.add(Category.objects.get(name='Internet'))


	Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).


Comment.objects.create(commentPost=Post.objects.get(title='games for everyone'), commentUser=Author.objects.get(id=1).authorUser, text='If you can not completely refuse fast food, you should be more particular about pro
ducts when choosing the menu. It is advisable to stop preference on dietary dishes, vegetable salads with olive oil.')
 
 
Comment.objects.create(commentPost=Post.objects.get(title='COMPUTER GAMES'), commentUser=Author.objects.get(id=2).authorUser, text='Do not use spices, mayonnaise and fatty sauces. It is very important to chew food thoro
ughly and never to drink carbonated water. All these rules will help to fans of fast food to reduce the risk of disease. ')

Comment.objects.create(commentPost=Post.objects.get(title='COMPUTER GAMES'), commentUser=Author.objects.get(id=2).authorUser, text='Soou GooD')


Comment.objects.create(commentPost=Post.objects.get(title='FAST FOOD'), commentUser=Author.objects.get(id=2).authorUser, text='Very BAD ')



	ПРИМЕНЯЯ ФУНКЦИИ LIKE() И DISLIKE() К СТАТЬЯМ/НОВОСТЯМ И КОММЕНТАРИЯМ, СКОРРЕКТИРОВАТЬ РЕЙТИНГИ ЭТИХ ОБЪЕКТОВ.
	
	
Comment.objects.get(id=1).like()
Post.objects.get(title='COMPUTER GAMES').like()
Post.objects.get(title='FAST FOOD').dislike()
Post.objects.get(title='games for everyone').like()
Comment.objects.get(text='Soou GooD').like()
Comment.objects.get(id=1).rating
Comment.objects.get(id=2).dislike()
Post.objects.get(title='COMPUTER GAMES').like()
>>> Post.objects.get(title='COMPUTER GAMES').like()
>>> Post.objects.get(title='COMPUTER GAMES').like()
>>> Post.objects.get(title='COMPUTER GAMES').like()
>>> Post.objects.get(title='COMPUTER GAMES').like()
>>> Post.objects.get(title='FAST FOOD').dislike()
>>> Post.objects.get(title='FAST FOOD').dislike()
>>> Post.objects.get(title='games for everyone').like()
>>> Comment.objects.get(text='Soou GooD').like()
>>> Comment.objects.get(text='Soou GooD').like()
>>> Comment.objects.get(id=1).dislike()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()
>>> Comment.objects.get(id=2).like()

	
	ОБНОВИТЬ РЕЙТИНГИ ПОЛЬЗОВАТЕЛЕЙ.
	
	
Author.objects.get(id=1)
a = Author.objects.get(id=1)
a.update_rating()
a.ratingAuthor

Post.objects.get(id=1).like()

a.update_rating()
a.ratingAuthor

b = Author.objects.get(id=2)
b.update_rating()
b.ratingAuthor


	ВЫВЕСТИ USERNAME И РЕЙТИНГ ЛУЧШЕГО ПОЛЬЗОВАТЕЛЯ (ПРИМЕНЯЯ СОРТИРОВКУ И ВОЗВРАЩАЯ ПОЛЯ ПЕРВОГО ОБЪЕКТА).
	
	
c = Author.objects.order_by('-ratingAuthor')[:1]
c

for i in c:
	i.ratingAuthor
	i.authorUser.username
	

	ВЫВЕСТИ ДАТУ ДОБАВЛЕНИЯ, USERNAME АВТОРА, РЕЙТИНГ, ЗАГОЛОВОК И ПРЕВЬЮ ЛУЧШЕЙ СТАТЬИ, ОСНОВЫВАЯСЬ НА ЛАЙКАХ/ДИСЛАЙКАХ К ЭТОЙ СТАТЬЕ.


a = Post.objects.order_by('-rating').values('dateCreation', 'author__authorUser__username', 'rating', 'title')[0]
a
Post.objects.order_by('-rating')[0].preview().


	ВЫВЕСТИ ВСЕ КОММЕНТАРИИ (ДАТА, ПОЛЬЗОВАТЕЛЬ, РЕЙТИНГ, ТЕКСТ) К ЭТОЙ СТАТЬЕ.


Post.objects.order_by('-rating')[0].comment_set.all().values('dateCreation', 'commentUser', 'rating', 'text')


