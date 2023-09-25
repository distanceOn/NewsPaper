from datetime import timedelta, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Category, Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_weekly_newsletter():
    end_date = timezone.now()
    start_date = end_date - timedelta(weeks=1)

    new_posts = Post.objects.filter(created_at__range=(start_date, end_date))

    for category in Category.objects.all():
        subscribers = category.subscribers.all()

        new_posts_in_category = new_posts.filter(categories=category)

        if new_posts_in_category:
            
            subject = f"Новые статьи в разделе '{category.name}' за последнюю неделю"
            for user in subscribers:
               
                html_content = render_to_string('news/weekly_newsletter.html', {'new_posts': new_posts_in_category})

           
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='',  
                    from_email='distanceOn@yandex.ru',
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html") 

             
                msg.send()



class Command(BaseCommand):
    help = "Schedule and run the weekly newsletter task."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        
        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(
                day_of_week="mon", hour="12", minute="0"  
            ),
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        self.stdout.write(self.style.SUCCESS("Added job 'send_weekly_newsletter'."))

        try:
            self.stdout.write(self.style.SUCCESS("Starting scheduler..."))
            scheduler.start()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Stopping scheduler..."))
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("Scheduler shut down successfully!"))