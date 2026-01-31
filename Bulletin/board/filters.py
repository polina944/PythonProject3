from django_filters import FilterSet
from board.models import Comment, Post


class CommentFilter(FilterSet):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.filters['post'].queryset = Post.objects.filter(user=self.user)
        self.filters['post'].label = 'Фильтрация по объявлениям'
        self.filters['post'].field.empyt_label = 'Все объявления'


    class Meta:
        model = Comment
        fields = ['post']

