from __future__ import unicode_literals

from django.db import models



class Course(models.Model):
    title = models.CharField(max_length=256, default='', db_index=True)
    image=models.TextField(default="")
    description=models.TextField("")
    price=models.IntegerField(default=0)
    author_id=models.IntegerField(default=0,db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        managed = True
        db_table = 'course'



class Lession(models.Model):
	title=models.TextField(default="")
	description=models.TextField(default="")
	course_id=models.IntegerField(default=0,db_index=True)
	rank=models.IntegerField(default=0,db_index=True)
	created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        managed = True
        db_table = 'lession'



class Chapter(models.Model):
	title=models.TextField(default="")
	lession_id=models.IntegerField(default=0,db_index=True)
	is_active=models.IntegerField(default=True,db_index=True)
	quiz_id=models.IntegerField(default=0,db_index=True)
	video_link=models.TextField(default='')

	class Meta:
        managed = True
        db_table = 'chapter'



