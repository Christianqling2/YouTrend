from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category'


class Likes(models.Model):
    user = models.ForeignKey('OurUser', models.DO_NOTHING)
    video_object = models.ForeignKey('Video', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Likes'


class Region(models.Model):
    region_name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'Region'


class OurUser(models.Model):
    password = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    auth_user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'User'


class Video(models.Model):
    channel = models.ForeignKey('YoutubeChannel', models.DO_NOTHING)
    region = models.ForeignKey(Region, models.DO_NOTHING)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    video_title = models.CharField(max_length=128)
    publish_date = models.DateTimeField(blank=True, null=True)
    trending_date = models.DateTimeField(blank=True, null=True)
    tags = models.CharField(max_length=512, blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    likes_count = models.IntegerField(blank=True, null=True)
    dislikes = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    thumbnail_link = models.CharField(max_length=256, blank=True, null=True)
    comments_disabled = models.IntegerField(blank=True, null=True)
    ratings_disabled = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=4096, blank=True, null=True)
    external_video_id = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Video'


class VideoProposal(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=4096, blank=True, null=True)
    tags = models.CharField(max_length=512, blank=True, null=True)
    user = models.ForeignKey(OurUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'VideoProposal'


class YoutubeChannel(models.Model):
    channel_name = models.CharField(max_length=128)
    external_channel_id = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'YouTubeChannel'
