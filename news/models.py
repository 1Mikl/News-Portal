from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

# Create your models
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # def __str__(self):
    #     return self.authorUser



    def update_rating(self):
        posRat = self.post_set.aggregate(postRat=Sum('rating'))
        pRat = 0
        pRat += posRat.get('postRat') if posRat.get('postRat') else 0

        commentRat = self.authorUser.comment_set.aggregate(commRat=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commRat') if commentRat.get('commRat') else 0

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')


    def __str__(self):
        return self.name

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES=(
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through="postCategory")
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    # category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='posts')

    def preview(self):
        preview = f'{self.text[:124]} ...'
        return preview

    # def __str__(self):
    #     return f'{self.title} | {self.author}'


    def __str__(self):
        return self.title
    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    # def preview(self):
    #     return self.text[0:123] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )