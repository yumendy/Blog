from models import Mood


class LeastMoodMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(LeastMoodMixin, self).get_context_data(*args, **kwargs)
        if Mood.objects.count() > 0:
            context['mood'] = Mood.objects.all()[0]
        else:
            pass
        return context
