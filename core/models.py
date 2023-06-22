from django.db import models
from django.contrib.auth.models import User, AbstractUser



class Department(models.Model):
    dep_no = models.CharField(max_length=15, unique=True)
    name_la = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name_en} ({self.name_la})'


class Major(models.Model):
    major_no = models.CharField(max_length=15, unique=True)
    name_la = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name_en} ({self.name_la})'


class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# user, role, role_user
class User(AbstractUser):
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    dob = models.DateField(null=True, blank=True)
    village = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    tribe = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    # status = 
    degree = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    classroom = models.ForeignKey(ClassRoom, null=True, blank=True, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Course(models.Model):
    name_la = models.CharField(max_length=30)
    name_en = models.CharField(max_length=30)
    credit = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name_en} ({self.name_la})'


class TeachDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class TermScore(models.Model):
    # academic_year = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=10)
    term = models.CharField(max_length=10)
    sum_credit = models.FloatField(default=0)
    gpa = models.FloatField(default=0)
    ps = models.TextField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # classroom = 
    # created_by = 

    def __str__(self):
        return f'{self.term}'


class ScoreDetail(models.Model):
    credit = models.IntegerField(default=0)
    s_check = models.FloatField(default=0)
    s_test = models.FloatField(default=0)
    s_homework = models.FloatField(default=0)
    s_activity = models.FloatField(default=0)
    s_project = models.FloatField(default=0)
    s_midterm = models.FloatField(default=0)
    s_final = models.FloatField(default=0)
    s_total = models.FloatField(default=0, editable=False)
    s_grade = models.FloatField(default=0, verbose_name='s_gpa', editable=False)
    sum_credit = models.FloatField(default=0, editable=False)
    grade = models.CharField(max_length=5, editable=False)
    ps = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    term_score = models.ForeignKey(TermScore, on_delete=models.CASCADE, related_name='score_details')
    teach_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # user = 
    # classroom = 
    
    # def calculate_sum_credit_and_gpa(self):
    #     term_score = self.term_score
    #     score_details = term_score.score_details.all()
    #     term_score.sum_credit = sum(score_detail.credit for score_detail in score_details)
    #     total_weighted_score = sum(score_detail.credit * score_detail.s_grade for score_detail in score_details)
    #     term_score.gpa = total_weighted_score / term_score.sum_credit if term_score.sum_credit != 0 else 0
    #     term_score.save()
        
    # def calculate_sum_credit_and_gpa(self):
    #     term_score_id = self.term_score_id
    #     score_details = ScoreDetail.objects.filter(term_score_id=term_score_id)
    #     term_score = TermScore.objects.get(id=term_score_id)
    #     term_score.sum_credit = sum(score_detail.credit for score_detail in score_details)
    #     total_weighted_score = sum(score_detail.credit * score_detail.s_grade for score_detail in score_details)
    #     term_score.gpa = total_weighted_score / term_score.sum_credit if term_score.sum_credit != 0 else 0
    #     term_score.save()
    
    def calculate_sum_credit_and_gpa(self):
        term_scores = TermScore.objects.filter(score_details__id=self.id)
        for term_score in term_scores:
            score_details = term_score.score_details.all()
            term_score.sum_credit = sum(score_detail.credit for score_detail in score_details)
            total_weighted_score = sum(score_detail.credit * score_detail.s_grade for score_detail in score_details)
            term_score.gpa = total_weighted_score / term_score.sum_credit if term_score.sum_credit != 0 else 0
            term_score.save()
    
    def save(self, *args, **kwargs):
        # Calculate the sum of all individual scores
        sum_scores = (
            self.s_check + self.s_test + self.s_homework +
            self.s_activity + self.s_project + self.s_midterm + self.s_final
        )

        # Calculate the total score (sum of all individual scores)
        self.s_total = sum_scores

        # Calculate the average grade (total score divided by the number of individual scores)
        # num_scores = 7  # Total number of individual scores
        # self.s_grade = sum_scores / num_scores

        # Calculate the sum of credits (assuming there's only one instance of ScoreDetail per course)
        self.sum_credit = self.credit

        # Determine the grade based on the s_grade value
        if self.s_total > 100:
            self.s_total = 100

        if self.s_total >= 91:
            self.grade = 'A'
            self.s_grade = 4.00
            self.ps = 'ດີເລີດ'
        elif self.s_total >= 81:
            self.grade = 'B+'
            self.s_grade = 3.50
            self.ps = 'ດີຫຼາຍ'
        elif self.s_total >= 70:
            self.grade = 'B'
            self.s_grade = 3.00
            self.ps = 'ດີ'
        elif self.s_total >= 65:
            self.grade = 'C+'
            self.s_grade = 2.50
            self.ps = 'ດີພໍໃຊ້'
        elif self.s_total >= 60:
            self.grade = 'C'
            self.s_grade = 2.00
            self.ps = 'ພໍໃຊ້ໄດ້'
        elif self.s_total >= 55:
            self.grade = 'D+'
            self.s_grade = 1.50
            self.ps = 'ອ່ອນ'
        elif self.s_total >= 50:
            self.grade = 'D'
            self.s_grade = 1.00
            self.ps = 'ອ່ອນຫຼາຍ'
        else:
            self.grade = 'F'
            self.s_grade = 0.00
            self.ps = 'ຕົກ'
        
        # check if it is a new instance
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        term_scores = TermScore.objects.filter(score_details__id=self.id)
        print('term_scores:', term_scores)
        for term_score in term_scores:
            print('term_score: ', term_score)
            score_details = term_score.score_details.all()
            term_score.sum_credit = sum(score_detail.credit for score_detail in score_details)
            total_weighted_score = sum(score_detail.credit * score_detail.s_grade for score_detail in score_details)
            term_score.gpa = total_weighted_score / term_score.sum_credit if term_score.sum_credit != 0 else 0
            term_score.save()
            # super().save(*args, **kwargs)
        
        # term_score_id = self.term_score_id
        # score_details = ScoreDetail.objects.filter(term_score_id=term_score_id)
        # term_score = TermScore.objects.get(id=term_score_id)
        # term_score.sum_credit = sum(score_detail.credit for score_detail in score_details)
        # total_weighted_score = sum(score_detail.credit * score_detail.s_grade for score_detail in score_details)
        # term_score.gpa = total_weighted_score / term_score.sum_credit if term_score.sum_credit != 0 else 0
        # term_score.save()

    def delete(self, *args, **kwargs):
        self.calculate_sum_credit_and_gpa()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.credit}'
