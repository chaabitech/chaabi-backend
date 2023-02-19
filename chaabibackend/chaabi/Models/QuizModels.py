from __future__ import unicode_literals

from django.db import models



class Quiz(models.Model):
	title=models.TextField(default="")
	score=models.IntegerField(default=0)
	published=models.BooleanField(default=True,db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
	
	class Meta:
		managed = True
        db_table = 'course'


class Question(models.Model):
	QUESTION_TYPE_CHOICES = (
        (0, 'Single Choice'),
        (1, 'Multiple Choice'))

	DIFFICULTY_LEVEL_CHOICES=(
        (0, 'Single Choice'),
        (1, 'Multiple Choice'),
        (2, 'Multiple Choice'))

	quiz = models.ForeignKey(Quiz)
	title=models.TextField(default="")
	description=models.TextField(default="")
	question_type=models.CharField(max_length=1,default=0,choices=QUESTION_TYPE_CHOICES,db_index=True)
	level=models.CharField(max_length=1,default=0,choices=DIFFICULTY_LEVEL_CHOICES,db_index=True)
	score=models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
	

	class Meta:
		managed = True
        db_table = 'question'


class Answer(models.Model):
	quiz_id=models.IntegerField(default=0,db_index=True)
	question=models.ForeignKey(Question)
	text=models.TextField(default="")
	is_active=models.IntegerField(default=True,db_index=True)
	is_correct=models.BooleanField(default=False,db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
    	managed=True
    	db_table="answer"






