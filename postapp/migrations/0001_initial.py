# Generated by Django 4.2.4 on 2023-09-19 09:11

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import postapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('loginapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentdetail', models.CharField(blank=True, max_length=1000, null=True)),
                ('Upvote', models.PositiveIntegerField(blank=True, null=True)),
                ('downvote', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('commentwriter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loginapp.websiteuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('report_count', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('postby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loginapp.websiteuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserPostUpvoteDownvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Upvote', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('downvote', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('userpostid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='postapp.userpost')),
                ('voteby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loginapp.websiteuser')),
            ],
        ),
        migrations.CreateModel(
            name='Reportpost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaintonpost', models.CharField(blank=True, max_length=550, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('reported_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loginapp.websiteuser')),
                ('reported_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='postapp.userpost')),
            ],
        ),
        migrations.CreateModel(
            name='Postimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, max_length=500, null=True, upload_to=postapp.models.get_file_path)),
                ('file_type', models.SmallIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('userpostid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postapp.userpost')),
            ],
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentdetail', models.CharField(blank=True, max_length=1000, null=True)),
                ('Upvote', models.PositiveIntegerField(blank=True, null=True)),
                ('downvote', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('Commentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='postapp.comment')),
                ('commentreplyuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loginapp.websiteuser')),
                ('mainpostid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postapp.userpost')),
                ('subreplyof', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_replies', to='postapp.commentreply')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='userpostid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postapp.userpost'),
        ),
    ]
