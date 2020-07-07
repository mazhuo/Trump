

from django.db import models

# Create your models here.

class NewsPiece(models.Model):
	news_title = models.CharField(max_length=200)
	news_content = models.CharField(max_length=10000)
	pub_date = models.CharField(max_length=200)
	news_abstract = models.CharField(max_length=200)
	def __str__(self):
		return self.news_title

class Tag(models.Model):
	newspiece = models.ForeignKey(
		NewsPiece, 
		on_delete=models.CASCADE, 
	)
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class ContentTag(models.Model):
	newspiece = models.ForeignKey(
		NewsPiece,
		on_delete=models.CASCADE,
	)
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class Student(models.Model):
	news_title = models.CharField(max_length=200)

class news_test(models.Model):
	news_id = models.IntegerField(primary_key = True)
	news_title = models.CharField(max_length=200,blank=True)
	new_data = models.CharField(max_length=200,blank=True)
	news_content = models.CharField(max_length=10000,blank=True)
	news_emotion = models.CharField(max_length=200,blank=True)
	news_comment = models.CharField(max_length=10000,blank=True)
	def __str__(self):
		return self.news_title

class trump(models.Model):
	news_id = models.IntegerField(primary_key = True)
	news_title = models.CharField(max_length=200)
	new_date = models.CharField(max_length=200)
	news_content = models.CharField(max_length=10000)
	news_emotion = models.CharField(max_length=200)
	news_comment = models.CharField(max_length=10000)
	def __str__(self):
		return self.news_title

class trump1(models.Model):
	news_id = models.IntegerField(primary_key = True)
	news_title = models.CharField(max_length=200)
	news_date = models.CharField(max_length=200)
	news_content = models.CharField(max_length=10000)
	news_emotion = models.CharField(max_length=200)
	news_comment = models.CharField(max_length=10000)
	def __str__(self):
		return self.news_title