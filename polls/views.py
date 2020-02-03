from django.http import Http404

from django.http import HttpResponseRedirect
from .models import Choice, Question, Suggestion
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from django.utils import timezone
from .forms import SuggestionForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def get_suggestions(request):
    return render(request, 'polls/suggestions.html')

@csrf_exempt
def get_suggestions_list(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SuggestionForm()
    suggestions = Suggestion.objects.all()
    return render(request, 'polls/suggestions_list.html', {'suggestions': suggestions})


# >>> from myapp.forms import ArticleForm

# # Create a form instance from POST data.
# >>> f = ArticleForm(request.POST)

# # Save a new Article object from the form's data.
# >>> new_article = f.save()

# # Create a form to edit an existing Article, but use
# # POST data to populate the form.
# >>> a = Article.objects.get(pk=1)
# >>> f = ArticleForm(request.POST, instance=a)
# >>> f.save()
