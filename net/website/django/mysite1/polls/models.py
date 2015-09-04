from django.db import models

# Create your models here.
class Question(models.Model): 
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published') 
    def __str__(self):
        return '%s, %s' %(self.question_text,self.pub_date)

class Choice(models.Model): 
    question = models.ForeignKey(Question) 
    choice_text = models.CharField(max_length=200)
    votes=models.IntegerField(default=0) 
    def __str__(self):
        return '%s, %s' %(self.choice_text,self.votes)
