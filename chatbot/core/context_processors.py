from core.models import Special_Question

def sidebar_notifications(request):
   return {
      'unanswered_count': Special_Question.objects.filter(answer__isnull=True).count()
   }